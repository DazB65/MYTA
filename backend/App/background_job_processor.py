"""
Background Job Processing System for MYTA
Handles heavy AI operations, analytics processing, and async tasks
"""

import asyncio
import json
import logging
import time
import uuid
from typing import Dict, Any, Optional, List, Callable, Awaitable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from queue import Queue, Empty, PriorityQueue

from .enhanced_caching_service import get_cache_service
from .redis_service import get_redis_service

logger = logging.getLogger(__name__)

class JobStatus(Enum):
    """Job execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"

class JobPriority(Enum):
    """Job priority levels"""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5

@dataclass
class JobResult:
    """Job execution result"""
    job_id: str
    status: JobStatus
    result: Optional[Any] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    retry_count: int = 0

@dataclass
class BackgroundJob:
    """Background job definition"""
    job_id: str
    job_type: str
    priority: JobPriority
    payload: Dict[str, Any]
    user_id: Optional[str] = None
    created_at: datetime = None
    scheduled_at: Optional[datetime] = None
    max_retries: int = 3
    timeout_seconds: int = 300
    callback_url: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'job_id': self.job_id,
            'job_type': self.job_type,
            'priority': self.priority.value,
            'payload': self.payload,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'max_retries': self.max_retries,
            'timeout_seconds': self.timeout_seconds,
            'callback_url': self.callback_url
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BackgroundJob':
        """Create from dictionary"""
        return cls(
            job_id=data['job_id'],
            job_type=data['job_type'],
            priority=JobPriority(data['priority']),
            payload=data['payload'],
            user_id=data.get('user_id'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            scheduled_at=datetime.fromisoformat(data['scheduled_at']) if data.get('scheduled_at') else None,
            max_retries=data.get('max_retries', 3),
            timeout_seconds=data.get('timeout_seconds', 300),
            callback_url=data.get('callback_url')
        )

class JobProcessor:
    """Processes background jobs"""
    
    def __init__(self):
        self.job_handlers: Dict[str, Callable] = {}
        self.running = False
        self.worker_threads: List[threading.Thread] = []
        self.job_queue = PriorityQueue()
        self.results_cache = get_cache_service()
        self.redis_service = get_redis_service()
        self.max_workers = 4
        self.stats = {
            'jobs_processed': 0,
            'jobs_failed': 0,
            'jobs_retried': 0,
            'average_duration': 0.0
        }
    
    def register_handler(self, job_type: str, handler: Callable[[Dict[str, Any]], Awaitable[Any]]):
        """Register a job handler function"""
        self.job_handlers[job_type] = handler
        logger.info(f"Registered handler for job type: {job_type}")
    
    def submit_job(self, job: BackgroundJob) -> str:
        """Submit a job for processing"""
        # Store job in Redis for persistence
        job_key = f"myta:job:{job.job_id}"
        job_data = job.to_dict()
        
        if self.redis_service and self.redis_service.is_connected():
            self.redis_service.set(job_key, json.dumps(job_data), ex=86400)  # 24 hours
        
        # Add to priority queue
        priority_tuple = (job.priority.value, time.time(), job)
        self.job_queue.put(priority_tuple)
        
        # Store initial result
        result = JobResult(
            job_id=job.job_id,
            status=JobStatus.PENDING
        )
        self._store_result(result)
        
        logger.info(f"Submitted job {job.job_id} of type {job.job_type} with priority {job.priority.name}")
        return job.job_id
    
    def get_job_status(self, job_id: str) -> Optional[JobResult]:
        """Get job status and result"""
        result_key = f"myta:job_result:{job_id}"
        
        if self.redis_service and self.redis_service.is_connected():
            result_data = self.redis_service.get(result_key)
            if result_data:
                try:
                    data = json.loads(result_data)
                    return JobResult(
                        job_id=data['job_id'],
                        status=JobStatus(data['status']),
                        result=data.get('result'),
                        error=data.get('error'),
                        started_at=datetime.fromisoformat(data['started_at']) if data.get('started_at') else None,
                        completed_at=datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None,
                        duration_seconds=data.get('duration_seconds'),
                        retry_count=data.get('retry_count', 0)
                    )
                except (json.JSONDecodeError, ValueError) as e:
                    logger.error(f"Failed to parse job result for {job_id}: {e}")
        
        return None
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a pending job"""
        result = self.get_job_status(job_id)
        if result and result.status == JobStatus.PENDING:
            result.status = JobStatus.CANCELLED
            result.completed_at = datetime.now()
            self._store_result(result)
            logger.info(f"Cancelled job {job_id}")
            return True
        return False
    
    def start_workers(self, num_workers: int = None):
        """Start background worker threads"""
        if self.running:
            logger.warning("Workers already running")
            return
        
        self.running = True
        num_workers = num_workers or self.max_workers
        
        for i in range(num_workers):
            worker = threading.Thread(target=self._worker_loop, args=(i,), daemon=True)
            worker.start()
            self.worker_threads.append(worker)
        
        logger.info(f"Started {num_workers} background workers")
    
    def stop_workers(self):
        """Stop background worker threads"""
        self.running = False
        
        # Add sentinel values to wake up workers
        for _ in self.worker_threads:
            self.job_queue.put((0, 0, None))
        
        # Wait for workers to finish
        for worker in self.worker_threads:
            worker.join(timeout=5)
        
        self.worker_threads.clear()
        logger.info("Stopped background workers")
    
    def _worker_loop(self, worker_id: int):
        """Main worker loop"""
        logger.info(f"Worker {worker_id} started")
        
        while self.running:
            try:
                # Get job from queue with timeout
                try:
                    priority, timestamp, job = self.job_queue.get(timeout=1)
                    if job is None:  # Sentinel value
                        break
                except Empty:
                    continue
                
                # Process the job
                asyncio.run(self._process_job(job, worker_id))
                
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}")
        
        logger.info(f"Worker {worker_id} stopped")
    
    async def _process_job(self, job: BackgroundJob, worker_id: int):
        """Process a single job"""
        start_time = time.time()
        
        # Update job status to running
        result = JobResult(
            job_id=job.job_id,
            status=JobStatus.RUNNING,
            started_at=datetime.now()
        )
        self._store_result(result)
        
        logger.info(f"Worker {worker_id} processing job {job.job_id} ({job.job_type})")
        
        try:
            # Check if handler exists
            if job.job_type not in self.job_handlers:
                raise ValueError(f"No handler registered for job type: {job.job_type}")
            
            # Execute job handler
            handler = self.job_handlers[job.job_type]
            job_result = await asyncio.wait_for(
                handler(job.payload),
                timeout=job.timeout_seconds
            )
            
            # Job completed successfully
            duration = time.time() - start_time
            result.status = JobStatus.COMPLETED
            result.result = job_result
            result.completed_at = datetime.now()
            result.duration_seconds = duration
            
            self.stats['jobs_processed'] += 1
            self._update_average_duration(duration)
            
            logger.info(f"Job {job.job_id} completed in {duration:.2f}s")
            
        except asyncio.TimeoutError:
            result.status = JobStatus.FAILED
            result.error = f"Job timed out after {job.timeout_seconds} seconds"
            result.completed_at = datetime.now()
            self.stats['jobs_failed'] += 1
            logger.error(f"Job {job.job_id} timed out")
            
        except Exception as e:
            result.status = JobStatus.FAILED
            result.error = str(e)
            result.completed_at = datetime.now()
            self.stats['jobs_failed'] += 1
            logger.error(f"Job {job.job_id} failed: {e}")
            
            # Check if we should retry
            if result.retry_count < job.max_retries:
                result.retry_count += 1
                result.status = JobStatus.RETRYING
                self.stats['jobs_retried'] += 1
                
                # Re-queue the job with delay
                retry_job = BackgroundJob(
                    job_id=f"{job.job_id}_retry_{result.retry_count}",
                    job_type=job.job_type,
                    priority=job.priority,
                    payload=job.payload,
                    user_id=job.user_id,
                    max_retries=job.max_retries - result.retry_count,
                    timeout_seconds=job.timeout_seconds
                )
                
                # Add delay before retry
                retry_delay = min(2 ** result.retry_count, 60)  # Exponential backoff, max 60s
                time.sleep(retry_delay)
                
                self.submit_job(retry_job)
                logger.info(f"Retrying job {job.job_id} (attempt {result.retry_count + 1})")
        
        finally:
            self._store_result(result)
    
    def _store_result(self, result: JobResult):
        """Store job result"""
        result_key = f"myta:job_result:{result.job_id}"
        result_data = {
            'job_id': result.job_id,
            'status': result.status.value,
            'result': result.result,
            'error': result.error,
            'started_at': result.started_at.isoformat() if result.started_at else None,
            'completed_at': result.completed_at.isoformat() if result.completed_at else None,
            'duration_seconds': result.duration_seconds,
            'retry_count': result.retry_count
        }
        
        if self.redis_service and self.redis_service.is_connected():
            self.redis_service.set(result_key, json.dumps(result_data), ex=86400)  # 24 hours
    
    def _update_average_duration(self, duration: float):
        """Update average job duration"""
        if self.stats['jobs_processed'] == 1:
            self.stats['average_duration'] = duration
        else:
            # Running average
            total_jobs = self.stats['jobs_processed']
            current_avg = self.stats['average_duration']
            self.stats['average_duration'] = ((current_avg * (total_jobs - 1)) + duration) / total_jobs
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processor statistics"""
        return {
            'running': self.running,
            'active_workers': len(self.worker_threads),
            'queue_size': self.job_queue.qsize(),
            'registered_handlers': list(self.job_handlers.keys()),
            'stats': self.stats.copy()
        }

# Global job processor instance
_job_processor: Optional[JobProcessor] = None

def get_job_processor() -> JobProcessor:
    """Get or create global job processor"""
    global _job_processor
    if _job_processor is None:
        _job_processor = JobProcessor()
    return _job_processor

def submit_background_job(
    job_type: str,
    payload: Dict[str, Any],
    user_id: Optional[str] = None,
    priority: JobPriority = JobPriority.NORMAL,
    max_retries: int = 3,
    timeout_seconds: int = 300
) -> str:
    """Submit a background job"""
    job_id = str(uuid.uuid4())
    job = BackgroundJob(
        job_id=job_id,
        job_type=job_type,
        priority=priority,
        payload=payload,
        user_id=user_id,
        max_retries=max_retries,
        timeout_seconds=timeout_seconds
    )
    
    processor = get_job_processor()
    return processor.submit_job(job)

def get_job_status(job_id: str) -> Optional[JobResult]:
    """Get job status"""
    processor = get_job_processor()
    return processor.get_job_status(job_id)

# Job handler decorators
def job_handler(job_type: str):
    """Decorator to register job handlers"""
    def decorator(func):
        processor = get_job_processor()
        processor.register_handler(job_type, func)
        return func
    return decorator

# Common job handlers
@job_handler("ai_analysis")
async def handle_ai_analysis(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle AI analysis jobs"""
    from .ai_service import AIService

    ai_service = AIService()
    user_id = payload.get('user_id')
    messages = payload.get('messages', [])
    agent_id = payload.get('agent_id', '1')

    result = await ai_service.generate_response(
        messages=messages,
        agent_id=agent_id,
        user_id=user_id
    )

    return {
        'analysis_result': result,
        'processed_at': datetime.now().isoformat()
    }

@job_handler("youtube_data_fetch")
async def handle_youtube_data_fetch(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle YouTube data fetching jobs"""
    from .cached_youtube_service import get_cached_youtube_service

    operation = payload.get('operation')
    params = payload.get('params', {})

    # This would need the actual YouTube service instance
    # cached_service = get_cached_youtube_service(youtube_service)

    # Placeholder for now
    return {
        'operation': operation,
        'params': params,
        'fetched_at': datetime.now().isoformat(),
        'status': 'completed'
    }

@job_handler("bulk_video_analysis")
async def handle_bulk_video_analysis(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle bulk video analysis jobs"""
    video_ids = payload.get('video_ids', [])
    user_id = payload.get('user_id')
    analysis_type = payload.get('analysis_type', 'performance')

    results = []
    for video_id in video_ids:
        # Simulate video analysis
        await asyncio.sleep(0.1)  # Simulate processing time
        results.append({
            'video_id': video_id,
            'analysis_type': analysis_type,
            'score': 85.5,  # Placeholder
            'recommendations': ['Improve thumbnail', 'Optimize title']
        })

    return {
        'analyzed_videos': len(video_ids),
        'results': results,
        'completed_at': datetime.now().isoformat()
    }

@job_handler("channel_audit")
async def handle_channel_audit(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle comprehensive channel audit jobs"""
    channel_id = payload.get('channel_id')
    user_id = payload.get('user_id')
    audit_depth = payload.get('audit_depth', 'standard')

    # Simulate comprehensive audit
    await asyncio.sleep(2)  # Simulate processing time

    return {
        'channel_id': channel_id,
        'audit_depth': audit_depth,
        'overall_score': 78.5,
        'strengths': ['Consistent upload schedule', 'Good engagement rate'],
        'weaknesses': ['Low CTR', 'Poor thumbnail quality'],
        'recommendations': [
            'Improve thumbnail design',
            'Optimize video titles for SEO',
            'Increase video frequency'
        ],
        'completed_at': datetime.now().isoformat()
    }
