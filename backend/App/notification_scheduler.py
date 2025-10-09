"""
Notification Scheduler Service for MYTA
Background service for automated notification monitoring and delivery
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass

from .smart_notification_engine import get_notification_engine
from .supabase_client import get_supabase_service
from .logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.SCHEDULER)

@dataclass
class ScheduledTask:
    """Scheduled notification task"""
    task_id: str
    user_id: str
    channel_id: str
    task_type: str
    scheduled_time: datetime
    interval_minutes: int
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    enabled: bool = True

class NotificationScheduler:
    """Background scheduler for automated notifications"""
    
    def __init__(self):
        self.notification_engine = get_notification_engine()
        self.supabase = get_supabase_service()
        self.running = False
        self.scheduled_tasks = {}
        self.monitoring_intervals = {
            "real_time": 5,      # 5 minutes for critical monitoring
            "frequent": 15,      # 15 minutes for important checks
            "regular": 60,       # 1 hour for standard monitoring
            "daily": 1440,       # 24 hours for daily summaries
            "weekly": 10080      # 7 days for weekly reports
        }
    
    async def start_scheduler(self):
        """Start the notification scheduler"""
        
        if self.running:
            logger.warning("Scheduler is already running")
            return
        
        self.running = True
        logger.info("Starting notification scheduler")
        
        try:
            # Load scheduled tasks
            await self._load_scheduled_tasks()
            
            # Start monitoring loops
            await asyncio.gather(
                self._real_time_monitoring_loop(),
                self._frequent_monitoring_loop(),
                self._regular_monitoring_loop(),
                self._daily_summary_loop(),
                self._weekly_report_loop(),
                self._cleanup_loop()
            )
        
        except Exception as e:
            logger.error(f"Error in scheduler: {e}")
            self.running = False
    
    async def stop_scheduler(self):
        """Stop the notification scheduler"""
        
        self.running = False
        logger.info("Notification scheduler stopped")
    
    async def schedule_user_monitoring(
        self, 
        user_id: str, 
        channel_id: str, 
        monitoring_type: str = "regular"
    ):
        """Schedule monitoring for a specific user"""
        
        try:
            if monitoring_type not in self.monitoring_intervals:
                monitoring_type = "regular"
            
            interval = self.monitoring_intervals[monitoring_type]
            task_id = f"{user_id}_{channel_id}_{monitoring_type}"
            
            task = ScheduledTask(
                task_id=task_id,
                user_id=user_id,
                channel_id=channel_id,
                task_type=monitoring_type,
                scheduled_time=datetime.now(),
                interval_minutes=interval,
                next_run=datetime.now() + timedelta(minutes=interval)
            )
            
            self.scheduled_tasks[task_id] = task
            
            # Save to database
            await self._save_scheduled_task(task)
            
            logger.info(f"Scheduled {monitoring_type} monitoring for user {user_id}, channel {channel_id}")
            
        except Exception as e:
            logger.error(f"Error scheduling user monitoring: {e}")
    
    async def _real_time_monitoring_loop(self):
        """Real-time monitoring loop (5 minutes)"""
        
        while self.running:
            try:
                await self._run_monitoring_cycle("real_time")
                await asyncio.sleep(300)  # 5 minutes
            except Exception as e:
                logger.error(f"Error in real-time monitoring loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry
    
    async def _frequent_monitoring_loop(self):
        """Frequent monitoring loop (15 minutes)"""
        
        while self.running:
            try:
                await self._run_monitoring_cycle("frequent")
                await asyncio.sleep(900)  # 15 minutes
            except Exception as e:
                logger.error(f"Error in frequent monitoring loop: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes before retry
    
    async def _regular_monitoring_loop(self):
        """Regular monitoring loop (1 hour)"""
        
        while self.running:
            try:
                await self._run_monitoring_cycle("regular")
                await asyncio.sleep(3600)  # 1 hour
            except Exception as e:
                logger.error(f"Error in regular monitoring loop: {e}")
                await asyncio.sleep(600)  # Wait 10 minutes before retry
    
    async def _daily_summary_loop(self):
        """Daily summary loop (24 hours)"""
        
        while self.running:
            try:
                await self._run_monitoring_cycle("daily")
                await asyncio.sleep(86400)  # 24 hours
            except Exception as e:
                logger.error(f"Error in daily summary loop: {e}")
                await asyncio.sleep(3600)  # Wait 1 hour before retry
    
    async def _weekly_report_loop(self):
        """Weekly report loop (7 days)"""
        
        while self.running:
            try:
                await self._run_monitoring_cycle("weekly")
                await asyncio.sleep(604800)  # 7 days
            except Exception as e:
                logger.error(f"Error in weekly report loop: {e}")
                await asyncio.sleep(86400)  # Wait 1 day before retry
    
    async def _cleanup_loop(self):
        """Cleanup loop for old notifications and tasks"""
        
        while self.running:
            try:
                await self._cleanup_old_data()
                await asyncio.sleep(3600)  # Run cleanup every hour
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")
                await asyncio.sleep(1800)  # Wait 30 minutes before retry
    
    async def _run_monitoring_cycle(self, cycle_type: str):
        """Run monitoring cycle for specific type"""
        
        try:
            # Get tasks for this cycle type
            tasks_to_run = [
                task for task in self.scheduled_tasks.values()
                if task.task_type == cycle_type and task.enabled
                and (task.next_run is None or task.next_run <= datetime.now())
            ]
            
            logger.info(f"Running {cycle_type} monitoring cycle for {len(tasks_to_run)} tasks")
            
            # Process tasks in batches to avoid overwhelming the system
            batch_size = 10
            for i in range(0, len(tasks_to_run), batch_size):
                batch = tasks_to_run[i:i + batch_size]
                
                # Run batch in parallel
                await asyncio.gather(*[
                    self._execute_monitoring_task(task)
                    for task in batch
                ], return_exceptions=True)
                
                # Small delay between batches
                if i + batch_size < len(tasks_to_run):
                    await asyncio.sleep(1)
        
        except Exception as e:
            logger.error(f"Error in {cycle_type} monitoring cycle: {e}")
    
    async def _execute_monitoring_task(self, task: ScheduledTask):
        """Execute a single monitoring task"""
        
        try:
            # Run notification monitoring
            notifications = await self.notification_engine.monitor_and_notify(
                task.user_id, task.channel_id
            )
            
            # Update task timing
            task.last_run = datetime.now()
            task.next_run = datetime.now() + timedelta(minutes=task.interval_minutes)
            
            # Save updated task
            await self._save_scheduled_task(task)
            
            logger.debug(f"Executed monitoring task {task.task_id}, generated {len(notifications)} notifications")
            
        except Exception as e:
            logger.error(f"Error executing monitoring task {task.task_id}: {e}")
    
    async def _load_scheduled_tasks(self):
        """Load scheduled tasks from database"""
        
        try:
            # In real implementation, load from database
            # For now, create some default tasks
            
            # Example: Load active users and create monitoring tasks
            sample_users = [
                {"user_id": "user_1", "channel_id": "channel_1"},
                {"user_id": "user_2", "channel_id": "channel_2"}
            ]
            
            for user_data in sample_users:
                await self.schedule_user_monitoring(
                    user_data["user_id"],
                    user_data["channel_id"],
                    "regular"
                )
            
            logger.info(f"Loaded {len(self.scheduled_tasks)} scheduled tasks")
            
        except Exception as e:
            logger.error(f"Error loading scheduled tasks: {e}")
    
    async def _save_scheduled_task(self, task: ScheduledTask):
        """Save scheduled task to database"""
        
        try:
            # In real implementation, save to database
            # For now, just update in-memory storage
            self.scheduled_tasks[task.task_id] = task
            
        except Exception as e:
            logger.error(f"Error saving scheduled task: {e}")
    
    async def _cleanup_old_data(self):
        """Clean up old notifications and expired tasks"""
        
        try:
            # Clean up expired notifications (older than 30 days)
            cutoff_date = datetime.now() - timedelta(days=30)
            
            # In real implementation, clean up database
            logger.debug("Cleaned up old notification data")
            
            # Remove disabled tasks
            disabled_tasks = [
                task_id for task_id, task in self.scheduled_tasks.items()
                if not task.enabled
            ]
            
            for task_id in disabled_tasks:
                del self.scheduled_tasks[task_id]
            
            if disabled_tasks:
                logger.info(f"Removed {len(disabled_tasks)} disabled tasks")
            
        except Exception as e:
            logger.error(f"Error in cleanup: {e}")
    
    async def get_scheduler_status(self) -> Dict[str, Any]:
        """Get scheduler status and statistics"""
        
        try:
            active_tasks = len([t for t in self.scheduled_tasks.values() if t.enabled])
            total_tasks = len(self.scheduled_tasks)
            
            # Task breakdown by type
            task_breakdown = {}
            for task in self.scheduled_tasks.values():
                task_type = task.task_type
                task_breakdown[task_type] = task_breakdown.get(task_type, 0) + 1
            
            # Next run times
            next_runs = {}
            for cycle_type in self.monitoring_intervals.keys():
                next_run_tasks = [
                    task for task in self.scheduled_tasks.values()
                    if task.task_type == cycle_type and task.enabled and task.next_run
                ]
                if next_run_tasks:
                    next_runs[cycle_type] = min(task.next_run for task in next_run_tasks).isoformat()
            
            return {
                "running": self.running,
                "total_tasks": total_tasks,
                "active_tasks": active_tasks,
                "task_breakdown": task_breakdown,
                "monitoring_intervals": self.monitoring_intervals,
                "next_runs": next_runs,
                "uptime": "running" if self.running else "stopped"
            }
        
        except Exception as e:
            logger.error(f"Error getting scheduler status: {e}")
            return {"error": str(e)}
    
    async def add_custom_monitoring(
        self, 
        user_id: str, 
        channel_id: str, 
        custom_interval: int,
        task_name: str = "custom"
    ):
        """Add custom monitoring with specific interval"""
        
        try:
            task_id = f"{user_id}_{channel_id}_{task_name}_{custom_interval}"
            
            task = ScheduledTask(
                task_id=task_id,
                user_id=user_id,
                channel_id=channel_id,
                task_type=f"custom_{task_name}",
                scheduled_time=datetime.now(),
                interval_minutes=custom_interval,
                next_run=datetime.now() + timedelta(minutes=custom_interval)
            )
            
            self.scheduled_tasks[task_id] = task
            await self._save_scheduled_task(task)
            
            logger.info(f"Added custom monitoring task {task_id} with {custom_interval} minute interval")
            
            return task_id
        
        except Exception as e:
            logger.error(f"Error adding custom monitoring: {e}")
            return None
    
    async def remove_monitoring(self, task_id: str):
        """Remove monitoring task"""
        
        try:
            if task_id in self.scheduled_tasks:
                self.scheduled_tasks[task_id].enabled = False
                logger.info(f"Disabled monitoring task {task_id}")
                return True
            return False
        
        except Exception as e:
            logger.error(f"Error removing monitoring: {e}")
            return False

# Global scheduler instance
_notification_scheduler: Optional[NotificationScheduler] = None

def get_notification_scheduler() -> NotificationScheduler:
    """Get or create global notification scheduler instance"""
    global _notification_scheduler
    if _notification_scheduler is None:
        _notification_scheduler = NotificationScheduler()
    return _notification_scheduler

async def start_notification_scheduler():
    """Start the global notification scheduler"""
    scheduler = get_notification_scheduler()
    await scheduler.start_scheduler()

async def stop_notification_scheduler():
    """Stop the global notification scheduler"""
    scheduler = get_notification_scheduler()
    await scheduler.stop_scheduler()
