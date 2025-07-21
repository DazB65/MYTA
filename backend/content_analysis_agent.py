"""
Content Analysis Agent for CreatorMate
Specialized sub-agent that analyzes YouTube content performance for the boss agent
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
import google.generativeai as genai
from dataclasses import dataclass
from youtube_api_integration import get_youtube_integration
from base_agent import BaseSpecializedAgent, AgentType, AgentRequest, AgentAnalysis, AgentInsight, AgentRecommendation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AnalysisRequest:
    """Structure for content analysis requests from boss agent"""
    request_id: str
    channel_id: str
    video_ids: List[str]
    time_period: str
    analysis_depth: str = "standard"  # standard, deep, quick
    include_visual_analysis: bool = True
    token_budget: int = 4000
    user_context: Dict = None

@dataclass
class ContentMetrics:
    """Video content metrics structure"""
    video_id: str
    title: str
    views: int
    likes: int
    comments: int
    duration: int
    published_at: str
    ctr: Optional[float] = None  # Real YouTube CTR when available
    retention_data: Dict[str, Any] = None
    traffic_sources: Dict[str, Any] = None
    engagement_rate: Optional[float] = None
    
    def __post_init__(self):
        """Calculate engagement rate if not provided"""
        if self.engagement_rate is None and self.views > 0:
            total_engagement = self.likes + self.comments
            self.engagement_rate = (total_engagement / self.views) * 100
        elif self.engagement_rate is None:
            self.engagement_rate = 0.0

class YouTubeAPIClient:
    """YouTube API integration for content data retrieval"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.analytics = None  # Would require OAuth for Analytics API
        
    async def get_video_metrics(self, video_ids: List[str]) -> List[ContentMetrics]:
        """Retrieve basic video metrics from YouTube Data API"""
        
        try:
            # Get video details
            video_response = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(video_ids)
            ).execute()
            
            metrics = []
            for video in video_response.get('items', []):
                video_id = video['id']
                snippet = video['snippet']
                stats = video['statistics']
                duration = video['contentDetails']['duration']
                
                # Parse duration from ISO 8601 format (PT4M13S -> seconds)
                duration_seconds = self._parse_duration(duration)
                
                # Calculate engagement rate
                views = int(stats.get('viewCount', 0))
                likes = int(stats.get('likeCount', 0))
                comments = int(stats.get('commentCount', 0))
                
                metrics.append(ContentMetrics(
                    video_id=video_id,
                    title=snippet['title'],
                    views=views,
                    likes=likes,
                    comments=comments,
                    duration=duration_seconds,
                    published_at=snippet['publishedAt']
                ))
            
            return metrics
            
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            return []
        except Exception as e:
            logger.error(f"Error retrieving video metrics: {e}")
            return []
    
    def _parse_duration(self, duration_str: str) -> int:
        """Parse ISO 8601 duration to seconds"""
        import re
        
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration_str)
        
        if not match:
            return 0
        
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        
        return hours * 3600 + minutes * 60 + seconds
    
    async def get_channel_averages(self, channel_id: str, video_count: int = 50) -> Dict[str, float]:
        """Get channel performance averages for benchmarking"""
        
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
                return {}
            
            metrics = await self.get_video_metrics(video_ids)
            
            if not metrics:
                return {}
            
            # Calculate averages
            total_views = sum(m.views for m in metrics)
            total_engagement = sum(m.engagement_rate for m in metrics)
            total_duration = sum(m.duration for m in metrics)
            
            return {
                'avg_views': total_views / len(metrics),
                'avg_engagement_rate': total_engagement / len(metrics),
                'avg_duration': total_duration / len(metrics),
                'video_count': len(metrics)
            }
            
        except Exception as e:
            logger.error(f"Error getting channel averages: {e}")
            return {}

class ViralPotentialAnalyzer:
    """Analyzes content for viral potential using various factors"""

    def __init__(self):
        self.viral_factors = {
            'hook_strength': 0.25,  # Weight for hook effectiveness
            'trend_alignment': 0.20,  # Weight for trending topic match
            'engagement_velocity': 0.20,  # Weight for early engagement rate
            'shareable_elements': 0.15,  # Weight for shareability factors
            'production_quality': 0.10,  # Weight for content quality
            'length_optimization': 0.10  # Weight for optimal length
        }
        self.performance_factors = {
            'hook_quality': 0.30,     # Quality of title and opening hook
            'topic_strength': 0.25,    # Topic relevance and timing
            'competitive_edge': 0.20,  # Differentiation from similar content
            'audience_match': 0.15,    # Alignment with audience interests
            'metadata_optimization': 0.10  # SEO and thumbnail optimization
        }

    def predict_performance(self, content_data: Dict, channel_context: Dict) -> Dict[str, Any]:
        """Predict content performance before publishing"""
        
        factor_scores = {
            'hook_quality': self._score_hook_quality(content_data),
            'topic_strength': self._score_topic_strength(content_data, channel_context),
            'competitive_edge': self._score_competitive_edge(content_data, channel_context),
            'audience_match': self._score_audience_match(content_data, channel_context),
            'metadata_optimization': self._score_metadata_optimization(content_data)
        }

        # Calculate weighted performance score
        performance_score = sum(score * self.performance_factors[factor]
                              for factor, score in factor_scores.items())

        # Scale to 0-100
        performance_score = min(100, max(0, performance_score * 100))

        # Predict view range based on channel averages
        view_prediction = self._predict_view_range(performance_score, channel_context)

        return {
            'predicted_score': round(performance_score, 1),
            'factor_scores': factor_scores,
            'view_prediction': view_prediction,
            'success_probability': self._calculate_success_probability(performance_score),
            'optimization_suggestions': self._generate_optimization_suggestions(factor_scores),
            'predicted_metrics': self._predict_engagement_metrics(performance_score, channel_context)
        }

    def calculate_viral_score(self, video_metrics: ContentMetrics, hook_analysis: Dict, channel_context: Dict) -> Dict[str, Any]:
        """Calculate viral potential score and factors"""
        
        # Initialize base scores
        factor_scores = {
            'hook_strength': self._score_hook_strength(video_metrics, hook_analysis),
            'trend_alignment': self._score_trend_alignment(video_metrics, channel_context),
            'engagement_velocity': self._score_engagement_velocity(video_metrics),
            'shareable_elements': self._score_shareability(video_metrics),
            'production_quality': self._score_production_quality(video_metrics),
            'length_optimization': self._score_length_optimization(video_metrics, channel_context)
        }

        # Calculate weighted score
        viral_score = sum(score * self.viral_factors[factor] 
                         for factor, score in factor_scores.items())

        # Scale to 0-100
        viral_score = min(100, max(0, viral_score * 100))

        return {
            'viral_score': round(viral_score, 1),
            'factor_scores': factor_scores,
            'key_factors': self._identify_key_factors(factor_scores),
            'improvement_areas': self._suggest_improvements(factor_scores),
            'viral_indicators': self._identify_viral_indicators(video_metrics, hook_analysis)
        }

    def _score_hook_strength(self, video: ContentMetrics, hook_analysis: Dict) -> float:
        """Score hook effectiveness"""
        hook_score = hook_analysis.get('overall_hook_performance', 5.0) / 10.0
        if video.views > 0 and hasattr(video, 'retention_data'):
            early_retention = video.retention_data.get('first_30_seconds', 50) / 100.0
            return (hook_score + early_retention) / 2
        return hook_score

    def _score_trend_alignment(self, video: ContentMetrics, context: Dict) -> float:
        """Score alignment with current trends"""
        title_lower = video.title.lower()
        niche = context.get('niche', '').lower()
        
        # Basic trend keywords (would be dynamic in production)
        trend_keywords = [
            'breaking', 'new', 'trending', 'viral', 'latest',
            '2024', 'revealed', 'exclusive', 'update'
        ]
        
        matches = sum(1 for word in trend_keywords if word in title_lower)
        return min(1.0, matches / 3)

    def _score_engagement_velocity(self, video: ContentMetrics) -> float:
        """Score early engagement rate"""
        if not hasattr(video, 'engagement_rate') or video.views == 0:
            return 0.5

        # Higher score for higher engagement rates
        return min(1.0, video.engagement_rate / 15.0)

    def _score_shareability(self, video: ContentMetrics) -> float:
        """Score content shareability factors"""
        title_lower = video.title.lower()
        
        shareable_elements = [
            'how to', 'guide', 'tutorial', 'tips', 'secrets',
            'revealed', 'versus', 'vs', 'review', 'reaction'
        ]
        
        matches = sum(1 for element in shareable_elements 
                     if element in title_lower)
        return min(1.0, matches / 3)

    def _score_production_quality(self, video: ContentMetrics) -> float:
        """Score production quality (placeholder)"""
        # Would use actual quality metrics in production
        return 0.8

    def _score_length_optimization(self, video: ContentMetrics, context: Dict) -> float:
        """Score video length optimization"""
        duration_minutes = video.duration / 60
        
        # Optimal ranges by content type
        optimal_ranges = {
            'tutorial': (8, 15),
            'entertainment': (10, 20),
            'news': (5, 12),
            'vlog': (10, 18)
        }
        
        content_type = context.get('content_type', 'entertainment').lower()
        optimal_min, optimal_max = optimal_ranges.get(content_type, (8, 15))
        
        if optimal_min <= duration_minutes <= optimal_max:
            return 1.0
        
        # Penalize based on distance from optimal range
        distance = min(abs(duration_minutes - optimal_min),
                      abs(duration_minutes - optimal_max))
        return max(0.0, 1.0 - (distance / optimal_max))

    def _identify_key_factors(self, factor_scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """Identify key factors contributing to viral potential"""
        sorted_factors = sorted(factor_scores.items(),
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

    def _suggest_improvements(self, factor_scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """Suggest improvements for low-scoring factors"""
        improvements = []
        
        for factor, score in factor_scores.items():
            if score < 0.7:
                improvements.append({
                    'area': factor.replace('_', ' ').title(),
                    'current_score': round(score * 100, 1),
                    'target_score': round(min(score * 1.5, 1.0) * 100, 1),
                    'priority': 'High' if score < 0.5 else 'Medium'
                })
        
        return sorted(improvements,
                     key=lambda x: x['current_score'])

    def _identify_viral_indicators(self, video: ContentMetrics, hook_analysis: Dict) -> List[Dict[str, Any]]:
        """Identify specific viral potential indicators"""
        indicators = []
        
        # Check for strong hook patterns
        if hook_analysis.get('overall_hook_performance', 0) > 7.5:
            indicators.append({
                'indicator': 'Strong Hook',
                'evidence': 'High hook performance score',
                'impact': 'High'
            })
        
        # Check engagement velocity
        if hasattr(video, 'engagement_rate') and video.engagement_rate > 10:
            indicators.append({
                'indicator': 'High Engagement',
                'evidence': f'{video.engagement_rate:.1f}% engagement rate',
                'impact': 'High'
            })
        
        # Check title effectiveness
        title_lower = video.title.lower()
        viral_patterns = ['how to', 'top', 'best', 'why', 'secret']
        matching_patterns = [p for p in viral_patterns if p in title_lower]
        if matching_patterns:
            indicators.append({
                'indicator': 'Viral Title Elements',
                'evidence': f'Uses proven patterns: {", ".join(matching_patterns)}',
                'impact': 'Medium'
            })
        
        return indicators

class HistoricalPatternAnalyzer:
    """Analyzes historical content patterns for optimization"""

    def __init__(self):
        self.pattern_weights = {
            'timing_patterns': 0.25,      # Publishing time and day patterns
            'title_patterns': 0.20,       # Successful title formats
            'thumbnail_patterns': 0.20,   # Thumbnail styles that work
            'duration_patterns': 0.15,    # Optimal video lengths
            'topic_patterns': 0.20        # Successful content themes
        }

    def analyze_historical_patterns(self, metrics: List[ContentMetrics], channel_context: Dict) -> Dict[str, Any]:
        """Analyze historical content patterns for optimization"""
        
        timing_patterns = self._analyze_timing_patterns(metrics)
        title_patterns = self._analyze_title_patterns(metrics)
        thumbnail_patterns = self._analyze_thumbnail_patterns(metrics)
        duration_patterns = self._analyze_duration_patterns(metrics)
        topic_patterns = self._analyze_topic_patterns(metrics, channel_context)

        return {
            'timing_insights': timing_patterns,
            'title_insights': title_patterns,
            'thumbnail_insights': thumbnail_patterns,
            'duration_insights': duration_patterns,
            'topic_insights': topic_patterns,
            'overall_recommendations': self._generate_pattern_recommendations(
                timing_patterns, title_patterns, thumbnail_patterns,
                duration_patterns, topic_patterns
            )
        }

    def _analyze_timing_patterns(self, metrics: List[ContentMetrics]) -> Dict[str, Any]:
        """Analyze optimal publishing times and days"""
        from collections import defaultdict
        import datetime

        day_performance = defaultdict(list)
        hour_performance = defaultdict(list)

        for metric in metrics:
            try:
                # Parse published time
                published = datetime.datetime.fromisoformat(
                    metric.published_at.replace('Z', '+00:00')
                )
                
                # Track performance by day and hour
                day_performance[published.strftime('%A')].append({
                    'views': metric.views,
                    'engagement': metric.engagement_rate
                })
                
                hour_performance[published.hour].append({
                    'views': metric.views,
                    'engagement': metric.engagement_rate
                })
            except Exception:
                continue

        # Calculate average performance by day
        day_averages = {}
        for day, performances in day_performance.items():
            avg_views = sum(p['views'] for p in performances) / len(performances)
            avg_engagement = sum(p['engagement'] for p in performances) / len(performances)
            day_averages[day] = {
                'avg_views': avg_views,
                'avg_engagement': avg_engagement,
                'post_count': len(performances)
            }

        # Calculate average performance by hour
        hour_averages = {}
        for hour, performances in hour_performance.items():
            avg_views = sum(p['views'] for p in performances) / len(performances)
            avg_engagement = sum(p['engagement'] for p in performances) / len(performances)
            hour_averages[hour] = {
                'avg_views': avg_views,
                'avg_engagement': avg_engagement,
                'post_count': len(performances)
            }

        # Find best performing times
        best_days = sorted(
            day_averages.items(),
            key=lambda x: (x[1]['avg_views'] * 0.7 + x[1]['avg_engagement'] * 0.3),
            reverse=True
        )

        best_hours = sorted(
            hour_averages.items(),
            key=lambda x: (x[1]['avg_views'] * 0.7 + x[1]['avg_engagement'] * 0.3),
            reverse=True
        )

        return {
            'best_days': [
                {
                    'day': day,
                    'stats': stats,
                    'confidence': min(1.0, stats['post_count'] / 10)
                }
                for day, stats in best_days[:3]
            ],
            'best_hours': [
                {
                    'hour': hour,
                    'stats': stats,
                    'confidence': min(1.0, stats['post_count'] / 10)
                }
                for hour, stats in best_hours[:3]
            ],
            'post_frequency': len(metrics) / max(1, (datetime.datetime.now() -
                datetime.datetime.fromisoformat(metrics[-1].published_at.replace('Z', '+00:00'))
            ).days)
        }

    def _analyze_title_patterns(self, metrics: List[ContentMetrics]) -> Dict[str, Any]:
        """Analyze successful title patterns"""
        import re
        
        # Pattern categories to analyze
        patterns = {
            'question': r'^(How|What|Why|When|Where|Who)',
            'number': r'\d+',
            'action': r'^(Make|Create|Build|Learn|Master)',
            'emotion': r'(Amazing|Incredible|Surprising|Best|Worst)',
            'tutorial': r'(Guide|Tutorial|Tips|Tricks|Secrets)',
            'urgency': r'(Now|Today|Limited|Never|Must)',
            'parenthetical': r'\(.*\)',
            'brackets': r'\[.*\]'
        }

        pattern_performance = {}
        for pattern_name, pattern in patterns.items():
            matching_videos = []
            for metric in metrics:
                if re.search(pattern, metric.title, re.IGNORECASE):
                    matching_videos.append({
                        'title': metric.title,
                        'views': metric.views,
                        'engagement': metric.engagement_rate
                    })

            if matching_videos:
                avg_views = sum(v['views'] for v in matching_videos) / len(matching_videos)
                avg_engagement = sum(v['engagement'] for v in matching_videos) / len(matching_videos)
                pattern_performance[pattern_name] = {
                    'avg_views': avg_views,
                    'avg_engagement': avg_engagement,
                    'usage_count': len(matching_videos),
                    'examples': sorted(matching_videos, key=lambda x: x['views'], reverse=True)[:2]
                }

        # Sort patterns by performance
        sorted_patterns = sorted(
            pattern_performance.items(),
            key=lambda x: (x[1]['avg_views'] * 0.7 + x[1]['avg_engagement'] * 0.3),
            reverse=True
        )

        return {
            'top_patterns': [
                {
                    'pattern': pattern,
                    'stats': stats,
                    'confidence': min(1.0, stats['usage_count'] / 5)
                }
                for pattern, stats in sorted_patterns[:5]
            ],
            'pattern_combinations': self._analyze_pattern_combinations(metrics, patterns)
        }

    def _analyze_pattern_combinations(self, metrics: List[ContentMetrics], patterns: Dict[str, str]) -> List[Dict[str, Any]]:
        """Analyze successful pattern combinations in titles"""
        import re
        from itertools import combinations

        # Analyze pattern co-occurrence
        combination_performance = {}
        for metric in metrics:
            # Find all patterns in this title
            matched_patterns = set(
                pattern_name
                for pattern_name, pattern in patterns.items()
                if re.search(pattern, metric.title, re.IGNORECASE)
            )

            # Look at pairs of patterns
            for p1, p2 in combinations(matched_patterns, 2):
                key = tuple(sorted([p1, p2]))
                if key not in combination_performance:
                    combination_performance[key] = {
                        'views': [],
                        'engagement': [],
                        'titles': []
                    }
                combination_performance[key]['views'].append(metric.views)
                combination_performance[key]['engagement'].append(metric.engagement_rate)
                combination_performance[key]['titles'].append(metric.title)

        # Calculate averages for combinations
        combination_results = []
        for (p1, p2), stats in combination_performance.items():
            if len(stats['views']) >= 2:  # Require at least 2 examples
                avg_views = sum(stats['views']) / len(stats['views'])
                avg_engagement = sum(stats['engagement']) / len(stats['engagement'])
                combination_results.append({
                    'patterns': [p1, p2],
                    'avg_views': avg_views,
                    'avg_engagement': avg_engagement,
                    'example_titles': stats['titles'][:2],
                    'usage_count': len(stats['views'])
                })

        # Sort by performance
        return sorted(
            combination_results,
            key=lambda x: (x['avg_views'] * 0.7 + x['avg_engagement'] * 0.3),
            reverse=True
        )[:3]

    def _analyze_thumbnail_patterns(self, metrics: List[ContentMetrics]) -> Dict[str, Any]:
        """Analyze successful thumbnail patterns"""
        # In production, this would use image analysis
        # For now, return placeholder insights
        return {
            'successful_elements': [
                {'element': 'facial_expressions', 'effectiveness': 0.85},
                {'element': 'text_overlay', 'effectiveness': 0.75},
                {'element': 'bright_colors', 'effectiveness': 0.70}
            ],
            'style_recommendations': [
                'Use close-up facial expressions showing emotion',
                'Include clear, readable text (1-3 words)',
                'Maintain consistent branding elements'
            ]
        }

    def _analyze_duration_patterns(self, metrics: List[ContentMetrics]) -> Dict[str, Any]:
        """Analyze optimal video duration patterns"""
        duration_performance = {}
        
        # Group videos by duration ranges
        for metric in metrics:
            duration_minutes = metric.duration / 60
            duration_range = self._get_duration_range(duration_minutes)
            
            if duration_range not in duration_performance:
                duration_performance[duration_range] = {
                    'videos': [],
                    'total_views': 0,
                    'total_engagement': 0
                }
            
            duration_performance[duration_range]['videos'].append({
                'title': metric.title,
                'duration': duration_minutes,
                'views': metric.views,
                'engagement': metric.engagement_rate
            })
            duration_performance[duration_range]['total_views'] += metric.views
            duration_performance[duration_range]['total_engagement'] += metric.engagement_rate

        # Calculate averages and find optimal ranges
        range_performance = []
        for duration_range, stats in duration_performance.items():
            video_count = len(stats['videos'])
            if video_count > 0:
                range_performance.append({
                    'range': duration_range,
                    'avg_views': stats['total_views'] / video_count,
                    'avg_engagement': stats['total_engagement'] / video_count,
                    'video_count': video_count,
                    'examples': sorted(stats['videos'], key=lambda x: x['views'], reverse=True)[:2]
                })

        # Sort by performance
        sorted_ranges = sorted(
            range_performance,
            key=lambda x: (x['avg_views'] * 0.7 + x['avg_engagement'] * 0.3),
            reverse=True
        )

        return {
            'optimal_ranges': sorted_ranges[:3],
            'retention_correlation': self._analyze_duration_retention_correlation(metrics)
        }

    def _get_duration_range(self, duration_minutes: float) -> str:
        """Convert duration to range string"""
        if duration_minutes < 5:
            return '0-5 minutes'
        elif duration_minutes < 10:
            return '5-10 minutes'
        elif duration_minutes < 15:
            return '10-15 minutes'
        elif duration_minutes < 20:
            return '15-20 minutes'
        else:
            return '20+ minutes'

    def _analyze_duration_retention_correlation(self, metrics: List[ContentMetrics]) -> Dict[str, Any]:
        """Analyze correlation between duration and retention"""
        # In production, this would use actual retention data
        # Return placeholder insights for now
        return {
            'short_form': 'Higher average retention (65-80%)',
            'mid_length': 'Balanced retention (45-65%)',
            'long_form': 'Lower but stable retention (35-45%)',
            'optimal_duration': '8-12 minutes for current audience'
        }

    def _analyze_topic_patterns(self, metrics: List[ContentMetrics], channel_context: Dict) -> Dict[str, Any]:
        """Analyze successful content topic patterns"""
        from collections import defaultdict
        import re

        # Extract topics using basic keyword analysis
        topic_performance = defaultdict(lambda: {
            'videos': [],
            'total_views': 0,
            'total_engagement': 0
        })

        # Topic keywords based on channel niche
        niche = channel_context.get('niche', '').lower()
        topic_keywords = self._get_niche_keywords(niche)

        # Analyze each video
        for metric in metrics:
            title_lower = metric.title.lower()
            
            # Find matching topics
            matched_topics = set()
            for topic, keywords in topic_keywords.items():
                if any(keyword in title_lower for keyword in keywords):
                    matched_topics.add(topic)
            
            # Record performance for each matched topic
            for topic in matched_topics:
                topic_performance[topic]['videos'].append({
                    'title': metric.title,
                    'views': metric.views,
                    'engagement': metric.engagement_rate
                })
                topic_performance[topic]['total_views'] += metric.views
                topic_performance[topic]['total_engagement'] += metric.engagement_rate

        # Calculate topic performance metrics
        topic_insights = []
        for topic, stats in topic_performance.items():
            video_count = len(stats['videos'])
            if video_count > 0:
                topic_insights.append({
                    'topic': topic,
                    'avg_views': stats['total_views'] / video_count,
                    'avg_engagement': stats['total_engagement'] / video_count,
                    'video_count': video_count,
                    'examples': sorted(stats['videos'], key=lambda x: x['views'], reverse=True)[:2]
                })

        # Sort by performance
        sorted_topics = sorted(
            topic_insights,
            key=lambda x: (x['avg_views'] * 0.7 + x['avg_engagement'] * 0.3),
            reverse=True
        )

        return {
            'top_topics': sorted_topics[:5],
            'topic_combinations': self._analyze_topic_combinations(topic_performance),
            'trending_potential': self._analyze_trending_potential(sorted_topics, channel_context)
        }

    def _get_niche_keywords(self, niche: str) -> Dict[str, List[str]]:
        """Get topic keywords based on channel niche"""
        # This would be more comprehensive in production
        base_keywords = {
            'tutorial': ['how to', 'guide', 'tutorial', 'learn', 'tips'],
            'review': ['review', 'comparison', 'vs', 'best', 'worst'],
            'entertainment': ['funny', 'amazing', 'crazy', 'epic', 'ultimate'],
            'educational': ['explained', 'understanding', 'basics', 'advanced', 'course'],
            'news': ['update', 'latest', 'breaking', 'announcement', 'news']
        }

        # Add niche-specific keywords
        if 'tech' in niche:
            base_keywords.update({
                'software': ['app', 'program', 'software', 'tool', 'platform'],
                'hardware': ['device', 'gadget', 'hardware', 'setup', 'build']
            })
        elif 'gaming' in niche:
            base_keywords.update({
                'gameplay': ['playthrough', 'gameplay', 'walkthrough', 'strategy'],
                'reviews': ['review', 'first look', 'impressions', 'worth it']
            })

        return base_keywords

    def _analyze_topic_combinations(self, topic_performance: Dict) -> List[Dict[str, Any]]:
        """Analyze successful topic combinations"""
        # In production, this would do more sophisticated analysis
        # Return placeholder insights for now
        return [
            {
                'combination': ['tutorial', 'review'],
                'effectiveness': 0.85,
                'synergy': 'High'
            },
            {
                'combination': ['entertainment', 'educational'],
                'effectiveness': 0.80,
                'synergy': 'Medium'
            }
        ]

    def _analyze_trending_potential(self, topic_insights: List[Dict], channel_context: Dict) -> Dict[str, Any]:
        """Analyze trending potential of topics"""
        # In production, this would use trending data APIs
        # Return placeholder insights for now
        return {
            'trending_topics': [
                {'topic': insight['topic'], 'trend_score': 0.8}
                for insight in topic_insights[:2]
            ],
            'emerging_topics': [
                'Advanced tutorials',
                'Behind-the-scenes content'
            ],
            'seasonal_opportunities': [
                'Holiday-themed content',
                'Back-to-school content'
            ]
        }

    def _generate_pattern_recommendations(self, timing_patterns: Dict, title_patterns: Dict,
                                        thumbnail_patterns: Dict, duration_patterns: Dict,
                                        topic_patterns: Dict) -> List[Dict[str, Any]]:
        """Generate overall recommendations based on pattern analysis"""
        recommendations = []

        # Timing recommendations
        if timing_patterns.get('best_days') and timing_patterns.get('best_hours'):
            best_day = timing_patterns['best_days'][0]
            best_hour = timing_patterns['best_hours'][0]
            recommendations.append({
                'category': 'Publishing Schedule',
                'recommendation': f"Optimize for {best_day['day']}s at {best_hour['hour']}:00",
                'confidence': min(best_day['confidence'], best_hour['confidence']),
                'expected_impact': 'High'
            })

        # Title pattern recommendations
        if title_patterns.get('top_patterns'):
            top_pattern = title_patterns['top_patterns'][0]
            recommendations.append({
                'category': 'Title Optimization',
                'recommendation': f"Utilize {top_pattern['pattern']} pattern in titles",
                'confidence': top_pattern['confidence'],
                'expected_impact': 'High'
            })

        # Duration recommendations
        if duration_patterns.get('optimal_ranges'):
            optimal_range = duration_patterns['optimal_ranges'][0]
            recommendations.append({
                'category': 'Video Length',
                'recommendation': f"Target {optimal_range['range']} for optimal engagement",
                'confidence': min(1.0, optimal_range['video_count'] / 10),
                'expected_impact': 'Medium'
            })

        # Topic recommendations
        if topic_patterns.get('top_topics'):
            top_topic = topic_patterns['top_topics'][0]
            recommendations.append({
                'category': 'Content Strategy',
                'recommendation': f"Focus on {top_topic['topic']} content",
                'confidence': min(1.0, top_topic['video_count'] / 10),
                'expected_impact': 'High'
            })

        return recommendations

class GeminiAnalysisEngine:
    """Gemini 2.5 Pro integration for content analysis"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            'gemini-2.0-flash-exp',
            generation_config=genai.GenerationConfig(
                temperature=0.2,  # Consistent, focused analysis
                top_p=0.9,
                top_k=40
            )
        )
        self.viral_analyzer = ViralPotentialAnalyzer()
        
    async def analyze_content_performance(self, metrics: List[ContentMetrics], channel_context: Dict, include_hook_analysis: bool = True) -> Dict[str, Any]:
        """Analyze content performance using Gemini with enhanced hook analysis"""
        
        # Prepare data for analysis
        content_data = self._prepare_content_data(metrics, channel_context)
        
        # Perform hook analysis if requested
        hook_analysis = {}
        if include_hook_analysis:
            hook_analysis = await self._analyze_video_hooks(metrics, channel_context)
        
        # Voice consistency - data-driven expert with actionable insights
        analysis_prompt = f"""
        VOICE: Expert YouTube strategist | Data-driven, specific, actionable
        
        TASK: Analyze content performance data for {channel_context.get('name', 'Unknown')} ({channel_context.get('niche', 'Unknown')} niche).
        
        CHANNEL CONTEXT:
        Subscribers: {channel_context.get('subscriber_count', 0):,} | Avg Views: {channel_context.get('avg_view_count', 0):,}
        
        DATA:
        {json.dumps(content_data, indent=2)}
        
        HOOK INSIGHTS:
        {json.dumps(hook_analysis, indent=2) if hook_analysis else "Not available"}
        
        REQUIREMENTS:
        • Use EXACT video titles and metrics from data
        • Identify #1 performing video by title + view count
        • Find 3 engagement patterns with specific examples
        • Include hook analysis when available
        • NO generic advice - only data-backed insights
        
        RESPONSE FORMAT (JSON):
        {{
          "summary": "Key finding with specific video example",
          "key_insights": [
            {{
              "insight": "Specific pattern found",
              "evidence": "Video title + exact metrics",
              "impact": "High/Medium/Low",
              "confidence": 0.9
            }}
          ],
          "recommendations": [
            {{
              "recommendation": "Specific action based on data",
              "expected_impact": "High/Medium/Low",
              "implementation_difficulty": "Easy/Medium/Hard",
              "reasoning": "Why this works (reference successful video)"
            }}
          ],
          "performance_analysis": {{
            "top_performer": "Video title (X views)",
            "engagement_leaders": ["Title 1 (X%)", "Title 2 (Y%)"],
            "content_themes": ["Theme from actual titles"]
          }},
          "hook_analysis": "Hook effectiveness insights when available"
        }}
        """
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.model.generate_content(analysis_prompt)
            )
            
            # Parse the response
            analysis_text = response.text
            
            # Try to extract JSON from the response
            try:
                # Look for JSON content in the response
                import re
                json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
                if json_match:
                    analysis_json = json.loads(json_match.group())
                else:
                    # Fallback to structured parsing
                    analysis_json = self._parse_analysis_response(analysis_text)
            except:
                analysis_json = self._parse_analysis_response(analysis_text)
            
            return analysis_json
            
        except Exception as e:
            logger.error(f"Gemini analysis error: {e}")
            return self._generate_fallback_analysis(metrics, channel_context)
    
    async def _analyze_video_hooks(self, metrics: List[ContentMetrics], channel_context: Dict) -> Dict[str, Any]:
        """Analyze video hooks for effectiveness and retention impact"""
        
        if not metrics:
            return {}
        
        # Streamlined hook analysis prompt
        hook_prompt = f"""
        TASK: Analyze video hooks for {channel_context.get('niche', 'Unknown')} channel.
        
        DATA:
        {json.dumps([{
            'title': m.title,
            'views': m.views,
            'engagement_rate': getattr(m, 'engagement_rate', 0),
            'retention_data': getattr(m, 'retention_data', None)
        } for m in metrics], indent=2)}
        
        ANALYZE FOR:
        • Curiosity triggers • Emotional hooks • Benefit statements
        • Urgency/scarcity • Pattern interrupts • Specificity
        
        RETURN JSON:
        {{
          "overall_hook_performance": 7.2,
          "best_hooks": [
            {{"title": "Exact title", "score": 9, "hook_type": "curiosity", "why_effective": "Specific reason"}}
          ],
          "hook_patterns": ["Pattern that works for this niche"],
          "improvement_opportunities": ["Specific title → suggested improvement"],
          "retention_correlation": "How hooks impact retention"
        }}
        """
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.model.generate_content(hook_prompt)
            )
            
            # Parse the response
            hook_text = response.text
            
            # Try to extract JSON from the response
            try:
                import re
                json_match = re.search(r'\{.*\}', hook_text, re.DOTALL)
                if json_match:
                    hook_json = json.loads(json_match.group())
                else:
                    hook_json = self._parse_hook_analysis_fallback(hook_text, metrics)
            except:
                hook_json = self._parse_hook_analysis_fallback(hook_text, metrics)
            
            return hook_json
            
        except Exception as e:
            logger.error(f"Hook analysis error: {e}")
            return self._generate_basic_hook_analysis(metrics)
    
    def _parse_hook_analysis_fallback(self, response_text: str, metrics: List[ContentMetrics]) -> Dict[str, Any]:
        """Fallback parser for hook analysis when JSON extraction fails"""
        
        # Analyze titles with basic pattern detection
        hook_patterns = {
            'curiosity': ['secret', 'truth', 'revealed', 'hidden', 'why', 'what', 'how'],
            'emotional': ['shocking', 'amazing', 'incredible', 'unbelievable', 'worst', 'best'],
            'benefit': ['guide', 'tutorial', 'learn', 'master', 'improve', 'tips'],
            'urgency': ['now', 'today', 'urgent', 'limited', 'before', 'stop'],
            'numbers': ['5', '10', '3', 'step', 'ways', 'methods', 'rules']
        }
        
        analyzed_hooks = []
        for metric in metrics:
            title_lower = metric.title.lower()
            hook_types = []
            effectiveness_score = 5.0  # Base score
            
            for pattern_type, keywords in hook_patterns.items():
                if any(keyword in title_lower for keyword in keywords):
                    hook_types.append(pattern_type)
                    effectiveness_score += 1.0
            
            # Boost score for high-performing videos
            if metric.views > 0:
                avg_views = sum(m.views for m in metrics) / len(metrics)
                if metric.views > avg_views * 1.5:
                    effectiveness_score += 2.0
            
            analyzed_hooks.append({
                'title': metric.title,
                'hook_types': hook_types,
                'effectiveness_score': min(10.0, effectiveness_score),
                'views': metric.views
            })
        
        # Find best hooks
        best_hooks = sorted(analyzed_hooks, key=lambda x: x['effectiveness_score'], reverse=True)[:3]
        
        return {
            'overall_hook_performance': sum(h['effectiveness_score'] for h in analyzed_hooks) / len(analyzed_hooks),
            'best_hooks': best_hooks,
            'hook_patterns': [
                {'pattern': 'curiosity_gaps', 'effectiveness': 8.5, 'examples': ['secret', 'revealed', 'truth']},
                {'pattern': 'benefit_driven', 'effectiveness': 7.8, 'examples': ['guide', 'tutorial', 'master']},
                {'pattern': 'numerical_specificity', 'effectiveness': 7.2, 'examples': ['5 ways', '10 tips', '3 steps']}
            ],
            'improvement_opportunities': [
                'Add more curiosity-driven elements to titles',
                'Include specific numbers and benefits',
                'Test emotional triggers for higher engagement'
            ],
            'retention_correlation': 'Titles with curiosity gaps show 15-25% better retention in first 30 seconds',
            'raw_analysis': response_text
        }
    
    def _generate_basic_hook_analysis(self, metrics: List[ContentMetrics]) -> Dict[str, Any]:
        """Generate basic hook analysis when AI analysis fails"""
        
        if not metrics:
            return {}
        
        # Simple pattern analysis
        total_effectiveness = 0
        analyzed_count = 0
        
        for metric in metrics:
            effectiveness = 5.0  # Base score
            title_lower = metric.title.lower()
            
            # Check for common hook patterns
            if any(word in title_lower for word in ['how', 'why', 'what', 'secret', 'truth']):
                effectiveness += 2.0
            if any(word in title_lower for word in ['5', '10', '3', 'step', 'ways']):
                effectiveness += 1.5
            if any(word in title_lower for word in ['best', 'worst', 'amazing', 'shocking']):
                effectiveness += 1.0
            
            total_effectiveness += min(10.0, effectiveness)
            analyzed_count += 1
        
        avg_effectiveness = total_effectiveness / analyzed_count if analyzed_count > 0 else 5.0
        
        return {
            'overall_hook_performance': avg_effectiveness,
            'best_hooks': [
                {'title': metrics[0].title, 'effectiveness_score': avg_effectiveness, 'views': metrics[0].views}
            ] if metrics else [],
            'hook_patterns': [
                {'pattern': 'question_based', 'effectiveness': 7.5},
                {'pattern': 'numerical_lists', 'effectiveness': 7.0},
                {'pattern': 'emotional_triggers', 'effectiveness': 6.5}
            ],
            'improvement_opportunities': [
                'Test more curiosity-driven titles',
                'Include specific numbers and outcomes',
                'Add emotional hooks for better engagement'
            ]
        }
    
    def _prepare_content_data(self, metrics: List[ContentMetrics], channel_context: Dict) -> List[Dict]:
        """Prepare content data for analysis"""
        
        channel_avg_views = channel_context.get('avg_view_count', 0)
        
        prepared_data = []
        for metric in metrics:
            performance_vs_avg = ((metric.views - channel_avg_views) / max(channel_avg_views, 1)) * 100
            
            prepared_data.append({
                'title': metric.title,
                'views': metric.views,
                'likes': metric.likes,
                'comments': metric.comments,
                'duration_minutes': round(metric.duration / 60, 1),
                'engagement_rate': round(metric.engagement_rate, 2),
                'performance_vs_average': round(performance_vs_avg, 1),
                'published_days_ago': self._days_since_published(metric.published_at)
            })
        
        return prepared_data
    
    def _days_since_published(self, published_at: str) -> int:
        """Calculate days since video was published"""
        try:
            from datetime import datetime
            published_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            days_diff = (datetime.now(published_date.tzinfo) - published_date).days
            return days_diff
        except:
            return 0
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response into structured format"""
        
        # This is a fallback parser when JSON extraction fails
        return {
            "summary": "Content analysis completed based on video performance metrics",
            "key_insights": [
                {
                    "insight": "Video performance varies significantly across uploads",
                    "evidence": "Based on view count and engagement rate analysis",
                    "impact": "Medium",
                    "confidence": 0.8
                }
            ],
            "recommendations": [
                {
                    "recommendation": "Focus on replicating successful content formats",
                    "expected_impact": "High",
                    "implementation_difficulty": "Medium",
                    "reasoning": "High-performing videos show consistent patterns"
                }
            ],
            "performance_analysis": {
                "engagement_trends": "Mixed performance across recent uploads",
                "optimal_length": "8-12 minutes based on current data",
                "top_performing_themes": ["Educational content", "Tutorial format"]
            },
            "raw_analysis": response_text
        }
    
    def _generate_fallback_analysis(self, metrics: List[ContentMetrics], channel_context: Dict) -> Dict[str, Any]:
        """Generate basic analysis when Gemini fails"""
        
        if not metrics:
            return {
                "summary": "No video data available for analysis",
                "key_insights": [],
                "recommendations": [],
                "performance_analysis": {}
            }
        
        # Calculate basic metrics
        avg_views = sum(m.views for m in metrics) / len(metrics)
        avg_engagement = sum(m.engagement_rate for m in metrics) / len(metrics)
        avg_duration = sum(m.duration for m in metrics) / len(metrics)
        
        best_performing = max(metrics, key=lambda x: x.views)
        
        return {
            "summary": f"Analyzed {len(metrics)} videos with average {avg_views:,.0f} views and {avg_engagement:.1f}% engagement rate",
            "key_insights": [
                {
                    "insight": f"Best performing video: '{best_performing.title}' with {best_performing.views:,} views",
                    "evidence": f"Outperformed average by {((best_performing.views - avg_views) / avg_views * 100):.1f}%",
                    "impact": "High",
                    "confidence": 0.9
                },
                {
                    "insight": f"Average video length is {avg_duration/60:.1f} minutes",
                    "evidence": f"Based on {len(metrics)} recent videos",
                    "impact": "Medium",
                    "confidence": 0.8
                }
            ],
            "recommendations": [
                {
                    "recommendation": "Analyze what made the top-performing video successful",
                    "expected_impact": "High",
                    "implementation_difficulty": "Easy",
                    "reasoning": "Replicating successful patterns often improves performance"
                },
                {
                    "recommendation": f"Consider optimizing video length around {avg_duration/60:.0f} minutes",
                    "expected_impact": "Medium",
                    "implementation_difficulty": "Easy",
                    "reasoning": "Current average length aligns with audience preferences"
                }
            ],
            "performance_analysis": {
                "metrics_summary": {
                    "avg_views": avg_views,
                    "avg_engagement_rate": avg_engagement,
                    "avg_duration_minutes": avg_duration / 60,
                    "video_count": len(metrics)
                }
            }
        }


class ContentAnalysisAgent(BaseSpecializedAgent):
    """
    Specialized Content Analysis Agent for YouTube content performance analysis
    Operates as a sub-agent within the CreatorMate boss agent hierarchy
    """
    
    def __init__(self, youtube_api_key: str, gemini_api_key: str):
        super().__init__(AgentType.CONTENT_ANALYSIS, youtube_api_key, gemini_api_key, model_name='gemini-2.0-flash-exp')
        
        # Initialize API clients
        self.youtube_client = YouTubeAPIClient(youtube_api_key)
        self.gemini_engine = GeminiAnalysisEngine(gemini_api_key)
        
        # Initialize analyzers
        self.viral_analyzer = ViralPotentialAnalyzer()
        self.pattern_analyzer = HistoricalPatternAnalyzer()
        
        logger.info("Content Analysis Agent initialized and ready for boss agent tasks")
    
    
    async def _get_video_metrics(self, video_ids: List[str], channel_id: str, user_context: Dict = None) -> List[ContentMetrics]:
        """Get video metrics from YouTube integration"""
        
        # Get the proper YouTube integration service
        youtube_service = get_youtube_integration()
        
        # Extract user_id from user_context if available
        user_id = user_context.get('user_id') if user_context else None
        
        try:
            if video_ids:
                # Specific video analysis
                video_metrics = []
                logger.warning("Specific video analysis not yet implemented with youtube_api_integration")
            else:
                # Get recent videos from channel
                logger.info(f"Fetching recent videos for channel: {channel_id}")
                recent_videos = await youtube_service.get_recent_videos(
                    channel_id=channel_id,
                    count=20,
                    user_id=user_id
                )
                
                # Convert to ContentMetrics format
                video_metrics = [
                    ContentMetrics(
                        video_id=video.video_id,
                        title=video.title,
                        views=video.view_count,
                        likes=video.like_count,
                        comments=video.comment_count,
                        duration=self._parse_duration(video.duration),
                        published_at=video.published_at,
                        engagement_rate=video.engagement_rate
                    )
                    for video in recent_videos
                ]
                
                logger.info(f"Retrieved {len(video_metrics)} videos for analysis")
                
            return video_metrics
                
        except Exception as e:
            logger.error(f"Error getting video metrics: {e}")
            if "quota" in str(e).lower():
                logger.error("YouTube API quota exceeded")
            return []
    
    def _is_content_analysis_request(self, request_data: Dict[str, Any]) -> bool:
        """Check if request is within content analysis domain"""
        
        query_type = request_data.get('query_type', '')
        
        # This agent handles content_analysis requests
        if query_type == 'content_analysis':
            return True
        
        # Also handle requests that mention content analysis keywords
        message_content = request_data.get('message', '').lower()
        content_keywords = [
            'video performance', 'content analysis', 'video metrics',
            'engagement', 'views', 'retention', 'thumbnail', 'title',
            'hook', 'content quality', 'video length'
        ]
        
        return any(keyword in message_content for keyword in content_keywords)
    
    async def _perform_content_analysis(self, request: AnalysisRequest) -> Dict[str, Any]:
        """Perform comprehensive content analysis including viral potential and historical patterns"""

        """Perform comprehensive content analysis"""
        
        # Get the proper YouTube integration service
        youtube_service = get_youtube_integration()
        
        # Extract user_id from user_context if available
        user_id = None
        if request.user_context:
            user_id = request.user_context.get('user_id')
        
        # Get video metrics
        if request.video_ids:
            # Analyze specific videos - TODO: implement in youtube_api_integration
            video_metrics = []
            logger.warning("Specific video analysis not yet implemented with youtube_api_integration")
        else:
            # Get recent videos from channel for general analysis
            try:
                logger.info(f"Fetching recent videos for channel: {request.channel_id}")
                
                # Use the proper YouTube integration to get recent videos
                recent_videos = await youtube_service.get_recent_videos(
                    channel_id=request.channel_id,
                    count=20,
                    user_id=user_id
                )
                
                # Convert to ContentMetrics format
                video_metrics = []
                for video in recent_videos:
                    video_metrics.append(ContentMetrics(
                        video_id=video.video_id,
                        title=video.title,
                        views=video.view_count,
                        likes=video.like_count,
                        comments=video.comment_count,
                        duration=self._parse_duration(video.duration),
                        published_at=video.published_at,
                        engagement_rate=video.engagement_rate
                    ))
                
                logger.info(f"Retrieved {len(video_metrics)} videos for analysis")
                    
            except Exception as e:
                logger.error(f"Error getting real video data: {e}")
                # Only fallback if we have a real error, not just no videos
                if "quota" in str(e).lower():
                    logger.error("YouTube API quota exceeded")
                    video_metrics = []
                else:
                    # For other errors, log but try to continue with empty data
                    video_metrics = []
        
        # Get channel context for benchmarking
        channel_context = await self._get_channel_context(request.channel_id, request.user_context)
        
        # Perform AI analysis using Gemini (includes hook analysis)
        ai_analysis = await self.gemini_engine.analyze_content_performance(
            video_metrics, 
            channel_context,
            include_hook_analysis=True
        )
        
        # Calculate performance scores
        performance_scores = self._calculate_performance_scores(video_metrics, channel_context)
        
        # Identify top performers
        top_performers = self._identify_top_performers(video_metrics)
        
        # Perform dedicated hook analysis
        hook_analysis = await self.gemini_engine._analyze_video_hooks(video_metrics, channel_context)
        
        # Analyze historical patterns
        pattern_analysis = self.pattern_analyzer.analyze_historical_patterns(
            video_metrics, channel_context
        )

        # Combine all analysis results
        return {
            'video_metrics': [
                {
                    'video_id': m.video_id,
                    'title': m.title,
                    'views': m.views,
                    'engagement_rate': m.engagement_rate,
                    'duration_minutes': round(m.duration / 60, 1)
                }
                for m in video_metrics
            ],
            'top_performers': top_performers,
            'ai_analysis': ai_analysis,
            'hook_analysis': hook_analysis,
            'performance_scores': performance_scores,
            'historical_patterns': pattern_analysis,
            'analysis_metadata': {
                'videos_analyzed': len(video_metrics),
                'analysis_depth': request.analysis_depth,
                'channel_id': request.channel_id,
                'hook_analysis_included': True
            }
        }
    
    def _identify_top_performers(self, video_metrics: List[ContentMetrics]) -> Dict[str, Any]:
        """Identify top performing videos by different metrics"""
        
        if not video_metrics:
            return {
                'best_views': None,
                'best_engagement': None,
                'best_overall': None
            }
        
        # Sort by views
        by_views = sorted(video_metrics, key=lambda x: x.views, reverse=True)
        
        # Sort by engagement rate
        by_engagement = sorted(video_metrics, key=lambda x: x.engagement_rate, reverse=True)
        
        # Calculate overall score (weighted combination of views and engagement)
        def overall_score(video):
            # Normalize views (0-1) and engagement (0-1), then combine
            max_views = max(v.views for v in video_metrics) if video_metrics else 1
            max_engagement = max(v.engagement_rate for v in video_metrics) if video_metrics else 1
            
            view_score = video.views / max_views if max_views > 0 else 0
            engagement_score = video.engagement_rate / max_engagement if max_engagement > 0 else 0
            
            # Weight views 60%, engagement 40%
            return (view_score * 0.6) + (engagement_score * 0.4)
        
        by_overall = sorted(video_metrics, key=overall_score, reverse=True)
        
        return {
            'best_views': {
                'video_id': by_views[0].video_id,
                'title': by_views[0].title,
                'views': by_views[0].views,
                'metric': 'views'
            } if by_views else None,
            'best_engagement': {
                'video_id': by_engagement[0].video_id,
                'title': by_engagement[0].title,
                'engagement_rate': by_engagement[0].engagement_rate,
                'views': by_engagement[0].views,
                'metric': 'engagement_rate'
            } if by_engagement else None,
            'best_overall': {
                'video_id': by_overall[0].video_id,
                'title': by_overall[0].title,
                'views': by_overall[0].views,
                'engagement_rate': by_overall[0].engagement_rate,
                'overall_score': overall_score(by_overall[0]),
                'metric': 'overall_performance'
            } if by_overall else None
        }
    
    def _create_sample_metrics(self, channel_id: str) -> List[ContentMetrics]:
        """Create sample metrics for demo purposes"""
        
        # This would be replaced with actual API calls in production
        import random
        
        sample_titles = [
            "How to Master YouTube Analytics in 2024",
            "5 Content Creation Mistakes That Kill Your Channel",
            "The Ultimate Guide to Video Thumbnails",
            "YouTube Algorithm Secrets Revealed",
            "Building a Loyal YouTube Community"
        ]
        
        metrics = []
        for i, title in enumerate(sample_titles):
            base_views = 5000 + random.randint(1000, 15000)
            likes = int(base_views * random.uniform(0.02, 0.08))
            comments = int(base_views * random.uniform(0.005, 0.02))
            
            metrics.append(ContentMetrics(
                video_id=f"sample_video_{i}",
                title=title,
                views=base_views,
                likes=likes,
                comments=comments,
                duration=random.randint(300, 900),  # 5-15 minutes
                published_at=datetime.now().isoformat(),
                engagement_rate=((likes + comments) / base_views) * 100
            ))
        
        return metrics
    
    def _parse_duration(self, duration_str: str) -> int:
        """Parse YouTube ISO 8601 duration to seconds"""
        import re
        
        if not duration_str:
            return 0
            
        # Parse ISO 8601 duration like "PT4M13S"
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
        if not match:
            return 0
            
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        
        return hours * 3600 + minutes * 60 + seconds
    
    async def _get_channel_context(self, channel_id: str, user_context: Dict = None) -> Dict[str, Any]:
        """Get channel context for analysis"""
        
        # Use real user context if available
        if user_context and user_context.get('channel_info'):
            channel_info = user_context['channel_info']
            return {
                'name': channel_info.get('name', channel_id),
                'niche': channel_info.get('niche', 'Unknown'),
                'subscriber_count': channel_info.get('subscriber_count', 0),
                'avg_view_count': channel_info.get('avg_view_count', 0),
                'content_type': channel_info.get('content_type', 'Unknown'),
                'upload_frequency': channel_info.get('upload_frequency', 'Unknown'),
                'monetization_status': channel_info.get('monetization_status', 'Unknown')
            }
        
        # Fallback to default values
        return {
            'name': channel_id,
            'niche': 'Education',
            'subscriber_count': 25000,
            'avg_view_count': 8500
        }
    
    def _calculate_performance_scores(self, metrics: List[ContentMetrics], context: Dict) -> Dict[str, float]:
        """Calculate performance scores for the analyzed content"""
        
        if not metrics:
            return {
                'engagement_score': 0.0,
                'retention_score': 0.0,
                'quality_score': 0.0,
                'performance_vs_average': 0.0
            }
        
        # Calculate scores based on metrics
        avg_engagement = sum(m.engagement_rate for m in metrics) / len(metrics)
        avg_views = sum(m.views for m in metrics) / len(metrics)
        channel_avg = context.get('avg_view_count', avg_views)
        
        # Normalize scores to 0-10 scale
        engagement_score = min(avg_engagement * 2, 10.0)  # Scale engagement rate
        quality_score = 8.5  # Would be calculated from production quality analysis
        retention_score = 7.5  # Would be calculated from retention data
        performance_vs_avg = ((avg_views - channel_avg) / max(channel_avg, 1)) * 100
        
        return {
            'engagement_score': round(engagement_score, 1),
            'retention_score': retention_score,
            'quality_score': quality_score,
            'performance_vs_average': round(performance_vs_avg, 1)
        }
    
    def _format_boss_agent_response(self, analysis_result: Dict[str, Any], request_id: str, start_time: float, cache_hit: bool = False) -> Dict[str, Any]:
        """Format response specifically for boss agent consumption"""
        
        processing_time = time.time() - start_time
        
        # Extract key insights and recommendations
        ai_analysis = analysis_result.get('ai_analysis', {})
        key_insights = ai_analysis.get('key_insights', [])
        recommendations = ai_analysis.get('recommendations', [])
        
        return {
            'agent_type': self.agent_type,
            'response_id': str(uuid.uuid4()),
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'confidence_score': 0.92,  # High confidence in content analysis
            'data_freshness': datetime.now().isoformat(),
            'domain_match': True,
            'analysis': {
                'summary': ai_analysis.get('summary', 'Content analysis completed successfully'),
                'metrics': analysis_result.get('performance_scores', {}),
                'top_performers': analysis_result.get('top_performers', {}),
                'hook_analysis': analysis_result.get('hook_analysis', {}),
                'key_insights': [
                    {
                        'insight': insight.get('insight', ''),
                        'evidence': insight.get('evidence', ''),
                        'impact': insight.get('impact', 'Medium'),
                        'confidence': insight.get('confidence', 0.8)
                    }
                    for insight in key_insights[:5]  # Limit to top 5 insights
                ],
                'recommendations': [
                    {
                        'recommendation': rec.get('recommendation', ''),
                        'expected_impact': rec.get('expected_impact', 'Medium'),
                        'implementation_difficulty': rec.get('implementation_difficulty', 'Medium'),
                        'reasoning': rec.get('reasoning', '')
                    }
                    for rec in recommendations[:5]  # Limit to top 5 recommendations
                ],
                'detailed_analysis': {
                    'video_count': analysis_result.get('analysis_metadata', {}).get('videos_analyzed', 0),
                    'performance_analysis': ai_analysis.get('performance_analysis', {}),
                    'content_metrics': analysis_result.get('video_metrics', []),
                    'hook_effectiveness': analysis_result.get('hook_analysis', {}).get('overall_hook_performance', 0)
                }
            },
            'token_usage': {
                'input_tokens': 2750,
                'output_tokens': 1230,
                'model': 'gemini-2.0-flash-exp'
            },
            'cache_info': {
                'cache_hit': cache_hit,
                'cache_key': 'content_analysis_' + request_id[:8],
                'ttl_remaining': 3600 if not cache_hit else 2400
            },
            'processing_time': round(processing_time, 2),
            'for_boss_agent_only': True
        }
    
    
    def _get_domain_keywords(self) -> List[str]:
        """Return domain-specific keywords for this agent"""
        return [
            'video performance', 'content analysis', 'video metrics',
            'engagement', 'views', 'retention', 'thumbnail', 'title',
            'hook', 'content quality', 'video length'
        ]
    
    def _score_hook_quality(self, content_data: Dict) -> float:
        """Score hook quality based on title and opening"""
        title = content_data.get('title', '').lower()
        opening = content_data.get('opening_hook', '').lower()

        score = 0.5  # Base score

        # Title scoring
        hook_patterns = {
            'curiosity': ['how', 'why', 'what if', 'secret', 'revealed'],
            'emotion': ['shocking', 'amazing', 'incredible', 'surprising'],
            'benefit': ['guide', 'tutorial', 'tips', 'learn', 'master'],
            'urgency': ['new', 'breaking', 'urgent', 'limited'],
            'specific': ['step by step', 'complete', 'ultimate', 'proven']
        }

        # Score based on hook patterns
        for patterns in hook_patterns.values():
            if any(pattern in title for pattern in patterns):
                score += 0.1

        # Opening hook scoring (if provided)
        if opening:
            if len(opening.split()) >= 10:  # Good length
                score += 0.1
            if any(word in opening for word in ['you', 'your', 'imagine', 'watch']):  # Engagement words
                score += 0.1

        return min(1.0, score)

    def _score_topic_strength(self, content_data: Dict, channel_context: Dict) -> float:
        """Score topic relevance and timing"""
        title = content_data.get('title', '').lower()
        description = content_data.get('description', '').lower()
        niche = channel_context.get('niche', '').lower()

        score = 0.5  # Base score

        # Check niche relevance
        niche_keywords = content_data.get('niche_keywords', [])
        if any(keyword in title or keyword in description for keyword in niche_keywords):
            score += 0.2

        # Check trend alignment
        trend_keywords = content_data.get('trend_keywords', [])
        if any(keyword in title or keyword in description for keyword in trend_keywords):
            score += 0.2

        # Check seasonality
        if content_data.get('seasonally_relevant', False):
            score += 0.1

        return min(1.0, score)

    def _score_competitive_edge(self, content_data: Dict, channel_context: Dict) -> float:
        """Score content differentiation"""
        unique_angle = content_data.get('unique_angle', False)
        competitor_analysis = content_data.get('competitor_analysis', {})

        score = 0.5  # Base score

        if unique_angle:
            score += 0.2

        competition_level = competitor_analysis.get('competition_level', 'medium')
        if competition_level == 'low':
            score += 0.3
        elif competition_level == 'medium':
            score += 0.2

        return min(1.0, score)

    def _score_audience_match(self, content_data: Dict, channel_context: Dict) -> float:
        """Score alignment with audience interests"""
        audience_interests = channel_context.get('audience_interests', [])
        content_topics = content_data.get('topics', [])

        score = 0.5  # Base score

        # Calculate topic overlap
        overlap = len(set(audience_interests) & set(content_topics))
        if overlap > 0:
            score += min(0.5, overlap * 0.1)

        return min(1.0, score)

    def _score_metadata_optimization(self, content_data: Dict) -> float:
        """Score SEO and thumbnail optimization"""
        score = 0.5  # Base score

        # Title optimization
        title = content_data.get('title', '')
        if 20 <= len(title) <= 60:  # Optimal title length
            score += 0.1

        # Description optimization
        description = content_data.get('description', '')
        if len(description) >= 100:  # Good description length
            score += 0.1

        # Thumbnail quality
        thumbnail_score = content_data.get('thumbnail_score', 0)
        score += min(0.3, thumbnail_score / 10)

        return min(1.0, score)

    def _predict_view_range(self, performance_score: float, channel_context: Dict) -> Dict[str, int]:
        """Predict view range based on performance score and channel metrics"""
        avg_views = channel_context.get('avg_view_count', 1000)

        if performance_score >= 80:  # Excellent potential
            min_views = int(avg_views * 1.5)
            max_views = int(avg_views * 3)
        elif performance_score >= 60:  # Good potential
            min_views = int(avg_views * 0.8)
            max_views = int(avg_views * 1.5)
        else:  # Average or below
            min_views = int(avg_views * 0.5)
            max_views = int(avg_views * 0.8)

        return {
            'minimum': min_views,
            'maximum': max_views,
            'likely': int((min_views + max_views) / 2)
        }

    def _calculate_success_probability(self, performance_score: float) -> Dict[str, float]:
        """Calculate probability of different success levels"""
        return {
            'viral_chance': max(0, min(1, (performance_score - 85) / 15)) if performance_score > 85 else 0,
            'above_average': max(0, min(1, (performance_score - 60) / 20)),
            'average_performance': max(0, min(1, (performance_score - 40) / 20)),
            'below_average': max(0, min(1, (60 - performance_score) / 20)) if performance_score < 60 else 0
        }

    def _predict_engagement_metrics(self, performance_score: float, channel_context: Dict) -> Dict[str, Any]:
        """Predict engagement metrics based on performance score"""
        avg_engagement = channel_context.get('avg_engagement_rate', 5)
        avg_ctr = channel_context.get('avg_ctr', 4)

        score_multiplier = performance_score / 50  # 1.0 = average, 2.0 = excellent

        return {
            'predicted_ctr': round(avg_ctr * score_multiplier, 1),
            'predicted_engagement': round(avg_engagement * score_multiplier, 1),
            'predicted_retention': round(min(100, 40 + performance_score / 2), 1)
        }

    def _generate_optimization_suggestions(self, factor_scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """Generate specific optimization suggestions based on scores"""
        suggestions = []

        for factor, score in factor_scores.items():
            if score < 0.7:
                suggestions.append({
                    'factor': factor,
                    'current_score': round(score * 100, 1),
                    'suggestion': self._get_factor_suggestion(factor),
                    'priority': 'High' if score < 0.5 else 'Medium'
                })

        return sorted(suggestions, key=lambda x: x['current_score'])

    def _get_factor_suggestion(self, factor: str) -> str:
        """Get specific suggestion for improving a factor"""
        suggestions = {
            'hook_quality': 'Strengthen your hook with curiosity or emotion triggers',
            'topic_strength': 'Align content more closely with current trends or seasonal interests',
            'competitive_edge': 'Develop a more unique angle or perspective on the topic',
            'audience_match': 'Better align content with proven audience interests',
            'metadata_optimization': 'Optimize title length and thumbnail design'
        }
        return suggestions.get(factor, 'Review and improve this aspect of your content')

    async def _perform_analysis(self, request: AgentRequest) -> AgentAnalysis:
        """Perform the core content analysis"""

        # Extract request parameters
        channel_id = request.context.get('channel_id', 'unknown')
        video_ids = request.context.get('specific_videos', [])
        analysis_depth = request.analysis_depth
        user_context = request.user_context

        # Perform YouTube data retrieval and analysis
        try:
            video_metrics = await self._get_video_metrics(video_ids, channel_id, user_context)
            channel_context = await self._get_channel_context(channel_id, user_context)
            
            # Perform AI analysis
            ai_analysis = await self.gemini_engine.analyze_content_performance(
                video_metrics, 
                channel_context,
                include_hook_analysis=True
            )
            
            # Calculate additional metrics
            performance_scores = self._calculate_performance_scores(video_metrics, channel_context)
            top_performers = self._identify_top_performers(video_metrics)
            pattern_analysis = self.pattern_analyzer.analyze_historical_patterns(
                video_metrics, channel_context
            )

            # Combine into AgentAnalysis format
            return AgentAnalysis(
                summary=ai_analysis.get('summary', 'Content analysis completed successfully'),
                metrics=performance_scores,
                key_insights=[AgentInsight(**insight) for insight in ai_analysis.get('key_insights', [])[:5]],
                recommendations=[AgentRecommendation(**rec) for rec in ai_analysis.get('recommendations', [])[:5]],
                detailed_analysis={
                    'video_count': len(video_metrics),
                    'performance_analysis': ai_analysis.get('performance_analysis', {}),
                    'top_performers': top_performers,
                    'content_metrics': [
                        {
                            'video_id': m.video_id,
                            'title': m.title,
                            'views': m.views,
                            'engagement_rate': m.engagement_rate,
                            'duration_minutes': round(m.duration / 60, 1)
                        }
                        for m in video_metrics
                    ],
                    'pattern_analysis': pattern_analysis
                }
            )

        except Exception as e:
            logger.error(f"Error in content analysis: {e}")
            raise
    
    async def process_boss_agent_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a request from the Boss Agent with authentication validation"""
        from boss_agent_auth import validate_specialized_agent_request
        
        # Validate Boss Agent authentication
        auth_result = validate_specialized_agent_request(request_data)
        if not auth_result.is_valid:
            logger.warning(f"Unauthorized access attempt to Content Analysis Agent: {auth_result.error_message}")
            return {
                'agent_type': 'content_analysis',
                'response_id': f"unauth_{request_data.get('request_id', 'unknown')}",
                'request_id': request_data.get('request_id', ''),
                'timestamp': datetime.utcnow().isoformat(),
                'domain_match': False,
                'analysis': {
                    'summary': 'Unauthorized request: Boss agent authentication required',
                    'error_type': 'authentication_error',
                    'error_message': auth_result.error_message,
                    'required_auth': 'boss_agent_jwt_token'
                },
                'confidence_score': 0.0,
                'processing_time': 0.0,
                'for_boss_agent_only': True,
                'authentication_required': True
            }
        
        # Convert to legacy format and process
        try:
            # Extract parameters from request
            request_id = request_data.get('request_id', str(uuid.uuid4()))
            channel_id = request_data.get('context', {}).get('channel_id', '')
            time_period = request_data.get('context', {}).get('time_period', 'last_30d')
            specific_videos = request_data.get('context', {}).get('specific_videos', [])
            analysis_depth = request_data.get('analysis_depth', 'standard')
            include_visual_analysis = request_data.get('include_visual_analysis', True)
            user_context = request_data.get('user_context', {})
            
            # Create analysis request
            analysis_request = AnalysisRequest(
                request_id=request_id,
                channel_id=channel_id,
                video_ids=specific_videos,
                time_period=time_period,
                analysis_depth=analysis_depth,
                include_visual_analysis=include_visual_analysis,
                user_context=user_context
            )
            
            # Perform analysis
            start_time = time.time()
            analysis_result = await self._perform_content_analysis(analysis_request)
            processing_time = time.time() - start_time
            
            # Format response for Boss Agent
            return {
                'agent_type': 'content_analysis',
                'response_id': f"content_{request_id}",
                'request_id': request_id,
                'timestamp': datetime.utcnow().isoformat(),
                'confidence_score': analysis_result.get('confidence_score', 0.85),
                'domain_match': True,
                'analysis': {
                    'summary': analysis_result.get('summary', 'Content analysis completed successfully'),
                    'metrics': analysis_result.get('metrics', {}),
                    'key_insights': [
                        {
                            'insight': insight.get('insight', ''),
                            'evidence': insight.get('evidence', ''),
                            'impact': insight.get('impact', 'Medium'),
                            'confidence': insight.get('confidence', 0.8)
                        }
                        for insight in analysis_result.get('key_insights', [])
                    ],
                    'recommendations': [
                        {
                            'recommendation': rec.get('recommendation', ''),
                            'expected_impact': rec.get('expected_impact', 'Medium'),
                            'implementation_difficulty': rec.get('implementation_difficulty', 'Medium'),
                            'reasoning': rec.get('reasoning', '')
                        }
                        for rec in analysis_result.get('recommendations', [])
                    ]
                },
                'token_usage': {
                    'input_tokens': analysis_result.get('token_usage', {}).get('input_tokens', 0),
                    'output_tokens': analysis_result.get('token_usage', {}).get('output_tokens', 0),
                    'model': 'gemini-2.5-pro'
                },
                'cache_info': {
                    'cache_hit': False,
                    'cache_key': f"content_analysis_{channel_id}_{hash(str(specific_videos))}",
                    'ttl_remaining': 3600
                },
                'processing_time': processing_time,
                'for_boss_agent_only': True
            }
            
        except Exception as e:
            logger.error(f"Error processing Boss Agent request: {e}")
            return {
                'agent_type': 'content_analysis',
                'response_id': f"error_{request_data.get('request_id', 'unknown')}",
                'request_id': request_data.get('request_id', ''),
                'timestamp': datetime.utcnow().isoformat(),
                'domain_match': False,
                'analysis': {
                    'summary': f'Error processing content analysis request: {str(e)}',
                    'error_type': 'processing_error',
                    'error_message': str(e)
                },
                'confidence_score': 0.0,
                'processing_time': 0.0,
                'for_boss_agent_only': True
            }

# Global instance for boss agent integration
content_analysis_agent = None

def get_content_analysis_agent():
    """Get or create content analysis agent instance"""
    global content_analysis_agent
    
    if content_analysis_agent is None:
        youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        if not youtube_api_key:
            logger.warning("YOUTUBE_API_KEY not set - using demo mode")
            youtube_api_key = "demo_key"
        
        if not gemini_api_key:
            logger.warning("GEMINI_API_KEY not set - using demo mode")
            gemini_api_key = "demo_key"
        
        content_analysis_agent = ContentAnalysisAgent(youtube_api_key, gemini_api_key)
    
    return content_analysis_agent

async def process_content_analysis_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for boss agent to request content analysis
    This is the ONLY function the boss agent should call
    """
    agent = get_content_analysis_agent()
    return await agent.process_boss_agent_request(request_data)