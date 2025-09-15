"""
Advanced Content Intelligence API Router
API endpoints for thumbnail analysis, hook optimization, and content structure analysis
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel, Field

from backend.App.advanced_content_intelligence import get_content_intelligence, ThumbnailAnalysis, HookAnalysis, ContentStructureAnalysis

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/content-intelligence", tags=["Content Intelligence"])

# Request/Response Models
class ThumbnailAnalysisRequest(BaseModel):
    thumbnail_url: Optional[str] = Field(default=None, description="URL to thumbnail image")
    thumbnail_description: str = Field(default="", description="Description of thumbnail elements")
    has_face: bool = Field(default=True, description="Whether thumbnail contains a face")
    text_elements: List[str] = Field(default=[], description="Text elements in thumbnail")
    colors: List[str] = Field(default=[], description="Main colors in thumbnail")
    background: str = Field(default="simple", description="Background type")
    objects: List[str] = Field(default=[], description="Objects visible in thumbnail")
    composition: str = Field(default="centered", description="Composition style")
    niche: Optional[str] = Field(default=None, description="Content niche for targeted analysis")

class ThumbnailAnalysisResponse(BaseModel):
    success: bool
    analysis: Optional[Dict[str, Any]]
    processing_time_ms: float

class HookAnalysisRequest(BaseModel):
    hook_text: str = Field(..., description="Video hook/opening text")
    video_title: Optional[str] = Field(default=None, description="Video title for context")
    video_topic: Optional[str] = Field(default=None, description="Video topic/subject")
    target_length: Optional[float] = Field(default=None, description="Target hook length in seconds")

class HookAnalysisResponse(BaseModel):
    success: bool
    analysis: Optional[Dict[str, Any]]
    processing_time_ms: float

class ContentStructureRequest(BaseModel):
    content_script: str = Field(..., description="Video script or content outline")
    video_length: Optional[float] = Field(default=None, description="Expected video length in minutes")
    content_type: str = Field(default="tutorial", description="Type of content")

class ContentStructureResponse(BaseModel):
    success: bool
    analysis: Optional[Dict[str, Any]]
    processing_time_ms: float

class QuickOptimizationRequest(BaseModel):
    content_type: str = Field(..., description="Type of content to optimize")
    current_data: Dict[str, Any] = Field(..., description="Current content data")
    optimization_focus: List[str] = Field(default=["thumbnail", "hook"], description="Areas to focus optimization on")

# Dependency to get user ID (simplified for demo)
async def get_current_user_id() -> str:
    # In production, extract from JWT token or session
    return "demo_user_123"

@router.post("/analyze-thumbnail", response_model=ThumbnailAnalysisResponse)
async def analyze_thumbnail(
    request: ThumbnailAnalysisRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Analyze thumbnail effectiveness and provide optimization recommendations
    
    Provides comprehensive analysis including:
    - Visual element scoring (color, text, composition, contrast)
    - Click-through probability prediction
    - Specific optimization suggestions
    - A/B testing recommendations
    - Niche-specific benchmarking
    """
    try:
        start_time = datetime.now()
        logger.info(f"🎨 Analyzing thumbnail for user {user_id}")
        
        # Get content intelligence engine
        content_intelligence = get_content_intelligence()
        
        # Prepare thumbnail data
        thumbnail_data = {
            'thumbnail_url': request.thumbnail_url,
            'description': request.thumbnail_description,
            'has_face': request.has_face,
            'text_elements': request.text_elements,
            'colors': request.colors,
            'background': request.background,
            'objects': request.objects,
            'composition': request.composition
        }
        
        # Analyze thumbnail
        analysis = await content_intelligence.analyze_thumbnail(
            user_id=user_id,
            thumbnail_data=thumbnail_data,
            niche_context=request.niche
        )
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return ThumbnailAnalysisResponse(
            success=True,
            analysis={
                'overall_score': analysis.overall_score,
                'effectiveness_rating': analysis.effectiveness_rating,
                'click_probability': analysis.click_probability,
                'scores': {
                    'color_psychology': analysis.color_psychology_score,
                    'text_readability': analysis.text_readability_score,
                    'facial_expression': analysis.facial_expression_score,
                    'composition': analysis.composition_score,
                    'contrast': analysis.contrast_score
                },
                'insights': {
                    'strengths': analysis.strengths,
                    'weaknesses': analysis.weaknesses,
                    'optimization_suggestions': analysis.optimization_suggestions
                },
                'ab_testing': {
                    'variations': analysis.ab_test_variations
                },
                'benchmarking': {
                    'vs_niche_average': analysis.vs_niche_average,
                    'improvement_potential': analysis.improvement_potential
                }
            },
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error analyzing thumbnail: {e}")
        raise HTTPException(status_code=500, detail=f"Thumbnail analysis failed: {str(e)}")

@router.post("/analyze-hook", response_model=HookAnalysisResponse)
async def analyze_hook(
    request: HookAnalysisRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Analyze video hook effectiveness and provide optimization recommendations
    
    Analyzes:
    - Hook type identification and effectiveness
    - Emotional impact and curiosity factors
    - Engagement and retention predictions
    - Alternative hook suggestions
    - Optimal timing and pacing recommendations
    """
    try:
        start_time = datetime.now()
        logger.info(f"🎯 Analyzing hook for user {user_id}")
        
        # Get content intelligence engine
        content_intelligence = get_content_intelligence()
        
        # Prepare video context
        video_context = {
            'title': request.video_title,
            'topic': request.video_topic,
            'target_length': request.target_length
        }
        
        # Analyze hook
        analysis = await content_intelligence.analyze_hook(
            user_id=user_id,
            hook_text=request.hook_text,
            video_context=video_context
        )
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return HookAnalysisResponse(
            success=True,
            analysis={
                'hook_score': analysis.hook_score,
                'predictions': {
                    'engagement': analysis.engagement_prediction,
                    'retention': analysis.retention_prediction
                },
                'hook_analysis': {
                    'type': analysis.hook_type.value,
                    'effectiveness_factors': analysis.effectiveness_factors,
                    'optimal_length': analysis.optimal_length,
                    'pacing_score': analysis.pacing_score
                },
                'optimization': {
                    'improvements': analysis.improvements,
                    'alternative_hooks': analysis.alternative_hooks
                }
            },
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error analyzing hook: {e}")
        raise HTTPException(status_code=500, detail=f"Hook analysis failed: {str(e)}")

@router.post("/analyze-content-structure", response_model=ContentStructureResponse)
async def analyze_content_structure(
    request: ContentStructureRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Analyze content structure for retention optimization
    
    Provides:
    - Retention curve prediction
    - Drop-off point identification
    - Pacing and flow analysis
    - Structure improvement recommendations
    - Optimal segment suggestions
    """
    try:
        start_time = datetime.now()
        logger.info(f"📊 Analyzing content structure for user {user_id}")
        
        # Get content intelligence engine
        content_intelligence = get_content_intelligence()
        
        # Analyze content structure
        analysis = await content_intelligence.analyze_content_structure(
            user_id=user_id,
            content_script=request.content_script,
            video_length=request.video_length
        )
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return ContentStructureResponse(
            success=True,
            analysis={
                'retention_prediction': analysis.retention_prediction,
                'performance_metrics': {
                    'pacing_score': analysis.pacing_score,
                    'flow_score': analysis.flow_score,
                    'transition_quality': analysis.transition_quality
                },
                'insights': {
                    'drop_off_points': analysis.drop_off_points,
                    'engagement_curve': analysis.engagement_curve,
                    'structure_improvements': analysis.structure_improvements,
                    'optimal_segments': analysis.optimal_segments
                }
            },
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error analyzing content structure: {e}")
        raise HTTPException(status_code=500, detail=f"Content structure analysis failed: {str(e)}")

@router.post("/quick-optimization")
async def quick_optimization(
    request: QuickOptimizationRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Get quick optimization suggestions for content elements
    
    Provides rapid analysis and suggestions for:
    - Thumbnail improvements
    - Hook optimization
    - Title enhancements
    - Overall content scoring
    """
    try:
        logger.info(f"⚡ Quick optimization for user {user_id}")
        
        # Get content intelligence engine
        content_intelligence = get_content_intelligence()
        
        optimization_results = {}
        
        # Thumbnail optimization
        if "thumbnail" in request.optimization_focus and "thumbnail" in request.current_data:
            thumbnail_data = request.current_data["thumbnail"]
            thumbnail_analysis = await content_intelligence.analyze_thumbnail(
                user_id=user_id,
                thumbnail_data=thumbnail_data
            )
            optimization_results["thumbnail"] = {
                "score": thumbnail_analysis.overall_score,
                "top_suggestions": thumbnail_analysis.optimization_suggestions[:3],
                "quick_fixes": [
                    suggestion for suggestion in thumbnail_analysis.optimization_suggestions 
                    if any(word in suggestion.lower() for word in ["color", "contrast", "text"])
                ][:2]
            }
        
        # Hook optimization
        if "hook" in request.optimization_focus and "hook" in request.current_data:
            hook_text = request.current_data["hook"]
            hook_analysis = await content_intelligence.analyze_hook(
                user_id=user_id,
                hook_text=hook_text
            )
            optimization_results["hook"] = {
                "score": hook_analysis.hook_score,
                "type": hook_analysis.hook_type.value,
                "top_improvements": hook_analysis.improvements[:3],
                "alternative": hook_analysis.alternative_hooks[0] if hook_analysis.alternative_hooks else None
            }
        
        return {
            "success": True,
            "optimization_results": optimization_results,
            "overall_recommendations": [
                "Focus on highest-impact improvements first",
                "Test variations to validate improvements",
                "Monitor performance after implementing changes"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error in quick optimization: {e}")
        raise HTTPException(status_code=500, detail=f"Quick optimization failed: {str(e)}")

@router.get("/optimization-tips")
async def get_optimization_tips(
    content_type: str = "general",
    user_id: str = Depends(get_current_user_id)
):
    """
    Get general optimization tips and best practices
    
    Returns curated tips for:
    - Thumbnail design
    - Hook creation
    - Content structure
    - Engagement optimization
    """
    try:
        tips_database = {
            "thumbnail": [
                "Use high-contrast colors (blue/yellow, red/white) for better visibility",
                "Keep text to 5 words or less for mobile readability",
                "Include expressive faces showing emotion when possible",
                "Apply rule of thirds for better composition",
                "Test different color schemes with A/B testing"
            ],
            "hook": [
                "Start with a question to immediately engage viewers",
                "Use specific numbers and statistics for credibility",
                "Create curiosity gaps that require watching to resolve",
                "Keep hooks under 15 seconds for optimal retention",
                "Match hook energy to your target audience"
            ],
            "structure": [
                "Front-load value in the first 30 seconds",
                "Use pattern interrupts every 2-3 minutes",
                "End segments with cliffhangers to maintain interest",
                "Vary pacing between fast and slow sections",
                "Include clear transitions between topics"
            ],
            "general": [
                "Optimize for mobile viewing (60%+ of traffic)",
                "Test one element at a time for clear results",
                "Monitor analytics to validate improvements",
                "Consider your niche's specific preferences",
                "Consistency in style builds brand recognition"
            ]
        }
        
        return {
            "success": True,
            "tips": tips_database.get(content_type, tips_database["general"]),
            "content_type": content_type
        }
        
    except Exception as e:
        logger.error(f"Error getting optimization tips: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get tips: {str(e)}")
