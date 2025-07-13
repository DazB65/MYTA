# Implementation Patterns for YouTube Analytics Integration in CreatorMate

from typing import Dict, List, Any, Optional
import asyncio
from datetime import datetime, timedelta
from dataclasses import dataclass
import json

# 1. Enhanced Backend Service Layer
class YouTubeAnalyticsService:
    """Enhanced service for YouTube Analytics API integration"""
    
    def __init__(self, youtube_service):
        self.youtube = youtube_service
        self.cache = {}  # Simple cache - could use Redis in production
    
    async def get_enhanced_video_data(self, channel_id: str, video_ids: List[str], days: int = 28) -> List[Dict]:
        """
        Get comprehensive video analytics data
        """
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Batch requests for efficiency
        video_analytics = await self._get_video_analytics(channel_id, start_date, end_date)
        retention_data = await self._get_retention_data(channel_id, video_ids, start_date, end_date)
        revenue_data = await self._get_revenue_data(channel_id, start_date, end_date)
        
        # Combine and enhance data
        enhanced_videos = []
        for video_id in video_ids:
            enhanced_video = await self._build_enhanced_video(
                video_id, video_analytics, retention_data, revenue_data
            )
            enhanced_videos.append(enhanced_video)
        
        return enhanced_videos
    
    async def _get_video_analytics(self, channel_id: str, start_date: str, end_date: str):
        """Get core video metrics"""
        cache_key = f"video_analytics_{channel_id}_{start_date}_{end_date}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        request = self.youtube.reports().query(
            ids=f'channel=={channel_id}',
            startDate=start_date,
            endDate=end_date,
            metrics='views,estimatedMinutesWatched,averageViewDuration,subscribersGained,impressions,impressionClickThroughRate,cardClickRate,endScreenClickRate',
            dimensions='video',
            maxResults=50,
            sort='-views'
        )
        
        response = request.execute()
        self.cache[cache_key] = response
        return response
    
    async def _get_retention_data(self, channel_id: str, video_ids: List[str], start_date: str, end_date: str):
        """Get audience retention curves"""
        retention_data = {}
        
        for video_id in video_ids:
            request = self.youtube.reports().query(
                ids=f'channel=={channel_id}',
                startDate=start_date,
                endDate=end_date,
                metrics='audienceWatchRatio,relativeRetentionPerformance',
                dimensions='elapsedVideoTimeRatio',
                filters=f'video=={video_id}',
                maxResults=100
            )
            
            response = request.execute()
            retention_data[video_id] = response
        
        return retention_data
    
    async def _get_revenue_data(self, channel_id: str, start_date: str, end_date: str):
        """Get monetization data if available"""
        try:
            request = self.youtube.reports().query(
                ids=f'channel=={channel_id}',
                startDate=start_date,
                endDate=end_date,
                metrics='estimatedRevenue,estimatedAdRevenue,estimatedRedRevenue,cpm,playbackBasedCpm',
                dimensions='video',
                maxResults=50
            )
            return request.execute()
        except Exception:
            # Channel might not be monetized
            return None

# 2. Data Processing and Enhancement
@dataclass
class VideoPerformanceGrade:
    retention_grade: str
    ctr_grade: str
    overall_score: float
    insights: List[str]
    recommendations: List[Dict[str, str]]

class PerformanceAnalyzer:
    """Analyze video performance and generate insights"""
    
    def __init__(self, channel_benchmarks: Dict[str, float]):
        self.benchmarks = channel_benchmarks
    
    def analyze_video_performance(self, video_data: Dict) -> VideoPerformanceGrade:
        """Generate performance grades and insights"""
        analytics = video_data.get('analytics', {})
        
        # Calculate grades
        retention = analytics.get('average_view_percentage', 0)
        ctr = analytics.get('impression_click_through_rate', 0)
        
        retention_grade = self._grade_retention(retention)
        ctr_grade = self._grade_ctr(ctr)
        overall_score = self._calculate_overall_score(analytics)
        
        # Generate insights
        insights = self._generate_insights(analytics)
        recommendations = self._generate_recommendations(analytics)
        
        return VideoPerformanceGrade(
            retention_grade=retention_grade,
            ctr_grade=ctr_grade,
            overall_score=overall_score,
            insights=insights,
            recommendations=recommendations
        )
    
    def _grade_retention(self, retention: float) -> str:
        """Grade retention performance"""
        if retention >= 0.8: return "A+"
        elif retention >= 0.7: return "A"
        elif retention >= 0.6: return "B+"
        elif retention >= 0.5: return "B"
        elif retention >= 0.4: return "C"
        else: return "D"
    
    def _grade_ctr(self, ctr: float) -> str:
        """Grade click-through rate"""
        if ctr >= 0.1: return "A+"
        elif ctr >= 0.08: return "A"
        elif ctr >= 0.06: return "B+"
        elif ctr >= 0.04: return "B"
        elif ctr >= 0.02: return "C"
        else: return "D"
    
    def _generate_insights(self, analytics: Dict) -> List[str]:
        """Generate actionable insights"""
        insights = []
        
        retention = analytics.get('average_view_percentage', 0)
        ctr = analytics.get('impression_click_through_rate', 0)
        impressions = analytics.get('impressions', 0)
        
        # Retention insights
        if retention > 0.75:
            insights.append("Excellent retention - audience highly engaged")
        elif retention < 0.5:
            insights.append("Low retention - consider improving hooks and pacing")
        
        # CTR insights
        if ctr > 0.08:
            insights.append("Strong thumbnail/title performance")
        elif ctr < 0.05:
            insights.append("Thumbnail/title needs improvement")
        
        # Reach insights
        if impressions > 10000:
            insights.append("Good reach - algorithm is promoting this content")
        elif impressions < 1000:
            insights.append("Limited reach - may need SEO optimization")
        
        return insights
    
    def _generate_recommendations(self, analytics: Dict) -> List[Dict[str, str]]:
        """Generate specific recommendations"""
        recommendations = []
        
        ctr = analytics.get('impression_click_through_rate', 0)
        retention = analytics.get('average_view_percentage', 0)
        
        if ctr < 0.06:
            recommendations.append({
                "type": "thumbnail",
                "action": "Test new thumbnail designs with brighter colors and clearer text",
                "reason": "CTR below industry average"
            })
        
        if retention < 0.6:
            recommendations.append({
                "type": "content",
                "action": "Improve video hooks in first 15 seconds",
                "reason": "High drop-off rate in early seconds"
            })
        
        traffic_sources = analytics.get('traffic_sources', {})
        if traffic_sources.get('youtube_search', 0) < 0.2:
            recommendations.append({
                "type": "seo",
                "action": "Optimize title and description for search keywords",
                "reason": "Low search traffic indicates poor discoverability"
            })
        
        return recommendations

# 3. Enhanced API Endpoints
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/videos/{channel_id}/enhanced")
async def get_enhanced_video_analytics(
    channel_id: str,
    days: int = 28,
    limit: int = 20,
    analytics_service: YouTubeAnalyticsService = Depends()
):
    """Get enhanced video analytics with performance insights"""
    try:
        # Get video IDs first (from existing endpoint or database)
        video_ids = await get_channel_video_ids(channel_id, limit)
        
        # Get enhanced analytics
        enhanced_videos = await analytics_service.get_enhanced_video_data(
            channel_id, video_ids, days
        )
        
        # Add performance analysis
        analyzer = PerformanceAnalyzer(channel_benchmarks={})
        for video in enhanced_videos:
            video['performance_grade'] = analyzer.analyze_video_performance(video)
        
        return {
            "videos": enhanced_videos,
            "summary": {
                "total_videos": len(enhanced_videos),
                "avg_retention": sum(v['analytics']['average_view_percentage'] for v in enhanced_videos) / len(enhanced_videos),
                "avg_ctr": sum(v['analytics']['impression_click_through_rate'] for v in enhanced_videos) / len(enhanced_videos)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/channel/{channel_id}/insights")
async def get_channel_insights(
    channel_id: str,
    days: int = 28,
    analytics_service: YouTubeAnalyticsService = Depends()
):
    """Get channel-level insights and trends"""
    try:
        insights = await analytics_service.get_channel_insights(channel_id, days)
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. Frontend Component Integration
"""
// Enhanced Video Card Component (React + TypeScript)

interface EnhancedVideoData {
  video_id: string;
  title: string;
  views: number;
  analytics: {
    average_view_percentage: number;
    impression_click_through_rate: number;
    estimated_revenue?: number;
    retention_curve: Array<{time: number, retention: number}>;
  };
  performance_grade: {
    retention_grade: string;
    ctr_grade: string;
    insights: string[];
    recommendations: Array<{type: string, action: string, reason: string}>;
  };
}

const EnhancedVideoCard: React.FC<{video: EnhancedVideoData}> = ({ video }) => {
  return (
    <div className="bg-gray-800 rounded-lg p-4">
      {/* Existing basic info */}
      <div className="flex items-center gap-4">
        <img src={video.thumbnail} className="w-20 h-14 object-cover rounded" />
        <div className="flex-1">
          <h3 className="text-white font-medium">{video.title}</h3>
          <div className="flex gap-4 text-sm text-gray-400">
            <span>{video.views} views</span>
            <span>{video.analytics.average_view_percentage * 100}% retention</span>
            <span>{video.analytics.impression_click_through_rate * 100}% CTR</span>
          </div>
        </div>
      </div>
      
      {/* NEW: Performance indicators */}
      <div className="mt-3 flex gap-2">
        <span className={`px-2 py-1 rounded text-xs ${getGradeColor(video.performance_grade.retention_grade)}`}>
          Retention: {video.performance_grade.retention_grade}
        </span>
        <span className={`px-2 py-1 rounded text-xs ${getGradeColor(video.performance_grade.ctr_grade)}`}>
          CTR: {video.performance_grade.ctr_grade}
        </span>
        {video.analytics.estimated_revenue && (
          <span className="px-2 py-1 bg-green-600 rounded text-xs text-white">
            ${video.analytics.estimated_revenue.toFixed(2)}
          </span>
        )}
      </div>
      
      {/* NEW: Quick insights */}
      {video.performance_grade.insights.length > 0 && (
        <div className="mt-3 text-sm text-blue-300">
          💡 {video.performance_grade.insights[0]}
        </div>
      )}
      
      {/* NEW: Retention curve mini-chart */}
      <RetentionMiniChart data={video.analytics.retention_curve} />
    </div>
  );
};
"""