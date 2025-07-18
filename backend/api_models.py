"""
API Models for CreatorMate
Centralized Pydantic models for request/response validation
"""

from pydantic import BaseModel, ValidationError
from typing import List, Optional, Dict, Any
from datetime import datetime

# =============================================================================
# Core API Models
# =============================================================================

class ChatMessage(BaseModel):
    """Chat message request model"""
    message: str
    user_id: str = "default_user"
    
    class Config:
        str_strip_whitespace = True
        str_min_length = 1
        str_max_length = 2000

class QuickActionRequest(BaseModel):
    """Quick action request model"""
    action: str
    user_id: str = "default_user"
    context: str = ""
    
    class Config:
        str_strip_whitespace = True

class ChannelInfo(BaseModel):
    """Channel information model"""
    name: str = "Unknown"
    niche: str = "Unknown"
    content_type: str = "Unknown"
    subscriber_count: int = 0
    avg_view_count: int = 0
    ctr: float = 0
    retention: float = 0
    upload_frequency: str = "Unknown"
    video_length: str = "Unknown"
    monetization_status: str = "Unknown"
    primary_goal: str = "Unknown"
    notes: str = ""
    user_id: str = "default_user"
    
    class Config:
        str_strip_whitespace = True
        
    def validate_metrics(self):
        """Validate channel metrics are within reasonable ranges"""
        if self.subscriber_count < 0:
            raise ValueError("Subscriber count cannot be negative")
        if self.avg_view_count < 0:
            raise ValueError("Average view count cannot be negative")
        if not (0 <= self.ctr <= 100):
            raise ValueError("CTR must be between 0 and 100")
        if not (0 <= self.retention <= 100):
            raise ValueError("Retention must be between 0 and 100")
        if len(self.notes) > 1000:
            raise ValueError("Notes cannot exceed 1000 characters")

# =============================================================================
# Agent System Models
# =============================================================================

class AgentTaskRequest(BaseModel):
    """Request model for specialized agent tasks"""
    request_id: str
    agent_type: str
    query_type: str
    context: dict
    token_budget: dict = {"input_tokens": 3000, "output_tokens": 1500}
    analysis_depth: str = "standard"
    boss_agent_token: str
    timestamp: str = None
    
    class Config:
        str_strip_whitespace = True

class AgentCallbackRequest(BaseModel):
    """Request model for agent callback responses"""
    request_id: str
    agent_type: str
    response_data: dict
    processing_time: float
    success: bool
    
    class Config:
        str_strip_whitespace = True

class ModelStatusResponse(BaseModel):
    """Response model for model integration status"""
    available_models: dict
    model_status: dict
    active_integrations: List[str]

# =============================================================================
# YouTube API Models
# =============================================================================

class YouTubeAnalyticsRequest(BaseModel):
    """Request model for YouTube analytics"""
    channel_id: str
    user_id: str = "default_user"
    analysis_type: str = "comprehensive"
    time_period: str = "last_30d"
    include_videos: bool = True
    video_count: int = 20

class ContentPillarsRequest(BaseModel):
    """Request model for content pillars analysis"""
    channel_id: str
    user_id: str = "default_user"
    video_count: int = 50
    analysis_depth: str = "standard"

# =============================================================================
# Content Pillars Models
# =============================================================================

class CreatePillarRequest(BaseModel):
    """Request model for creating a content pillar"""
    name: str
    icon: str = "🎯"
    color: str = "from-blue-500 to-cyan-400"
    description: str = ""
    user_id: str = "default_user"
    
    class Config:
        str_strip_whitespace = True

class UpdatePillarRequest(BaseModel):
    """Request model for updating a content pillar"""
    name: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None
    
    class Config:
        str_strip_whitespace = True

class PillarResponse(BaseModel):
    """Response model for content pillar"""
    id: str
    name: str
    icon: str
    color: str
    description: str
    created_at: str
    updated_at: str

class VideoAllocationRequest(BaseModel):
    """Request model for allocating video to pillar"""
    video_id: str
    pillar_id: str
    user_id: str = "default_user"
    allocation_type: str = "manual"
    confidence_score: float = 1.0
    
    class Config:
        str_strip_whitespace = True

class VideoAllocationResponse(BaseModel):
    """Response model for video allocation"""
    video_id: str
    pillar_id: str
    pillar_name: str
    pillar_icon: str
    pillar_color: str
    allocation_type: str
    confidence_score: float

# =============================================================================
# Standard Response Models
# =============================================================================

class StandardResponse(BaseModel):
    """Standard API response model"""
    status: str = "success"
    message: str = ""
    data: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    status: str = "success"

class InsightResponse(BaseModel):
    """Insight response model"""
    insights: List[Dict[str, Any]]
    status: str = "success"

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: str
    service: str
    version: str

class SystemHealthResponse(BaseModel):
    """System health response model"""
    overall_health: float
    model_integrations: Dict[str, Any]
    youtube_api: Dict[str, Any]
    cache_system: Dict[str, Any]
    timestamp: str
    status: str

# =============================================================================
# Error Models
# =============================================================================

class ErrorResponse(BaseModel):
    """Standard error response model"""
    error: str
    detail: str
    status_code: int = 500
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class ValidationErrorResponse(BaseModel):
    """Validation error response model"""
    error: str = "Validation error"
    detail: str
    status_code: int = 422
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

# =============================================================================
# Utility Functions
# =============================================================================

def create_error_response(error: str, detail: str, status_code: int = 500) -> Dict[str, Any]:
    """Create standardized error response"""
    return {
        "error": error,
        "detail": detail,
        "status_code": status_code,
        "timestamp": datetime.now().isoformat()
    }

def create_success_response(message: str = "", data: Any = None) -> Dict[str, Any]:
    """Create standardized success response"""
    response = {
        "status": "success",
        "timestamp": datetime.now().isoformat()
    }
    
    if message:
        response["message"] = message
    if data is not None:
        response["data"] = data
    
    return response

# =============================================================================
# Content Cards Models
# =============================================================================

class ContentCardCreate(BaseModel):
    """Request model for creating a new content card"""
    title: str
    description: str = ""
    status: str = "ideas"
    pillars: List[Dict[str, Any]] = []
    due_date: Optional[str] = None
    progress: Optional[Dict[str, Any]] = None
    user_id: str
    
    class Config:
        str_strip_whitespace = True
        str_min_length = 1
        str_max_length = 500

class ContentCardUpdate(BaseModel):
    """Request model for updating an existing content card"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    pillars: Optional[List[Dict[str, Any]]] = None
    due_date: Optional[str] = None
    progress: Optional[Dict[str, Any]] = None
    archived: Optional[bool] = None
    order_index: Optional[int] = None
    
    class Config:
        str_strip_whitespace = True

class ContentCardStatusUpdate(BaseModel):
    """Request model for updating just the status of a content card"""
    status: str
    user_id: str
    order_index: Optional[int] = None
    
    class Config:
        str_strip_whitespace = True

class ContentCardResponse(BaseModel):
    """Response model for content card data"""
    id: str
    user_id: str
    title: str
    description: str
    status: str
    pillars: List[Dict[str, Any]]
    due_date: Optional[str]
    progress: Optional[Dict[str, Any]]
    archived: bool
    order_index: int
    created_at: str
    updated_at: str

class ContentCardsListResponse(BaseModel):
    """Response model for list of content cards"""
    cards: List[ContentCardResponse]
    total_count: int
    status_counts: Dict[str, int]

def validate_request_model(model_class: BaseModel, data: Dict[str, Any]) -> BaseModel:
    """Validate request data against Pydantic model"""
    try:
        return model_class(**data)
    except ValidationError as e:
        raise ValueError(f"Validation failed: {str(e)}")
    except Exception as e:
        raise ValueError(f"Invalid request data: {str(e)}")