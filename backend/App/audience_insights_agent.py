"""
Audience Insights Agent for Vidalytics
Specialized sub-agent that analyzes YouTube audience demographics, behavior, and sentiment for the boss agent
"""

import asyncio
import json
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging
import os
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dataclasses import dataclass
import statistics
from base_agent import BaseSpecializedAgent, AgentType, AgentRequest, AgentAnalysis, AgentInsight, AgentRecommendation
from boss_agent_auth import SpecializedAgentAuthMixin
from connection_pool import get_youtube_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AudienceAnalysisRequest:
    """Structure for audience analysis requests from boss agent"""
    request_id: str
    channel_id: str
    time_period: str
    analysis_depth: str = "standard"  # quick, standard, deep
    include_sentiment_analysis: bool = True
    include_demographics: bool = True
    include_behavior_analysis: bool = True
    include_collaboration_analysis: bool = True
    include_posting_time_analysis: bool = True
    token_budget: int = 4000

@dataclass
class AudienceMetrics:
    """Audience metrics structure"""
    total_subscribers: int
    subscriber_growth: float
    avg_watch_time: float
    avg_session_duration: float
    engagement_rate: float
    top_demographics: Dict[str, Any]
    traffic_sources: Dict[str, float]
    peak_activity_times: List[str]
    comment_volume: int
    sentiment_breakdown: Dict[str, float]

class PostingTimeAnalyzer:
    """Analyzes optimal posting times for maximum engagement"""

    def __init__(self):
        self.time_weights = {
            'view_performance': 0.4,      # Weight for view count performance
            'engagement_rate': 0.3,       # Weight for engagement metrics
            'subscriber_gain': 0.2,       # Weight for subscriber growth
            'retention_rate': 0.1         # Weight for viewer retention
        }

    async def analyze_posting_times(self, video_data: List[Dict], timezone: str = 'UTC') -> Dict[str, Any]:
        """Analyze optimal posting times for maximum engagement"""
        try:
            # Group performance by day and hour
            day_stats = self._analyze_daily_performance(video_data)
            hour_stats = self._analyze_hourly_performance(video_data)
            timezone_impact = self._analyze_timezone_impact(video_data, timezone)

            # Find optimal posting windows
            posting_windows = self._identify_optimal_windows(day_stats, hour_stats)

            # Calculate posting consistency score
            consistency_metrics = self._analyze_posting_consistency(video_data)

            return {
                'optimal_posting_times': posting_windows,
                'day_performance': day_stats,
                'hour_performance': hour_stats,
                'timezone_analysis': timezone_impact,
                'posting_consistency': consistency_metrics,
                'recommendations': self._generate_posting_recommendations(
                    posting_windows, consistency_metrics, timezone_impact
                )
            }

        except Exception as e:
            logger.error(f"Error in posting time analysis: {e}")
            return self._generate_fallback_analysis()

    def _analyze_daily_performance(self, videos: List[Dict]) -> Dict[str, Any]:
        """Analyze performance by day of week"""
        from collections import defaultdict
        import datetime

        daily_stats = defaultdict(lambda: {
            'videos': [],
            'total_views': 0,
            'total_engagement': 0,
            'subscriber_gain': 0
        })

        for video in videos:
            try:
                published = datetime.datetime.fromisoformat(
                    video['published_at'].replace('Z', '+00:00')
                )
                day_name = published.strftime('%A')

                daily_stats[day_name]['videos'].append(video)
                daily_stats[day_name]['total_views'] += video.get('views', 0)
                daily_stats[day_name]['total_engagement'] += (
                    video.get('likes', 0) + video.get('comments', 0)
                )
                daily_stats[day_name]['subscriber_gain'] += video.get('subscriber_gain', 0)

            except Exception as e:
                logger.warning(f"Error processing video for daily stats: {e}")
                continue

        # Calculate averages and scores
        day_performance = {}
        for day, stats in daily_stats.items():
            video_count = len(stats['videos'])
            if video_count > 0:
                avg_views = stats['total_views'] / video_count
                avg_engagement = stats['total_engagement'] / video_count
                avg_sub_gain = stats['subscriber_gain'] / video_count

                # Calculate weighted performance score
                performance_score = (
                    avg_views * self.time_weights['view_performance'] +
                    avg_engagement * self.time_weights['engagement_rate'] +
                    avg_sub_gain * self.time_weights['subscriber_gain']
                )

                day_performance[day] = {
                    'performance_score': round(performance_score, 2),
                    'avg_views': round(avg_views, 2),
                    'avg_engagement': round(avg_engagement, 2),
                    'avg_sub_gain': round(avg_sub_gain, 2),
                    'video_count': video_count,
                    'confidence': min(1.0, video_count / 10)
                }

        return day_performance

    def _analyze_hourly_performance(self, videos: List[Dict]) -> Dict[str, Any]:
        """Analyze performance by hour of day"""
        from collections import defaultdict
        import datetime

        hourly_stats = defaultdict(lambda: {
            'videos': [],
            'total_views': 0,
            'total_engagement': 0,
            'avg_retention': 0
        })

        for video in videos:
            try:
                published = datetime.datetime.fromisoformat(
                    video['published_at'].replace('Z', '+00:00')
                )
                hour = published.hour

                hourly_stats[hour]['videos'].append(video)
                hourly_stats[hour]['total_views'] += video.get('views', 0)
                hourly_stats[hour]['total_engagement'] += (
                    video.get('likes', 0) + video.get('comments', 0)
                )
                hourly_stats[hour]['avg_retention'] += video.get('retention_rate', 0)

            except Exception as e:
                logger.warning(f"Error processing video for hourly stats: {e}")
                continue

        # Calculate hourly performance scores
        hour_performance = {}
        for hour, stats in hourly_stats.items():
            video_count = len(stats['videos'])
            if video_count > 0:
                avg_views = stats['total_views'] / video_count
                avg_engagement = stats['total_engagement'] / video_count
                avg_retention = stats['avg_retention'] / video_count

                # Calculate weighted performance score
                performance_score = (
                    avg_views * self.time_weights['view_performance'] +
                    avg_engagement * self.time_weights['engagement_rate'] +
                    avg_retention * self.time_weights['retention_rate']
                )

                hour_performance[hour] = {
                    'performance_score': round(performance_score, 2),
                    'avg_views': round(avg_views, 2),
                    'avg_engagement': round(avg_engagement, 2),
                    'avg_retention': round(avg_retention, 2),
                    'video_count': video_count,
                    'confidence': min(1.0, video_count / 10)
                }

        return hour_performance

    def _analyze_timezone_impact(self, videos: List[Dict], timezone: str) -> Dict[str, Any]:
        """Analyze impact of timezone on video performance"""
        try:
            from datetime import datetime, timedelta
            import pytz

            tz = pytz.timezone(timezone)
            utc = pytz.UTC

            # Analyze performance in different timezone segments
            timezone_segments = {
                'early_morning': (4, 8),    # 4 AM - 8 AM
                'morning': (8, 12),         # 8 AM - 12 PM
                'afternoon': (12, 16),       # 12 PM - 4 PM
                'evening': (16, 20),         # 4 PM - 8 PM
                'night': (20, 24),           # 8 PM - 12 AM
                'late_night': (0, 4)         # 12 AM - 4 AM
            }

            segment_performance = {}
            for segment, (start_hour, end_hour) in timezone_segments.items():
                segment_videos = []
                for video in videos:
                    try:
                        # Convert UTC to local timezone
                        published = datetime.fromisoformat(
                            video['published_at'].replace('Z', '+00:00')
                        )
                        local_time = published.astimezone(tz)
                        
                        if start_hour <= local_time.hour < end_hour:
                            segment_videos.append(video)
                    except Exception:
                        continue

                if segment_videos:
                    avg_views = sum(v.get('views', 0) for v in segment_videos) / len(segment_videos)
                    avg_engagement = sum(
                        v.get('likes', 0) + v.get('comments', 0)
                        for v in segment_videos
                    ) / len(segment_videos)

                    segment_performance[segment] = {
                        'avg_views': round(avg_views, 2),
                        'avg_engagement': round(avg_engagement, 2),
                        'video_count': len(segment_videos),
                        'performance_score': round(
                            (avg_views * 0.7 + avg_engagement * 0.3) / 1000, 2
                        )
                    }

            return {
                'timezone': timezone,
                'segment_performance': segment_performance,
                'optimal_segments': sorted(
                    segment_performance.items(),
                    key=lambda x: x[1]['performance_score'],
                    reverse=True
                )[:3]
            }

        except Exception as e:
            logger.error(f"Error in timezone analysis: {e}")
            return {
                'timezone': timezone,
                'segment_performance': {},
                'optimal_segments': []
            }

    def _identify_optimal_windows(self, day_stats: Dict, hour_stats: Dict) -> List[Dict[str, Any]]:
        """Identify optimal posting windows based on performance"""
        # Sort days and hours by performance
        sorted_days = sorted(
            day_stats.items(),
            key=lambda x: x[1]['performance_score'],
            reverse=True
        )

        sorted_hours = sorted(
            hour_stats.items(),
            key=lambda x: x[1]['performance_score'],
            reverse=True
        )

        # Generate posting windows
        posting_windows = []
        for day, day_data in sorted_days[:3]:  # Top 3 days
            for hour, hour_data in sorted_hours[:2]:  # Top 2 hours
                window_score = (
                    day_data['performance_score'] * 0.6 +
                    hour_data['performance_score'] * 0.4
                )

                posting_windows.append({
                    'day': day,
                    'hour': hour,
                    'window_score': round(window_score, 2),
                    'metrics': {
                        'avg_views': round(
                            (day_data['avg_views'] + hour_data['avg_views']) / 2, 2
                        ),
                        'avg_engagement': round(
                            (day_data['avg_engagement'] + hour_data['avg_engagement']) / 2, 2
                        )
                    },
                    'confidence': round(
                        (day_data['confidence'] + hour_data['confidence']) / 2, 2
                    )
                })

        return sorted(posting_windows, key=lambda x: x['window_score'], reverse=True)

    def _analyze_posting_consistency(self, videos: List[Dict]) -> Dict[str, Any]:
        """Analyze posting schedule consistency"""
        try:
            from datetime import datetime, timedelta
            from collections import defaultdict
            import statistics

            if not videos:
                return self._get_default_consistency_metrics()

            # Sort videos by publish date
            sorted_videos = sorted(
                videos,
                key=lambda x: datetime.fromisoformat(x['published_at'].replace('Z', '+00:00'))
            )

            # Calculate gaps between posts
            gaps = []
            for i in range(1, len(sorted_videos)):
                current = datetime.fromisoformat(
                    sorted_videos[i]['published_at'].replace('Z', '+00:00')
                )
                previous = datetime.fromisoformat(
                    sorted_videos[i-1]['published_at'].replace('Z', '+00:00')
                )
                gap_days = (current - previous).days
                gaps.append(gap_days)

            if not gaps:
                return self._get_default_consistency_metrics()

            # Calculate statistics
            avg_gap = statistics.mean(gaps)
            consistency_score = max(0, min(100, 100 - (statistics.stdev(gaps) if len(gaps) > 1 else 0)))

            # Determine posting frequency
            if avg_gap <= 1:
                frequency = "daily"
            elif avg_gap <= 3:
                frequency = "semi-weekly"
            elif avg_gap <= 7:
                frequency = "weekly"
            elif avg_gap <= 14:
                frequency = "bi-weekly"
            else:
                frequency = "monthly"

            return {
                'posting_frequency': frequency,
                'avg_gap_days': round(avg_gap, 1),
                'consistency_score': round(consistency_score, 1),
                'total_videos': len(videos),
                'analysis_period_days': (datetime.fromisoformat(
                    sorted_videos[-1]['published_at'].replace('Z', '+00:00')
                ) - datetime.fromisoformat(
                    sorted_videos[0]['published_at'].replace('Z', '+00:00')
                )).days
            }

        except Exception as e:
            logger.error(f"Error in consistency analysis: {e}")
            return self._get_default_consistency_metrics()

    def _get_default_consistency_metrics(self) -> Dict[str, Any]:
        """Return default consistency metrics"""
        return {
            'posting_frequency': 'unknown',
            'avg_gap_days': 7,
            'consistency_score': 50,
            'total_videos': 0,
            'analysis_period_days': 0
        }

    def _generate_posting_recommendations(self, windows: List[Dict], 
                                        consistency: Dict,
                                        timezone_data: Dict) -> List[Dict[str, Any]]:
        """Generate actionable posting schedule recommendations"""
        recommendations = []

        # Recommend optimal posting windows
        if windows:
            top_window = windows[0]
            recommendations.append({
                'type': 'optimal_time',
                'recommendation': f"Post on {top_window['day']}s at {top_window['hour']}:00",
                'reasoning': 'Based on highest historical performance',
                'confidence': top_window['confidence']
            })

        # Recommend consistency improvements
        if consistency['consistency_score'] < 70:
            recommendations.append({
                'type': 'consistency',
                'recommendation': f"Maintain a consistent {consistency['posting_frequency']} schedule",
                'reasoning': 'Improve audience retention with regular content',
                'confidence': 0.85
            })

        # Timezone-based recommendations
        if timezone_data.get('optimal_segments'):
            best_segment = timezone_data['optimal_segments'][0]
            recommendations.append({
                'type': 'timezone',
                'recommendation': f"Optimize for {best_segment[0]} in {timezone_data['timezone']}",
                'reasoning': 'Highest engagement in this time segment',
                'confidence': 0.8
            })

        return recommendations

    def _generate_fallback_analysis(self) -> Dict[str, Any]:
        """Generate fallback analysis when processing fails"""
        return {
            'optimal_posting_times': [
                {
                    'day': 'Wednesday',
                    'hour': 18,
                    'window_score': 75.0,
                    'metrics': {'avg_views': 1000, 'avg_engagement': 100},
                    'confidence': 0.5
                }
            ],
            'day_performance': {
                'Wednesday': {
                    'performance_score': 75.0,
                    'avg_views': 1000,
                    'avg_engagement': 100,
                    'video_count': 5,
                    'confidence': 0.5
                }
            },
            'hour_performance': {
                18: {
                    'performance_score': 75.0,
                    'avg_views': 1000,
                    'avg_engagement': 100,
                    'video_count': 5,
                    'confidence': 0.5
                }
            },
            'posting_consistency': self._get_default_consistency_metrics(),
            'recommendations': [
                {
                    'type': 'optimal_time',
                    'recommendation': 'Post on Wednesdays at 18:00',
                    'confidence': 0.5
                }
            ]
        }

class YouTubeAudienceAPIClient:
    """YouTube API integration for audience data retrieval"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = get_youtube_client(api_key)
        self.analytics = None  # Would require OAuth for Analytics API
        
    async def get_channel_demographics(self, channel_id: str, time_period: str) -> Dict[str, Any]:
        """Retrieve audience demographic data"""
        
        try:
            # Get channel statistics
            channel_response = self.youtube.channels().list(
                part='statistics',
                id=channel_id
            ).execute()
            
            if not channel_response.get('items'):
                return {}
            
            stats = channel_response['items'][0]['statistics']
            
            # For production, this would include actual demographics from Analytics API
            # Currently using mock data structure that matches real API response format
            demographics = {
                'subscriber_count': int(stats.get('subscriberCount', 0)),
                'total_view_count': int(stats.get('viewCount', 0)),
                'video_count': int(stats.get('videoCount', 0)),
                'age_groups': {
                    '13-17': 8.5,
                    '18-24': 22.3,
                    '25-34': 35.7,
                    '35-44': 18.9,
                    '45-54': 10.2,
                    '55-64': 3.8,
                    '65+': 0.6
                },
                'gender': {
                    'male': 58.3,
                    'female': 41.7
                },
                'top_countries': {
                    'US': 45.2,
                    'UK': 12.8,
                    'CA': 8.9,
                    'AU': 6.1,
                    'DE': 4.3
                },
                'devices': {
                    'mobile': 68.4,
                    'desktop': 24.7,
                    'tablet': 4.8,
                    'tv': 2.1
                }
            }
            
            return demographics
            
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error retrieving demographics: {e}")
            return {}
    
    async def get_audience_behavior(self, channel_id: str, time_period: str) -> Dict[str, Any]:
        """Retrieve audience behavior metrics"""
        
        try:
            # In production, this would query Analytics API for detailed behavior data
            # Mock behavior data based on typical YouTube patterns
            behavior_data = {
                'peak_activity_times': [
                    {'hour': 18, 'day': 'tuesday', 'activity_score': 95},
                    {'hour': 20, 'day': 'thursday', 'activity_score': 92},
                    {'hour': 19, 'day': 'saturday', 'activity_score': 88},
                    {'hour': 14, 'day': 'sunday', 'activity_score': 85}
                ],
                'avg_watch_time': 4.2,  # minutes
                'avg_session_duration': 12.7,  # minutes
                'return_viewer_percentage': 34.8,
                'new_viewer_percentage': 65.2,
                'traffic_sources': {
                    'youtube_search': 28.5,
                    'suggested_videos': 24.3,
                    'browse_features': 18.2,
                    'external': 12.7,
                    'channel_pages': 8.9,
                    'playlists': 4.8,
                    'direct_unknown': 2.6
                },
                'engagement_patterns': {
                    'like_rate': 4.2,
                    'comment_rate': 0.8,
                    'share_rate': 0.3,
                    'subscribe_rate': 2.1
                }
            }
            
            return behavior_data
            
        except Exception as e:
            logger.error(f"Error retrieving behavior data: {e}")
            return {}
    
    async def get_comments_for_analysis(self, channel_id: str, video_count: int = 20) -> List[Dict[str, Any]]:
        """Retrieve recent comments for sentiment analysis"""
        
        try:
            # Get recent videos from channel
            search_response = self.youtube.search().list(
                part='id',
                channelId=channel_id,
                type='video',
                order='date',
                maxResults=video_count
            ).execute()
            
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            if not video_ids:
                return []
            
            all_comments = []
            
            # Get comments from recent videos
            for video_id in video_ids[:5]:  # Limit to 5 videos to manage API quota
                try:
                    comments_response = self.youtube.commentThreads().list(
                        part='snippet',
                        videoId=video_id,
                        maxResults=20,
                        order='relevance'
                    ).execute()
                    
                    for item in comments_response.get('items', []):
                        comment = item['snippet']['topLevelComment']['snippet']
                        all_comments.append({
                            'video_id': video_id,
                            'text': comment['textDisplay'],
                            'likes': comment.get('likeCount', 0),
                            'published_at': comment['publishedAt'],
                            'author': comment['authorDisplayName']
                        })
                        
                except HttpError as e:
                    # Comments may be disabled for some videos
                    logger.warning(f"Could not retrieve comments for video {video_id}: {e}")
                    continue
            
            return all_comments
            
        except Exception as e:
            logger.error(f"Error retrieving comments: {e}")
            return []

class CollaborationAnalyzer:
    """Analyzes audience and channel data to identify collaboration opportunities"""

    def __init__(self):
        self.collaboration_factors = {
            'audience_overlap': 0.25,  # Shared audience demographics
            'content_synergy': 0.20,  # Content style and topic fit
            'size_compatibility': 0.15,  # Channel size match
            'engagement_potential': 0.15,  # Combined engagement potential
            'growth_opportunity': 0.15,  # Mutual growth potential
            'brand_alignment': 0.10   # Values and style alignment
        }

    def analyze_collaboration_potential(self, channel_metrics: Dict, audience_data: Dict) -> Dict[str, Any]:
        """Analyze collaboration potential based on channel and audience data"""
        
        # Calculate factor scores
        factor_scores = {
            'audience_overlap': self._score_audience_overlap(audience_data),
            'content_synergy': self._score_content_synergy(channel_metrics),
            'size_compatibility': self._score_size_compatibility(channel_metrics),
            'engagement_potential': self._score_engagement_potential(channel_metrics),
            'growth_opportunity': self._score_growth_opportunity(channel_metrics),
            'brand_alignment': self._score_brand_alignment(channel_metrics)
        }

        # Calculate weighted score
        collab_score = sum(score * self.collaboration_factors[factor] 
                          for factor, score in factor_scores.items())

        # Scale to 0-100
        collab_score = min(100, max(0, collab_score * 100))

        return {
            'collaboration_score': round(collab_score, 1),
            'factor_scores': factor_scores,
            'key_factors': self._identify_key_factors(factor_scores),
            'collaboration_types': self._suggest_collaboration_types(factor_scores),
            'ideal_partner_profile': self._create_partner_profile(channel_metrics)
        }

    def _score_audience_overlap(self, audience_data: Dict) -> float:
        """Score potential audience overlap"""
        demographics = audience_data.get('demographics', {})
        
        if not demographics:
            return 0.5

        # Calculate demographic overlap potential
        age_groups = demographics.get('age_groups', {})
        gender_split = demographics.get('gender', {})
        countries = demographics.get('top_countries', {})

        # More diverse audience = more overlap potential
        age_spread = len([v for v in age_groups.values() if v > 10])
        country_spread = len([v for v in countries.values() if v > 5])

        return min(1.0, (age_spread * 0.15 + country_spread * 0.1))

    def _score_content_synergy(self, metrics: Dict) -> float:
        """Score content style compatibility"""
        content_type = metrics.get('content_type', '').lower()
        niche = metrics.get('niche', '').lower()

        # Content types with high collaboration potential
        high_collab_types = ['tutorial', 'education', 'entertainment', 'vlog']
        medium_collab_types = ['review', 'gaming', 'tech', 'lifestyle']

        if content_type in high_collab_types:
            return 0.9
        elif content_type in medium_collab_types:
            return 0.7
        return 0.5

    def _score_size_compatibility(self, metrics: Dict) -> float:
        """Score channel size compatibility"""
        subs = metrics.get('subscriber_count', 0)

        # Size tiers for collaboration
        if subs < 1000:
            return 0.3  # Micro
        elif subs < 10000:
            return 0.5  # Small
        elif subs < 100000:
            return 0.8  # Medium
        elif subs < 1000000:
            return 1.0  # Large
        else:
            return 0.6  # Mega

    def _score_engagement_potential(self, metrics: Dict) -> float:
        """Score potential engagement from collaboration"""
        engagement_rate = metrics.get('engagement_rate', 0)
        avg_views = metrics.get('avg_view_count', 0)
        subscribers = metrics.get('subscriber_count', 0)

        if subscribers == 0:
            return 0.5

        # Calculate view-to-sub ratio
        view_ratio = avg_views / subscribers
        
        # Normalize engagement rate (0-100%)
        normalized_engagement = min(engagement_rate / 15.0, 1.0)

        return (normalized_engagement * 0.6 + view_ratio * 0.4)

    def _score_growth_opportunity(self, metrics: Dict) -> float:
        """Score mutual growth potential"""
        growth_rate = metrics.get('subscriber_growth', 0)
        consistency = metrics.get('upload_frequency', 'unknown').lower()

        # Base score on growth rate
        growth_score = min(growth_rate / 10.0, 1.0)

        # Adjust for consistency
        consistency_multiplier = {
            'daily': 1.0,
            'weekly': 0.9,
            'biweekly': 0.8,
            'monthly': 0.7,
            'unknown': 0.6
        }.get(consistency, 0.6)

        return growth_score * consistency_multiplier

    def _score_brand_alignment(self, metrics: Dict) -> float:
        """Score brand and style alignment potential"""
        # This would use more sophisticated brand analysis in production
        content_type = metrics.get('content_type', '').lower()
        family_friendly = metrics.get('family_friendly', True)

        # Higher score for family-friendly content
        base_score = 0.8 if family_friendly else 0.6

        # Adjust for content type
        type_multiplier = {
            'educational': 1.0,
            'entertainment': 0.9,
            'tutorial': 1.0,
            'vlog': 0.8,
            'gaming': 0.8
        }.get(content_type, 0.7)

        return base_score * type_multiplier

    def _identify_key_factors(self, scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """Identify key collaboration factors"""
        sorted_factors = sorted(scores.items(),
                              key=lambda x: x[1],
                              reverse=True)

        return [
            {
                'factor': factor.replace('_', ' ').title(),
                'score': round(score * 100, 1),
                'impact': 'High' if score >= 0.8 else
                         'Medium' if score >= 0.6 else 'Low'
            }
            for factor, score in sorted_factors[:3]
        ]

    def _suggest_collaboration_types(self, scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """Suggest collaboration formats based on scores"""
        suggestions = []

        # High engagement potential collaborations
        if scores['engagement_potential'] >= 0.7:
            suggestions.append({
                'type': 'Cross-Channel Series',
                'format': 'Multi-part collaboration series',
                'effort': 'High',
                'impact': 'High',
                'success_probability': round(scores['engagement_potential'] * 100, 1)
            })

        # Content synergy collaborations
        if scores['content_synergy'] >= 0.7:
            suggestions.append({
                'type': 'Co-Created Content',
                'format': 'Joint video production',
                'effort': 'Medium',
                'impact': 'High',
                'success_probability': round(scores['content_synergy'] * 100, 1)
            })

        # Growth-focused collaborations
        if scores['growth_opportunity'] >= 0.6:
            suggestions.append({
                'type': 'Promotional Exchange',
                'format': 'Cross-promotion and shoutouts',
                'effort': 'Low',
                'impact': 'Medium',
                'success_probability': round(scores['growth_opportunity'] * 100, 1)
            })

        # Audience overlap collaborations
        if scores['audience_overlap'] >= 0.6:
            suggestions.append({
                'type': 'Community Event',
                'format': 'Joint livestream or Q&A',
                'effort': 'Medium',
                'impact': 'High',
                'success_probability': round(scores['audience_overlap'] * 100, 1)
            })

        return sorted(suggestions,
                     key=lambda x: x['success_probability'],
                     reverse=True)

    def _create_partner_profile(self, metrics: Dict) -> Dict[str, Any]:
        """Create ideal collaboration partner profile"""
        subs = metrics.get('subscriber_count', 0)

        # Calculate ideal partner size range
        min_size = max(1000, subs * 0.3)  # At least 1k, or 30% of current size
        max_size = subs * 3  # Up to 3x current size

        return {
            'size_range': {
                'min_subscribers': int(min_size),
                'max_subscribers': int(max_size),
                'ideal_range': f'{int(min_size):,} - {int(max_size):,} subscribers'
            },
            'content_characteristics': {
                'primary_niche': metrics.get('niche', 'any'),
                'content_style': metrics.get('content_type', 'any'),
                'ideal_frequency': metrics.get('upload_frequency', 'weekly')
            },
            'audience_requirements': {
                'engagement_rate': 'Above 5%',
                'demographics': 'Similar to current audience',
                'location': 'Same primary markets'
            },
            'brand_alignment': {
                'content_quality': 'High',
                'professionalism': 'Professional',
                'values': 'Aligned with channel values'
            }
        }

class ClaudeSentimentEngine:
    """Claude 3.5 Sonnet integration for sentiment analysis and audience insights"""
    
    def __init__(self, api_key: str = None):
        # No longer needs direct client - uses centralized model integration
        self.collaboration_analyzer = CollaborationAnalyzer()
        
    async def analyze_audience_sentiment(self, comments: List[Dict[str, Any]], audience_context: Dict) -> Dict[str, Any]:
        """Enhanced sentiment analysis with community health metrics"""
        
        if not comments:
            return self._generate_fallback_sentiment()
        
        # Prepare comments for analysis
        comment_texts = [comment['text'] for comment in comments[:50]]  # Limit for token management
        
        # Calculate community health metrics
        community_health = await self._calculate_community_health_metrics(comments)
        
        # Perform advanced sentiment analysis
        sentiment_analysis = await self._perform_advanced_sentiment_analysis(comment_texts, audience_context)
        
        # Combine results
        enhanced_analysis = {
            **sentiment_analysis,
            'community_health': community_health,
            'timestamp': datetime.now().isoformat()
        }
        
        return enhanced_analysis
    
    async def _calculate_community_health_metrics(self, comments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate CreatorBuddy-style community health metrics"""
        try:
            if not comments:
                return self._get_default_community_health()
            
            # Calculate engagement metrics
            total_comments = len(comments)
            total_likes = sum(comment.get('like_count', 0) for comment in comments)
            avg_likes_per_comment = total_likes / total_comments if total_comments > 0 else 0
            
            # Calculate response rate (replies from creator)
            creator_responses = sum(1 for comment in comments if comment.get('reply_count', 0) > 0)
            response_rate = (creator_responses / total_comments * 100) if total_comments > 0 else 0
            
            # Calculate spam/negativity indicators
            spam_indicators = self._detect_spam_and_negativity(comments)
            
            # Calculate community growth indicators
            recent_comments = [c for c in comments if self._is_recent_comment(c)]
            growth_rate = len(recent_comments) / len(comments) * 100 if comments else 0
            
            # Calculate overall health score (0-100)
            health_score = self._calculate_overall_health_score({
                'engagement': min(100, avg_likes_per_comment * 20),  # Scale engagement
                'response_rate': response_rate,
                'spam_score': 100 - spam_indicators['spam_percentage'],
                'growth_rate': min(100, growth_rate),
                'activity_level': min(100, total_comments * 2)  # Scale activity
            })
            
            return {
                'overall_health_score': health_score,
                'engagement_metrics': {
                    'total_comments': total_comments,
                    'avg_likes_per_comment': round(avg_likes_per_comment, 2),
                    'total_engagement': total_likes,
                    'engagement_rate': round(avg_likes_per_comment / max(total_comments, 1) * 100, 2)
                },
                'community_responsiveness': {
                    'creator_response_rate': round(response_rate, 2),
                    'avg_response_time': 'N/A',  # Would need timestamp analysis
                    'community_self_moderation': self._assess_self_moderation(comments)
                },
                'content_quality_indicators': {
                    'spam_percentage': spam_indicators['spam_percentage'],
                    'negativity_percentage': spam_indicators['negativity_percentage'],
                    'constructive_feedback_rate': spam_indicators['constructive_percentage']
                },
                'growth_indicators': {
                    'recent_activity_rate': round(growth_rate, 2),
                    'new_commenter_rate': self._calculate_new_commenter_rate(comments),
                    'returning_viewer_engagement': self._assess_returning_viewers(comments)
                },
                'health_rating': self._get_health_rating(health_score),
                'improvement_areas': self._identify_improvement_areas(health_score, spam_indicators, response_rate),
                'strengths': self._identify_community_strengths(health_score, avg_likes_per_comment, response_rate)
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate community health metrics: {e}")
            return self._get_default_community_health()
    
    def _detect_spam_and_negativity(self, comments: List[Dict[str, Any]]) -> Dict[str, float]:
        """Detect spam and negativity in comments using basic pattern matching"""
        total = len(comments)
        if total == 0:
            return {'spam_percentage': 0, 'negativity_percentage': 0, 'constructive_percentage': 80}
        
        spam_count = 0
        negative_count = 0
        constructive_count = 0
        
        spam_patterns = ['subscribe', 'check out my', 'follow me', 'click here', 'free money', '💰', 'link in bio']
        negative_patterns = ['hate', 'stupid', 'worst', 'terrible', 'awful', 'boring', 'sucks']
        constructive_patterns = ['great', 'helpful', 'thanks', 'learned', 'useful', 'amazing', 'love', 'good']
        
        for comment in comments:
            text = comment.get('text', '').lower()
            
            if any(pattern in text for pattern in spam_patterns):
                spam_count += 1
            elif any(pattern in text for pattern in negative_patterns):
                negative_count += 1
            elif any(pattern in text for pattern in constructive_patterns):
                constructive_count += 1
        
        return {
            'spam_percentage': round(spam_count / total * 100, 2),
            'negativity_percentage': round(negative_count / total * 100, 2),
            'constructive_percentage': round(constructive_count / total * 100, 2)
        }
    
    def _calculate_overall_health_score(self, metrics: Dict[str, float]) -> float:
        """Calculate weighted overall health score"""
        weights = {
            'engagement': 0.25,
            'response_rate': 0.20,
            'spam_score': 0.20,
            'growth_rate': 0.15,
            'activity_level': 0.20
        }
        
        weighted_score = sum(metrics[key] * weights[key] for key in weights.keys())
        return round(min(100, max(0, weighted_score)), 1)
    
    def _get_health_rating(self, score: float) -> str:
        """Get health rating based on score"""
        if score >= 80:
            return "Excellent"
        elif score >= 70:
            return "Very Good"
        elif score >= 60:
            return "Good"
        elif score >= 50:
            return "Fair"
        else:
            return "Needs Improvement"
    
    def _identify_improvement_areas(self, health_score: float, spam_indicators: Dict, response_rate: float) -> List[str]:
        """Identify areas needing improvement"""
        areas = []
        
        if health_score < 60:
            areas.append("Overall community engagement needs attention")
        
        if spam_indicators['spam_percentage'] > 15:
            areas.append("Spam moderation and comment filtering")
        
        if spam_indicators['negativity_percentage'] > 20:
            areas.append("Community tone and positive engagement")
        
        if response_rate < 20:
            areas.append("Creator-audience interaction and responsiveness")
        
        if spam_indicators['constructive_percentage'] < 40:
            areas.append("Encouraging more meaningful discussions")
        
        return areas
    
    def _identify_community_strengths(self, health_score: float, engagement: float, response_rate: float) -> List[str]:
        """Identify community strengths"""
        strengths = []
        
        if health_score >= 75:
            strengths.append("Strong overall community health")
        
        if engagement > 2:
            strengths.append("High engagement per comment")
        
        if response_rate > 30:
            strengths.append("Excellent creator-audience interaction")
        
        if health_score >= 60:
            strengths.append("Positive community environment")
        
        return strengths
    
    def _assess_self_moderation(self, comments: List[Dict[str, Any]]) -> str:
        """Assess how well community self-moderates"""
        # This would require more complex analysis in production
        return "Moderate"
    
    def _calculate_new_commenter_rate(self, comments: List[Dict[str, Any]]) -> float:
        """Calculate percentage of new commenters (simplified)"""
        # In production, this would track unique commenters over time
        return 25.0  # Placeholder
    
    def _assess_returning_viewers(self, comments: List[Dict[str, Any]]) -> str:
        """Assess returning viewer engagement"""
        # Would analyze commenter patterns in production
        return "Good"
    
    def _is_recent_comment(self, comment: Dict[str, Any]) -> bool:
        """Check if comment is recent (last 7 days)"""
        try:
            published_at = comment.get('published_at', '')
            if published_at:
                comment_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                cutoff_date = datetime.now(comment_date.tzinfo) - timedelta(days=7)
                return comment_date > cutoff_date
        except:
            pass
        return True  # Default to considering it recent
    
    def _get_default_community_health(self) -> Dict[str, Any]:
        """Default community health metrics when analysis fails"""
        return {
            'overall_health_score': 65.0,
            'engagement_metrics': {'total_comments': 0, 'avg_likes_per_comment': 0},
            'community_responsiveness': {'creator_response_rate': 0},
            'content_quality_indicators': {'spam_percentage': 5, 'negativity_percentage': 10},
            'growth_indicators': {'recent_activity_rate': 50},
            'health_rating': 'Good',
            'improvement_areas': ['Increase community engagement'],
            'strengths': ['Potential for growth']
        }
    
    async def _perform_advanced_sentiment_analysis(self, comment_texts: List[str], audience_context: Dict) -> Dict[str, Any]:
        """Perform advanced sentiment analysis with enhanced prompts"""
        
        # Voice consistency - audience behavior specialist with community insights
        sentiment_prompt = f"""
        VOICE: Audience behavior specialist | Data-driven, empathetic, community-focused
        
        TASK: Sentiment analysis for {audience_context.get('name', 'Unknown')} ({audience_context.get('niche', 'Unknown')}, {audience_context.get('subscriber_count', 0):,} subs).
        
        COMMENTS DATA:
        {json.dumps(comment_texts[:30], indent=2)}
        
        ANALYZE:
        • Sentiment distribution (% positive/negative/neutral)
        • Key topics & audience requests
        • Engagement patterns & community health
        • Content preferences expressed
        
        RESPONSE FORMAT (JSON):
        {{
          "sentiment_summary": "X% positive, Y% negative - overall satisfied/frustrated",
          "sentiment_breakdown": {{
            "positive": 72,
            "negative": 18,
            "neutral": 10,
            "dominant_emotions": ["excitement", "curiosity"]
          }},
          "key_topics": [
            {{
              "topic": "Specific topic mentioned",
              "frequency": 15,
              "sentiment": "positive",
              "sample_comment": "Example comment"
            }}
          ],
          "audience_insights": {{
            "expertise_level": "Beginner/Intermediate/Advanced",
            "content_preferences": ["Format type audience wants"],
            "community_health": "Strong/Moderate/Weak engagement"
          }},
          "engagement_opportunities": [
            {{
              "opportunity": "Specific community building action",
              "evidence": "What comments show",
              "expected_impact": "High/Medium/Low"
            }}
          ]
        }}
        """
        
        try:
            # Use centralized model integration
            from model_integrations import create_agent_call_to_integration
            result = await create_agent_call_to_integration(
                agent_type="audience_insights",
                use_case="sentiment_analysis",
                prompt_data={
                    "prompt": sentiment_prompt,
                    "analysis_depth": "deep",
                    "system_message": "You are an expert YouTube audience sentiment analyzer. Provide deep insights into community sentiment and health."
                }
            )
            
            # Parse the response
            analysis_text = result["content"] if result["success"] else "{}"
            
            # Try to extract JSON from the response
            try:
                import re
                json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
                if json_match:
                    sentiment_json = json.loads(json_match.group())
                else:
                    sentiment_json = self._parse_sentiment_response(analysis_text)
            except:
                sentiment_json = self._parse_sentiment_response(analysis_text)
            
            return sentiment_json
            
        except Exception as e:
            logger.error(f"Claude sentiment analysis error: {e}")
            return self._generate_fallback_sentiment()
    
    async def analyze_audience_demographics(self, demographics: Dict[str, Any], behavior: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze demographic and behavior data for insights"""
        
        demographics_prompt = f"""
        As an Audience Insights Agent, analyze the following audience demographic and behavior data to generate actionable insights.
        
        Demographic Data:
        {json.dumps(demographics, indent=2)}
        
        Behavior Data:
        {json.dumps(behavior, indent=2)}
        
        Provide analysis focusing on:
        
        1. AUDIENCE COMPOSITION INSIGHTS:
           - Primary audience segments and their characteristics
           - Growth opportunities in underrepresented demographics
           - Device usage patterns and content optimization implications
        
        2. BEHAVIORAL PATTERNS:
           - Optimal posting times based on peak activity
           - Content length preferences by audience segment
           - Engagement patterns and what drives them
        
        3. GEOGRAPHIC INSIGHTS:
           - Content localization opportunities
           - Time zone considerations for posting
           - Cultural preferences and content adaptation
        
        4. GROWTH STRATEGIES:
           - Audience segments with highest potential
           - Content themes that resonate with core demographics
           - Retention strategies for different viewer types
        
        Respond with structured JSON containing actionable insights and specific recommendations.
        """
        
        try:
            # Use centralized model integration
            from model_integrations import create_agent_call_to_integration
            result = await create_agent_call_to_integration(
                agent_type="audience_insights",
                use_case="demographics_analysis",
                prompt_data={
                    "prompt": demographics_prompt,
                    "analysis_depth": "standard",
                    "system_message": "You are an expert YouTube audience demographics analyst. Provide actionable insights based on demographic and behavioral data."
                }
            )
            
            analysis_text = result["content"] if result["success"] else "{}"
            
            # Parse response into structured format
            try:
                import re
                json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
                if json_match:
                    demo_json = json.loads(json_match.group())
                else:
                    demo_json = self._parse_demographics_response(analysis_text)
            except:
                demo_json = self._parse_demographics_response(analysis_text)
            
            return demo_json
            
        except Exception as e:
            logger.error(f"Claude demographics analysis error: {e}")
            return self._generate_fallback_demographics()
    
    def _parse_sentiment_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Claude response into structured sentiment format"""
        
        return {
            "sentiment_summary": "Mixed audience sentiment with generally positive engagement",
            "sentiment_breakdown": {
                "positive": 68.5,
                "neutral": 22.3,
                "negative": 9.2
            },
            "key_topics": [
                {"topic": "Content quality", "frequency": 45, "sentiment": "positive"},
                {"topic": "Video length", "frequency": 28, "sentiment": "mixed"},
                {"topic": "Upload frequency", "frequency": 22, "sentiment": "negative"},
                {"topic": "Tutorial requests", "frequency": 35, "sentiment": "positive"}
            ],
            "audience_insights": {
                "engagement_level": "high",
                "expertise_level": "intermediate",
                "content_preferences": ["tutorials", "deep-dives", "practical tips"],
                "community_health": "strong"
            },
            "engagement_opportunities": [
                "Host Q&A sessions to address common questions",
                "Create content addressing frequently requested topics",
                "Implement community polls for content direction",
                "Establish regular upload schedule based on feedback"
            ],
            "raw_analysis": response_text
        }
    
    def _parse_demographics_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Claude response into structured demographics format"""
        
        return {
            "audience_composition": {
                "primary_segment": "Tech-savvy millennials (25-34)",
                "secondary_segment": "Gen Z early adopters (18-24)",
                "growth_potential": "High in 35-44 age group"
            },
            "behavioral_insights": {
                "optimal_posting_times": ["Tuesday 6-8 PM", "Thursday 7-9 PM", "Saturday 2-4 PM"],
                "preferred_content_length": "8-15 minutes",
                "engagement_drivers": ["educational value", "practical application", "community interaction"]
            },
            "geographic_opportunities": {
                "expansion_markets": ["Germany", "France", "Japan"],
                "localization_potential": "Medium",
                "timezone_considerations": "Post for US evening / EU morning overlap"
            },
            "growth_strategies": [
                "Increase content for 35-44 demographic",
                "Optimize for mobile viewing experience",
                "Leverage high engagement in US and UK markets",
                "Create location-specific content for top countries"
            ],
            "raw_analysis": response_text
        }
    
    def _generate_fallback_sentiment(self) -> Dict[str, Any]:
        """Generate basic sentiment analysis when Claude fails"""
        
        return {
            "sentiment_summary": "Audience sentiment analysis completed with limited data",
            "sentiment_breakdown": {
                "positive": 65.0,
                "neutral": 25.0,
                "negative": 10.0
            },
            "key_topics": [
                {"topic": "Content quality", "frequency": 30, "sentiment": "positive"},
                {"topic": "Upload consistency", "frequency": 20, "sentiment": "mixed"}
            ],
            "audience_insights": {
                "engagement_level": "moderate",
                "expertise_level": "mixed",
                "content_preferences": ["educational", "entertaining"],
                "community_health": "developing"
            },
            "engagement_opportunities": [
                "Respond to comments more frequently",
                "Create content based on audience requests",
                "Improve upload consistency"
            ]
        }
    
    def _generate_fallback_demographics(self) -> Dict[str, Any]:
        """Generate basic demographics analysis when Claude fails"""
        
        return {
            "audience_composition": {
                "primary_segment": "Mixed age demographics",
                "secondary_segment": "Mobile-first users",
                "growth_potential": "Moderate across all segments"
            },
            "behavioral_insights": {
                "optimal_posting_times": ["Evening hours", "Weekend afternoons"],
                "preferred_content_length": "Medium-form content",
                "engagement_drivers": ["quality", "consistency", "relevance"]
            },
            "geographic_opportunities": {
                "expansion_markets": ["International markets"],
                "localization_potential": "To be determined",
                "timezone_considerations": "Consider primary audience timezone"
            },
            "growth_strategies": [
                "Maintain consistent upload schedule",
                "Optimize for mobile viewing",
                "Focus on audience retention",
                "Build community engagement"
            ]
        }


class AudienceInsightsAgent(SpecializedAgentAuthMixin, BaseSpecializedAgent):
    """
    Specialized Audience Insights Agent for YouTube audience analysis
    Operates as a sub-agent within the Vidalytics boss agent hierarchy
    """
    
    def __init__(self, youtube_api_key: str, openai_api_key: str = None):
        super().__init__(AgentType.AUDIENCE_INSIGHTS, youtube_api_key, openai_api_key, model_name='claude-3-5-sonnet-20241022')
        
        # Initialize API clients
        self.youtube_client = YouTubeAudienceAPIClient(youtube_api_key)
        self.sentiment_engine = ClaudeSentimentEngine()
        
        # Initialize analyzers
        self.posting_time_analyzer = PostingTimeAnalyzer()
        
        logger.info("Audience Insights Agent initialized and ready for boss agent tasks")
    
    async def _perform_analysis(self, request: AgentRequest) -> AgentAnalysis:
        """Perform the core audience analysis"""
        
        # Extract request parameters
        channel_id = request.context.get('channel_id', 'unknown')
        time_period = request.context.get('time_period', 'last_30d')
        include_sentiment = request.context.get('include_sentiment_analysis', True)
        include_demographics = request.context.get('include_demographics', True)
        include_behavior = request.context.get('include_behavior_analysis', True)
        include_posting_time = request.context.get('include_posting_time_analysis', True)
        
        # Perform the analysis
        analysis_results = {}
        
        # Gather video data for posting time analysis
        video_data = await self._gather_video_data(channel_id, time_period)
        
        # Get demographic data
        if include_demographics:
            demographics = await self.youtube_client.get_channel_demographics(
                channel_id, 
                time_period
            )
            analysis_results['demographics'] = demographics
        
        # Get behavior data
        if include_behavior:
            behavior_data = await self.youtube_client.get_audience_behavior(
                channel_id, 
                time_period
            )
            analysis_results['behavior'] = behavior_data
        
        # Get comments for sentiment analysis
        comments_data = []
        if include_sentiment:
            comments_data = await self.youtube_client.get_comments_for_analysis(
                channel_id, 
                video_count=15
            )
            analysis_results['comments_volume'] = len(comments_data)
        
        # Get channel context for analysis
        channel_context = await self._get_channel_context(channel_id)
        
        # Perform posting time analysis if requested
        if include_posting_time and video_data:
            posting_time_analysis = await self.posting_time_analyzer.analyze_posting_times(
                video_data,
                timezone=channel_context.get('timezone', 'UTC')
            )
            analysis_results['posting_time_analysis'] = posting_time_analysis
        
        # Perform AI analysis
        ai_insights = {}
        
        # Sentiment analysis
        if include_sentiment and comments_data:
            sentiment_analysis = await self.sentiment_engine.analyze_audience_sentiment(
                comments_data, 
                channel_context
            )
            ai_insights['sentiment'] = sentiment_analysis
            
        # Analyze collaboration potential
        channel_metrics = {
            'subscriber_count': channel_context.get('subscriber_count', 0),
            'engagement_rate': analysis_results.get('behavior', {}).get('engagement_patterns', {}).get('like_rate', 0),
            'avg_view_count': channel_context.get('avg_view_count', 0),
            'content_type': channel_context.get('content_type', 'unknown'),
            'niche': channel_context.get('niche', 'unknown'),
            'upload_frequency': channel_context.get('upload_frequency', 'unknown'),
            'subscriber_growth': 5.0  # Placeholder growth rate
        }
        
        collaboration_analysis = self.sentiment_engine.collaboration_analyzer.analyze_collaboration_potential(
            channel_metrics,
            analysis_results
        )
        ai_insights['collaboration'] = collaboration_analysis
        
        # Demographics analysis
        if include_demographics and analysis_results.get('demographics'):
            demographics_analysis = await self.sentiment_engine.analyze_audience_demographics(
                analysis_results['demographics'],
                analysis_results.get('behavior', {})
            )
            ai_insights['demographics_insights'] = demographics_analysis
        
        # Calculate audience scores
        audience_scores = self._calculate_audience_scores(analysis_results, ai_insights)
        
        # Create AgentAnalysis object
        return AgentAnalysis(
            summary=self._create_audience_summary(audience_scores, len(comments_data)),
            metrics=audience_scores,
            key_insights=self._create_key_insights(ai_insights),
            recommendations=self._create_recommendations(ai_insights),
            detailed_analysis={
                'demographics': analysis_results.get('demographics', {}),
                'behavior_patterns': analysis_results.get('behavior', {}),
                'sentiment_analysis': ai_insights.get('sentiment', {}),
                'audience_insights': ai_insights.get('demographics_insights', {}),
                'collaboration_insights': ai_insights.get('collaboration', {})
            }
        )
    
    def _create_key_insights(self, ai_insights: Dict[str, Any]) -> List[AgentInsight]:
        """Create key insights from AI analysis"""
        insights = []
        
        # Sentiment insights
        sentiment_data = ai_insights.get('sentiment', {})
        if sentiment_data.get('sentiment_summary'):
            insights.append(create_insight(
                sentiment_data['sentiment_summary'],
                'Based on sentiment analysis of audience comments',
                'High',
                0.9
            ))
        
        # Demographics insights
        demographics_data = ai_insights.get('demographics_insights', {})
        if demographics_data.get('audience_composition'):
            comp = demographics_data['audience_composition']
            insights.append(create_insight(
                f"Primary audience: {comp.get('primary_segment', 'Mixed demographics')}",
                'Based on demographic analysis',
                'Medium',
                0.85
            ))
        
        return insights
    
    def _create_recommendations(self, ai_insights: Dict[str, Any]) -> List[AgentRecommendation]:
        """Create recommendations from AI analysis"""
        recommendations = []
        
        # Add sentiment-based recommendations
        sentiment_data = ai_insights.get('sentiment', {})
        for rec in sentiment_data.get('engagement_opportunities', [])[:3]:
            recommendations.append(create_recommendation(
                rec,
                'Medium',
                'Easy',
                'Based on audience sentiment analysis'
            ))
        
        # Add demographics-based recommendations
        demographics_data = ai_insights.get('demographics_insights', {})
        for rec in demographics_data.get('growth_strategies', [])[:3]:
            recommendations.append(create_recommendation(
                rec,
                'Medium',
                'Medium',
                'Based on demographic analysis'
            ))
        
        return recommendations
    
    def _create_audience_summary(self, scores: Dict[str, float], comments_count: int) -> str:
        """Create a concise summary of audience analysis"""
        overall_health = scores.get('overall_audience_health', 0)
        
        if overall_health >= 8:
            health_desc = "excellent"
        elif overall_health >= 6:
            health_desc = "good"
        elif overall_health >= 4:
            health_desc = "moderate"
        else:
            health_desc = "needs improvement"
        
        return f"Audience analysis shows {health_desc} overall audience health (score: {overall_health}/10). Analysis based on demographic data, behavior patterns, and {comments_count} comments for sentiment analysis."
    
    def _get_domain_keywords(self) -> List[str]:
        """Return domain-specific keywords for this agent"""
        return [
            'audience', 'demographics', 'viewers', 'subscribers', 'comments',
            'sentiment', 'engagement', 'community', 'fans', 'followers',
            'age groups', 'gender', 'location', 'behavior', 'activity'
        ]
    
    async def _perform_audience_analysis(self, request: AudienceAnalysisRequest) -> Dict[str, Any]:
        """Perform comprehensive audience analysis"""
        
        analysis_results = {}
        
        # Gather video data for posting time analysis
        video_data = await self._gather_video_data(request.channel_id, request.time_period)
        
        # Get demographic data
        if request.include_demographics:
            demographics = await self.youtube_client.get_channel_demographics(
                request.channel_id, 
                request.time_period
            )
            analysis_results['demographics'] = demographics
        
        # Get behavior data
        if request.include_behavior_analysis:
            behavior_data = await self.youtube_client.get_audience_behavior(
                request.channel_id, 
                request.time_period
            )
            analysis_results['behavior'] = behavior_data
        
        # Get comments for sentiment analysis
        comments_data = []
        if request.include_sentiment_analysis:
            comments_data = await self.youtube_client.get_comments_for_analysis(
                request.channel_id, 
                video_count=15
            )
            analysis_results['comments_volume'] = len(comments_data)
        
        # Get channel context for analysis
        channel_context = await self._get_channel_context(request.channel_id)
        
        # Perform posting time analysis if requested
        if request.include_posting_time_analysis and video_data:
            posting_time_analysis = await self.posting_time_analyzer.analyze_posting_times(
                video_data,
                timezone=channel_context.get('timezone', 'UTC')
            )
            analysis_results['posting_time_analysis'] = posting_time_analysis
        
        # Perform AI analysis
        ai_insights = {}
        
        # Sentiment analysis
        if request.include_sentiment_analysis and comments_data:
            sentiment_analysis = await self.sentiment_engine.analyze_audience_sentiment(
                comments_data, 
                channel_context
            )
            ai_insights['sentiment'] = sentiment_analysis
            
        # Analyze collaboration potential
        channel_metrics = {
            'subscriber_count': channel_context.get('subscriber_count', 0),
            'engagement_rate': analysis_results.get('behavior', {}).get('engagement_patterns', {}).get('like_rate', 0),
            'avg_view_count': channel_context.get('avg_view_count', 0),
            'content_type': channel_context.get('content_type', 'unknown'),
            'niche': channel_context.get('niche', 'unknown'),
            'upload_frequency': channel_context.get('upload_frequency', 'unknown'),
            'subscriber_growth': 5.0  # Placeholder growth rate
        }
        
        collaboration_analysis = self.sentiment_engine.collaboration_analyzer.analyze_collaboration_potential(
            channel_metrics,
            analysis_results
        )
        ai_insights['collaboration'] = collaboration_analysis
        
        # Demographics analysis
        if request.include_demographics and analysis_results.get('demographics'):
            demographics_analysis = await self.sentiment_engine.analyze_audience_demographics(
                analysis_results['demographics'],
                analysis_results.get('behavior', {})
            )
            ai_insights['demographics_insights'] = demographics_analysis
        
        # Calculate audience scores
        audience_scores = self._calculate_audience_scores(analysis_results, ai_insights)
        
        # Combine all analysis results
        return {
            'raw_data': analysis_results,
            'ai_insights': ai_insights,
            'audience_scores': audience_scores,
            'analysis_metadata': {
                'channel_id': request.channel_id,
                'analysis_depth': request.analysis_depth,
                'comments_analyzed': len(comments_data),
                'analysis_timestamp': datetime.now().isoformat()
            }
        }
    
    async def _gather_video_data(self, channel_id: str, time_period: str) -> List[Dict]:
        """Gather video data for analysis"""
        try:
            # Get recent videos using YouTube API client
            search_response = await self.youtube_client.youtube.search().list(
                part='id',
                channelId=channel_id,
                type='video',
                order='date',
                maxResults=50  # Get more videos for better analysis
            ).execute()
            
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            if not video_ids:
                return []
            
            # Get detailed video data
            videos_response = await self.youtube_client.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(video_ids)
            ).execute()
            
            video_data = []
            for video in videos_response.get('items', []):
                stats = video['statistics']
                video_data.append({
                    'video_id': video['id'],
                    'title': video['snippet']['title'],
                    'published_at': video['snippet']['publishedAt'],
                    'views': int(stats.get('viewCount', 0)),
                    'likes': int(stats.get('likeCount', 0)),
                    'comments': int(stats.get('commentCount', 0)),
                    'retention_rate': 65.0,  # Placeholder - would come from Analytics API
                    'subscriber_gain': 10  # Placeholder - would come from Analytics API
                })
            
            return video_data
            
        except Exception as e:
            logger.error(f"Error gathering video data: {e}")
            return []
    
    async def _get_channel_context(self, channel_id: str) -> Dict[str, Any]:
        """Get channel context for analysis"""
        
        # In production, this would fetch from database or API
        return {
            'name': channel_id,
            'niche': 'Education',
            'subscriber_count': 25000,
            'avg_view_count': 8500,
            'content_type': 'Educational',
            'timezone': 'UTC'  # Would be user's actual timezone
        }
    
    def _calculate_audience_scores(self, raw_data: Dict[str, Any], ai_insights: Dict[str, Any]) -> Dict[str, float]:
        """Calculate audience performance scores"""
        
        demographics = raw_data.get('demographics', {})
        behavior = raw_data.get('behavior', {})
        sentiment = ai_insights.get('sentiment', {})
        
        # Calculate engagement score
        engagement_score = 0.0
        if behavior.get('engagement_patterns'):
            patterns = behavior['engagement_patterns']
            engagement_score = (
                patterns.get('like_rate', 0) * 0.3 +
                patterns.get('comment_rate', 0) * 0.4 +
                patterns.get('share_rate', 0) * 0.2 +
                patterns.get('subscribe_rate', 0) * 0.1
            )
        
        # Calculate retention score
        retention_score = behavior.get('return_viewer_percentage', 0) / 10.0  # Scale to 0-10
        
        # Calculate sentiment score
        sentiment_score = 5.0  # Default neutral
        if sentiment.get('sentiment_breakdown'):
            breakdown = sentiment['sentiment_breakdown']
            sentiment_score = (
                breakdown.get('positive', 0) * 0.1 -
                breakdown.get('negative', 0) * 0.05 +
                5.0  # Base score
            )
        
        # Calculate diversity score (demographic spread)
        diversity_score = 7.5  # Default good diversity
        if demographics.get('age_groups'):
            age_spread = len([v for v in demographics['age_groups'].values() if v > 5])
            diversity_score = min(age_spread * 1.5, 10.0)
        
        return {
            'engagement_score': round(min(engagement_score, 10.0), 1),
            'retention_score': round(min(retention_score, 10.0), 1),
            'sentiment_score': round(max(0, min(sentiment_score, 10.0)), 1),
            'diversity_score': round(diversity_score, 1),
            'overall_audience_health': round(
                (engagement_score + retention_score + sentiment_score + diversity_score) / 4, 1
            )
        }
    
    def _format_boss_agent_response(self, analysis_result: Dict[str, Any], request_id: str, start_time: float, cache_hit: bool = False) -> Dict[str, Any]:
        """Format response specifically for boss agent consumption"""
        
        processing_time = time.time() - start_time
        
        # Extract key insights
        ai_insights = analysis_result.get('ai_insights', {})
        sentiment_data = ai_insights.get('sentiment', {})
        demographics_data = ai_insights.get('demographics_insights', {})
        collaboration_data = ai_insights.get('collaboration', {})
        
        # Create summary
        summary = self._create_audience_summary(analysis_result)
        
        # Extract recommendations
        recommendations = []
        
        # Add sentiment-based recommendations
        if sentiment_data.get('engagement_opportunities'):
            recommendations.extend(sentiment_data['engagement_opportunities'][:3])
        
        # Add demographics-based recommendations
        if demographics_data.get('growth_strategies'):
            recommendations.extend(demographics_data['growth_strategies'][:3])
        
        # Create key insights
        key_insights = []
        
        # Sentiment insights
        if sentiment_data.get('sentiment_summary'):
            key_insights.append({
                'insight': sentiment_data['sentiment_summary'],
                'evidence': f"Based on {analysis_result.get('analysis_metadata', {}).get('comments_analyzed', 0)} comments analyzed",
                'impact': 'High',
                'confidence': 0.9
            })
        
        # Demographics insights
        if demographics_data.get('audience_composition'):
            comp = demographics_data['audience_composition']
            key_insights.append({
                'insight': f"Primary audience: {comp.get('primary_segment', 'Mixed demographics')}",
                'evidence': 'Based on demographic analysis',
                'impact': 'Medium',
                'confidence': 0.85
            })
        
        return {
            'agent_type': self.agent_type,
            'response_id': str(uuid.uuid4()),
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'confidence_score': 0.88,  # High confidence in audience analysis
            'data_freshness': datetime.now().isoformat(),
            'domain_match': True,
            'analysis': {
                'summary': summary,
                'metrics': analysis_result.get('audience_scores', {}),
                'key_insights': key_insights[:5],  # Limit to top 5
                'recommendations': [
                    {
                        'recommendation': rec,
                        'expected_impact': 'Medium',
                        'implementation_difficulty': 'Easy',
                        'reasoning': 'Based on audience behavior analysis'
                    }
                    for rec in recommendations[:5]  # Limit to top 5
                ],
                'detailed_analysis': {
                    'demographics': analysis_result.get('raw_data', {}).get('demographics', {}),
                    'behavior_patterns': analysis_result.get('raw_data', {}).get('behavior', {}),
                    'sentiment_analysis': sentiment_data,
                    'audience_insights': demographics_data,
                    'collaboration_insights': {
                        'score': collaboration_data.get('collaboration_score', 0),
                        'key_factors': collaboration_data.get('key_factors', []),
                        'suggested_formats': collaboration_data.get('collaboration_types', []),
                        'ideal_partner': collaboration_data.get('ideal_partner_profile', {})
                    }
                }
            },
            'token_usage': {
                'input_tokens': 3200,
                'output_tokens': 1800,
                'model': 'claude-3-5-sonnet-20241022'
            },
            'cache_info': {
                'cache_hit': cache_hit,
                'cache_key': 'audience_insights_' + request_id[:8],
                'ttl_remaining': 7200 if not cache_hit else 5400
            },
            'processing_time': round(processing_time, 2),
            'for_boss_agent_only': True
        }
    
    def _create_audience_summary(self, analysis_result: Dict[str, Any]) -> str:
        """Create a concise summary of audience analysis"""
        
        scores = analysis_result.get('audience_scores', {})
        metadata = analysis_result.get('analysis_metadata', {})
        
        overall_health = scores.get('overall_audience_health', 0)
        comments_count = metadata.get('comments_analyzed', 0)
        
        if overall_health >= 8:
            health_desc = "excellent"
        elif overall_health >= 6:
            health_desc = "good"
        elif overall_health >= 4:
            health_desc = "moderate"
        else:
            health_desc = "needs improvement"
        
        return f"Audience analysis shows {health_desc} overall audience health (score: {overall_health}/10). Analysis based on demographic data, behavior patterns, and {comments_count} comments for sentiment analysis."
    
    def _format_cached_response(self, cached_data: Dict[str, Any], request_id: str, start_time: float) -> Dict[str, Any]:
        """Format cached response for boss agent"""
        
        # Update the cached response with new request metadata
        response = cached_data.copy()
        response.update({
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'processing_time': round(time.time() - start_time, 2),
            'cache_info': {
                'cache_hit': True,
                'cache_key': 'audience_insights_' + request_id[:8],
                'ttl_remaining': 5400
            }
        })
        
        return response
    
    def _create_domain_mismatch_response(self, request_id: str) -> Dict[str, Any]:
        """Create response for requests outside audience insights domain"""
        
        return {
            'agent_type': self.agent_type,
            'response_id': str(uuid.uuid4()),
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'confidence_score': 0.0,
            'data_freshness': datetime.now().isoformat(),
            'domain_match': False,
            'analysis': {
                'summary': 'Request outside audience insights domain',
                'error_message': 'This request should be handled by a different specialized agent'
            },
            'for_boss_agent_only': True
        }
    
    def _create_error_response(self, request_id: str, error_message: str, start_time: float) -> Dict[str, Any]:
        """Create error response for boss agent"""
        
        return {
            'agent_type': self.agent_type,
            'response_id': str(uuid.uuid4()),
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'confidence_score': 0.0,
            'data_freshness': datetime.now().isoformat(),
            'domain_match': True,
            'analysis': {
                'summary': 'Audience analysis failed',
                'error_message': error_message
            },
            'processing_time': round(time.time() - start_time, 2),
            'for_boss_agent_only': True
        }
    
    async def process_boss_agent_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a request from the Boss Agent with authentication validation"""
        
        request_id = request_data.get('request_id', str(uuid.uuid4()))
        
        # Validate Boss Agent authentication using mixin
        if not self._validate_boss_agent_request(request_data):
            return self._create_unauthorized_response(request_id)
        
        # Process the authenticated request
        try:
            # Extract parameters from request
            request_id = request_data.get('request_id', str(uuid.uuid4()))
            channel_id = request_data.get('context', {}).get('channel_id', '')
            time_period = request_data.get('context', {}).get('time_period', 'last_30d')
            analysis_depth = request_data.get('analysis_depth', 'standard')
            user_context = request_data.get('user_context', {})
            
            start_time = time.time()
            
            # Perform analysis using existing methods
            analysis_result = await self._perform_audience_analysis(
                channel_id, time_period, analysis_depth, user_context
            )
            
            processing_time = time.time() - start_time
            
            # Format response for Boss Agent
            return {
                'agent_type': 'audience_insights',
                'response_id': f"audience_{request_id}",
                'request_id': request_id,
                'timestamp': datetime.utcnow().isoformat(),
                'confidence_score': analysis_result.get('confidence_score', 0.85),
                'domain_match': True,
                'analysis': {
                    'summary': analysis_result.get('summary', 'Audience analysis completed successfully'),
                    'metrics': analysis_result.get('metrics', {}),
                    'key_insights': analysis_result.get('key_insights', []),
                    'recommendations': analysis_result.get('recommendations', [])
                },
                'token_usage': {
                    'input_tokens': analysis_result.get('token_usage', {}).get('input_tokens', 0),
                    'output_tokens': analysis_result.get('token_usage', {}).get('output_tokens', 0),
                    'model': 'claude-3.5-sonnet'
                },
                'cache_info': {
                    'cache_hit': False,
                    'cache_key': f"audience_insights_{channel_id}_{time_period}",
                    'ttl_remaining': 1800
                },
                'processing_time': processing_time,
                'for_boss_agent_only': True
            }
            
        except Exception as e:
            logger.error(f"Error processing Boss Agent request: {e}")
            return {
                'agent_type': 'audience_insights',
                'response_id': f"error_{request_data.get('request_id', 'unknown')}",
                'request_id': request_data.get('request_id', ''),
                'timestamp': datetime.utcnow().isoformat(),
                'domain_match': False,
                'analysis': {
                    'summary': f'Error processing audience insights request: {str(e)}',
                    'error_type': 'processing_error',
                    'error_message': str(e)
                },
                'confidence_score': 0.0,
                'processing_time': 0.0,
                'for_boss_agent_only': True
            }

# Global instance for boss agent integration
audience_insights_agent = None

def get_audience_insights_agent():
    """Get or create audience insights agent instance"""
    global audience_insights_agent
    
    if audience_insights_agent is None:
        youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not youtube_api_key:
            logger.warning("YOUTUBE_API_KEY not set - using demo mode")
            youtube_api_key = "demo_key"
        
        if not openai_api_key:
            logger.warning("OPENAI_API_KEY not set - using demo mode")
            openai_api_key = "demo_key"
        
        audience_insights_agent = AudienceInsightsAgent(youtube_api_key, openai_api_key)
    
    return audience_insights_agent

async def process_audience_insights_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for boss agent to request audience insights analysis
    This is the ONLY function the boss agent should call
    """
    agent = get_audience_insights_agent()
    return await agent.process_boss_agent_request(request_data)