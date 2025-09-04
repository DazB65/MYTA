"""
Strategic Content Classifier

This module determines whether user queries should be routed to:
- Strategic Planning Dashboard (quarterly strategies, long-term planning)
- Agent Chat (everyday insights, tactical questions)
"""

import re
from typing import Dict, List, Tuple
from enum import Enum

class ContentType(Enum):
    STRATEGIC_PLANNING = "strategic_planning"
    EVERYDAY_INSIGHTS = "everyday_insights"
    AMBIGUOUS = "ambiguous"

class StrategicContentClassifier:
    """Classifies user messages to determine appropriate routing"""
    
    def __init__(self):
        # Strategic planning indicators
        self.strategic_keywords = {
            'timeframe': [
                'quarterly', 'annual', 'yearly', 'long-term', 'long term',
                'next quarter', 'this quarter', 'q1', 'q2', 'q3', 'q4',
                'next year', 'this year', '2024', '2025', 'months ahead',
                'roadmap', 'timeline', 'planning horizon'
            ],
            'planning': [
                'strategic planning', 'strategy session', 'team strategy',
                'strategic direction', 'big picture', 'overall strategy',
                'master plan', 'strategic goals', 'strategic objectives',
                'long-term goals', 'quarterly goals', 'annual goals',
                'strategic review', 'planning session', 'goal setting',
                'comprehensive planning', 'strategic approach', 'strategic framework',
                'strategic vision', 'strategic roadmap', 'strategic priorities'
            ],
            'scope': [
                'channel strategy', 'business strategy', 'growth strategy',
                'content strategy roadmap', 'monetization strategy',
                'brand strategy', 'competitive strategy', 'market strategy',
                'strategic initiatives', 'strategic priorities'
            ],
            'collaboration': [
                'team planning', 'collaborative strategy', 'team alignment',
                'strategic coordination', 'cross-team strategy',
                'team strategic session', 'strategic workshop'
            ]
        }
        
        # Everyday insights indicators
        self.tactical_keywords = {
            'immediacy': [
                'today', 'now', 'this week', 'immediate', 'quickly',
                'right now', 'asap', 'urgent', 'current', 'latest',
                'recent', 'this video', 'my last video', 'yesterday'
            ],
            'optimization': [
                'optimize', 'improve', 'fix', 'boost', 'increase',
                'enhance', 'tweak', 'adjust', 'fine-tune',
                'quick win', 'quick fix', 'immediate improvement'
            ],
            'specific_content': [
                'this video', 'my latest', 'current performance',
                'recent upload', 'last video', 'specific video',
                'individual video', 'single video', 'one video'
            ],
            'tactical_actions': [
                'thumbnail test', 'title optimization', 'description update',
                'tag adjustment', 'posting time', 'engagement boost',
                'ctr improvement', 'retention fix', 'hook optimization'
            ]
        }
        
        # Ambiguous terms that could go either way
        self.ambiguous_keywords = [
            'strategy', 'growth', 'plan', 'goals', 'analysis',
            'insights', 'recommendations', 'advice'
        ]
    
    def classify_content(self, message: str) -> Tuple[ContentType, float, Dict]:
        """
        Classify message content and return type with confidence score
        
        Returns:
            Tuple of (ContentType, confidence_score, analysis_details)
        """
        message_lower = message.lower()
        
        # Calculate strategic score
        strategic_score = self._calculate_strategic_score(message_lower)
        
        # Calculate tactical score
        tactical_score = self._calculate_tactical_score(message_lower)
        
        # Determine classification
        classification, confidence = self._determine_classification(
            strategic_score, tactical_score, message_lower
        )
        
        analysis_details = {
            'strategic_score': strategic_score,
            'tactical_score': tactical_score,
            'message_length': len(message),
            'strategic_indicators': self._get_matched_indicators(message_lower, self.strategic_keywords),
            'tactical_indicators': self._get_matched_indicators(message_lower, self.tactical_keywords),
            'ambiguous_terms': [term for term in self.ambiguous_keywords if term in message_lower]
        }
        
        return classification, confidence, analysis_details
    
    def _calculate_strategic_score(self, message: str) -> float:
        """Calculate how strategic the message appears to be"""
        score = 0.0
        total_weight = 0.0
        
        # Weight different categories
        weights = {
            'timeframe': 4.0,      # Very strong indicator
            'planning': 3.5,       # Very strong indicator
            'scope': 2.5,          # Strong indicator
            'collaboration': 2.0   # Medium indicator
        }
        
        for category, keywords in self.strategic_keywords.items():
            weight = weights[category]
            matches = sum(1 for keyword in keywords if keyword in message)
            if matches > 0:
                # Diminishing returns for multiple matches in same category
                category_score = min(matches * 0.3, 1.0) * weight
                score += category_score
                total_weight += weight
        
        # Normalize score
        return min(score / max(total_weight, 1.0), 1.0) if total_weight > 0 else 0.0
    
    def _calculate_tactical_score(self, message: str) -> float:
        """Calculate how tactical/immediate the message appears to be"""
        score = 0.0
        total_weight = 0.0
        
        # Weight different categories
        weights = {
            'immediacy': 3.0,        # Strong indicator
            'optimization': 2.5,     # Strong indicator
            'specific_content': 2.0, # Medium indicator
            'tactical_actions': 1.5  # Medium indicator
        }
        
        for category, keywords in self.tactical_keywords.items():
            weight = weights[category]
            matches = sum(1 for keyword in keywords if keyword in message)
            if matches > 0:
                # Diminishing returns for multiple matches in same category
                category_score = min(matches * 0.3, 1.0) * weight
                score += category_score
                total_weight += weight
        
        # Normalize score
        return min(score / max(total_weight, 1.0), 1.0) if total_weight > 0 else 0.0
    
    def _determine_classification(self, strategic_score: float, tactical_score: float, message: str) -> Tuple[ContentType, float]:
        """Determine final classification based on scores"""
        
        # Clear strategic indicators (lowered threshold)
        if strategic_score >= 0.4 and strategic_score > tactical_score * 1.2:
            return ContentType.STRATEGIC_PLANNING, strategic_score

        # Clear tactical indicators
        if tactical_score >= 0.4 and tactical_score > strategic_score * 1.2:
            return ContentType.EVERYDAY_INSIGHTS, tactical_score
        
        # Check for specific patterns that override scores
        if self._has_strategic_patterns(message):
            return ContentType.STRATEGIC_PLANNING, max(strategic_score, 0.8)

        if self._has_tactical_patterns(message):
            return ContentType.EVERYDAY_INSIGHTS, max(tactical_score, 0.8)
        
        # Default to everyday insights for ambiguous cases
        # (better to keep in chat than incorrectly redirect)
        if strategic_score > tactical_score:
            return ContentType.STRATEGIC_PLANNING, strategic_score
        elif tactical_score > strategic_score:
            return ContentType.EVERYDAY_INSIGHTS, tactical_score
        else:
            return ContentType.AMBIGUOUS, 0.5
    
    def _has_strategic_patterns(self, message: str) -> bool:
        """Check for specific strategic patterns"""
        strategic_patterns = [
            r'quarterly?\s+(strategy|planning|goals|review)',
            r'long[- ]?term\s+(strategy|planning|goals)',
            r'strategic\s+(planning|session|review|direction|roadmap|priorities)',
            r'team\s+strategy\s+(session|meeting|planning)',
            r'(q[1-4]|quarter)\s+(strategy|planning|goals)',
            r'annual\s+(strategy|planning|goals|review)',
            r'roadmap\s+(planning|strategy|development)',
            r'comprehensive\s+(strategy|planning)',
            r'goal\s+setting',
            r'strategic\s+(approach|framework|vision)',
            r'big\s+picture',
            r'overall\s+strategy',
            r'master\s+plan'
        ]
        
        return any(re.search(pattern, message, re.IGNORECASE) for pattern in strategic_patterns)
    
    def _has_tactical_patterns(self, message: str) -> bool:
        """Check for specific tactical patterns"""
        tactical_patterns = [
            r'(this|my|latest|recent)\s+(video|upload|content)',
            r'(optimize|improve|fix|boost)\s+(this|my|current)',
            r'(today|now|immediately|quickly)\s+(need|want|should)',
            r'(current|recent|latest)\s+(performance|metrics|analytics)',
            r'(thumbnail|title|description)\s+(optimization|improvement|test)'
        ]
        
        return any(re.search(pattern, message, re.IGNORECASE) for pattern in tactical_patterns)
    
    def _get_matched_indicators(self, message: str, keyword_dict: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Get which specific indicators were matched"""
        matched = {}
        for category, keywords in keyword_dict.items():
            matches = [keyword for keyword in keywords if keyword in message]
            if matches:
                matched[category] = matches
        return matched
    
    def should_redirect_to_strategic_planning(self, message: str, confidence_threshold: float = 0.4) -> Tuple[bool, Dict]:
        """
        Determine if message should be redirected to strategic planning
        
        Returns:
            Tuple of (should_redirect, analysis_details)
        """
        classification, confidence, details = self.classify_content(message)
        
        should_redirect = (
            classification == ContentType.STRATEGIC_PLANNING and 
            confidence >= confidence_threshold
        )
        
        return should_redirect, {
            'classification': classification.value,
            'confidence': confidence,
            'threshold': confidence_threshold,
            'analysis': details
        }

# Global instance
_strategic_classifier = None

def get_strategic_content_classifier() -> StrategicContentClassifier:
    """Get the global strategic content classifier instance"""
    global _strategic_classifier
    if _strategic_classifier is None:
        _strategic_classifier = StrategicContentClassifier()
    return _strategic_classifier
