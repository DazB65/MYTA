"""
Context Analyzer for MYTA
Analyzes conversation context, user patterns, and situational factors
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import re

from backend.App.channel_analyzer import ChannelProfile
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.AGENT)

@dataclass
class ConversationContext:
    """Analyzed conversation context"""
    user_intent: str
    emotional_state: str
    expertise_level: str
    question_type: str
    topic_focus: List[str]
    urgency_signals: List[str]
    success_indicators: List[str]
    frustration_indicators: List[str]
    previous_topics: List[str]
    conversation_stage: str

@dataclass
class UserPattern:
    """User behavior and preference patterns"""
    preferred_communication_style: str
    typical_question_types: List[str]
    engagement_level: str
    learning_pace: str
    goal_orientation: str
    technical_comfort: str
    response_preferences: Dict[str, Any]

class ContextAnalyzer:
    """Analyzes conversation context and user patterns"""
    
    def __init__(self):
        self.intent_patterns = self._load_intent_patterns()
        self.emotional_indicators = self._load_emotional_indicators()
        self.expertise_markers = self._load_expertise_markers()
        self.urgency_signals = self._load_urgency_signals()
    
    def _load_intent_patterns(self) -> Dict[str, List[str]]:
        """Load patterns for intent recognition"""
        return {
            "seeking_help": [
                "help", "how do i", "can you", "need to", "struggling", "stuck",
                "don't know", "confused", "not sure", "having trouble"
            ],
            "requesting_analysis": [
                "analyze", "check", "review", "look at", "examine", "evaluate",
                "assess", "what do you think", "feedback", "opinion"
            ],
            "seeking_strategy": [
                "strategy", "plan", "approach", "method", "way to", "best practice",
                "should i", "recommend", "suggest", "advice"
            ],
            "reporting_problem": [
                "problem", "issue", "not working", "broken", "wrong", "error",
                "failing", "declining", "dropping", "low", "bad"
            ],
            "sharing_success": [
                "working", "improved", "better", "increased", "growing", "success",
                "great", "awesome", "thanks", "helped", "fixed"
            ],
            "exploring_options": [
                "what if", "could i", "would it", "options", "alternatives",
                "different", "other ways", "possibilities", "consider"
            ],
            "seeking_education": [
                "learn", "understand", "explain", "teach", "show me", "how does",
                "what is", "why", "difference", "meaning"
            ]
        }
    
    def _load_emotional_indicators(self) -> Dict[str, List[str]]:
        """Load emotional state indicators"""
        return {
            "frustrated": [
                "frustrated", "annoying", "hate", "terrible", "awful", "worst",
                "stupid", "ridiculous", "impossible", "give up", "quit"
            ],
            "excited": [
                "excited", "amazing", "awesome", "fantastic", "incredible",
                "love", "perfect", "brilliant", "excellent", "thrilled"
            ],
            "worried": [
                "worried", "concerned", "scared", "afraid", "nervous", "anxious",
                "stress", "panic", "fear", "trouble", "danger"
            ],
            "confident": [
                "confident", "sure", "ready", "prepared", "capable", "strong",
                "determined", "motivated", "positive", "optimistic"
            ],
            "confused": [
                "confused", "lost", "unclear", "don't understand", "complicated",
                "overwhelming", "mixed up", "puzzled", "bewildered"
            ],
            "hopeful": [
                "hope", "optimistic", "positive", "looking forward", "expecting",
                "anticipating", "promising", "encouraging", "bright"
            ],
            "neutral": [
                "okay", "fine", "normal", "standard", "regular", "typical",
                "usual", "average", "moderate", "reasonable"
            ]
        }
    
    def _load_expertise_markers(self) -> Dict[str, List[str]]:
        """Load expertise level markers"""
        return {
            "beginner": [
                "new", "beginner", "just started", "first time", "don't know",
                "basic", "simple", "easy", "learning", "tutorial"
            ],
            "intermediate": [
                "some experience", "been doing", "understand basics", "familiar",
                "intermediate", "moderate", "improving", "developing"
            ],
            "advanced": [
                "experienced", "advanced", "expert", "professional", "years of",
                "sophisticated", "complex", "detailed", "technical", "optimize"
            ],
            "expert": [
                "expert", "master", "professional", "consultant", "teach others",
                "industry", "enterprise", "scale", "systematic", "strategic"
            ]
        }
    
    def _load_urgency_signals(self) -> Dict[str, List[str]]:
        """Load urgency signal patterns"""
        return {
            "immediate": [
                "urgent", "emergency", "asap", "immediately", "right now",
                "crisis", "disaster", "critical", "help!", "broken"
            ],
            "high": [
                "soon", "quickly", "fast", "deadline", "important", "priority",
                "need to", "must", "should", "time sensitive"
            ],
            "medium": [
                "when possible", "sometime", "eventually", "planning", "future",
                "considering", "thinking about", "maybe", "might"
            ],
            "low": [
                "curious", "wondering", "interested", "exploring", "learning",
                "general", "overview", "background", "understanding"
            ]
        }
    
    def analyze_conversation_context(
        self, 
        user_message: str, 
        conversation_history: List[Dict[str, Any]]
    ) -> ConversationContext:
        """Analyze conversation context from message and history"""
        
        try:
            # Analyze current message
            user_intent = self._identify_intent(user_message)
            emotional_state = self._identify_emotional_state(user_message)
            expertise_level = self._identify_expertise_level(user_message, conversation_history)
            question_type = self._identify_question_type(user_message)
            topic_focus = self._extract_topic_focus(user_message)
            urgency_signals = self._identify_urgency_signals(user_message)
            
            # Analyze conversation patterns
            success_indicators = self._identify_success_indicators(user_message, conversation_history)
            frustration_indicators = self._identify_frustration_indicators(user_message, conversation_history)
            previous_topics = self._extract_previous_topics(conversation_history)
            conversation_stage = self._determine_conversation_stage(conversation_history)
            
            return ConversationContext(
                user_intent=user_intent,
                emotional_state=emotional_state,
                expertise_level=expertise_level,
                question_type=question_type,
                topic_focus=topic_focus,
                urgency_signals=urgency_signals,
                success_indicators=success_indicators,
                frustration_indicators=frustration_indicators,
                previous_topics=previous_topics,
                conversation_stage=conversation_stage
            )
        
        except Exception as e:
            logger.error(f"Error analyzing conversation context: {e}")
            return self._get_default_context()
    
    def analyze_user_patterns(
        self, 
        conversation_history: List[Dict[str, Any]], 
        user_profile: Dict[str, Any] = None
    ) -> UserPattern:
        """Analyze user behavior and preference patterns"""
        
        try:
            # Analyze communication style
            communication_style = self._analyze_communication_style(conversation_history)
            
            # Analyze question patterns
            question_types = self._analyze_question_patterns(conversation_history)
            
            # Analyze engagement level
            engagement_level = self._analyze_engagement_level(conversation_history)
            
            # Analyze learning pace
            learning_pace = self._analyze_learning_pace(conversation_history)
            
            # Analyze goal orientation
            goal_orientation = self._analyze_goal_orientation(conversation_history)
            
            # Analyze technical comfort
            technical_comfort = self._analyze_technical_comfort(conversation_history)
            
            # Analyze response preferences
            response_preferences = self._analyze_response_preferences(conversation_history)
            
            return UserPattern(
                preferred_communication_style=communication_style,
                typical_question_types=question_types,
                engagement_level=engagement_level,
                learning_pace=learning_pace,
                goal_orientation=goal_orientation,
                technical_comfort=technical_comfort,
                response_preferences=response_preferences
            )
        
        except Exception as e:
            logger.error(f"Error analyzing user patterns: {e}")
            return self._get_default_user_pattern()
    
    def _identify_intent(self, message: str) -> str:
        """Identify user intent from message"""
        
        message_lower = message.lower()
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = sum(1 for pattern in patterns if pattern in message_lower)
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            return max(intent_scores, key=intent_scores.get)
        
        return "seeking_help"  # Default intent
    
    def _identify_emotional_state(self, message: str) -> str:
        """Identify emotional state from message"""
        
        message_lower = message.lower()
        emotion_scores = {}
        
        for emotion, indicators in self.emotional_indicators.items():
            score = sum(1 for indicator in indicators if indicator in message_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        # Check for punctuation indicators
        if "!" in message and len([c for c in message if c == "!"]) > 1:
            emotion_scores["excited"] = emotion_scores.get("excited", 0) + 1
        
        if "?" in message and len([c for c in message if c == "?"]) > 1:
            emotion_scores["confused"] = emotion_scores.get("confused", 0) + 1
        
        if emotion_scores:
            return max(emotion_scores, key=emotion_scores.get)
        
        return "neutral"
    
    def _identify_expertise_level(self, message: str, history: List[Dict]) -> str:
        """Identify user expertise level"""
        
        message_lower = message.lower()
        expertise_scores = {}
        
        for level, markers in self.expertise_markers.items():
            score = sum(1 for marker in markers if marker in message_lower)
            if score > 0:
                expertise_scores[level] = score
        
        # Consider conversation history
        if len(history) > 5:  # Experienced user
            expertise_scores["intermediate"] = expertise_scores.get("intermediate", 0) + 1
        
        if len(history) > 15:  # Very experienced user
            expertise_scores["advanced"] = expertise_scores.get("advanced", 0) + 1
        
        if expertise_scores:
            return max(expertise_scores, key=expertise_scores.get)
        
        return "intermediate"
    
    def _identify_question_type(self, message: str) -> str:
        """Identify type of question being asked"""
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["how", "how to", "how do"]):
            return "how_to"
        elif any(word in message_lower for word in ["what", "what is", "what are"]):
            return "what_is"
        elif any(word in message_lower for word in ["why", "why is", "why do"]):
            return "why"
        elif any(word in message_lower for word in ["when", "when should", "when to"]):
            return "when"
        elif any(word in message_lower for word in ["where", "where to", "where can"]):
            return "where"
        elif any(word in message_lower for word in ["which", "which one", "what's better"]):
            return "which"
        elif "?" in message:
            return "general_question"
        else:
            return "statement"
    
    def _extract_topic_focus(self, message: str) -> List[str]:
        """Extract main topics from message"""
        
        message_lower = message.lower()
        
        topics = {
            "analytics": ["analytics", "metrics", "performance", "stats", "data"],
            "content": ["content", "video", "videos", "create", "creation"],
            "thumbnails": ["thumbnail", "thumbnails", "image", "visual"],
            "titles": ["title", "titles", "headline", "name"],
            "seo": ["seo", "search", "keywords", "tags", "ranking"],
            "engagement": ["engagement", "comments", "likes", "community"],
            "growth": ["growth", "grow", "subscribers", "audience", "reach"],
            "monetization": ["monetization", "money", "revenue", "ads", "income"],
            "algorithm": ["algorithm", "recommended", "discovery", "suggested"],
            "retention": ["retention", "watch time", "drop off", "boring"]
        }
        
        identified_topics = []
        for topic, keywords in topics.items():
            if any(keyword in message_lower for keyword in keywords):
                identified_topics.append(topic)
        
        return identified_topics[:3]  # Return top 3 topics
    
    def _identify_urgency_signals(self, message: str) -> List[str]:
        """Identify urgency signals in message"""
        
        message_lower = message.lower()
        signals = []
        
        for urgency_level, patterns in self.urgency_signals.items():
            for pattern in patterns:
                if pattern in message_lower:
                    signals.append(f"{urgency_level}: {pattern}")
        
        return signals
    
    def _identify_success_indicators(self, message: str, history: List[Dict]) -> List[str]:
        """Identify success indicators"""
        
        message_lower = message.lower()
        indicators = []
        
        success_words = ["working", "improved", "better", "increased", "success", "great", "awesome", "thanks"]
        
        for word in success_words:
            if word in message_lower:
                indicators.append(f"success_keyword: {word}")
        
        # Check recent history for improvement mentions
        recent_messages = history[-3:] if len(history) >= 3 else history
        for msg in recent_messages:
            content = msg.get("content", "").lower()
            if any(word in content for word in ["improved", "better", "working"]):
                indicators.append("recent_improvement_mentioned")
        
        return indicators
    
    def _identify_frustration_indicators(self, message: str, history: List[Dict]) -> List[str]:
        """Identify frustration indicators"""
        
        message_lower = message.lower()
        indicators = []
        
        frustration_words = ["frustrated", "stuck", "not working", "broken", "confused", "help"]
        
        for word in frustration_words:
            if word in message_lower:
                indicators.append(f"frustration_keyword: {word}")
        
        # Check for repeated questions
        if len(history) >= 2:
            current_topics = self._extract_topic_focus(message)
            recent_topics = self._extract_topic_focus(history[-1].get("content", ""))
            
            if current_topics and recent_topics and set(current_topics) & set(recent_topics):
                indicators.append("repeated_topic")
        
        return indicators
    
    def _extract_previous_topics(self, history: List[Dict]) -> List[str]:
        """Extract topics from conversation history"""
        
        all_topics = []
        
        for msg in history[-5:]:  # Last 5 messages
            content = msg.get("content", "")
            topics = self._extract_topic_focus(content)
            all_topics.extend(topics)
        
        # Return unique topics in order of appearance
        unique_topics = []
        for topic in all_topics:
            if topic not in unique_topics:
                unique_topics.append(topic)
        
        return unique_topics[:5]  # Top 5 previous topics
    
    def _determine_conversation_stage(self, history: List[Dict]) -> str:
        """Determine what stage the conversation is in"""
        
        if len(history) <= 1:
            return "initial"
        elif len(history) <= 3:
            return "exploration"
        elif len(history) <= 8:
            return "problem_solving"
        elif len(history) <= 15:
            return "optimization"
        else:
            return "advanced_consultation"
    
    def _analyze_communication_style(self, history: List[Dict]) -> str:
        """Analyze user's preferred communication style"""
        
        if not history:
            return "standard"
        
        total_length = sum(len(msg.get("content", "")) for msg in history)
        avg_length = total_length / len(history)
        
        question_count = sum(1 for msg in history if "?" in msg.get("content", ""))
        question_ratio = question_count / len(history)
        
        if avg_length > 200:
            return "detailed"
        elif avg_length < 50:
            return "concise"
        elif question_ratio > 0.7:
            return "inquisitive"
        else:
            return "conversational"
    
    def _analyze_question_patterns(self, history: List[Dict]) -> List[str]:
        """Analyze typical question patterns"""
        
        question_types = []
        
        for msg in history:
            content = msg.get("content", "")
            q_type = self._identify_question_type(content)
            if q_type not in question_types and q_type != "statement":
                question_types.append(q_type)
        
        return question_types[:3]  # Top 3 question types
    
    def _analyze_engagement_level(self, history: List[Dict]) -> str:
        """Analyze user engagement level"""
        
        if len(history) > 20:
            return "high"
        elif len(history) > 10:
            return "medium"
        elif len(history) > 3:
            return "moderate"
        else:
            return "low"
    
    def _analyze_learning_pace(self, history: List[Dict]) -> str:
        """Analyze user's learning pace"""
        
        if not history:
            return "standard"
        
        # Analyze time between messages (if timestamps available)
        # For now, use message complexity as proxy
        
        complex_words = ["optimize", "algorithm", "analytics", "strategy", "systematic"]
        complex_count = sum(
            1 for msg in history 
            for word in complex_words 
            if word in msg.get("content", "").lower()
        )
        
        if complex_count > len(history) * 0.3:
            return "fast"
        elif complex_count < len(history) * 0.1:
            return "slow"
        else:
            return "standard"
    
    def _analyze_goal_orientation(self, history: List[Dict]) -> str:
        """Analyze user's goal orientation"""
        
        goal_words = ["goal", "target", "achieve", "reach", "milestone", "objective"]
        action_words = ["do", "implement", "execute", "start", "begin", "action"]
        
        goal_mentions = sum(
            1 for msg in history 
            for word in goal_words 
            if word in msg.get("content", "").lower()
        )
        
        action_mentions = sum(
            1 for msg in history 
            for word in action_words 
            if word in msg.get("content", "").lower()
        )
        
        if goal_mentions > action_mentions:
            return "strategic"
        elif action_mentions > goal_mentions:
            return "tactical"
        else:
            return "balanced"
    
    def _analyze_technical_comfort(self, history: List[Dict]) -> str:
        """Analyze user's technical comfort level"""
        
        technical_terms = [
            "api", "algorithm", "metadata", "seo", "analytics", "optimization",
            "technical", "code", "settings", "configuration", "integration"
        ]
        
        technical_count = sum(
            1 for msg in history 
            for term in technical_terms 
            if term in msg.get("content", "").lower()
        )
        
        if technical_count > len(history) * 0.2:
            return "high"
        elif technical_count > len(history) * 0.1:
            return "medium"
        else:
            return "low"
    
    def _analyze_response_preferences(self, history: List[Dict]) -> Dict[str, Any]:
        """Analyze user's response preferences"""
        
        preferences = {
            "detail_level": "medium",
            "examples_preferred": True,
            "step_by_step": True,
            "visual_aids": False,
            "follow_up_questions": True
        }
        
        if not history:
            return preferences
        
        # Analyze based on conversation patterns
        total_length = sum(len(msg.get("content", "")) for msg in history)
        avg_length = total_length / len(history)
        
        if avg_length > 150:
            preferences["detail_level"] = "high"
        elif avg_length < 50:
            preferences["detail_level"] = "low"
        
        # Check for requests for examples
        example_requests = sum(
            1 for msg in history 
            if any(word in msg.get("content", "").lower() for word in ["example", "show me", "demonstrate"])
        )
        
        preferences["examples_preferred"] = example_requests > 0
        
        return preferences
    
    def _get_default_context(self) -> ConversationContext:
        """Get default conversation context"""
        return ConversationContext(
            user_intent="seeking_help",
            emotional_state="neutral",
            expertise_level="intermediate",
            question_type="general_question",
            topic_focus=["general"],
            urgency_signals=[],
            success_indicators=[],
            frustration_indicators=[],
            previous_topics=[],
            conversation_stage="initial"
        )
    
    def _get_default_user_pattern(self) -> UserPattern:
        """Get default user pattern"""
        return UserPattern(
            preferred_communication_style="conversational",
            typical_question_types=["how_to"],
            engagement_level="medium",
            learning_pace="standard",
            goal_orientation="balanced",
            technical_comfort="medium",
            response_preferences={
                "detail_level": "medium",
                "examples_preferred": True,
                "step_by_step": True,
                "visual_aids": False,
                "follow_up_questions": True
            }
        )

# Global context analyzer instance
_context_analyzer: Optional[ContextAnalyzer] = None

def get_context_analyzer() -> ContextAnalyzer:
    """Get or create global context analyzer instance"""
    global _context_analyzer
    if _context_analyzer is None:
        _context_analyzer = ContextAnalyzer()
    return _context_analyzer
