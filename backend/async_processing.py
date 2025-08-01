"""
Async Processing System for Vidalytics
Handles background processing for heavy AI operations
"""

import asyncio
import uuid
import time
import json
from typing import Dict, Any, Optional, Callable, List, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import traceback

from exceptions import (
    AgentCommunicationError, AgentTimeoutError, SystemError,
    BusinessLogicError, ValidationError
)
from distributed_cache import cache_set, cache_get, cache_delete
from logging_config import get_logger, LogCategory


logger = get_logger(__name__, LogCategory.AGENT)


class TaskStatus(Enum):
    """Task status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5


@dataclass
class TaskResult:
    """Task execution result"""
    task_id: str
    status: TaskStatus
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            "status": self.status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


@dataclass
class Task:
    """Background task definition"""
    task_id: str
    func: Callable
    args: tuple
    kwargs: Dict[str, Any]
    priority: TaskPriority
    timeout: Optional[int] = None
    retry_count: int = 0
    max_retries: int = 3
    retry_delay: float = 1.0
    user_id: Optional[str] = None
    agent_type: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()


class TaskQueue:
    """Priority queue for background tasks"""
    
    def __init__(self, max_size: int = 1000):
        self.queues: Dict[TaskPriority, asyncio.Queue] = {
            priority: asyncio.Queue(maxsize=max_size) for priority in TaskPriority
        }
        self.total_tasks = 0
        self._lock = asyncio.Lock()
    
    async def put(self, task: Task):
        """Add task to queue"""
        async with self._lock:
            await self.queues[task.priority].put(task)
            self.total_tasks += 1
    
    async def get(self) -> Optional[Task]:
        """Get highest priority task"""
        # Check queues in priority order (highest first)
        for priority in sorted(TaskPriority, key=lambda p: p.value, reverse=True):
            queue = self.queues[priority]
            if not queue.empty():
                async with self._lock:
                    task = await queue.get()
                    self.total_tasks -= 1
                    return task
        return None
    
    async def size(self) -> Dict[str, int]:
        """Get queue sizes"""
        sizes = {}
        for priority, queue in self.queues.items():
            sizes[priority.name.lower()] = queue.qsize()
        sizes["total"] = self.total_tasks
        return sizes
    
    def empty(self) -> bool:
        """Check if all queues are empty"""
        return all(queue.empty() for queue in self.queues.values())


class TaskTracker:
    """Tracks running and completed tasks"""
    
    def __init__(self, max_completed: int = 1000):
        self.running_tasks: Dict[str, Task] = {}
        self.completed_tasks: Dict[str, TaskResult] = {}
        self.max_completed = max_completed
        self._lock = asyncio.Lock()
    
    async def start_task(self, task: Task):
        """Mark task as started"""
        async with self._lock:
            self.running_tasks[task.task_id] = task
    
    async def complete_task(self, result: TaskResult):
        """Mark task as completed"""
        async with self._lock:
            if result.task_id in self.running_tasks:
                del self.running_tasks[result.task_id]
            
            self.completed_tasks[result.task_id] = result
            
            # Limit completed tasks to prevent memory growth
            if len(self.completed_tasks) > self.max_completed:
                oldest_task_id = min(
                    self.completed_tasks.keys(),
                    key=lambda tid: self.completed_tasks[tid].completed_at or datetime.min
                )
                del self.completed_tasks[oldest_task_id]
    
    async def get_task_status(self, task_id: str) -> Optional[Union[Task, TaskResult]]:
        """Get task status"""
        if task_id in self.running_tasks:
            return self.running_tasks[task_id]
        return self.completed_tasks.get(task_id)
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get task statistics"""
        async with self._lock:
            running_count = len(self.running_tasks)
            completed_count = len(self.completed_tasks)
            
            status_counts = {}
            for result in self.completed_tasks.values():
                status = result.status.value
                status_counts[status] = status_counts.get(status, 0) + 1
            
            return {
                "running_tasks": running_count,
                "completed_tasks": completed_count,
                "status_breakdown": status_counts,
                "total_tracked": running_count + completed_count
            }


class AsyncProcessor:
    """Async background task processor"""
    
    def __init__(
        self,
        max_workers: int = 5,
        max_thread_workers: int = 2,
        max_process_workers: int = 1,
        queue_size: int = 1000
    ):
        self.max_workers = max_workers
        self.max_thread_workers = max_thread_workers
        self.max_process_workers = max_process_workers
        
        self.task_queue = TaskQueue(queue_size)
        self.task_tracker = TaskTracker()
        
        self.workers: List[asyncio.Task] = []
        self.thread_executor = ThreadPoolExecutor(max_workers=max_thread_workers)
        self.process_executor = ProcessPoolExecutor(max_workers=max_process_workers)
        
        self.running = False
        self.stats = {
            "tasks_processed": 0,
            "tasks_failed": 0,
            "tasks_timeout": 0,
            "total_execution_time": 0.0,
            "started_at": None
        }
    
    async def start(self):
        """Start the async processor"""
        if self.running:
            return
        
        self.running = True
        self.stats["started_at"] = datetime.utcnow()
        
        # Start worker coroutines
        for i in range(self.max_workers):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self.workers.append(worker)
        
        logger.info(f"Started async processor with {self.max_workers} workers")
    
    async def stop(self):
        """Stop the async processor"""
        if not self.running:
            return
        
        self.running = False
        
        # Cancel all workers
        for worker in self.workers:
            worker.cancel()
        
        # Wait for workers to finish
        await asyncio.gather(*self.workers, return_exceptions=True)
        self.workers.clear()
        
        # Shutdown executors
        self.thread_executor.shutdown(wait=True)
        self.process_executor.shutdown(wait=True)
        
        logger.info("Stopped async processor")
    
    async def submit_task(
        self,
        func: Callable,
        *args,
        priority: TaskPriority = TaskPriority.NORMAL,
        timeout: Optional[int] = None,
        user_id: Optional[str] = None,
        agent_type: Optional[str] = None,
        use_thread: bool = False,
        use_process: bool = False,
        **kwargs
    ) -> str:
        """Submit task for async processing"""
        task_id = str(uuid.uuid4())
        
        # Store execution context in kwargs
        kwargs["_use_thread"] = use_thread
        kwargs["_use_process"] = use_process
        
        task = Task(
            task_id=task_id,
            func=func,
            args=args,
            kwargs=kwargs,
            priority=priority,
            timeout=timeout or 300,  # 5 minute default
            user_id=user_id,
            agent_type=agent_type
        )
        
        await self.task_queue.put(task)
        
        # Cache task for user if user_id provided
        if user_id:
            await cache_set(
                f"user_task:{user_id}:{task_id}",
                {"task_id": task_id, "status": "pending", "created_at": datetime.utcnow().isoformat()},
                ttl=3600,  # 1 hour
                category="user_context"
            )
        
        logger.info(
            f"Task submitted: {task_id}",
            extra={
                "category": LogCategory.AGENT.value,
                "metadata": {
                    "task_id": task_id,
                    "priority": priority.name,
                    "user_id": user_id,
                    "agent_type": agent_type,
                    "timeout": timeout
                }
            }
        )
        
        return task_id
    
    async def get_task_result(self, task_id: str, wait: bool = False, timeout: int = 30) -> Optional[TaskResult]:
        """Get task result"""
        if wait:
            # Poll for result
            start_time = time.time()
            while time.time() - start_time < timeout:
                status = await self.task_tracker.get_task_status(task_id)
                if isinstance(status, TaskResult):
                    return status
                await asyncio.sleep(0.5)
            return None
        else:
            status = await self.task_tracker.get_task_status(task_id)
            return status if isinstance(status, TaskResult) else None
    
    async def _worker(self, worker_name: str):
        """Worker coroutine"""
        logger.info(f"Worker {worker_name} started")
        
        while self.running:
            try:
                # Get next task
                task = await self.task_queue.get()
                if task is None:
                    await asyncio.sleep(0.1)
                    continue
                
                # Process task
                await self._process_task(task, worker_name)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker {worker_name} error: {e}", exc_info=True)
                await asyncio.sleep(1)
        
        logger.info(f"Worker {worker_name} stopped")
    
    async def _process_task(self, task: Task, worker_name: str):
        """Process a single task"""
        start_time = time.time()
        result = TaskResult(
            task_id=task.task_id,
            status=TaskStatus.RUNNING,
            created_at=task.created_at,
            started_at=datetime.utcnow()
        )
        
        try:
            # Mark task as started
            await self.task_tracker.start_task(task)
            
            logger.info(
                f"Processing task {task.task_id} on {worker_name}",
                extra={
                    "category": LogCategory.AGENT.value,
                    "metadata": {
                        "task_id": task.task_id,
                        "worker": worker_name,
                        "priority": task.priority.name,
                        "agent_type": task.agent_type
                    }
                }
            )
            
            # Execute task with timeout
            task_result = await self._execute_task_with_timeout(task)
            
            # Success
            result.status = TaskStatus.COMPLETED
            result.result = task_result
            result.completed_at = datetime.utcnow()
            result.execution_time = time.time() - start_time
            
            self.stats["tasks_processed"] += 1
            self.stats["total_execution_time"] += result.execution_time
            
            logger.info(
                f"Task {task.task_id} completed in {result.execution_time:.2f}s",
                extra={
                    "category": LogCategory.AGENT.value,
                    "metadata": {
                        "task_id": task.task_id,
                        "execution_time": result.execution_time,
                        "status": "completed"
                    }
                }
            )
            
        except asyncio.TimeoutError:
            result.status = TaskStatus.TIMEOUT
            result.error = f"Task timed out after {task.timeout} seconds"
            result.completed_at = datetime.utcnow()
            result.execution_time = time.time() - start_time
            
            self.stats["tasks_timeout"] += 1
            
            logger.warning(
                f"Task {task.task_id} timed out",
                extra={
                    "category": LogCategory.AGENT.value,
                    "metadata": {
                        "task_id": task.task_id,
                        "timeout": task.timeout,
                        "execution_time": result.execution_time
                    }
                }
            )
            
        except Exception as e:
            result.status = TaskStatus.FAILED
            result.error = str(e)
            result.completed_at = datetime.utcnow()
            result.execution_time = time.time() - start_time
            
            self.stats["tasks_failed"] += 1
            
            logger.error(
                f"Task {task.task_id} failed: {e}",
                extra={
                    "category": LogCategory.AGENT.value,
                    "metadata": {
                        "task_id": task.task_id,
                        "error": str(e),
                        "execution_time": result.execution_time,
                        "traceback": traceback.format_exc()
                    }
                }
            )
        
        # Store result
        await self.task_tracker.complete_task(result)
        
        # Update user cache if user_id provided
        if task.user_id:
            await cache_set(
                f"user_task:{task.user_id}:{task.task_id}",
                result.to_dict(),
                ttl=3600,
                category="user_context"
            )
    
    async def _execute_task_with_timeout(self, task: Task) -> Any:
        """Execute task with timeout"""
        use_thread = task.kwargs.pop("_use_thread", False)
        use_process = task.kwargs.pop("_use_process", False)
        
        if use_process:
            # Process executor for CPU-intensive tasks
            loop = asyncio.get_event_loop()
            future = loop.run_in_executor(
                self.process_executor,
                task.func,
                *task.args,
                **task.kwargs
            )
        elif use_thread:
            # Thread executor for I/O-bound tasks
            loop = asyncio.get_event_loop()
            future = loop.run_in_executor(
                self.thread_executor,
                task.func,
                *task.args,
                **task.kwargs
            )
        else:
            # Direct async execution
            if asyncio.iscoroutinefunction(task.func):
                future = task.func(*task.args, **task.kwargs)
            else:
                future = asyncio.to_thread(task.func, *task.args, **task.kwargs)
        
        # Apply timeout
        return await asyncio.wait_for(future, timeout=task.timeout)
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get processor statistics"""
        queue_stats = await self.task_queue.size()
        tracker_stats = await self.task_tracker.get_stats()
        
        avg_execution_time = (
            self.stats["total_execution_time"] / self.stats["tasks_processed"]
            if self.stats["tasks_processed"] > 0 else 0.0
        )
        
        return {
            "processor": {
                "running": self.running,
                "workers": len(self.workers),
                "max_workers": self.max_workers,
                "started_at": self.stats["started_at"].isoformat() if self.stats["started_at"] else None
            },
            "tasks": {
                **self.stats,
                "average_execution_time": avg_execution_time
            },
            "queue": queue_stats,
            "tracker": tracker_stats
        }


# Global async processor
_async_processor: Optional[AsyncProcessor] = None


async def get_async_processor() -> AsyncProcessor:
    """Get global async processor"""
    global _async_processor
    
    if _async_processor is None:
        _async_processor = AsyncProcessor()
        await _async_processor.start()
    
    return _async_processor


async def submit_background_task(
    func: Callable,
    *args,
    priority: TaskPriority = TaskPriority.NORMAL,
    timeout: Optional[int] = None,
    user_id: Optional[str] = None,
    agent_type: Optional[str] = None,
    **kwargs
) -> str:
    """Submit background task"""
    processor = await get_async_processor()
    return await processor.submit_task(
        func, *args,
        priority=priority,
        timeout=timeout,
        user_id=user_id,
        agent_type=agent_type,
        **kwargs
    )


async def get_task_result(task_id: str, wait: bool = False, timeout: int = 30) -> Optional[TaskResult]:
    """Get task result"""
    processor = await get_async_processor()
    return await processor.get_task_result(task_id, wait, timeout)


async def cleanup_async_processor():
    """Cleanup async processor"""
    global _async_processor
    if _async_processor:
        await _async_processor.stop()
        _async_processor = None