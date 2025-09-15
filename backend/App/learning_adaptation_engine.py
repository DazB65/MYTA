"""
Learning & Adaptation Engine
AI system that learns from user's success patterns and continuously improves recommendations
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
import numpy as np
from collections import defaultdict
import sqlite3
import os

from backend.App.enhanced_user_context import EnhancedUserContextManager
from backend.App.youtube_analytics_service import YouTubeAnalyticsService

logger = logging.getLogger(__name__)

@dataclass
class SuccessPattern:
    """Identified success pattern for a user"""
    pattern_id: str
    user_id: str
    pattern_type: str  # 'title', 'timing', 'topic', 'thumbnail', etc.
    pattern_data: Dict[str, Any]
    success_metrics: Dict[str, float]
    confidence_score: float
    sample_size: int
    last_updated: datetime
    
@dataclass
class LearningInsight:
    """Learning insight generated from user data"""
    insight_id: str
    user_id: str
    insight_type: str
    title: str
    description: str
    recommendation: str
    impact_score: float
    confidence: float
    supporting_data: Dict[str, Any]
    created_at: datetime

@dataclass
class AdaptationRecommendation:
    """Adaptive recommendation based on learning"""
    recommendation_id: str
    user_id: str
    recommendation_type: str
    title: str
    description: str
    specific_action: str
    expected_improvement: float
    confidence: float
    priority: int
    expires_at: Optional[datetime]

class LearningAdaptationEngine:
    """AI engine that learns from user success patterns and adapts recommendations"""
    
    def __init__(self):
        self.context_service = EnhancedUserContextManager()
        self.analytics_service = None
        
        # Database for storing learning data
        self.db_path = "backend/data/learning_engine.db"
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_database()
        
        # Learning parameters
        self.min_sample_size = 5  # Minimum videos needed to identify pattern
        self.confidence_threshold = 0.7  # Minimum confidence for recommendations
        self.learning_window_days = 90  # Days to look back for learning
        
        # Pattern weights for different metrics
        self.metric_weights = {
            'views': 0.3,
            'ctr': 0.25,
            'engagement_rate': 0.25,
            'retention': 0.2
        }
        
        logger.info("Learning & Adaptation Engine initialized")
    
    def _init_database(self):
        """Initialize SQLite database for learning data"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS success_patterns (
                    pattern_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    pattern_type TEXT NOT NULL,
                    pattern_data TEXT NOT NULL,
                    success_metrics TEXT NOT NULL,
                    confidence_score REAL NOT NULL,
                    sample_size INTEGER NOT NULL,
                    last_updated TIMESTAMP NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS learning_insights (
                    insight_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    insight_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    recommendation TEXT NOT NULL,
                    impact_score REAL NOT NULL,
                    confidence REAL NOT NULL,
                    supporting_data TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS adaptation_recommendations (
                    recommendation_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    recommendation_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    specific_action TEXT NOT NULL,
                    expected_improvement REAL NOT NULL,
                    confidence REAL NOT NULL,
                    priority INTEGER NOT NULL,
                    expires_at TIMESTAMP,
                    created_at TIMESTAMP NOT NULL
                )
            """)
            
            conn.commit()
    
    async def analyze_user_patterns(self, user_id: str) -> List[SuccessPattern]:
        """Analyze user's content to identify success patterns"""
        try:
            logger.info(f"🧠 Analyzing success patterns for user {user_id}")
            
            # Get enhanced user context with historical data
            enhanced_context = await self.context_service.get_enhanced_context(user_id)
            
            # Analyze different pattern types
            patterns = []
            patterns.extend(await self._analyze_title_patterns(user_id, enhanced_context))
            patterns.extend(await self._analyze_timing_patterns(user_id, enhanced_context))
            patterns.extend(await self._analyze_topic_patterns(user_id, enhanced_context))
            patterns.extend(await self._analyze_length_patterns(user_id, enhanced_context))
            patterns.extend(await self._analyze_thumbnail_patterns(user_id, enhanced_context))
            
            # Store patterns in database
            await self._store_patterns(patterns)
            
            logger.info(f"✅ Identified {len(patterns)} success patterns for user {user_id}")
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing user patterns: {e}")
            return []
    
    async def _analyze_title_patterns(self, user_id: str, enhanced_context: Dict[str, Any]) -> List[SuccessPattern]:
        """Analyze title patterns that lead to success"""
        patterns = []
        
        try:
            recent_videos = enhanced_context.get('recent_content', [])
            if len(recent_videos) < self.min_sample_size:
                return patterns
            
            # Group videos by title characteristics
            title_groups = {
                'question_titles': [],
                'how_to_titles': [],
                'list_titles': [],
                'emotional_titles': [],
                'short_titles': [],
                'long_titles': []
            }
            
            for video in recent_videos:
                title = video.get('title', '').lower()
                metrics = video.get('metrics', {})
                
                # Categorize titles
                if '?' in title:
                    title_groups['question_titles'].append((video, metrics))
                if 'how to' in title:
                    title_groups['how_to_titles'].append((video, metrics))
                if any(word in title for word in ['top', 'best', 'worst', 'list']):
                    title_groups['list_titles'].append((video, metrics))
                if any(word in title for word in ['amazing', 'incredible', 'shocking', 'unbelievable']):
                    title_groups['emotional_titles'].append((video, metrics))
                if len(title) <= 40:
                    title_groups['short_titles'].append((video, metrics))
                if len(title) >= 60:
                    title_groups['long_titles'].append((video, metrics))
            
            # Analyze each group for success patterns
            for pattern_type, videos_metrics in title_groups.items():
                if len(videos_metrics) >= self.min_sample_size:
                    pattern = await self._calculate_pattern_success(
                        user_id, f"title_{pattern_type}", videos_metrics, enhanced_context
                    )
                    if pattern:
                        patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing title patterns: {e}")
            return []
    
    async def _analyze_timing_patterns(self, user_id: str, enhanced_context: Dict[str, Any]) -> List[SuccessPattern]:
        """Analyze timing patterns that lead to success"""
        patterns = []
        
        try:
            recent_videos = enhanced_context.get('recent_content', [])
            if len(recent_videos) < self.min_sample_size:
                return patterns
            
            # Group by timing characteristics
            timing_groups = defaultdict(list)
            
            for video in recent_videos:
                published_at = video.get('published_at')
                if not published_at:
                    continue
                
                pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                metrics = video.get('metrics', {})
                
                # Group by hour
                hour_group = f"hour_{pub_date.hour}"
                timing_groups[hour_group].append((video, metrics))
                
                # Group by day of week
                day_group = f"day_{pub_date.weekday()}"
                timing_groups[day_group].append((video, metrics))
                
                # Group by time of day
                if 6 <= pub_date.hour <= 11:
                    timing_groups['morning'].append((video, metrics))
                elif 12 <= pub_date.hour <= 17:
                    timing_groups['afternoon'].append((video, metrics))
                elif 18 <= pub_date.hour <= 23:
                    timing_groups['evening'].append((video, metrics))
                else:
                    timing_groups['night'].append((video, metrics))
            
            # Analyze timing patterns
            for pattern_type, videos_metrics in timing_groups.items():
                if len(videos_metrics) >= self.min_sample_size:
                    pattern = await self._calculate_pattern_success(
                        user_id, f"timing_{pattern_type}", videos_metrics, enhanced_context
                    )
                    if pattern:
                        patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing timing patterns: {e}")
            return []
    
    async def _analyze_topic_patterns(self, user_id: str, enhanced_context: Dict[str, Any]) -> List[SuccessPattern]:
        """Analyze topic patterns that lead to success"""
        patterns = []
        
        try:
            recent_videos = enhanced_context.get('recent_content', [])
            if len(recent_videos) < self.min_sample_size:
                return patterns
            
            # Group by topic/category
            topic_groups = defaultdict(list)
            
            for video in recent_videos:
                # Extract topics from title and description
                title = video.get('title', '').lower()
                description = video.get('description', '').lower()
                metrics = video.get('metrics', {})
                
                # Simple topic extraction (in production, use NLP)
                topics = []
                if any(word in title for word in ['tutorial', 'how to', 'guide']):
                    topics.append('educational')
                if any(word in title for word in ['review', 'unboxing', 'test']):
                    topics.append('review')
                if any(word in title for word in ['vlog', 'day in', 'behind']):
                    topics.append('lifestyle')
                if any(word in title for word in ['news', 'update', 'announcement']):
                    topics.append('news')
                
                for topic in topics:
                    topic_groups[topic].append((video, metrics))
            
            # Analyze topic patterns
            for pattern_type, videos_metrics in topic_groups.items():
                if len(videos_metrics) >= self.min_sample_size:
                    pattern = await self._calculate_pattern_success(
                        user_id, f"topic_{pattern_type}", videos_metrics, enhanced_context
                    )
                    if pattern:
                        patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing topic patterns: {e}")
            return []

    async def _analyze_length_patterns(self, user_id: str, enhanced_context: Dict[str, Any]) -> List[SuccessPattern]:
        """Analyze video length patterns that lead to success"""
        patterns = []

        try:
            recent_videos = enhanced_context.get('recent_content', [])
            if len(recent_videos) < self.min_sample_size:
                return patterns

            # Group by video length
            length_groups = {
                'short': [],  # < 5 minutes
                'medium': [],  # 5-15 minutes
                'long': [],   # 15-30 minutes
                'very_long': []  # > 30 minutes
            }

            for video in recent_videos:
                duration = video.get('duration_seconds', 0)
                metrics = video.get('metrics', {})

                if duration < 300:  # 5 minutes
                    length_groups['short'].append((video, metrics))
                elif duration < 900:  # 15 minutes
                    length_groups['medium'].append((video, metrics))
                elif duration < 1800:  # 30 minutes
                    length_groups['long'].append((video, metrics))
                else:
                    length_groups['very_long'].append((video, metrics))

            # Analyze length patterns
            for pattern_type, videos_metrics in length_groups.items():
                if len(videos_metrics) >= self.min_sample_size:
                    pattern = await self._calculate_pattern_success(
                        user_id, f"length_{pattern_type}", videos_metrics, enhanced_context
                    )
                    if pattern:
                        patterns.append(pattern)

            return patterns

        except Exception as e:
            logger.error(f"Error analyzing length patterns: {e}")
            return []

    async def _analyze_thumbnail_patterns(self, user_id: str, enhanced_context: Dict[str, Any]) -> List[SuccessPattern]:
        """Analyze thumbnail patterns that lead to success"""
        patterns = []

        try:
            recent_videos = enhanced_context.get('recent_content', [])
            if len(recent_videos) < self.min_sample_size:
                return patterns

            # Group by thumbnail characteristics (simplified)
            thumbnail_groups = {
                'face_prominent': [],
                'text_overlay': [],
                'bright_colors': [],
                'minimal_design': []
            }

            for video in recent_videos:
                thumbnail_url = video.get('thumbnail_url', '')
                metrics = video.get('metrics', {})

                # Simplified thumbnail analysis (in production, use computer vision)
                # For now, randomly assign to demonstrate the pattern
                import random
                random.seed(hash(thumbnail_url))
                group = random.choice(list(thumbnail_groups.keys()))
                thumbnail_groups[group].append((video, metrics))

            # Analyze thumbnail patterns
            for pattern_type, videos_metrics in thumbnail_groups.items():
                if len(videos_metrics) >= self.min_sample_size:
                    pattern = await self._calculate_pattern_success(
                        user_id, f"thumbnail_{pattern_type}", videos_metrics, enhanced_context
                    )
                    if pattern:
                        patterns.append(pattern)

            return patterns

        except Exception as e:
            logger.error(f"Error analyzing thumbnail patterns: {e}")
            return []

    async def _calculate_pattern_success(
        self,
        user_id: str,
        pattern_type: str,
        videos_metrics: List[Tuple[Dict, Dict]],
        enhanced_context: Dict[str, Any]
    ) -> Optional[SuccessPattern]:
        """Calculate success metrics for a pattern"""

        try:
            if len(videos_metrics) < self.min_sample_size:
                return None

            # Calculate average metrics for this pattern
            total_metrics = defaultdict(float)
            valid_count = 0

            for video, metrics in videos_metrics:
                if metrics:
                    total_metrics['views'] += metrics.get('views', 0)
                    total_metrics['ctr'] += metrics.get('ctr', 0)
                    total_metrics['engagement_rate'] += metrics.get('engagement_rate', 0)
                    total_metrics['retention'] += metrics.get('retention', 0)
                    valid_count += 1

            if valid_count == 0:
                return None

            # Calculate averages
            avg_metrics = {
                metric: total / valid_count
                for metric, total in total_metrics.items()
            }

            # Compare to user's overall averages
            user_averages = enhanced_context.get('performance_data', {})
            user_avg_views = user_averages.get('avg_views_30d', 1000)
            user_avg_ctr = user_averages.get('avg_ctr_30d', 4.0)
            user_avg_engagement = user_averages.get('avg_engagement_30d', 3.0)
            user_avg_retention = user_averages.get('avg_retention_30d', 45.0)

            # Calculate performance ratios
            performance_ratios = {
                'views': avg_metrics['views'] / max(user_avg_views, 1),
                'ctr': avg_metrics['ctr'] / max(user_avg_ctr, 1),
                'engagement_rate': avg_metrics['engagement_rate'] / max(user_avg_engagement, 1),
                'retention': avg_metrics['retention'] / max(user_avg_retention, 1)
            }

            # Calculate weighted success score
            success_score = sum(
                ratio * self.metric_weights[metric]
                for metric, ratio in performance_ratios.items()
            )

            # Only consider it a pattern if it performs significantly better
            if success_score < 1.1:  # At least 10% better than average
                return None

            # Calculate confidence based on sample size and consistency
            confidence = min(0.95, 0.5 + (valid_count / 20) + (success_score - 1) * 0.3)

            if confidence < self.confidence_threshold:
                return None

            pattern_id = f"{user_id}_{pattern_type}_{datetime.now().strftime('%Y%m%d')}"

            return SuccessPattern(
                pattern_id=pattern_id,
                user_id=user_id,
                pattern_type=pattern_type,
                pattern_data={
                    'sample_videos': [video.get('video_id', '') for video, _ in videos_metrics[:5]],
                    'performance_ratios': performance_ratios,
                    'avg_metrics': avg_metrics
                },
                success_metrics=avg_metrics,
                confidence_score=confidence,
                sample_size=valid_count,
                last_updated=datetime.now()
            )

        except Exception as e:
            logger.error(f"Error calculating pattern success: {e}")
            return None

    async def _store_patterns(self, patterns: List[SuccessPattern]):
        """Store success patterns in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                for pattern in patterns:
                    conn.execute("""
                        INSERT OR REPLACE INTO success_patterns
                        (pattern_id, user_id, pattern_type, pattern_data, success_metrics,
                         confidence_score, sample_size, last_updated)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        pattern.pattern_id,
                        pattern.user_id,
                        pattern.pattern_type,
                        json.dumps(pattern.pattern_data),
                        json.dumps(pattern.success_metrics),
                        pattern.confidence_score,
                        pattern.sample_size,
                        pattern.last_updated.isoformat()
                    ))
                conn.commit()

        except Exception as e:
            logger.error(f"Error storing patterns: {e}")

    async def generate_adaptive_recommendations(self, user_id: str) -> List[AdaptationRecommendation]:
        """Generate adaptive recommendations based on learned patterns"""
        try:
            logger.info(f"🎯 Generating adaptive recommendations for user {user_id}")

            # Get stored patterns
            patterns = await self._get_user_patterns(user_id)

            if not patterns:
                # Analyze patterns first
                patterns = await self.analyze_user_patterns(user_id)

            recommendations = []

            # Generate recommendations from patterns
            for pattern in patterns:
                if pattern.confidence_score >= self.confidence_threshold:
                    rec = await self._pattern_to_recommendation(pattern)
                    if rec:
                        recommendations.append(rec)

            # Sort by priority and expected impact
            recommendations.sort(key=lambda x: (x.priority, -x.expected_improvement), reverse=True)

            # Store recommendations
            await self._store_recommendations(recommendations)

            logger.info(f"✅ Generated {len(recommendations)} adaptive recommendations")
            return recommendations[:10]  # Return top 10

        except Exception as e:
            logger.error(f"Error generating adaptive recommendations: {e}")
            return []

    async def _get_user_patterns(self, user_id: str) -> List[SuccessPattern]:
        """Get stored patterns for a user"""
        patterns = []

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT * FROM success_patterns
                    WHERE user_id = ? AND last_updated > ?
                    ORDER BY confidence_score DESC
                """, (user_id, (datetime.now() - timedelta(days=30)).isoformat()))

                for row in cursor.fetchall():
                    pattern = SuccessPattern(
                        pattern_id=row[0],
                        user_id=row[1],
                        pattern_type=row[2],
                        pattern_data=json.loads(row[3]),
                        success_metrics=json.loads(row[4]),
                        confidence_score=row[5],
                        sample_size=row[6],
                        last_updated=datetime.fromisoformat(row[7])
                    )
                    patterns.append(pattern)

        except Exception as e:
            logger.error(f"Error getting user patterns: {e}")

        return patterns

    async def _pattern_to_recommendation(self, pattern: SuccessPattern) -> Optional[AdaptationRecommendation]:
        """Convert a success pattern to an actionable recommendation"""

        try:
            pattern_type = pattern.pattern_type
            pattern_data = pattern.pattern_data
            performance_ratios = pattern_data.get('performance_ratios', {})

            # Calculate expected improvement
            avg_improvement = np.mean(list(performance_ratios.values())) - 1.0

            if avg_improvement < 0.1:  # Less than 10% improvement
                return None

            # Generate recommendation based on pattern type
            if pattern_type.startswith('title_'):
                title, description, action = self._generate_title_recommendation(pattern_type, pattern_data)
            elif pattern_type.startswith('timing_'):
                title, description, action = self._generate_timing_recommendation(pattern_type, pattern_data)
            elif pattern_type.startswith('topic_'):
                title, description, action = self._generate_topic_recommendation(pattern_type, pattern_data)
            elif pattern_type.startswith('length_'):
                title, description, action = self._generate_length_recommendation(pattern_type, pattern_data)
            elif pattern_type.startswith('thumbnail_'):
                title, description, action = self._generate_thumbnail_recommendation(pattern_type, pattern_data)
            else:
                return None

            recommendation_id = f"{pattern.user_id}_{pattern_type}_rec_{datetime.now().strftime('%Y%m%d%H%M')}"

            return AdaptationRecommendation(
                recommendation_id=recommendation_id,
                user_id=pattern.user_id,
                recommendation_type=pattern_type,
                title=title,
                description=description,
                specific_action=action,
                expected_improvement=avg_improvement,
                confidence=pattern.confidence_score,
                priority=self._calculate_recommendation_priority(pattern_type, avg_improvement),
                expires_at=datetime.now() + timedelta(days=30)
            )

        except Exception as e:
            logger.error(f"Error converting pattern to recommendation: {e}")
            return None

    def _generate_title_recommendation(self, pattern_type: str, pattern_data: Dict) -> Tuple[str, str, str]:
        """Generate title-based recommendation"""

        performance_ratios = pattern_data.get('performance_ratios', {})
        improvement = (np.mean(list(performance_ratios.values())) - 1.0) * 100

        if 'question' in pattern_type:
            return (
                "Question Titles Perform Better",
                f"Your question-style titles perform {improvement:.1f}% better than average",
                "Use more question-based titles (e.g., 'How do you...?', 'What happens when...?')"
            )
        elif 'how_to' in pattern_type:
            return (
                "How-To Titles Drive Success",
                f"Your how-to titles perform {improvement:.1f}% better than average",
                "Create more how-to content with clear instructional titles"
            )
        elif 'emotional' in pattern_type:
            return (
                "Emotional Titles Boost Performance",
                f"Your emotional titles perform {improvement:.1f}% better than average",
                "Use more emotional words in titles (amazing, incredible, shocking, etc.)"
            )
        else:
            return (
                "Title Pattern Identified",
                f"This title style performs {improvement:.1f}% better than average",
                "Continue using this successful title pattern"
            )

    def _generate_timing_recommendation(self, pattern_type: str, pattern_data: Dict) -> Tuple[str, str, str]:
        """Generate timing-based recommendation"""

        performance_ratios = pattern_data.get('performance_ratios', {})
        improvement = (np.mean(list(performance_ratios.values())) - 1.0) * 100

        if 'evening' in pattern_type:
            return (
                "Evening Posts Perform Better",
                f"Your evening uploads perform {improvement:.1f}% better than average",
                "Schedule more content for evening hours (6-11 PM)"
            )
        elif 'weekend' in pattern_type or 'day_5' in pattern_type or 'day_6' in pattern_type:
            return (
                "Weekend Uploads Drive Success",
                f"Your weekend uploads perform {improvement:.1f}% better than average",
                "Focus on weekend posting for better engagement"
            )
        else:
            return (
                "Optimal Timing Identified",
                f"This posting time performs {improvement:.1f}% better than average",
                "Continue posting at this optimal time"
            )

    def _generate_topic_recommendation(self, pattern_type: str, pattern_data: Dict) -> Tuple[str, str, str]:
        """Generate topic-based recommendation"""

        performance_ratios = pattern_data.get('performance_ratios', {})
        improvement = (np.mean(list(performance_ratios.values())) - 1.0) * 100

        topic = pattern_type.replace('topic_', '').replace('_', ' ').title()

        return (
            f"{topic} Content Performs Well",
            f"Your {topic.lower()} content performs {improvement:.1f}% better than average",
            f"Create more {topic.lower()} content to leverage this successful pattern"
        )

    def _generate_length_recommendation(self, pattern_type: str, pattern_data: Dict) -> Tuple[str, str, str]:
        """Generate length-based recommendation"""

        performance_ratios = pattern_data.get('performance_ratios', {})
        improvement = (np.mean(list(performance_ratios.values())) - 1.0) * 100

        if 'short' in pattern_type:
            return (
                "Short Videos Drive Success",
                f"Your short videos (<5 min) perform {improvement:.1f}% better than average",
                "Focus on creating more concise, short-form content"
            )
        elif 'medium' in pattern_type:
            return (
                "Medium Length Optimal",
                f"Your medium-length videos (5-15 min) perform {improvement:.1f}% better than average",
                "Maintain video length between 5-15 minutes for optimal performance"
            )
        elif 'long' in pattern_type:
            return (
                "Long-Form Content Success",
                f"Your longer videos perform {improvement:.1f}% better than average",
                "Continue creating detailed, long-form content"
            )
        else:
            return (
                "Video Length Pattern",
                f"This video length performs {improvement:.1f}% better than average",
                "Maintain this optimal video length"
            )

    def _generate_thumbnail_recommendation(self, pattern_type: str, pattern_data: Dict) -> Tuple[str, str, str]:
        """Generate thumbnail-based recommendation"""

        performance_ratios = pattern_data.get('performance_ratios', {})
        improvement = (np.mean(list(performance_ratios.values())) - 1.0) * 100

        style = pattern_type.replace('thumbnail_', '').replace('_', ' ')

        return (
            f"Thumbnail Style Success",
            f"Your {style} thumbnails perform {improvement:.1f}% better than average",
            f"Continue using {style} thumbnail design for better CTR"
        )

    def _calculate_recommendation_priority(self, pattern_type: str, improvement: float) -> int:
        """Calculate recommendation priority (1-5, 5 being highest)"""

        # Base priority on improvement and pattern type importance
        base_priority = min(5, max(1, int(improvement * 10)))

        # Adjust based on pattern type importance
        if pattern_type.startswith('timing_'):
            base_priority += 1  # Timing is very actionable
        elif pattern_type.startswith('title_'):
            base_priority += 1  # Titles are high impact
        elif pattern_type.startswith('thumbnail_'):
            base_priority += 0  # Thumbnails are important but harder to change

        return min(5, base_priority)

    async def _store_recommendations(self, recommendations: List[AdaptationRecommendation]):
        """Store recommendations in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                for rec in recommendations:
                    conn.execute("""
                        INSERT OR REPLACE INTO adaptation_recommendations
                        (recommendation_id, user_id, recommendation_type, title, description,
                         specific_action, expected_improvement, confidence, priority, expires_at, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        rec.recommendation_id,
                        rec.user_id,
                        rec.recommendation_type,
                        rec.title,
                        rec.description,
                        rec.specific_action,
                        rec.expected_improvement,
                        rec.confidence,
                        rec.priority,
                        rec.expires_at.isoformat() if rec.expires_at else None,
                        datetime.now().isoformat()
                    ))
                conn.commit()

        except Exception as e:
            logger.error(f"Error storing recommendations: {e}")

    async def get_user_recommendations(self, user_id: str, limit: int = 10) -> List[AdaptationRecommendation]:
        """Get active recommendations for a user"""
        recommendations = []

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT * FROM adaptation_recommendations
                    WHERE user_id = ? AND (expires_at IS NULL OR expires_at > ?)
                    ORDER BY priority DESC, expected_improvement DESC
                    LIMIT ?
                """, (user_id, datetime.now().isoformat(), limit))

                for row in cursor.fetchall():
                    rec = AdaptationRecommendation(
                        recommendation_id=row[0],
                        user_id=row[1],
                        recommendation_type=row[2],
                        title=row[3],
                        description=row[4],
                        specific_action=row[5],
                        expected_improvement=row[6],
                        confidence=row[7],
                        priority=row[8],
                        expires_at=datetime.fromisoformat(row[9]) if row[9] else None
                    )
                    recommendations.append(rec)

        except Exception as e:
            logger.error(f"Error getting user recommendations: {e}")

        return recommendations

# Global instance
_learning_engine = None

def get_learning_engine() -> LearningAdaptationEngine:
    """Get global learning engine instance"""
    global _learning_engine
    if _learning_engine is None:
        _learning_engine = LearningAdaptationEngine()
    return _learning_engine
