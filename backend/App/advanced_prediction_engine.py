"""
Advanced Content Performance Prediction Engine
Builds upon existing MYTA analytics to provide sophisticated content performance prediction
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os

from .content_analysis_agent import ContentAnalysisAgent
from .youtube_analytics_service import YouTubeAnalyticsService
from .enhanced_user_context import EnhancedUserContextManager
from backend.App.audience_insights_agent import AudienceInsightsAgent

logger = logging.getLogger(__name__)

@dataclass
class ContentPrediction:
    """Comprehensive content performance prediction"""
    predicted_views: int
    predicted_ctr: float
    predicted_engagement_rate: float
    predicted_retention: float
    success_probability: float
    performance_score: float
    confidence_level: float
    optimization_suggestions: List[str]
    risk_factors: List[str]
    timing_recommendations: Dict[str, Any]
    predicted_metrics: Dict[str, Any]

@dataclass
class PredictionFeatures:
    """Features used for ML prediction"""
    # Content features
    title_length: int
    title_sentiment: float
    title_keyword_strength: float
    description_length: int
    topic_trend_score: float
    competitive_saturation: float
    
    # Channel features
    channel_size: int
    avg_views_last_30: float
    avg_ctr_last_30: float
    avg_engagement_last_30: float
    subscriber_growth_rate: float
    
    # Timing features
    hour_of_day: int
    day_of_week: int
    days_since_last_upload: int
    seasonal_factor: float
    
    # Audience features
    audience_match_score: float
    demographic_alignment: float
    
    # Historical features
    similar_content_performance: float
    creator_consistency_score: float

class AdvancedPredictionEngine:
    """Advanced ML-powered content performance prediction system"""
    
    def __init__(self):
        self.content_agent = None
        self.analytics_service = None
        self.context_service = EnhancedUserContextManager()
        self.audience_agent = AudienceInsightsAgent()
        
        # ML models (will be trained/loaded)
        self.view_predictor = None
        self.ctr_predictor = None
        self.engagement_predictor = None
        self.scaler = StandardScaler()
        
        # Model paths
        self.model_dir = "backend/models"
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Feature importance weights
        self.feature_weights = {
            'title_optimization': 0.25,
            'timing_optimization': 0.20,
            'audience_match': 0.20,
            'topic_strength': 0.15,
            'channel_momentum': 0.10,
            'competitive_edge': 0.10
        }
        
        logger.info("Advanced Prediction Engine initialized")
    
    async def predict_content_performance(
        self, 
        user_id: str, 
        content_data: Dict[str, Any],
        prediction_type: str = "comprehensive"
    ) -> ContentPrediction:
        """
        Predict comprehensive content performance before publishing
        
        Args:
            user_id: User identifier
            content_data: Content details (title, description, topic, etc.)
            prediction_type: Type of prediction (quick, standard, comprehensive)
        
        Returns:
            ContentPrediction with detailed performance forecasts
        """
        try:
            logger.info(f"🔮 Predicting content performance for user {user_id}")
            
            # Get enhanced context
            enhanced_context = await self.context_service.get_enhanced_context(user_id)
            audience_insights = await self.audience_agent.get_audience_context_for_content(user_id)
            
            # Extract prediction features
            features = await self._extract_prediction_features(
                content_data, enhanced_context, audience_insights
            )
            
            # Generate ML predictions
            ml_predictions = await self._generate_ml_predictions(features, enhanced_context)
            
            # Generate AI-enhanced insights
            ai_insights = await self._generate_ai_insights(
                content_data, enhanced_context, ml_predictions
            )
            
            # Calculate optimization suggestions
            optimization_suggestions = await self._generate_optimization_suggestions(
                features, ml_predictions, enhanced_context
            )
            
            # Calculate timing recommendations
            timing_recommendations = await self._calculate_optimal_timing(
                user_id, enhanced_context, features
            )
            
            # Assess risk factors
            risk_factors = await self._assess_risk_factors(
                features, enhanced_context, ml_predictions
            )
            
            # Calculate confidence level
            confidence_level = self._calculate_prediction_confidence(
                features, enhanced_context, ml_predictions
            )
            
            prediction = ContentPrediction(
                predicted_views=ml_predictions['views'],
                predicted_ctr=ml_predictions['ctr'],
                predicted_engagement_rate=ml_predictions['engagement'],
                predicted_retention=ml_predictions['retention'],
                success_probability=ml_predictions['success_probability'],
                performance_score=ml_predictions['performance_score'],
                confidence_level=confidence_level,
                optimization_suggestions=optimization_suggestions,
                risk_factors=risk_factors,
                timing_recommendations=timing_recommendations,
                predicted_metrics=ml_predictions
            )
            
            logger.info(f"✅ Content prediction completed: {prediction.predicted_views:,} views predicted")
            return prediction
            
        except Exception as e:
            logger.error(f"Error predicting content performance: {e}")
            return self._get_fallback_prediction(content_data)
    
    async def _extract_prediction_features(
        self, 
        content_data: Dict[str, Any], 
        enhanced_context: Dict[str, Any],
        audience_insights: Dict[str, Any]
    ) -> PredictionFeatures:
        """Extract ML features from content and context data"""
        
        channel_info = enhanced_context.get('channel_info', {})
        performance_data = enhanced_context.get('performance_data', {})
        
        # Content features
        title = content_data.get('title', '')
        description = content_data.get('description', '')
        
        # Calculate advanced features
        title_sentiment = await self._analyze_title_sentiment(title)
        title_keyword_strength = await self._calculate_keyword_strength(title, enhanced_context)
        topic_trend_score = await self._calculate_topic_trend_score(content_data, enhanced_context)
        competitive_saturation = await self._calculate_competitive_saturation(content_data, enhanced_context)
        
        # Timing features
        now = datetime.now()
        last_upload = enhanced_context.get('last_upload_date')
        days_since_last = (now - datetime.fromisoformat(last_upload)).days if last_upload else 7
        
        # Audience features
        audience_match_score = await self._calculate_audience_match_score(content_data, audience_insights)
        demographic_alignment = await self._calculate_demographic_alignment(content_data, audience_insights)
        
        # Historical features
        similar_content_performance = await self._get_similar_content_performance(content_data, enhanced_context)
        consistency_score = await self._calculate_creator_consistency_score(enhanced_context)
        
        return PredictionFeatures(
            title_length=len(title),
            title_sentiment=title_sentiment,
            title_keyword_strength=title_keyword_strength,
            description_length=len(description),
            topic_trend_score=topic_trend_score,
            competitive_saturation=competitive_saturation,
            channel_size=channel_info.get('subscriber_count', 1000),
            avg_views_last_30=performance_data.get('avg_views_30d', 1000),
            avg_ctr_last_30=performance_data.get('avg_ctr_30d', 4.0),
            avg_engagement_last_30=performance_data.get('avg_engagement_30d', 3.0),
            subscriber_growth_rate=performance_data.get('growth_rate_30d', 0.05),
            hour_of_day=now.hour,
            day_of_week=now.weekday(),
            days_since_last_upload=min(days_since_last, 30),
            seasonal_factor=self._calculate_seasonal_factor(now),
            audience_match_score=audience_match_score,
            demographic_alignment=demographic_alignment,
            similar_content_performance=similar_content_performance,
            creator_consistency_score=consistency_score
        )
    
    async def _generate_ml_predictions(
        self, 
        features: PredictionFeatures, 
        enhanced_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate ML-based predictions"""
        
        # Convert features to array for ML model
        feature_array = self._features_to_array(features)
        
        # Use existing prediction logic as baseline
        channel_info = enhanced_context.get('channel_info', {})
        avg_views = features.avg_views_last_30
        
        # Enhanced prediction calculations
        base_performance_score = self._calculate_base_performance_score(features)
        
        # Predict views with ML enhancement
        view_multiplier = self._calculate_view_multiplier(features)
        predicted_views = int(avg_views * view_multiplier)
        
        # Predict CTR
        ctr_adjustment = self._calculate_ctr_adjustment(features)
        predicted_ctr = max(1.0, features.avg_ctr_last_30 * ctr_adjustment)
        
        # Predict engagement
        engagement_adjustment = self._calculate_engagement_adjustment(features)
        predicted_engagement = max(1.0, features.avg_engagement_last_30 * engagement_adjustment)
        
        # Predict retention
        predicted_retention = min(100, 35 + base_performance_score * 0.5)
        
        # Calculate success probability
        success_probability = self._calculate_success_probability(
            predicted_views, predicted_ctr, predicted_engagement, features
        )
        
        return {
            'views': predicted_views,
            'ctr': round(predicted_ctr, 1),
            'engagement': round(predicted_engagement, 1),
            'retention': round(predicted_retention, 1),
            'success_probability': round(success_probability, 2),
            'performance_score': round(base_performance_score, 1)
        }

    def _calculate_base_performance_score(self, features: PredictionFeatures) -> float:
        """Calculate base performance score from features"""
        score = 50.0  # Start with average

        # Title optimization
        if 30 <= features.title_length <= 60:
            score += 10
        elif features.title_length > 80:
            score -= 5

        # Sentiment boost
        score += features.title_sentiment * 10

        # Keyword strength
        score += features.title_keyword_strength * 15

        # Topic trend boost
        score += features.topic_trend_score * 20

        # Channel momentum
        if features.subscriber_growth_rate > 0.1:
            score += 10
        elif features.subscriber_growth_rate < 0:
            score -= 10

        # Timing factors
        if features.days_since_last_upload <= 3:
            score += 5
        elif features.days_since_last_upload > 14:
            score -= 10

        # Audience match
        score += features.audience_match_score * 15

        # Competitive advantage
        score -= features.competitive_saturation * 10

        return max(0, min(100, score))

    def _calculate_view_multiplier(self, features: PredictionFeatures) -> float:
        """Calculate view prediction multiplier"""
        multiplier = 1.0

        # Title optimization impact
        if features.title_keyword_strength > 0.7:
            multiplier *= 1.3
        elif features.title_keyword_strength < 0.3:
            multiplier *= 0.8

        # Trend impact
        multiplier *= (1 + features.topic_trend_score)

        # Timing impact
        if 18 <= features.hour_of_day <= 21:  # Prime time
            multiplier *= 1.2
        elif 2 <= features.hour_of_day <= 6:  # Dead hours
            multiplier *= 0.7

        # Weekend boost
        if features.day_of_week in [5, 6]:  # Saturday, Sunday
            multiplier *= 1.1

        # Channel momentum
        if features.subscriber_growth_rate > 0.1:
            multiplier *= 1.4
        elif features.subscriber_growth_rate < -0.05:
            multiplier *= 0.6

        # Consistency bonus
        multiplier *= (0.8 + features.creator_consistency_score * 0.4)

        return max(0.3, min(3.0, multiplier))

    def _calculate_ctr_adjustment(self, features: PredictionFeatures) -> float:
        """Calculate CTR prediction adjustment"""
        adjustment = 1.0

        # Title length optimization
        if 40 <= features.title_length <= 60:
            adjustment *= 1.2
        elif features.title_length > 80:
            adjustment *= 0.8

        # Sentiment impact
        adjustment *= (1 + features.title_sentiment * 0.3)

        # Keyword strength
        adjustment *= (0.8 + features.title_keyword_strength * 0.4)

        # Competitive saturation penalty
        adjustment *= (1 - features.competitive_saturation * 0.3)

        return max(0.5, min(2.0, adjustment))

    def _calculate_engagement_adjustment(self, features: PredictionFeatures) -> float:
        """Calculate engagement prediction adjustment"""
        adjustment = 1.0

        # Audience match impact
        adjustment *= (0.7 + features.audience_match_score * 0.6)

        # Topic trend impact
        adjustment *= (1 + features.topic_trend_score * 0.4)

        # Channel size impact (smaller channels often have higher engagement)
        if features.channel_size < 10000:
            adjustment *= 1.2
        elif features.channel_size > 100000:
            adjustment *= 0.9

        # Consistency impact
        adjustment *= (0.8 + features.creator_consistency_score * 0.4)

        return max(0.5, min(2.5, adjustment))

    def _calculate_success_probability(
        self,
        predicted_views: int,
        predicted_ctr: float,
        predicted_engagement: float,
        features: PredictionFeatures
    ) -> float:
        """Calculate overall success probability"""

        # Compare to channel averages
        view_ratio = predicted_views / max(features.avg_views_last_30, 100)
        ctr_ratio = predicted_ctr / max(features.avg_ctr_last_30, 2.0)
        engagement_ratio = predicted_engagement / max(features.avg_engagement_last_30, 1.0)

        # Weight the ratios
        success_score = (
            view_ratio * 0.4 +
            ctr_ratio * 0.3 +
            engagement_ratio * 0.3
        )

        # Convert to probability (sigmoid-like function)
        probability = 1 / (1 + np.exp(-(success_score - 1) * 2))

        return max(0.05, min(0.95, probability))

    def _features_to_array(self, features: PredictionFeatures) -> np.ndarray:
        """Convert features to numpy array for ML models"""
        return np.array([
            features.title_length,
            features.title_sentiment,
            features.title_keyword_strength,
            features.description_length,
            features.topic_trend_score,
            features.competitive_saturation,
            np.log1p(features.channel_size),  # Log transform for better scaling
            np.log1p(features.avg_views_last_30),
            features.avg_ctr_last_30,
            features.avg_engagement_last_30,
            features.subscriber_growth_rate,
            features.hour_of_day,
            features.day_of_week,
            features.days_since_last_upload,
            features.seasonal_factor,
            features.audience_match_score,
            features.demographic_alignment,
            features.similar_content_performance,
            features.creator_consistency_score
        ]).reshape(1, -1)

    def _calculate_seasonal_factor(self, date: datetime) -> float:
        """Calculate seasonal factor for content performance"""
        month = date.month

        # Holiday seasons tend to have different performance
        if month in [11, 12]:  # November, December
            return 1.1  # Holiday boost
        elif month in [6, 7, 8]:  # Summer months
            return 0.95  # Slight decrease
        elif month in [1, 2]:  # January, February
            return 0.9  # Post-holiday dip
        else:
            return 1.0  # Normal

    async def _analyze_title_sentiment(self, title: str) -> float:
        """Analyze title sentiment (simplified implementation)"""
        positive_words = ['best', 'amazing', 'incredible', 'ultimate', 'perfect', 'awesome', 'fantastic']
        negative_words = ['worst', 'terrible', 'awful', 'bad', 'horrible', 'disappointing']

        title_lower = title.lower()
        positive_count = sum(1 for word in positive_words if word in title_lower)
        negative_count = sum(1 for word in negative_words if word in title_lower)

        return (positive_count - negative_count) / max(len(title.split()), 1)

    async def _calculate_keyword_strength(self, title: str, enhanced_context: Dict[str, Any]) -> float:
        """Calculate keyword strength based on niche and trends"""
        # Simplified implementation - in production, use actual keyword analysis
        niche_keywords = enhanced_context.get('niche_keywords', [])
        title_lower = title.lower()

        keyword_matches = sum(1 for keyword in niche_keywords if keyword.lower() in title_lower)
        return min(1.0, keyword_matches / max(len(niche_keywords), 1))

    async def _calculate_topic_trend_score(self, content_data: Dict[str, Any], enhanced_context: Dict[str, Any]) -> float:
        """Calculate how trending the topic is"""
        # Simplified implementation - in production, use trending analysis
        trending_topics = enhanced_context.get('trending_opportunities', {}).get('hot_topics', [])
        topic = content_data.get('topic', '').lower()

        for trending_topic in trending_topics:
            if trending_topic.lower() in topic:
                return 0.8

        return 0.3  # Default moderate trend score

    async def _calculate_competitive_saturation(self, content_data: Dict[str, Any], enhanced_context: Dict[str, Any]) -> float:
        """Calculate competitive saturation for the topic"""
        # Simplified implementation - in production, use competitive analysis
        competitive_data = enhanced_context.get('competitive_intelligence', {})
        saturated_topics = competitive_data.get('saturated_topics', [])
        topic = content_data.get('topic', '').lower()

        for saturated_topic in saturated_topics:
            if saturated_topic.lower() in topic:
                return 0.8

        return 0.3  # Default low saturation

    async def _calculate_audience_match_score(self, content_data: Dict[str, Any], audience_insights: Dict[str, Any]) -> float:
        """Calculate how well content matches audience preferences"""
        demographics = audience_insights.get('demographics', {})
        content_preferences = demographics.get('content_preferences', '')
        topic = content_data.get('topic', '').lower()

        if content_preferences.lower() in topic or topic in content_preferences.lower():
            return 0.9

        return 0.6  # Default moderate match

    async def _calculate_demographic_alignment(self, content_data: Dict[str, Any], audience_insights: Dict[str, Any]) -> float:
        """Calculate demographic alignment score"""
        demographics = audience_insights.get('demographics', {})
        age_group = demographics.get('primary_age_group', 'General audience')

        # Simplified scoring based on age group
        if 'young' in age_group.lower() or 'teen' in age_group.lower():
            return 0.8 if 'trend' in content_data.get('topic', '').lower() else 0.6
        elif 'adult' in age_group.lower():
            return 0.8 if 'professional' in content_data.get('topic', '').lower() else 0.7

        return 0.7  # Default alignment

    async def _get_similar_content_performance(self, content_data: Dict[str, Any], enhanced_context: Dict[str, Any]) -> float:
        """Get performance of similar content"""
        # Simplified implementation - in production, analyze similar videos
        performance_data = enhanced_context.get('performance_data', {})
        avg_performance = performance_data.get('avg_views_30d', 1000)

        # Return normalized performance score
        return min(1.0, avg_performance / 10000)  # Normalize to 0-1 scale

    async def _calculate_creator_consistency_score(self, enhanced_context: Dict[str, Any]) -> float:
        """Calculate creator consistency score"""
        performance_data = enhanced_context.get('performance_data', {})
        upload_consistency = performance_data.get('upload_consistency', 0.7)
        quality_consistency = performance_data.get('quality_consistency', 0.8)

        return (upload_consistency + quality_consistency) / 2

    async def _generate_ai_insights(
        self,
        content_data: Dict[str, Any],
        enhanced_context: Dict[str, Any],
        ml_predictions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate AI-enhanced insights about the prediction"""

        insights = {
            'performance_outlook': 'positive' if ml_predictions['success_probability'] > 0.6 else 'moderate',
            'key_strengths': [],
            'improvement_areas': [],
            'market_position': 'competitive'
        }

        # Analyze strengths
        if ml_predictions['ctr'] > enhanced_context.get('performance_data', {}).get('avg_ctr_30d', 4.0):
            insights['key_strengths'].append('Strong CTR potential')

        if ml_predictions['engagement'] > enhanced_context.get('performance_data', {}).get('avg_engagement_30d', 3.0):
            insights['key_strengths'].append('High engagement potential')

        # Analyze improvement areas
        if ml_predictions['views'] < enhanced_context.get('performance_data', {}).get('avg_views_30d', 1000):
            insights['improvement_areas'].append('View optimization needed')

        return insights

    async def _generate_optimization_suggestions(
        self,
        features: PredictionFeatures,
        ml_predictions: Dict[str, Any],
        enhanced_context: Dict[str, Any]
    ) -> List[str]:
        """Generate specific optimization suggestions"""

        suggestions = []

        # Title optimization
        if features.title_length > 70:
            suggestions.append("Consider shortening title to 40-60 characters for better CTR")
        elif features.title_length < 30:
            suggestions.append("Consider expanding title to include more descriptive keywords")

        # Timing optimization
        if not (18 <= features.hour_of_day <= 21):
            suggestions.append("Consider posting between 6-9 PM for optimal audience engagement")

        # Keyword optimization
        if features.title_keyword_strength < 0.5:
            suggestions.append("Include more niche-specific keywords in your title")

        # Competitive positioning
        if features.competitive_saturation > 0.7:
            suggestions.append("Topic is highly competitive - consider a unique angle or sub-niche")

        # Audience alignment
        if features.audience_match_score < 0.6:
            suggestions.append("Align content more closely with your audience's interests")

        # Upload frequency
        if features.days_since_last_upload > 10:
            suggestions.append("Maintain consistent upload schedule for better algorithm performance")

        return suggestions[:5]  # Limit to top 5 suggestions

    async def _calculate_optimal_timing(
        self,
        user_id: str,
        enhanced_context: Dict[str, Any],
        features: PredictionFeatures
    ) -> Dict[str, Any]:
        """Calculate optimal timing recommendations"""

        audience_data = enhanced_context.get('audience_behavior', {})

        return {
            'optimal_hour': audience_data.get('peak_hours', [19, 20, 21]),
            'optimal_days': audience_data.get('peak_days', ['Saturday', 'Sunday']),
            'current_timing_score': self._score_current_timing(features),
            'timing_improvement_potential': self._calculate_timing_improvement(features, audience_data),
            'next_optimal_slot': self._get_next_optimal_slot(audience_data)
        }

    def _score_current_timing(self, features: PredictionFeatures) -> float:
        """Score the current timing choice"""
        score = 0.5  # Base score

        # Hour scoring
        if 18 <= features.hour_of_day <= 21:
            score += 0.3
        elif 12 <= features.hour_of_day <= 14:
            score += 0.2
        elif 2 <= features.hour_of_day <= 6:
            score -= 0.3

        # Day scoring
        if features.day_of_week in [5, 6]:  # Weekend
            score += 0.2
        elif features.day_of_week in [1, 2, 3]:  # Tue, Wed, Thu
            score += 0.1

        return max(0, min(1, score))

    def _calculate_timing_improvement(self, features: PredictionFeatures, audience_data: Dict[str, Any]) -> float:
        """Calculate potential improvement from better timing"""
        current_score = self._score_current_timing(features)
        optimal_score = 1.0  # Perfect timing

        return optimal_score - current_score

    def _get_next_optimal_slot(self, audience_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get next optimal posting slot"""
        now = datetime.now()
        peak_hours = audience_data.get('peak_hours', [19, 20, 21])

        # Find next peak hour
        next_peak = None
        for hour in peak_hours:
            next_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            if next_time > now:
                next_peak = next_time
                break

        if not next_peak:
            # Next day
            next_peak = (now + timedelta(days=1)).replace(hour=peak_hours[0], minute=0, second=0, microsecond=0)

        return {
            'datetime': next_peak.isoformat(),
            'hours_from_now': (next_peak - now).total_seconds() / 3600,
            'day_name': next_peak.strftime('%A'),
            'time_display': next_peak.strftime('%I:%M %p')
        }

    async def _assess_risk_factors(
        self,
        features: PredictionFeatures,
        enhanced_context: Dict[str, Any],
        ml_predictions: Dict[str, Any]
    ) -> List[str]:
        """Assess potential risk factors for content performance"""

        risks = []

        # Competition risk
        if features.competitive_saturation > 0.7:
            risks.append("High competition in this topic area")

        # Timing risk
        if features.days_since_last_upload > 14:
            risks.append("Long gap since last upload may affect algorithm performance")

        # Audience mismatch risk
        if features.audience_match_score < 0.5:
            risks.append("Content may not align well with your audience's interests")

        # Channel momentum risk
        if features.subscriber_growth_rate < 0:
            risks.append("Declining subscriber growth may impact reach")

        # Seasonal risk
        if features.seasonal_factor < 0.9:
            risks.append("Seasonal factors may negatively impact performance")

        # Performance prediction risk
        if ml_predictions['success_probability'] < 0.4:
            risks.append("Low predicted success probability based on current factors")

        return risks[:4]  # Limit to top 4 risks

    def _calculate_prediction_confidence(
        self,
        features: PredictionFeatures,
        enhanced_context: Dict[str, Any],
        ml_predictions: Dict[str, Any]
    ) -> float:
        """Calculate confidence level in the prediction"""

        confidence = 0.7  # Base confidence

        # Data quality factors
        channel_data_quality = enhanced_context.get('data_quality', 'medium')
        if channel_data_quality == 'high':
            confidence += 0.2
        elif channel_data_quality == 'low':
            confidence -= 0.2

        # Historical data availability
        if features.similar_content_performance > 0.5:
            confidence += 0.1

        # Channel consistency
        if features.creator_consistency_score > 0.8:
            confidence += 0.1
        elif features.creator_consistency_score < 0.5:
            confidence -= 0.1

        # Prediction stability
        if 0.3 <= ml_predictions['success_probability'] <= 0.8:
            confidence += 0.1  # Moderate predictions are more reliable

        return max(0.3, min(0.95, confidence))

    def _get_fallback_prediction(self, content_data: Dict[str, Any]) -> ContentPrediction:
        """Generate fallback prediction when main prediction fails"""

        return ContentPrediction(
            predicted_views=1000,
            predicted_ctr=4.0,
            predicted_engagement_rate=3.0,
            predicted_retention=45.0,
            success_probability=0.5,
            performance_score=50.0,
            confidence_level=0.3,
            optimization_suggestions=["Unable to generate specific suggestions - please try again"],
            risk_factors=["Prediction system temporarily unavailable"],
            timing_recommendations={
                'optimal_hour': [19, 20, 21],
                'optimal_days': ['Saturday', 'Sunday'],
                'current_timing_score': 0.5
            },
            predicted_metrics={
                'views': 1000,
                'ctr': 4.0,
                'engagement': 3.0,
                'retention': 45.0
            }
        )

# Global instance
_prediction_engine = None

def get_prediction_engine() -> AdvancedPredictionEngine:
    """Get global prediction engine instance"""
    global _prediction_engine
    if _prediction_engine is None:
        _prediction_engine = AdvancedPredictionEngine()
    return _prediction_engine
