"""
Background Video Sync Service
Handles intelligent background synchronization of video data
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json

from .video_data_service import VideoDataService, SyncPriority
from .youtube_api_integration import YouTubeAPIIntegration

logger = logging.getLogger(__name__)

class BackgroundSyncService:
    """Manages background synchronization of video data"""
    
    def __init__(self, db_path: str):
        self.video_service = VideoDataService(db_path)
        self.youtube_api = YouTubeAPIIntegration()
        self.is_running = False
        self.sync_interval = 300  # 5 minutes
        
    async def start(self):
        """Start the background sync service"""
        if self.is_running:
            logger.warning("Background sync service is already running")
            return
        
        self.is_running = True
        logger.info("Starting background video sync service")
        
        # Start the main sync loop
        asyncio.create_task(self._sync_loop())
        
        # Start cleanup task
        asyncio.create_task(self._cleanup_loop())
    
    async def stop(self):
        """Stop the background sync service"""
        self.is_running = False
        logger.info("Stopping background video sync service")
    
    async def _sync_loop(self):
        """Main synchronization loop"""
        while self.is_running:
            try:
                await self._process_sync_queue()
                await asyncio.sleep(self.sync_interval)
                
            except Exception as e:
                logger.error(f"Error in sync loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    async def _cleanup_loop(self):
        """Cleanup loop - runs every hour"""
        while self.is_running:
            try:
                await self.video_service.cleanup_expired_cache()
                await asyncio.sleep(3600)  # 1 hour
                
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")
                await asyncio.sleep(3600)
    
    async def _process_sync_queue(self):
        """Process pending sync jobs"""
        try:
            # Get pending sync jobs
            sync_jobs = await self.video_service.get_videos_needing_sync(limit=20)
            
            if not sync_jobs:
                return
            
            logger.info(f"Processing {len(sync_jobs)} sync jobs")
            
            # Group by user to batch API calls
            user_jobs = {}
            for job in sync_jobs:
                user_id = job['user_id']
                if user_id not in user_jobs:
                    user_jobs[user_id] = []
                user_jobs[user_id].append(job)
            
            # Process each user's jobs
            for user_id, jobs in user_jobs.items():
                await self._process_user_sync_jobs(user_id, jobs)
                
        except Exception as e:
            logger.error(f"Error processing sync queue: {e}")
    
    async def _process_user_sync_jobs(self, user_id: str, jobs: List[Dict[str, Any]]):
        """Process sync jobs for a specific user"""
        try:
            # Get user's YouTube credentials (if available)
            # This would integrate with your auth system
            access_token = await self._get_user_youtube_token(user_id)
            
            for job in jobs:
                await self._process_single_sync_job(job, access_token)
                
        except Exception as e:
            logger.error(f"Error processing user {user_id} sync jobs: {e}")
    
    async def _process_single_sync_job(self, job: Dict[str, Any], access_token: Optional[str]):
        """Process a single sync job"""
        sync_id = job['id']
        video_id = job['video_id']
        user_id = job['user_id']
        sync_type = job['sync_type']
        youtube_video_id = job['youtube_video_id']
        
        try:
            logger.info(f"Processing sync job {sync_id} for video {video_id} (type: {sync_type})")
            
            # Mark as processing
            await self._mark_sync_processing(sync_id)
            
            if sync_type == 'basic':
                await self._sync_basic_metrics(video_id, youtube_video_id, user_id)
            elif sync_type == 'analytics':
                await self._sync_analytics(video_id, youtube_video_id, user_id, access_token)
            elif sync_type == 'full':
                await self._sync_full_data(video_id, youtube_video_id, user_id, access_token)
            
            # Mark as completed
            await self.video_service.mark_sync_completed(sync_id)
            logger.info(f"Completed sync job {sync_id}")
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed sync job {sync_id}: {error_msg}")
            await self.video_service.mark_sync_failed(sync_id, error_msg)
    
    async def _sync_basic_metrics(self, video_id: str, youtube_video_id: str, user_id: str):
        """Sync basic video metrics (views, likes, comments)"""
        try:
            # Get basic video data from YouTube API
            video_data = await self.youtube_api.get_video_basic_metrics(youtube_video_id)
            
            if video_data:
                # Update video record with new metrics
                await self._update_video_metrics(video_id, video_data)
                
        except Exception as e:
            logger.error(f"Error syncing basic metrics for video {video_id}: {e}")
            raise
    
    async def _sync_analytics(self, video_id: str, youtube_video_id: str, 
                            user_id: str, access_token: Optional[str]):
        """Sync detailed analytics data"""
        try:
            if not access_token:
                logger.warning(f"No access token for user {user_id}, skipping analytics sync")
                return
            
            # Get detailed analytics from YouTube Analytics API
            analytics_data = await self.youtube_api.get_video_analytics(
                youtube_video_id, access_token
            )
            
            if analytics_data:
                # Store analytics in cache
                await self._update_video_analytics(video_id, user_id, analytics_data)
                
        except Exception as e:
            logger.error(f"Error syncing analytics for video {video_id}: {e}")
            raise
    
    async def _sync_full_data(self, video_id: str, youtube_video_id: str, 
                            user_id: str, access_token: Optional[str]):
        """Sync both basic metrics and analytics"""
        await self._sync_basic_metrics(video_id, youtube_video_id, user_id)
        await self._sync_analytics(video_id, youtube_video_id, user_id, access_token)
    
    async def _update_video_metrics(self, video_id: str, video_data: Dict[str, Any]):
        """Update video with new metrics"""
        try:
            # This would update the video record with new metrics
            # Implementation depends on your video_data_service structure
            pass
            
        except Exception as e:
            logger.error(f"Error updating video metrics: {e}")
            raise
    
    async def _update_video_analytics(self, video_id: str, user_id: str, 
                                    analytics_data: Dict[str, Any]):
        """Update video analytics cache"""
        try:
            # This would update the analytics cache
            # Implementation depends on your video_data_service structure
            pass
            
        except Exception as e:
            logger.error(f"Error updating video analytics: {e}")
            raise
    
    async def _get_user_youtube_token(self, user_id: str) -> Optional[str]:
        """Get user's YouTube access token"""
        try:
            # This would integrate with your OAuth system
            # For now, return None (no token available)
            return None
            
        except Exception as e:
            logger.error(f"Error getting YouTube token for user {user_id}: {e}")
            return None
    
    async def _mark_sync_processing(self, sync_id: str):
        """Mark sync job as processing"""
        try:
            import sqlite3
            with sqlite3.connect(self.video_service.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE video_sync_queue 
                    SET status = 'processing', updated_at = ?
                    WHERE id = ?
                ''', (datetime.now(), sync_id))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error marking sync as processing: {e}")
    
    async def queue_user_videos_sync(self, user_id: str, sync_type: str = 'basic', 
                                   priority: SyncPriority = SyncPriority.NORMAL):
        """Queue all user videos for synchronization"""
        try:
            # Get all user videos that need sync
            import sqlite3
            with sqlite3.connect(self.video_service.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Get videos that haven't been synced recently
                hours_threshold = 24 if sync_type == 'basic' else 168  # 1 day for basic, 1 week for analytics
                
                cursor.execute('''
                    SELECT id FROM videos 
                    WHERE user_id = ? AND is_deleted = FALSE
                    AND (last_synced IS NULL OR last_synced < datetime('now', '-{} hours'))
                '''.format(hours_threshold), (user_id,))
                
                video_ids = [row['id'] for row in cursor.fetchall()]
            
            # Queue each video for sync
            for video_id in video_ids:
                await self.video_service._queue_video_sync(
                    video_id, user_id, sync_type, priority
                )
            
            logger.info(f"Queued {len(video_ids)} videos for {sync_type} sync for user {user_id}")
            return len(video_ids)
            
        except Exception as e:
            logger.error(f"Error queuing user videos sync: {e}")
            return 0
    
    async def get_sync_status(self) -> Dict[str, Any]:
        """Get current sync service status"""
        try:
            import sqlite3
            with sqlite3.connect(self.video_service.db_path) as conn:
                cursor = conn.cursor()
                
                # Get queue statistics
                cursor.execute('''
                    SELECT 
                        status,
                        COUNT(*) as count
                    FROM video_sync_queue 
                    GROUP BY status
                ''')
                
                queue_stats = {row[0]: row[1] for row in cursor.fetchall()}
                
                # Get recent sync activity
                cursor.execute('''
                    SELECT COUNT(*) as recent_syncs
                    FROM video_sync_queue 
                    WHERE updated_at > datetime('now', '-1 hour')
                    AND status IN ('completed', 'failed')
                ''')
                
                recent_activity = cursor.fetchone()[0]
                
                return {
                    "is_running": self.is_running,
                    "sync_interval": self.sync_interval,
                    "queue_stats": queue_stats,
                    "recent_activity": recent_activity,
                    "last_check": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error getting sync status: {e}")
            return {"error": str(e)}
