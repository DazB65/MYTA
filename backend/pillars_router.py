"""
Content Pillars Router for CreatorMate
Contains all content pillars-related API endpoints extracted from main.py
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging
import traceback
import uuid
from typing import List

# Import models
from api_models import (
    ContentPillarsRequest, CreatePillarRequest, UpdatePillarRequest,
    PillarResponse, VideoAllocationRequest, VideoAllocationResponse,
    StandardResponse, create_error_response, create_success_response
)

# Import services
from youtube_api_integration import get_youtube_integration
from boss_agent_auth import get_boss_agent_authenticator

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api", tags=["pillars"])

# =============================================================================
# Content Pillars Analysis Endpoints
# =============================================================================

@router.post("/youtube/content-pillars", response_model=StandardResponse)
async def analyze_content_pillars(request: ContentPillarsRequest):
    """Analyze YouTube videos to generate content pillars"""
    try:
        logger.info(f"Analyzing content pillars for channel: {request.channel_id}")
        
        # Get YouTube data
        integration = get_youtube_integration()
        channel_data = await integration.get_channel_data(
            request.channel_id,
            include_recent_videos=True,
            video_count=request.video_count,
            user_id=request.user_id
        )
        
        if not channel_data or not channel_data.recent_videos:
            raise HTTPException(status_code=404, detail="No video data found for analysis")
        
        # Use Content Analysis Agent to analyze content pillars
        from content_analysis_agent import get_content_analysis_agent
        content_agent = get_content_analysis_agent()
        
        # Prepare request for content analysis agent
        analysis_request = {
            "request_id": str(uuid.uuid4()),
            "query_type": "content_pillars",
            "context": {
                "channel_id": request.channel_id,
                "video_data": [
                    {
                        "video_id": video.video_id,
                        "title": video.title,
                        "view_count": video.view_count,
                        "engagement_rate": video.engagement_rate,
                        "published_at": video.published_at
                    }
                    for video in channel_data.recent_videos
                ]
            },
            "analysis_depth": request.analysis_depth,
            "boss_agent_token": get_boss_agent_authenticator().generate_boss_agent_token(),
            "timestamp": datetime.now().isoformat()
        }
        
        # Get content pillar analysis
        pillars_response = await content_agent.process_request(analysis_request)
        
        if not pillars_response.get("domain_match", False):
            raise HTTPException(status_code=400, detail="Content pillar analysis failed")
        
        return create_success_response(
            "Content pillars analysis completed successfully",
            {
                "content_pillars": pillars_response.get("analysis", {}),
                "channel_stats": {
                    "total_videos": len(channel_data.recent_videos),
                    "total_views": sum(video.view_count for video in channel_data.recent_videos),
                    "avg_engagement": sum(video.engagement_rate for video in channel_data.recent_videos) / len(channel_data.recent_videos)
                }
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing content pillars: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Content pillar analysis failed: {e}")

# =============================================================================
# Content Pillars CRUD Endpoints
# =============================================================================

@router.post("/pillars", response_model=PillarResponse)
async def create_pillar(request: CreatePillarRequest):
    """Create a new content pillar"""
    try:
        from database import db_manager
        
        # Generate unique ID
        pillar_id = f"pillar-{uuid.uuid4()}"
        
        # Create pillar in database
        success = db_manager.create_content_pillar(
            user_id=request.user_id,
            pillar_id=pillar_id,
            name=request.name,
            icon=request.icon,
            color=request.color,
            description=request.description
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to create pillar")
        
        # Return created pillar
        pillars = db_manager.get_user_content_pillars(request.user_id)
        created_pillar = next((p for p in pillars if p["id"] == pillar_id), None)
        
        if not created_pillar:
            raise HTTPException(status_code=500, detail="Failed to retrieve created pillar")
        
        return PillarResponse(**created_pillar)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating pillar: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to create pillar: {e}")

@router.get("/pillars/{user_id}", response_model=List[PillarResponse])
async def get_user_pillars(user_id: str):
    """Get all content pillars for a user"""
    try:
        from database import db_manager
        
        pillars = db_manager.get_user_content_pillars(user_id)
        return [PillarResponse(**pillar) for pillar in pillars]
        
    except Exception as e:
        logger.error(f"Error getting user pillars: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to get pillars: {e}")

@router.put("/pillars/{pillar_id}", response_model=PillarResponse)
async def update_pillar(pillar_id: str, request: UpdatePillarRequest):
    """Update a content pillar"""
    try:
        from database import db_manager
        
        # Update pillar in database
        success = db_manager.update_content_pillar(
            pillar_id=pillar_id,
            name=request.name,
            icon=request.icon,
            color=request.color,
            description=request.description
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Pillar not found or update failed")
        
        # Get updated pillar
        updated_pillar = db_manager.get_content_pillar_by_id(pillar_id)
        if not updated_pillar:
            raise HTTPException(status_code=404, detail="Updated pillar not found")
        
        return PillarResponse(**updated_pillar)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating pillar: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to update pillar: {e}")

@router.delete("/pillars/{pillar_id}", response_model=StandardResponse)
async def delete_pillar(pillar_id: str):
    """Delete a content pillar"""
    try:
        from database import db_manager
        
        success = db_manager.delete_content_pillar(pillar_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Pillar not found")
        
        return create_success_response("Pillar deleted successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting pillar: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to delete pillar: {e}")

# =============================================================================
# Video Allocation Endpoints
# =============================================================================

@router.post("/videos/allocate", response_model=VideoAllocationResponse)
async def allocate_video_to_pillar(request: VideoAllocationRequest):
    """Allocate a video to a content pillar"""
    try:
        from database import db_manager
        
        # Allocate video to pillar
        success = db_manager.allocate_video_to_pillar(
            user_id=request.user_id,
            video_id=request.video_id,
            pillar_id=request.pillar_id,
            allocation_type=request.allocation_type,
            confidence_score=request.confidence_score
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to allocate video to pillar")
        
        # Get the allocation details
        allocation = db_manager.get_pillar_for_video(request.user_id, request.video_id)
        if not allocation:
            raise HTTPException(status_code=500, detail="Failed to retrieve allocation details")
        
        return VideoAllocationResponse(
            video_id=request.video_id,
            pillar_id=allocation["pillar_id"],
            pillar_name=allocation["pillar_name"],
            pillar_icon=allocation["pillar_icon"],
            pillar_color=allocation["pillar_color"],
            allocation_type=allocation["allocation_type"],
            confidence_score=allocation["confidence_score"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error allocating video to pillar: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to allocate video: {e}")

@router.get("/videos/{video_id}/pillar")
async def get_video_pillar(video_id: str, user_id: str = "default_user"):
    """Get the pillar allocation for a specific video"""
    try:
        from database import db_manager
        
        allocation = db_manager.get_pillar_for_video(user_id, video_id)
        if not allocation:
            return None
        
        return VideoAllocationResponse(
            video_id=video_id,
            pillar_id=allocation["pillar_id"],
            pillar_name=allocation["pillar_name"],
            pillar_icon=allocation["pillar_icon"],
            pillar_color=allocation["pillar_color"],
            allocation_type=allocation["allocation_type"],
            confidence_score=allocation["confidence_score"]
        )
        
    except Exception as e:
        logger.error(f"Error getting video pillar: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to get video pillar: {e}")

@router.delete("/videos/{video_id}/pillar", response_model=StandardResponse)
async def remove_video_allocation(video_id: str, user_id: str = "default_user"):
    """Remove video allocation from any pillar"""
    try:
        from database import db_manager
        
        success = db_manager.remove_video_allocation(user_id, video_id)
        if not success:
            raise HTTPException(status_code=404, detail="Video allocation not found")
        
        return create_success_response("Video allocation removed successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing video allocation: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to remove video allocation: {e}")

@router.get("/pillars/{pillar_id}/videos")
async def get_pillar_videos(pillar_id: str, user_id: str = "default_user"):
    """Get all videos allocated to a specific pillar"""
    try:
        from database import db_manager
        
        videos = db_manager.get_videos_for_pillar(user_id, pillar_id)
        
        return create_success_response(
            "Pillar videos retrieved successfully",
            {"videos": videos}
        )
        
    except Exception as e:
        logger.error(f"Error getting pillar videos: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to get pillar videos: {e}")

# =============================================================================
# Pillar Analytics Endpoints
# =============================================================================

@router.get("/pillars/{pillar_id}/analytics")
async def get_pillar_analytics(pillar_id: str, user_id: str = "default_user"):
    """Get analytics for a specific content pillar"""
    try:
        from database import db_manager
        
        # Get pillar info
        pillar = db_manager.get_content_pillar_by_id(pillar_id)
        if not pillar:
            raise HTTPException(status_code=404, detail="Pillar not found")
        
        # Get videos for this pillar
        videos = db_manager.get_videos_for_pillar(user_id, pillar_id)
        
        if not videos:
            return create_success_response(
                "Pillar analytics retrieved (no videos)",
                {
                    "pillar_info": pillar,
                    "video_count": 0,
                    "total_views": 0,
                    "avg_views": 0,
                    "total_engagement": 0,
                    "avg_engagement": 0
                }
            )
        
        # Calculate analytics
        total_views = sum(video.get("view_count", 0) for video in videos)
        avg_views = total_views / len(videos) if videos else 0
        
        total_engagement = sum(video.get("engagement_rate", 0) for video in videos)
        avg_engagement = total_engagement / len(videos) if videos else 0
        
        return create_success_response(
            "Pillar analytics retrieved successfully",
            {
                "pillar_info": pillar,
                "video_count": len(videos),
                "total_views": total_views,
                "avg_views": avg_views,
                "total_engagement": total_engagement,
                "avg_engagement": avg_engagement,
                "videos": videos
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting pillar analytics: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to get pillar analytics: {e}")

@router.get("/pillars/{user_id}/overview")
async def get_pillars_overview(user_id: str):
    """Get overview of all pillars for a user with analytics"""
    try:
        from database import db_manager
        
        # Get all pillars for user
        pillars = db_manager.get_user_content_pillars(user_id)
        
        pillars_with_stats = []
        total_videos = 0
        total_views = 0
        
        for pillar in pillars:
            pillar_id = pillar["id"]
            
            # Get videos for this pillar
            videos = db_manager.get_videos_for_pillar(user_id, pillar_id)
            
            pillar_views = sum(video.get("view_count", 0) for video in videos)
            pillar_engagement = sum(video.get("engagement_rate", 0) for video in videos) / len(videos) if videos else 0
            
            pillars_with_stats.append({
                **pillar,
                "video_count": len(videos),
                "total_views": pillar_views,
                "avg_views": pillar_views / len(videos) if videos else 0,
                "avg_engagement": pillar_engagement
            })
            
            total_videos += len(videos)
            total_views += pillar_views
        
        return create_success_response(
            "Pillars overview retrieved successfully",
            {
                "pillars": pillars_with_stats,
                "summary": {
                    "total_pillars": len(pillars),
                    "total_videos": total_videos,
                    "total_views": total_views,
                    "avg_videos_per_pillar": total_videos / len(pillars) if pillars else 0
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting pillars overview: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to get pillars overview: {e}")