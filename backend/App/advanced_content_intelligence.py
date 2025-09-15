"""
Advanced Content Intelligence Engine
Provides sophisticated thumbnail and hook optimization for maximum engagement
"""

import asyncio
import logging
import re
import base64
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np

from backend.App.enhanced_user_context import EnhancedUserContextManager
# AI services integration would go here in production

logger = logging.getLogger(__name__)

class ThumbnailElement(Enum):
    FACE = "face"
    TEXT = "text"
    BACKGROUND = "background"
    OBJECTS = "objects"
    COLORS = "colors"
    CONTRAST = "contrast"

class HookType(Enum):
    QUESTION = "question"
    STATEMENT = "statement"
    STORY = "story"
    STATISTIC = "statistic"
    CONTROVERSY = "controversy"
    PROMISE = "promise"

@dataclass
class ThumbnailAnalysis:
    """Comprehensive thumbnail analysis results"""
    overall_score: float  # 0-100
    effectiveness_rating: str  # poor, fair, good, excellent
    click_probability: float  # 0-1
    
    # Visual elements analysis
    color_psychology_score: float
    text_readability_score: float
    facial_expression_score: float
    composition_score: float
    contrast_score: float
    
    # Detailed insights
    strengths: List[str]
    weaknesses: List[str]
    optimization_suggestions: List[str]
    
    # A/B testing recommendations
    ab_test_variations: List[Dict[str, Any]]
    
    # Competitive analysis
    vs_niche_average: float  # How it compares to niche average
    improvement_potential: float

@dataclass
class HookAnalysis:
    """Video hook performance analysis"""
    hook_score: float  # 0-100
    engagement_prediction: float  # 0-1
    retention_prediction: float  # 0-1
    
    hook_type: HookType
    effectiveness_factors: Dict[str, float]
    
    # Optimization suggestions
    improvements: List[str]
    alternative_hooks: List[str]
    
    # Timing analysis
    optimal_length: float  # seconds
    pacing_score: float

@dataclass
class ContentStructureAnalysis:
    """Analysis of content structure for retention"""
    retention_prediction: float  # 0-1
    drop_off_points: List[Dict[str, Any]]
    pacing_score: float
    engagement_curve: List[float]
    
    # Structure recommendations
    structure_improvements: List[str]
    optimal_segments: List[Dict[str, Any]]
    
    # Content flow analysis
    flow_score: float
    transition_quality: float

class AdvancedContentIntelligence:
    """Advanced content intelligence for thumbnails, hooks, and retention optimization"""
    
    def __init__(self):
        self.context_service = EnhancedUserContextManager()
        
        # Thumbnail analysis weights
        self.thumbnail_weights = {
            'color_psychology': 0.20,
            'text_readability': 0.25,
            'facial_expression': 0.20,
            'composition': 0.15,
            'contrast': 0.20
        }
        
        # Hook effectiveness patterns
        self.hook_patterns = {
            HookType.QUESTION: {
                'engagement_multiplier': 1.3,
                'optimal_length': 8.0,
                'retention_boost': 0.15
            },
            HookType.STATEMENT: {
                'engagement_multiplier': 1.1,
                'optimal_length': 6.0,
                'retention_boost': 0.10
            },
            HookType.STORY: {
                'engagement_multiplier': 1.4,
                'optimal_length': 12.0,
                'retention_boost': 0.20
            },
            HookType.STATISTIC: {
                'engagement_multiplier': 1.2,
                'optimal_length': 7.0,
                'retention_boost': 0.12
            },
            HookType.CONTROVERSY: {
                'engagement_multiplier': 1.5,
                'optimal_length': 10.0,
                'retention_boost': 0.18
            },
            HookType.PROMISE: {
                'engagement_multiplier': 1.35,
                'optimal_length': 9.0,
                'retention_boost': 0.16
            }
        }
        
        logger.info("Advanced Content Intelligence Engine initialized")
    
    async def analyze_thumbnail(
        self, 
        user_id: str, 
        thumbnail_data: Dict[str, Any],
        niche_context: Optional[str] = None
    ) -> ThumbnailAnalysis:
        """
        Comprehensive thumbnail analysis with optimization recommendations
        
        Args:
            user_id: User identifier
            thumbnail_data: Thumbnail information (URL, description, etc.)
            niche_context: Content niche for targeted analysis
        
        Returns:
            Detailed thumbnail analysis with optimization suggestions
        """
        try:
            logger.info(f"🎨 Analyzing thumbnail for user {user_id}")
            
            # Get enhanced user context
            enhanced_context = await self.context_service.get_enhanced_context(user_id)
            
            # Analyze visual elements
            visual_analysis = await self._analyze_visual_elements(thumbnail_data, enhanced_context)
            
            # Calculate effectiveness scores
            scores = await self._calculate_thumbnail_scores(visual_analysis, enhanced_context, niche_context)
            
            # Generate optimization suggestions
            suggestions = await self._generate_thumbnail_optimizations(scores, visual_analysis, enhanced_context)
            
            # Create A/B testing recommendations
            ab_variations = await self._generate_ab_test_variations(thumbnail_data, scores, enhanced_context)
            
            # Compare to niche benchmarks
            niche_comparison = await self._compare_to_niche_benchmarks(scores, niche_context, enhanced_context)
            
            # Calculate overall score
            overall_score = self._calculate_overall_thumbnail_score(scores)
            
            analysis = ThumbnailAnalysis(
                overall_score=overall_score,
                effectiveness_rating=self._get_effectiveness_rating(overall_score),
                click_probability=self._predict_click_probability(overall_score, enhanced_context),
                color_psychology_score=scores['color_psychology'],
                text_readability_score=scores['text_readability'],
                facial_expression_score=scores['facial_expression'],
                composition_score=scores['composition'],
                contrast_score=scores['contrast'],
                strengths=suggestions['strengths'],
                weaknesses=suggestions['weaknesses'],
                optimization_suggestions=suggestions['optimizations'],
                ab_test_variations=ab_variations,
                vs_niche_average=niche_comparison['vs_average'],
                improvement_potential=niche_comparison['improvement_potential']
            )
            
            logger.info(f"✅ Thumbnail analysis completed: Score {overall_score:.1f}/100")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing thumbnail: {e}")
            # Return default analysis
            return ThumbnailAnalysis(
                overall_score=50.0,
                effectiveness_rating="fair",
                click_probability=0.5,
                color_psychology_score=50.0,
                text_readability_score=50.0,
                facial_expression_score=50.0,
                composition_score=50.0,
                contrast_score=50.0,
                strengths=["Analysis unavailable"],
                weaknesses=["Unable to analyze thumbnail"],
                optimization_suggestions=["Please try again"],
                ab_test_variations=[],
                vs_niche_average=0.0,
                improvement_potential=0.0
            )
    
    async def analyze_hook(
        self, 
        user_id: str, 
        hook_text: str, 
        video_context: Optional[Dict[str, Any]] = None
    ) -> HookAnalysis:
        """
        Analyze video hook effectiveness and provide optimization recommendations
        
        Args:
            user_id: User identifier
            hook_text: The opening hook text/script
            video_context: Additional video context (title, topic, etc.)
        
        Returns:
            Detailed hook analysis with improvement suggestions
        """
        try:
            logger.info(f"🎯 Analyzing hook for user {user_id}")
            
            # Get enhanced user context
            enhanced_context = await self.context_service.get_enhanced_context(user_id)
            
            # Identify hook type
            hook_type = self._identify_hook_type(hook_text)
            
            # Analyze hook effectiveness factors
            effectiveness_factors = await self._analyze_hook_factors(hook_text, hook_type, enhanced_context)
            
            # Calculate hook score
            hook_score = self._calculate_hook_score(effectiveness_factors, hook_type)
            
            # Predict engagement and retention
            engagement_prediction = self._predict_hook_engagement(hook_score, hook_type, enhanced_context)
            retention_prediction = self._predict_hook_retention(hook_score, hook_type, enhanced_context)
            
            # Generate improvements
            improvements = await self._generate_hook_improvements(hook_text, hook_type, effectiveness_factors, enhanced_context)
            
            # Create alternative hooks
            alternatives = await self._generate_alternative_hooks(hook_text, hook_type, video_context, enhanced_context)
            
            # Analyze timing and pacing
            timing_analysis = self._analyze_hook_timing(hook_text, hook_type)
            
            analysis = HookAnalysis(
                hook_score=hook_score,
                engagement_prediction=engagement_prediction,
                retention_prediction=retention_prediction,
                hook_type=hook_type,
                effectiveness_factors=effectiveness_factors,
                improvements=improvements,
                alternative_hooks=alternatives,
                optimal_length=timing_analysis['optimal_length'],
                pacing_score=timing_analysis['pacing_score']
            )
            
            logger.info(f"✅ Hook analysis completed: Score {hook_score:.1f}/100")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing hook: {e}")
            # Return default analysis
            return HookAnalysis(
                hook_score=50.0,
                engagement_prediction=0.5,
                retention_prediction=0.5,
                hook_type=HookType.STATEMENT,
                effectiveness_factors={},
                improvements=["Analysis unavailable"],
                alternative_hooks=["Please try again"],
                optimal_length=8.0,
                pacing_score=50.0
            )

    async def analyze_content_structure(
        self,
        user_id: str,
        content_script: str,
        video_length: Optional[float] = None
    ) -> ContentStructureAnalysis:
        """
        Analyze content structure for retention optimization

        Args:
            user_id: User identifier
            content_script: Video script or content outline
            video_length: Expected video length in minutes

        Returns:
            Content structure analysis with retention optimization suggestions
        """
        try:
            logger.info(f"📊 Analyzing content structure for user {user_id}")

            # Get enhanced user context
            enhanced_context = await self.context_service.get_enhanced_context(user_id)

            # Analyze content segments
            segments = self._segment_content(content_script)

            # Predict retention curve
            retention_curve = self._predict_retention_curve(segments, enhanced_context)

            # Identify potential drop-off points
            drop_off_points = self._identify_drop_off_points(retention_curve, segments)

            # Calculate pacing score
            pacing_score = self._calculate_pacing_score(segments, video_length)

            # Analyze content flow
            flow_analysis = self._analyze_content_flow(segments)

            # Generate structure improvements
            improvements = await self._generate_structure_improvements(
                segments, drop_off_points, pacing_score, enhanced_context
            )

            # Create optimal segment recommendations
            optimal_segments = self._generate_optimal_segments(segments, retention_curve)

            # Calculate overall retention prediction
            retention_prediction = np.mean(retention_curve)

            analysis = ContentStructureAnalysis(
                retention_prediction=retention_prediction,
                drop_off_points=drop_off_points,
                pacing_score=pacing_score,
                engagement_curve=retention_curve,
                structure_improvements=improvements,
                optimal_segments=optimal_segments,
                flow_score=flow_analysis['flow_score'],
                transition_quality=flow_analysis['transition_quality']
            )

            logger.info(f"✅ Content structure analysis completed: Retention {retention_prediction:.1%}")
            return analysis

        except Exception as e:
            logger.error(f"Error analyzing content structure: {e}")
            # Return default analysis
            return ContentStructureAnalysis(
                retention_prediction=0.5,
                drop_off_points=[],
                pacing_score=50.0,
                engagement_curve=[0.5],
                structure_improvements=["Analysis unavailable"],
                optimal_segments=[],
                flow_score=50.0,
                transition_quality=50.0
            )

    # Thumbnail Analysis Helper Methods
    async def _analyze_visual_elements(self, thumbnail_data: Dict[str, Any], enhanced_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze visual elements of thumbnail"""

        # Simulate visual analysis (in production, would use computer vision)
        visual_elements = {
            'has_face': thumbnail_data.get('has_face', True),
            'text_elements': thumbnail_data.get('text_elements', []),
            'color_scheme': thumbnail_data.get('colors', ['blue', 'white']),
            'background_type': thumbnail_data.get('background', 'simple'),
            'objects': thumbnail_data.get('objects', []),
            'composition': thumbnail_data.get('composition', 'centered')
        }

        return visual_elements

    async def _calculate_thumbnail_scores(
        self,
        visual_analysis: Dict[str, Any],
        enhanced_context: Dict[str, Any],
        niche_context: Optional[str]
    ) -> Dict[str, float]:
        """Calculate individual thumbnail effectiveness scores"""

        scores = {}

        # Color psychology score
        colors = visual_analysis.get('color_scheme', [])
        scores['color_psychology'] = self._score_color_psychology(colors, niche_context)

        # Text readability score
        text_elements = visual_analysis.get('text_elements', [])
        scores['text_readability'] = self._score_text_readability(text_elements)

        # Facial expression score
        has_face = visual_analysis.get('has_face', False)
        scores['facial_expression'] = self._score_facial_expression(has_face, enhanced_context)

        # Composition score
        composition = visual_analysis.get('composition', 'centered')
        scores['composition'] = self._score_composition(composition, visual_analysis)

        # Contrast score
        scores['contrast'] = self._score_contrast(visual_analysis)

        return scores

    def _score_color_psychology(self, colors: List[str], niche_context: Optional[str]) -> float:
        """Score color psychology effectiveness"""

        # Color effectiveness by niche
        niche_color_preferences = {
            'tech': {'blue': 90, 'green': 80, 'red': 70, 'orange': 85},
            'lifestyle': {'pink': 90, 'purple': 85, 'yellow': 80, 'blue': 75},
            'business': {'blue': 95, 'gray': 85, 'green': 80, 'red': 75},
            'gaming': {'red': 95, 'orange': 90, 'purple': 85, 'green': 80},
            'education': {'blue': 90, 'green': 85, 'orange': 80, 'purple': 75}
        }

        if not colors:
            return 50.0

        niche = niche_context or 'general'
        preferences = niche_color_preferences.get(niche, {'blue': 80, 'red': 75, 'green': 70})

        # Calculate average color effectiveness
        color_scores = [preferences.get(color.lower(), 60) for color in colors]
        base_score = np.mean(color_scores)

        # Bonus for color contrast
        if len(set(colors)) > 1:
            base_score += 10

        return min(100, base_score)

    def _score_text_readability(self, text_elements: List[str]) -> float:
        """Score text readability and effectiveness"""

        if not text_elements:
            return 40.0  # No text is not ideal

        total_score = 0
        for text in text_elements:
            # Length scoring
            length_score = 100 if len(text) <= 30 else max(50, 100 - (len(text) - 30) * 2)

            # Word count scoring
            word_count = len(text.split())
            word_score = 100 if word_count <= 5 else max(60, 100 - (word_count - 5) * 8)

            # Emotional words bonus
            emotional_words = ['amazing', 'shocking', 'secret', 'ultimate', 'instant', 'proven']
            emotion_bonus = sum(5 for word in emotional_words if word.lower() in text.lower())

            text_score = (length_score + word_score) / 2 + emotion_bonus
            total_score += min(100, text_score)

        return total_score / len(text_elements)

    def _score_facial_expression(self, has_face: bool, enhanced_context: Dict[str, Any]) -> float:
        """Score facial expression effectiveness"""

        if not has_face:
            return 60.0  # Not having a face isn't necessarily bad

        # Base score for having a face
        base_score = 80.0

        # Bonus based on niche (some niches benefit more from faces)
        niche = enhanced_context.get('channel_info', {}).get('niche', '').lower()
        face_bonus_niches = ['lifestyle', 'vlog', 'personal', 'tutorial']

        if any(bonus_niche in niche for bonus_niche in face_bonus_niches):
            base_score += 15

        return min(100, base_score)

    def _score_composition(self, composition: str, visual_analysis: Dict[str, Any]) -> float:
        """Score thumbnail composition"""

        composition_scores = {
            'rule_of_thirds': 95,
            'centered': 80,
            'left_aligned': 75,
            'right_aligned': 75,
            'diagonal': 85,
            'symmetrical': 80
        }

        base_score = composition_scores.get(composition, 70)

        # Bonus for multiple visual elements
        elements_count = len(visual_analysis.get('objects', [])) + len(visual_analysis.get('text_elements', []))
        if 2 <= elements_count <= 4:
            base_score += 10
        elif elements_count > 4:
            base_score -= 15  # Too cluttered

        return min(100, max(0, base_score))

    def _score_contrast(self, visual_analysis: Dict[str, Any]) -> float:
        """Score visual contrast effectiveness"""

        colors = visual_analysis.get('color_scheme', [])

        if len(colors) < 2:
            return 50.0  # Low contrast

        # High contrast color combinations
        high_contrast_pairs = [
            ('black', 'white'), ('blue', 'yellow'), ('red', 'white'),
            ('green', 'white'), ('purple', 'yellow'), ('orange', 'blue')
        ]

        base_score = 70.0

        # Check for high contrast combinations
        for color1 in colors:
            for color2 in colors:
                if color1 != color2:
                    for pair in high_contrast_pairs:
                        if (color1.lower() in pair and color2.lower() in pair):
                            base_score = 95.0
                            break

        return base_score

    # Hook Analysis Helper Methods
    def _identify_hook_type(self, hook_text: str) -> HookType:
        """Identify the type of hook being used"""

        hook_text_lower = hook_text.lower()

        # Question patterns
        question_patterns = ['?', 'how', 'what', 'why', 'when', 'where', 'which', 'who']
        if any(pattern in hook_text_lower for pattern in question_patterns):
            return HookType.QUESTION

        # Story patterns
        story_patterns = ['story', 'happened', 'experience', 'journey', 'time when', 'remember when']
        if any(pattern in hook_text_lower for pattern in story_patterns):
            return HookType.STORY

        # Statistic patterns
        stat_patterns = ['%', 'percent', 'study', 'research', 'data', 'statistics', 'numbers']
        if any(pattern in hook_text_lower for pattern in stat_patterns):
            return HookType.STATISTIC

        # Controversy patterns
        controversy_patterns = ['wrong', 'lie', 'myth', 'truth', 'secret', 'hidden', 'exposed']
        if any(pattern in hook_text_lower for pattern in controversy_patterns):
            return HookType.CONTROVERSY

        # Promise patterns
        promise_patterns = ['will', 'going to', 'promise', 'guarantee', 'show you', 'teach you']
        if any(pattern in hook_text_lower for pattern in promise_patterns):
            return HookType.PROMISE

        # Default to statement
        return HookType.STATEMENT

    async def _analyze_hook_factors(
        self,
        hook_text: str,
        hook_type: HookType,
        enhanced_context: Dict[str, Any]
    ) -> Dict[str, float]:
        """Analyze various effectiveness factors of the hook"""

        factors = {}

        # Length factor
        word_count = len(hook_text.split())
        optimal_length = self.hook_patterns[hook_type]['optimal_length']
        length_deviation = abs(word_count - optimal_length) / optimal_length
        factors['length_optimization'] = max(0, 100 - (length_deviation * 50))

        # Emotional impact
        factors['emotional_impact'] = self._score_emotional_impact(hook_text)

        # Curiosity factor
        factors['curiosity_factor'] = self._score_curiosity_factor(hook_text, hook_type)

        # Clarity score
        factors['clarity'] = self._score_clarity(hook_text)

        # Urgency factor
        factors['urgency'] = self._score_urgency(hook_text)

        # Relevance to audience
        factors['audience_relevance'] = self._score_audience_relevance(hook_text, enhanced_context)

        return factors

    def _score_emotional_impact(self, hook_text: str) -> float:
        """Score the emotional impact of the hook"""

        # High-impact emotional words
        high_impact_words = [
            'amazing', 'shocking', 'incredible', 'unbelievable', 'stunning',
            'devastating', 'heartbreaking', 'inspiring', 'mind-blowing', 'life-changing'
        ]

        # Medium-impact emotional words
        medium_impact_words = [
            'great', 'awesome', 'fantastic', 'wonderful', 'terrible',
            'horrible', 'exciting', 'interesting', 'surprising', 'impressive'
        ]

        hook_lower = hook_text.lower()

        high_count = sum(1 for word in high_impact_words if word in hook_lower)
        medium_count = sum(1 for word in medium_impact_words if word in hook_lower)

        # Calculate score
        score = (high_count * 25) + (medium_count * 15)

        # Bonus for emotional punctuation
        if '!' in hook_text:
            score += 10

        return min(100, max(20, score))

    def _score_curiosity_factor(self, hook_text: str, hook_type: HookType) -> float:
        """Score how much curiosity the hook generates"""

        curiosity_words = [
            'secret', 'hidden', 'revealed', 'truth', 'mystery', 'unknown',
            'discover', 'find out', 'learn', 'uncover', 'expose', 'behind'
        ]

        hook_lower = hook_text.lower()
        curiosity_count = sum(1 for word in curiosity_words if word in hook_lower)

        base_score = curiosity_count * 20

        # Hook type bonuses
        if hook_type == HookType.QUESTION:
            base_score += 25
        elif hook_type == HookType.CONTROVERSY:
            base_score += 30
        elif hook_type == HookType.STORY:
            base_score += 20

        # Incomplete information bonus (creates curiosity gap)
        incomplete_patterns = ['but', 'however', 'until', 'before', 'after']
        if any(pattern in hook_lower for pattern in incomplete_patterns):
            base_score += 15

        return min(100, max(30, base_score))

    def _score_clarity(self, hook_text: str) -> float:
        """Score how clear and understandable the hook is"""

        # Penalize overly complex sentences
        word_count = len(hook_text.split())
        sentence_count = len([s for s in hook_text.split('.') if s.strip()])

        if sentence_count == 0:
            sentence_count = 1

        avg_words_per_sentence = word_count / sentence_count

        # Optimal range: 8-15 words per sentence
        if 8 <= avg_words_per_sentence <= 15:
            clarity_score = 100
        elif avg_words_per_sentence < 8:
            clarity_score = 80 + (avg_words_per_sentence * 2.5)
        else:
            clarity_score = max(50, 100 - ((avg_words_per_sentence - 15) * 3))

        # Penalize jargon and complex words
        complex_words = ['subsequently', 'furthermore', 'nevertheless', 'consequently']
        jargon_penalty = sum(5 for word in complex_words if word.lower() in hook_text.lower())

        return max(30, clarity_score - jargon_penalty)

    def _score_urgency(self, hook_text: str) -> float:
        """Score the urgency factor of the hook"""

        urgency_words = [
            'now', 'today', 'immediately', 'urgent', 'quickly', 'fast',
            'instant', 'right now', 'this moment', 'before', 'deadline'
        ]

        time_sensitive_words = [
            'limited', 'ending', 'expires', 'last chance', 'final',
            'closing', 'disappearing', 'running out'
        ]

        hook_lower = hook_text.lower()

        urgency_count = sum(1 for word in urgency_words if word in hook_lower)
        time_count = sum(1 for word in time_sensitive_words if word in hook_lower)

        score = (urgency_count * 20) + (time_count * 25)

        return min(100, max(0, score))

    def _score_audience_relevance(self, hook_text: str, enhanced_context: Dict[str, Any]) -> float:
        """Score how relevant the hook is to the user's audience"""

        # Get audience insights
        audience_data = enhanced_context.get('audience_insights', {})
        demographics = audience_data.get('demographics', {})
        interests = audience_data.get('interests', [])

        base_score = 70.0  # Default relevance

        # Check for audience-specific language
        if demographics.get('age_group') == '18-24':
            young_language = ['guys', 'dude', 'literally', 'actually', 'like']
            if any(word in hook_text.lower() for word in young_language):
                base_score += 15

        # Check for interest alignment
        hook_lower = hook_text.lower()
        interest_matches = sum(1 for interest in interests if interest.lower() in hook_lower)
        base_score += interest_matches * 10

        return min(100, base_score)

    def _calculate_hook_score(self, effectiveness_factors: Dict[str, float], hook_type: HookType) -> float:
        """Calculate overall hook effectiveness score"""

        # Weight factors by importance
        weights = {
            'emotional_impact': 0.25,
            'curiosity_factor': 0.25,
            'clarity': 0.20,
            'audience_relevance': 0.15,
            'length_optimization': 0.10,
            'urgency': 0.05
        }

        weighted_score = sum(
            effectiveness_factors.get(factor, 50) * weight
            for factor, weight in weights.items()
        )

        # Hook type multiplier
        type_multiplier = self.hook_patterns[hook_type]['engagement_multiplier']
        final_score = weighted_score * (type_multiplier / 1.2)  # Normalize around 1.2

        return min(100, max(0, final_score))

    # Additional helper methods for comprehensive analysis
    def _calculate_overall_thumbnail_score(self, scores: Dict[str, float]) -> float:
        """Calculate weighted overall thumbnail score"""
        return sum(scores[factor] * weight for factor, weight in self.thumbnail_weights.items())

    def _get_effectiveness_rating(self, score: float) -> str:
        """Convert score to effectiveness rating"""
        if score >= 85:
            return "excellent"
        elif score >= 70:
            return "good"
        elif score >= 50:
            return "fair"
        else:
            return "poor"

    def _predict_click_probability(self, score: float, enhanced_context: Dict[str, Any]) -> float:
        """Predict click-through probability based on score and context"""
        base_probability = score / 100

        # Adjust based on user's historical CTR
        performance_data = enhanced_context.get('performance_data', {})
        avg_ctr = performance_data.get('avg_ctr_30d', 4.0) / 100

        # Blend prediction with historical performance
        adjusted_probability = (base_probability * 0.7) + (avg_ctr * 0.3)

        return min(1.0, max(0.0, adjusted_probability))

    async def _generate_thumbnail_optimizations(
        self,
        scores: Dict[str, float],
        visual_analysis: Dict[str, Any],
        enhanced_context: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Generate specific optimization suggestions"""

        suggestions = {
            'strengths': [],
            'weaknesses': [],
            'optimizations': []
        }

        # Identify strengths
        for factor, score in scores.items():
            if score >= 80:
                suggestions['strengths'].append(f"Strong {factor.replace('_', ' ')}")

        # Identify weaknesses and optimizations
        if scores['color_psychology'] < 70:
            suggestions['weaknesses'].append("Color scheme could be more engaging")
            suggestions['optimizations'].append("Try high-contrast color combinations like blue/yellow or red/white")

        if scores['text_readability'] < 70:
            suggestions['weaknesses'].append("Text may be hard to read")
            suggestions['optimizations'].append("Use larger, bolder fonts with better contrast")

        if scores['facial_expression'] < 70:
            suggestions['weaknesses'].append("Facial expression could be more engaging")
            suggestions['optimizations'].append("Use expressive faces showing emotion (surprise, excitement)")

        if scores['composition'] < 70:
            suggestions['weaknesses'].append("Composition could be improved")
            suggestions['optimizations'].append("Apply rule of thirds or create better visual balance")

        if scores['contrast'] < 70:
            suggestions['weaknesses'].append("Low visual contrast")
            suggestions['optimizations'].append("Increase contrast between foreground and background elements")

        return suggestions

    async def _generate_ab_test_variations(
        self,
        thumbnail_data: Dict[str, Any],
        scores: Dict[str, float],
        enhanced_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate A/B testing variations"""

        variations = []

        # Color variation
        if scores['color_psychology'] < 80:
            variations.append({
                'type': 'color_scheme',
                'description': 'Test high-contrast color combination',
                'suggestion': 'Try blue background with yellow text',
                'expected_improvement': '15-25%'
            })

        # Text variation
        if scores['text_readability'] < 80:
            variations.append({
                'type': 'text_style',
                'description': 'Test different text styling',
                'suggestion': 'Use larger, bolder font with outline',
                'expected_improvement': '10-20%'
            })

        # Composition variation
        variations.append({
            'type': 'composition',
            'description': 'Test different layout',
            'suggestion': 'Move main subject to follow rule of thirds',
            'expected_improvement': '8-15%'
        })

        return variations

    async def _compare_to_niche_benchmarks(
        self,
        scores: Dict[str, float],
        niche_context: Optional[str],
        enhanced_context: Dict[str, Any]
    ) -> Dict[str, float]:
        """Compare thumbnail to niche benchmarks"""

        # Simulated niche benchmarks (in production, would use real data)
        niche_benchmarks = {
            'tech': 75.0,
            'lifestyle': 80.0,
            'gaming': 85.0,
            'education': 70.0,
            'business': 72.0
        }

        overall_score = self._calculate_overall_thumbnail_score(scores)
        niche = niche_context or 'general'
        benchmark = niche_benchmarks.get(niche, 75.0)

        vs_average = overall_score - benchmark
        improvement_potential = max(0, benchmark - overall_score)

        return {
            'vs_average': vs_average,
            'improvement_potential': improvement_potential
        }

    # Hook optimization helper methods
    def _predict_hook_engagement(self, hook_score: float, hook_type: HookType, enhanced_context: Dict[str, Any]) -> float:
        """Predict engagement based on hook analysis"""
        base_engagement = hook_score / 100
        type_multiplier = self.hook_patterns[hook_type]['engagement_multiplier']

        # Adjust based on user's historical engagement
        performance_data = enhanced_context.get('performance_data', {})
        avg_engagement = performance_data.get('avg_engagement_30d', 3.0) / 100

        predicted_engagement = (base_engagement * type_multiplier * 0.7) + (avg_engagement * 0.3)
        return min(1.0, max(0.0, predicted_engagement))

    def _predict_hook_retention(self, hook_score: float, hook_type: HookType, enhanced_context: Dict[str, Any]) -> float:
        """Predict retention based on hook analysis"""
        base_retention = (hook_score / 100) * 0.8  # Hooks affect early retention most
        retention_boost = self.hook_patterns[hook_type]['retention_boost']

        # Adjust based on user's historical retention
        performance_data = enhanced_context.get('performance_data', {})
        avg_retention = performance_data.get('avg_retention_30d', 45.0) / 100

        predicted_retention = base_retention + retention_boost + (avg_retention * 0.3)
        return min(1.0, max(0.0, predicted_retention))

    async def _generate_hook_improvements(
        self,
        hook_text: str,
        hook_type: HookType,
        effectiveness_factors: Dict[str, float],
        enhanced_context: Dict[str, Any]
    ) -> List[str]:
        """Generate specific hook improvement suggestions"""

        improvements = []

        # Length optimization
        if effectiveness_factors.get('length_optimization', 100) < 70:
            optimal_length = self.hook_patterns[hook_type]['optimal_length']
            improvements.append(f"Adjust length to ~{optimal_length} words for optimal impact")

        # Emotional impact
        if effectiveness_factors.get('emotional_impact', 50) < 60:
            improvements.append("Add more emotional words (amazing, shocking, incredible)")

        # Curiosity factor
        if effectiveness_factors.get('curiosity_factor', 50) < 60:
            improvements.append("Create a stronger curiosity gap (use words like 'secret', 'revealed', 'truth')")

        # Clarity
        if effectiveness_factors.get('clarity', 50) < 60:
            improvements.append("Simplify language and reduce sentence complexity")

        # Urgency
        if effectiveness_factors.get('urgency', 0) < 30:
            improvements.append("Add time-sensitive language ('now', 'today', 'before it's too late')")

        # Hook type specific improvements
        if hook_type == HookType.QUESTION:
            improvements.append("Make the question more specific and intriguing")
        elif hook_type == HookType.STATEMENT:
            improvements.append("Consider converting to a question for higher engagement")
        elif hook_type == HookType.STORY:
            improvements.append("Start with the most compelling part of the story")

        return improvements[:5]  # Return top 5 improvements

    async def _generate_alternative_hooks(
        self,
        hook_text: str,
        hook_type: HookType,
        video_context: Optional[Dict[str, Any]],
        enhanced_context: Dict[str, Any]
    ) -> List[str]:
        """Generate alternative hook suggestions"""

        alternatives = []
        title = video_context.get('title', '') if video_context else ''
        topic = video_context.get('topic', '') if video_context else ''

        # Generate alternatives based on different hook types
        if hook_type != HookType.QUESTION:
            alternatives.append(f"What if I told you {hook_text.lower()}?")

        if hook_type != HookType.STATISTIC:
            alternatives.append(f"Studies show that {topic} can change everything...")

        if hook_type != HookType.CONTROVERSY:
            alternatives.append(f"Everyone's wrong about {topic}, and here's why...")

        if hook_type != HookType.STORY:
            alternatives.append(f"This happened to me last week, and it changed everything...")

        if hook_type != HookType.PROMISE:
            alternatives.append(f"I'm going to show you exactly how to {topic}...")

        return alternatives[:3]  # Return top 3 alternatives

    def _analyze_hook_timing(self, hook_text: str, hook_type: HookType) -> Dict[str, float]:
        """Analyze hook timing and pacing"""

        word_count = len(hook_text.split())
        optimal_length = self.hook_patterns[hook_type]['optimal_length']

        # Calculate pacing score based on word density
        # Assume average speaking rate of 150 words per minute
        estimated_duration = (word_count / 150) * 60  # seconds

        # Optimal hook duration is 8-12 seconds
        if 8 <= estimated_duration <= 12:
            pacing_score = 100
        elif estimated_duration < 8:
            pacing_score = 80 + (estimated_duration * 2.5)
        else:
            pacing_score = max(50, 100 - ((estimated_duration - 12) * 5))

        return {
            'optimal_length': optimal_length,
            'pacing_score': pacing_score,
            'estimated_duration': estimated_duration
        }

    # Content structure analysis helper methods
    def _segment_content(self, content_script: str) -> List[Dict[str, Any]]:
        """Segment content into analyzable parts"""

        # Split by paragraphs or major breaks
        paragraphs = [p.strip() for p in content_script.split('\n\n') if p.strip()]

        segments = []
        for i, paragraph in enumerate(paragraphs):
            segment = {
                'index': i,
                'content': paragraph,
                'word_count': len(paragraph.split()),
                'estimated_duration': len(paragraph.split()) / 150 * 60,  # seconds
                'type': self._classify_segment_type(paragraph)
            }
            segments.append(segment)

        return segments

    def _classify_segment_type(self, content: str) -> str:
        """Classify the type of content segment"""

        content_lower = content.lower()

        if any(word in content_lower for word in ['intro', 'hello', 'welcome', 'today']):
            return 'introduction'
        elif any(word in content_lower for word in ['conclusion', 'summary', 'recap', 'thanks']):
            return 'conclusion'
        elif any(word in content_lower for word in ['step', 'first', 'next', 'then', 'finally']):
            return 'instruction'
        elif any(word in content_lower for word in ['example', 'instance', 'case', 'story']):
            return 'example'
        elif '?' in content:
            return 'question'
        else:
            return 'content'

    def _predict_retention_curve(self, segments: List[Dict[str, Any]], enhanced_context: Dict[str, Any]) -> List[float]:
        """Predict retention curve for content segments"""

        retention_curve = []
        base_retention = 1.0

        for i, segment in enumerate(segments):
            # Retention typically drops over time
            time_decay = 0.95 ** i

            # Segment type affects retention
            segment_multiplier = {
                'introduction': 1.0,
                'instruction': 0.95,
                'example': 1.05,
                'question': 1.1,
                'content': 0.9,
                'conclusion': 0.85
            }.get(segment['type'], 0.9)

            # Length affects retention (too long = drop off)
            length_factor = 1.0 if segment['word_count'] <= 100 else 0.95

            segment_retention = base_retention * time_decay * segment_multiplier * length_factor
            retention_curve.append(max(0.1, segment_retention))

            base_retention = segment_retention

        return retention_curve

    def _identify_drop_off_points(self, retention_curve: List[float], segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify potential viewer drop-off points"""

        drop_off_points = []

        for i in range(1, len(retention_curve)):
            retention_drop = retention_curve[i-1] - retention_curve[i]

            if retention_drop > 0.1:  # Significant drop
                drop_off_points.append({
                    'segment_index': i,
                    'retention_drop': retention_drop,
                    'severity': 'high' if retention_drop > 0.2 else 'medium',
                    'reason': self._analyze_drop_off_reason(segments[i]),
                    'suggestion': self._suggest_drop_off_fix(segments[i])
                })

        return drop_off_points

    def _analyze_drop_off_reason(self, segment: Dict[str, Any]) -> str:
        """Analyze why viewers might drop off at this segment"""

        if segment['word_count'] > 150:
            return "Segment too long"
        elif segment['type'] == 'conclusion':
            return "Natural end point"
        elif 'boring' in segment['content'].lower():
            return "Low engagement content"
        else:
            return "Pacing issue"

    def _suggest_drop_off_fix(self, segment: Dict[str, Any]) -> str:
        """Suggest how to fix drop-off point"""

        if segment['word_count'] > 150:
            return "Break into shorter segments"
        elif segment['type'] == 'content':
            return "Add engaging examples or questions"
        else:
            return "Improve pacing and add pattern interrupts"

# Global instance
_content_intelligence = None

def get_content_intelligence() -> AdvancedContentIntelligence:
    """Get global content intelligence instance"""
    global _content_intelligence
    if _content_intelligence is None:
        _content_intelligence = AdvancedContentIntelligence()
    return _content_intelligence
