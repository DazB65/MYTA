"""
Video API endpoints with optimized data handling
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from ..video_data_service import VideoDataService, PaginatedVideos
from ..auth_middleware import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/videos", tags=["videos"])

# Initialize video service (will be dependency injected in production)
video_service = VideoDataService("data/vidalytics.db")

@router.get("/", response_model=Dict[str, Any])
async def get_videos(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(24, ge=1, le=100, description="Videos per page"),
    search: Optional[str] = Query(None, description="Search in title and tags"),
    pillar_id: Optional[str] = Query(None, description="Filter by pillar"),
    performance_tier: Optional[str] = Query(None, description="Filter by performance tier (HOT/WARM/COLD)"),
    date_from: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    sort_by: str = Query("published_at", description="Sort field"),
    sort_order: str = Query("DESC", description="Sort order (ASC/DESC)"),
    current_user: dict = Depends(get_current_user)
):
    """Get paginated videos with filtering and sorting"""
    try:
        user_id = current_user.get("id", "default_user")
        
        # Build filters
        filters = {}
        if search:
            filters["search"] = search
        if pillar_id:
            filters["pillar_id"] = pillar_id
        if performance_tier:
            filters["performance_tier"] = performance_tier
        if date_from:
            filters["date_from"] = date_from
        if date_to:
            filters["date_to"] = date_to
        
        # Get paginated results
        result = await video_service.get_videos_paginated(
            user_id=user_id,
            page=page,
            per_page=per_page,
            filters=filters,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        return {
            "success": True,
            "data": {
                "videos": result.videos,
                "pagination": {
                    "total_count": result.total_count,
                    "page": result.page,
                    "per_page": result.per_page,
                    "total_pages": result.total_pages,
                    "has_next": result.has_next,
                    "has_prev": result.has_prev
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting videos: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve videos")

@router.get("/{video_id}", response_model=Dict[str, Any])
async def get_video(
    video_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get single video with detailed analytics"""
    try:
        user_id = current_user.get("id", "default_user")
        
        video = await video_service.get_video_with_analytics(user_id, video_id)
        
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        return {
            "success": True,
            "data": video
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting video {video_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve video")

@router.get("/stats/summary", response_model=Dict[str, Any])
async def get_video_stats(
    current_user: dict = Depends(get_current_user)
):
    """Get aggregated video statistics for the user"""
    try:
        user_id = current_user.get("id", "default_user")
        
        stats = await video_service.get_user_video_stats(user_id)
        
        return {
            "success": True,
            "data": stats
        }
        
    except Exception as e:
        logger.error(f"Error getting video stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve video statistics")

@router.post("/bulk-update-tiers", response_model=Dict[str, Any])
async def bulk_update_performance_tiers(
    current_user: dict = Depends(get_current_user)
):
    """Recalculate performance tiers for all user videos"""
    try:
        user_id = current_user.get("id", "default_user")
        
        await video_service.bulk_update_performance_tiers(user_id)
        
        return {
            "success": True,
            "message": "Performance tiers updated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error updating performance tiers: {e}")
        raise HTTPException(status_code=500, detail="Failed to update performance tiers")

@router.post("/sync/{video_id}", response_model=Dict[str, Any])
async def sync_video(
    video_id: str,
    sync_type: str = Query("full", description="Sync type: basic, analytics, full"),
    current_user: dict = Depends(get_current_user)
):
    """Queue a video for immediate synchronization"""
    try:
        user_id = current_user.get("id", "default_user")
        
        from .video_data_service import SyncPriority
        await video_service._queue_video_sync(
            video_id, user_id, sync_type, SyncPriority.URGENT
        )
        
        return {
            "success": True,
            "message": f"Video {video_id} queued for {sync_type} sync"
        }
        
    except Exception as e:
        logger.error(f"Error queueing video sync: {e}")
        raise HTTPException(status_code=500, detail="Failed to queue video sync")

@router.get("/performance/tiers", response_model=Dict[str, Any])
async def get_performance_tier_distribution(
    current_user: dict = Depends(get_current_user)
):
    """Get distribution of videos across performance tiers"""
    try:
        user_id = current_user.get("id", "default_user")
        
        stats = await video_service.get_user_video_stats(user_id)
        
        tier_distribution = {
            "HOT": stats.get("hot_videos", 0),
            "WARM": stats.get("warm_videos", 0),
            "COLD": stats.get("cold_videos", 0)
        }
        
        total_videos = sum(tier_distribution.values())
        tier_percentages = {}
        
        if total_videos > 0:
            for tier, count in tier_distribution.items():
                tier_percentages[tier] = round((count / total_videos) * 100, 1)
        
        return {
            "success": True,
            "data": {
                "distribution": tier_distribution,
                "percentages": tier_percentages,
                "total_videos": total_videos
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting tier distribution: {e}")
        raise HTTPException(status_code=500, detail="Failed to get tier distribution")

@router.delete("/cache/cleanup", response_model=Dict[str, Any])
async def cleanup_cache(
    current_user: dict = Depends(get_current_user)
):
    """Clean up expired cache entries (admin function)"""
    try:
        await video_service.cleanup_expired_cache()
        
        return {
            "success": True,
            "message": "Cache cleanup completed"
        }
        
    except Exception as e:
        logger.error(f"Error cleaning up cache: {e}")
        raise HTTPException(status_code=500, detail="Failed to clean up cache")

# Legacy endpoint for backward compatibility
@router.get("/legacy/all", response_model=Dict[str, Any])
async def get_all_videos_legacy(
    current_user: dict = Depends(get_current_user)
):
    """Legacy endpoint - returns first page of videos for backward compatibility"""
    try:
        user_id = current_user.get("id", "default_user")
        
        result = await video_service.get_videos_paginated(
            user_id=user_id,
            page=1,
            per_page=50,  # Return more for legacy compatibility
            filters={},
            sort_by="published_at",
            sort_order="DESC"
        )
        
        return {
            "success": True,
            "videos": result.videos,
            "total_count": result.total_count,
            "showing": len(result.videos)
        }
        
    except Exception as e:
        logger.error(f"Error getting legacy videos: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve videos")
