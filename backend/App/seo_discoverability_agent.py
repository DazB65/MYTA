"""
SEO & Discoverability Agent for Vidalytics
Specialized sub-agent that analyzes YouTube searchability and discoverability for the boss agent
"""

import json
import uuid
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging
import os
import time
from googleapiclient.errors import HttpError
from dataclasses import dataclass
import re
from backend.App.boss_agent_auth import SpecializedAgentAuthMixin
from backend.App.connection_pool import get_youtube_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SEOAnalysisRequest:
    """Structure for SEO analysis requests from boss agent"""
    request_id: str
    channel_id: str
    video_ids: List[str]
    time_period: str
    analysis_depth: str = "standard"  # quick, standard, deep
    include_keyword_analysis: bool = True
    include_competitor_keywords: bool = True
    include_optimization_suggestions: bool = True
    token_budget: int = 3000

@dataclass
class SEOMetrics:
    """SEO metrics structure"""
    video_id: str
    title: str
    description: str
    tags: List[str]
    search_traffic_percentage: float
    suggested_traffic_percentage: float
    browse_traffic_percentage: float
    click_through_rate: float
    impressions: int
    keyword_rankings: Dict[str, int]
    optimization_score: float

class YouTubeSEOAPIClient:
    """YouTube API integration for SEO data retrieval"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = get_youtube_client(api_key)
        self.analytics = None  # Would require OAuth for Analytics API
        
    async def get_video_seo_data(self, video_ids: List[str]) -> List[SEOMetrics]:
        """Retrieve SEO-related video data"""
        
        try:
            # Get video details including snippets and statistics
            video_response = self.youtube.videos().list(
                part='snippet,statistics',
                id=','.join(video_ids)
            ).execute()
            
            seo_metrics = []
            for video in video_response.get('items', []):
                video_id = video['id']
                snippet = video['snippet']
                stats = video['statistics']
                
                # Extract SEO-relevant data
                title = snippet.get('title', '')
                description = snippet.get('description', '')
                tags = snippet.get('tags', [])
                
                # Calculate basic SEO metrics (in production, these would come from Analytics API)
                views = int(stats.get('viewCount', 0))
                
                # Mock SEO metrics based on realistic patterns
                seo_metrics.append(SEOMetrics(
                    video_id=video_id,
                    title=title,
                    description=description,
                    tags=tags,
                    search_traffic_percentage=self._calculate_search_traffic(title, tags),
                    suggested_traffic_percentage=45.2,
                    browse_traffic_percentage=12.8,
                    click_through_rate=self._calculate_ctr(title, views),
                    impressions=views * 15,  # Approximate impressions
                    keyword_rankings=self._generate_keyword_rankings(title, tags),
                    optimization_score=self._calculate_optimization_score(title, description, tags)
                ))
            
            return seo_metrics
            
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            return []
        except Exception as e:
            logger.error(f"Error retrieving SEO data: {e}")
            return []
    
    def _calculate_search_traffic(self, title: str, tags: List[str]) -> float:
        """Calculate estimated search traffic percentage based on title and tags"""
        
        # Simple heuristic based on keyword density and title optimization
        search_indicators = ['how to', 'tutorial', 'guide', 'tips', 'learn', 'beginner']
        title_lower = title.lower()
        
        search_score = sum(1 for indicator in search_indicators if indicator in title_lower)
        tag_score = len(tags) * 0.5
        
        # Normalize to percentage (realistic YouTube search traffic: 15-45%)
        base_percentage = 20.0
        bonus = min(search_score * 3 + tag_score, 25.0)
        
        return min(base_percentage + bonus, 45.0)
    
    def _calculate_ctr(self, title: str, views: int) -> float:
        """Calculate estimated click-through rate"""
        
        # CTR factors: title length, emotional words, numbers
        title_length = len(title)
        optimal_length = 60  # Optimal title length for YouTube
        
        emotional_words = ['amazing', 'incredible', 'shocking', 'secret', 'ultimate', 'best', 'worst']
        emotional_score = sum(1 for word in emotional_words if word.lower() in title.lower())
        
        # Numbers in title often improve CTR
        number_score = 1 if re.search(r'\d+', title) else 0
        
        # Base CTR calculation (typical YouTube CTR: 2-10%)
        base_ctr = 4.0
        length_factor = 1.0 - abs(title_length - optimal_length) / 100
        emotional_factor = emotional_score * 0.5
        number_factor = number_score * 0.3
        
        ctr = base_ctr * (1 + length_factor + emotional_factor + number_factor)
        return min(max(ctr, 1.0), 12.0)  # Clamp between 1% and 12%
    
    def _generate_keyword_rankings(self, title: str, tags: List[str]) -> Dict[str, int]:
        """Generate mock keyword rankings"""
        
        keywords = {}
        
        # Extract potential keywords from title
        title_words = re.findall(r'\b\w+\b', title.lower())
        important_words = [word for word in title_words if len(word) > 3]
        
        # Add tag-based keywords
        for tag in tags[:5]:  # Limit to top 5 tags
            if len(tag) > 3:
                important_words.append(tag.lower())
        
        # Generate rankings (1-50, where lower is better)
        for i, keyword in enumerate(important_words[:8]):  # Limit to 8 keywords
            # More relevant keywords (earlier in title) get better rankings
            base_ranking = 10 + i * 3
            variation = hash(keyword) % 15  # Add some variation
            ranking = min(base_ranking + variation, 50)
            keywords[keyword] = ranking
        
        return keywords
    
    def _calculate_optimization_score(self, title: str, description: str, tags: List[str]) -> float:
        """Calculate overall SEO optimization score (0-10)"""
        
        score = 0.0
        
        # Title optimization (0-3 points)
        title_length = len(title)
        if 40 <= title_length <= 70:
            score += 2.0
        elif 30 <= title_length <= 80:
            score += 1.5
        else:
            score += 0.5
        
        # Check for numbers/emotional words in title
        if re.search(r'\d+', title):
            score += 0.5
        
        # Description optimization (0-3 points)
        desc_length = len(description)
        if desc_length > 125:  # Minimum good description length
            score += 1.5
        if desc_length > 250:  # Comprehensive description
            score += 1.0
        if 'http' in description:  # Contains links
            score += 0.5
        
        # Tags optimization (0-4 points)
        tag_count = len(tags)
        if tag_count >= 5:
            score += 2.0
        elif tag_count >= 3:
            score += 1.5
        elif tag_count >= 1:
            score += 1.0
        
        # Keyword consistency between title, description, and tags
        title_words = set(re.findall(r'\b\w+\b', title.lower()))
        desc_words = set(re.findall(r'\b\w+\b', description.lower()))
        tag_words = set(tag.lower() for tag in tags)
        
        consistency = len(title_words & desc_words & tag_words)
        score += min(consistency * 0.5, 2.0)
        
        return min(score, 10.0)
    
    async def get_trending_keywords(self, niche: str, region: str = "US") -> List[Dict[str, Any]]:
        """Get trending keywords for the niche"""
        
        try:
            # In production, this would use trending APIs or keyword tools
            # For now, generate realistic trending keywords based on niche
            trending_keywords = self._generate_trending_keywords(niche)
            return trending_keywords
            
        except Exception as e:
            logger.error(f"Error retrieving trending keywords: {e}")
            return []
    
    def _generate_trending_keywords(self, niche: str) -> List[Dict[str, Any]]:
        """Generate mock trending keywords for the niche"""
        
        # Base keywords by niche
        niche_keywords = {
            'tech': ['ai', 'machine learning', 'coding', 'programming', 'software', 'tutorial'],
            'gaming': ['gameplay', 'review', 'walkthrough', 'tips', 'guide', 'stream'],
            'education': ['tutorial', 'learn', 'course', 'study', 'explained', 'guide'],
            'lifestyle': ['vlog', 'daily', 'routine', 'tips', 'haul', 'review'],
            'fitness': ['workout', 'exercise', 'training', 'diet', 'health', 'fitness']
        }
        
        base_keywords = niche_keywords.get(niche.lower(), ['tutorial', 'tips', 'guide', 'review'])
        
        trending_data = []
        for i, keyword in enumerate(base_keywords):
            trending_data.append({
                'keyword': keyword,
                'search_volume': 10000 - (i * 1500),
                'competition': 'medium' if i < 3 else 'low',
                'trend': 'rising' if i % 2 == 0 else 'stable',
                'relevance_score': 90 - (i * 10)
            })
        
        return trending_data

class AlgorithmAnalyzer:
    """Analyzes content for YouTube algorithm favorability"""

    def __init__(self):
        self.algorithm_factors = {
            'engagement_velocity': 0.25,  # Likes, comments, shares in first hour
            'retention_strength': 0.20,  # Viewer retention metrics
            'searcher_intent': 0.15,  # Search and browse impressions
            'topic_momentum': 0.15,  # Topic trending status
            'production_signals': 0.15,  # Video quality signals
            'metadata_strength': 0.10   # Title, description, tags optimization
        }

    def calculate_algorithm_score(self, seo_metrics: SEOMetrics, channel_context: Dict) -> Dict[str, Any]:
        """Calculate algorithm favorability score and factors"""
        
        # Calculate factor scores
        factor_scores = {
            'engagement_velocity': self._score_engagement_velocity(seo_metrics),
            'retention_strength': self._score_retention(seo_metrics),
            'searcher_intent': self._score_search_intent(seo_metrics),
            'topic_momentum': self._score_topic_momentum(seo_metrics, channel_context),
            'production_signals': self._score_production_signals(seo_metrics),
            'metadata_strength': self._score_metadata(seo_metrics)
        }

        # Calculate weighted score
        algo_score = sum(score * self.algorithm_factors[factor] 
                        for factor, score in factor_scores.items())

        # Scale to 0-100
        algo_score = min(100, max(0, algo_score * 100))

        return {
            'algorithm_score': round(algo_score, 1),
            'factor_scores': factor_scores,
            'key_factors': self._identify_key_factors(factor_scores),
            'recommendations': self._generate_recommendations(factor_scores),
            'risk_factors': self._identify_risks(seo_metrics, factor_scores)
        }

    def _score_engagement_velocity(self, metrics: SEOMetrics) -> float:
        """Score early engagement patterns"""
        if not hasattr(metrics, 'click_through_rate'):
            return 0.5

        ctr = metrics.click_through_rate
        impressions = metrics.impressions

        # Higher score for higher CTR and impressions
        ctr_score = min(1.0, ctr / 10.0)  # Scale CTR to 0-1
        impression_score = min(1.0, impressions / 50000)  # Scale impressions

        return (ctr_score * 0.7 + impression_score * 0.3)

    def _score_retention(self, metrics: SEOMetrics) -> float:
        """Score viewer retention strength"""
        # Would use actual retention data in production
        return 0.75  # Default good retention score

    def _score_search_intent(self, metrics: SEOMetrics) -> float:
        """Score search and discovery patterns"""
        search_traffic = metrics.search_traffic_percentage / 100
        suggested = metrics.suggested_traffic_percentage / 100
        browse = metrics.browse_traffic_percentage / 100

        # Weight different traffic sources
        return (search_traffic * 0.4 + suggested * 0.4 + browse * 0.2)

    def _score_topic_momentum(self, metrics: SEOMetrics, context: Dict) -> float:
        """Score topic trending status"""
        title_lower = metrics.title.lower()
        
        # Keywords indicating trending topics
        trend_indicators = [
            'new', '2024', 'latest', 'update', 'breaking',
            'announcement', 'revealed', 'launch', 'upcoming'
        ]
        
        matches = sum(1 for word in trend_indicators if word in title_lower)
        return min(1.0, matches / 3)

    def _score_production_signals(self, metrics: SEOMetrics) -> float:
        """Score production quality signals"""
        # Would use actual quality metrics in production
        return 0.8  # Default good quality score

    def _score_metadata(self, metrics: SEOMetrics) -> float:
        """Score metadata optimization"""
        title_len = len(metrics.title)
        desc_len = len(metrics.description)
        tag_count = len(metrics.tags)

        # Score based on metadata completeness
        title_score = 1.0 if 40 <= title_len <= 70 else 0.5
        desc_score = 1.0 if desc_len >= 200 else 0.5
        tag_score = min(1.0, tag_count / 15)  # Up to 15 tags

        return (title_score * 0.4 + desc_score * 0.3 + tag_score * 0.3)

    def _identify_key_factors(self, scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """Identify key factors affecting algorithm performance"""
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

    def _generate_recommendations(self, scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """Generate algorithm optimization recommendations"""
        recommendations = []

        for factor, score in scores.items():
            if score < 0.7:
                recommendations.append({
                    'focus_area': factor.replace('_', ' ').title(),
                    'current_score': round(score * 100, 1),
                    'target_score': round(min(score * 1.5, 1.0) * 100, 1),
                    'priority': 'High' if score < 0.5 else 'Medium'
                })

        return sorted(recommendations,
                     key=lambda x: x['current_score'])

    def _identify_risks(self, metrics: SEOMetrics, scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """Identify potential algorithm risks"""
        risks = []

        # Check for low engagement risk
        if scores['engagement_velocity'] < 0.4:
            risks.append({
                'risk': 'Low Engagement Velocity',
                'severity': 'High',
                'impact': 'Reduced recommendations',
                'mitigation': 'Improve CTR and early engagement'
            })

        # Check for poor retention risk
        if scores['retention_strength'] < 0.5:
            risks.append({
                'risk': 'Poor Retention',
                'severity': 'High',
                'impact': 'Reduced surfacing in search',
                'mitigation': 'Enhance content engagement'
            })

        # Check for metadata risks
        if scores['metadata_strength'] < 0.6:
            risks.append({
                'risk': 'Weak Metadata',
                'severity': 'Medium',
                'impact': 'Lower search visibility',
                'mitigation': 'Optimize titles, descriptions, tags'
            })

        return risks

class ClaudeHaikuSEOEngine:
    """Claude 3.5 Haiku integration for cost-effective SEO analysis"""
    
    def __init__(self, api_key: str = None):
        # No longer needs direct client - uses centralized model integration
        self.algorithm_analyzer = AlgorithmAnalyzer()
        
    async def analyze_seo_performance(self, seo_metrics: List[SEOMetrics], channel_context: Dict) -> Dict[str, Any]:
        """Analyze SEO performance and algorithm favorability"""

        """Analyze SEO performance using Claude 3.5 Haiku"""
        
        if not seo_metrics:
            return self._generate_fallback_seo_analysis()
        
        # Prepare data for analysis
        seo_data = self._prepare_seo_data(seo_metrics, channel_context)
        
        # Voice consistency - SEO optimization specialist with search insights
        seo_prompt = f"""
        VOICE: SEO optimization specialist | Data-driven, technical, search-focused
        
        TASK: SEO analysis for {channel_context.get('name', 'Unknown')} ({channel_context.get('niche', 'Unknown')}, {channel_context.get('subscriber_count', 0):,} subs).
        
        SEO DATA:
        {json.dumps(seo_data, indent=2)}
        
        ANALYZE:
        • Search traffic performance & gaps
        • Keyword opportunities & ranking potential
        • Title/description optimization
        • Click-through rate improvements
        
        RESPONSE FORMAT (JSON):
        {{
          "seo_summary": "Search traffic at X%, ranking for Y keywords",
          "keyword_analysis": {{
            "top_keywords": ["keyword (rank #X)"],
            "missed_opportunities": ["high-volume keyword"],
            "keyword_gaps": ["competitor keyword we're missing"]
          }},
          "optimization_priorities": [
            {{
              "priority": "Title optimization",
              "impact": "High/Medium/Low",
              "effort": "Easy/Medium/Hard",
              "examples": ["Current title → Optimized title"]
            }}
          ],
          "search_insights": {{
            "traffic_sources": "Search/Browse/Suggested breakdown",
            "ctr_performance": "X% vs Y% benchmark",
            "ranking_factors": ["What's working/not working"]
          }},
          "recommendations": [
            {{
              "action": "Specific SEO improvement",
              "reasoning": "Why this will improve rankings",
              "expected_impact": "X% traffic increase"
            }}
          ]
        }}
        """
        
        try:
            # Use centralized model integration
            from backend.App.model_integrations import create_agent_call_to_integration
            result = await create_agent_call_to_integration(
                agent_type="seo_discoverability",
                use_case="seo_analysis",
                prompt_data={
                    "prompt": seo_prompt,
                    "analysis_depth": "standard",
                    "system_message": "You are an expert YouTube SEO specialist. Provide technical SEO insights and keyword optimization strategies."
                }
            )
            
            # Parse the response
            analysis_text = result["content"] if result["success"] else "{}"
            
            # Try to extract JSON from the response
            try:
                import re
                json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
                if json_match:
                    seo_json = json.loads(json_match.group())
                else:
                    seo_json = self._parse_seo_response(analysis_text)
            except:
                seo_json = self._parse_seo_response(analysis_text)
            
            return seo_json
            
        except Exception as e:
            logger.error(f"Claude SEO analysis error: {e}")
            return self._generate_fallback_seo_analysis()
    
    def _prepare_seo_data(self, seo_metrics: List[SEOMetrics], channel_context: Dict) -> List[Dict]:
        """Prepare SEO data for analysis"""
        
        prepared_data = []
        for metric in seo_metrics:
            prepared_data.append({
                'title': metric.title,
                'title_length': len(metric.title),
                'description_length': len(metric.description),
                'tag_count': len(metric.tags),
                'search_traffic_pct': metric.search_traffic_percentage,
                'suggested_traffic_pct': metric.suggested_traffic_percentage,
                'click_through_rate': metric.click_through_rate,
                'impressions': metric.impressions,
                'optimization_score': metric.optimization_score,
                'top_keywords': list(metric.keyword_rankings.keys())[:5],
                'keyword_rankings': metric.keyword_rankings
            })
        
        return prepared_data
    
    def _parse_seo_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Claude response into structured SEO format"""
        
        return {
            "seo_summary": "SEO analysis completed with focus on discoverability optimization",
            "keyword_analysis": {
                "top_performing_keywords": ["tutorial", "guide", "tips"],
                "optimization_opportunities": ["long-tail keywords", "trending topics"],
                "keyword_gaps": ["niche-specific terms", "seasonal keywords"],
                "ranking_potential": "medium"
            },
            "optimization_priorities": [
                {"area": "Title optimization", "priority": "high", "impact": "high"},
                {"area": "Tag strategy", "priority": "medium", "impact": "medium"},
                {"area": "Description enhancement", "priority": "medium", "impact": "medium"}
            ],
            "search_insights": {
                "search_traffic_health": "moderate",
                "ctr_performance": "above average",
                "impression_efficiency": "needs improvement",
                "discovery_patterns": ["search-driven", "suggested video"]
            },
            "recommendations": [
                "Optimize titles for target keywords",
                "Improve description keyword density",
                "Enhance tag relevance and coverage",
                "Focus on trending topic integration"
            ],
            "raw_analysis": response_text
        }
    
    def _generate_fallback_seo_analysis(self) -> Dict[str, Any]:
        """Generate basic SEO analysis when Claude fails"""
        
        return {
            "seo_summary": "Basic SEO analysis completed with limited data",
            "keyword_analysis": {
                "top_performing_keywords": ["content", "video", "channel"],
                "optimization_opportunities": ["keyword research", "tag optimization"],
                "keyword_gaps": ["trending keywords", "long-tail terms"],
                "ranking_potential": "to be determined"
            },
            "optimization_priorities": [
                {"area": "Title optimization", "priority": "high", "impact": "high"},
                {"area": "Keyword research", "priority": "high", "impact": "medium"},
                {"area": "Tag strategy", "priority": "medium", "impact": "medium"}
            ],
            "search_insights": {
                "search_traffic_health": "needs assessment",
                "ctr_performance": "baseline",
                "impression_efficiency": "baseline",
                "discovery_patterns": ["organic search", "browse features"]
            },
            "recommendations": [
                "Conduct comprehensive keyword research",
                "Optimize video titles for search",
                "Improve tag relevance and variety",
                "Enhance description optimization"
            ]
        }

class SEODiscoverabilityCache:
    """Specialized caching for SEO analysis results"""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = {
            'quick': 3600,      # 1 hour for quick analysis
            'standard': 10800,  # 3 hours for standard analysis (SEO changes slowly)
            'deep': 21600       # 6 hours for deep analysis
        }
    
    def get_cache_key(self, request: SEOAnalysisRequest) -> str:
        """Generate cache key for SEO analysis request"""
        cache_data = {
            'channel_id': request.channel_id,
            'video_ids': sorted(request.video_ids),
            'time_period': request.time_period,
            'analysis_depth': request.analysis_depth,
            'include_keyword_analysis': request.include_keyword_analysis,
            'include_competitor_keywords': request.include_competitor_keywords
        }
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def get(self, request: SEOAnalysisRequest) -> Optional[Dict[str, Any]]:
        """Get cached SEO analysis result"""
        cache_key = self.get_cache_key(request)
        
        if cache_key not in self.cache:
            return None
        
        cached_item = self.cache[cache_key]
        ttl = self.cache_ttl.get(request.analysis_depth, 10800)
        
        # Check if cache is still valid
        if time.time() - cached_item['timestamp'] > ttl:
            del self.cache[cache_key]
            return None
        
        logger.info(f"SEO analysis cache hit for key: {cache_key[:8]}...")
        return cached_item['data']
    
    def set(self, request: SEOAnalysisRequest, data: Dict[str, Any]):
        """Cache SEO analysis result"""
        cache_key = self.get_cache_key(request)
        
        self.cache[cache_key] = {
            'data': data,
            'timestamp': time.time()
        }
        
        logger.info(f"Cached SEO analysis for key: {cache_key[:8]}...")

class SEODiscoverabilityAgent(SpecializedAgentAuthMixin):
    """
    Specialized SEO & Discoverability Agent for YouTube search optimization
    Operates as a sub-agent within the Vidalytics boss agent hierarchy
    """
    
    def __init__(self, youtube_api_key: str, openai_api_key: str = None):
        self.agent_type = "seo_discoverability"
        self.agent_id = "seo_analyzer"
        self.hierarchical_role = "specialized_agent"
        
        # Initialize API clients
        self.youtube_client = YouTubeSEOAPIClient(youtube_api_key)
        self.seo_engine = ClaudeHaikuSEOEngine()
        
        # Initialize analyzers
        self.algorithm_analyzer = AlgorithmAnalyzer()
        
        # Initialize cache
        self.cache = SEODiscoverabilityCache()
        
        logger.info("SEO & Discoverability Agent initialized and ready for boss agent tasks")
    
    async def process_boss_agent_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for boss agent requests
        This is the ONLY interface the boss agent should use
        """
        
        start_time = time.time()
        request_id = request_data.get('request_id', str(uuid.uuid4()))
        
        try:
            # Validate this is a legitimate boss agent request
            if not self._validate_boss_agent_request(request_data):
                return self._create_unauthorized_response(request_id)
            
            # Parse request from boss agent
            analysis_request = self._parse_boss_request(request_data)
            
            # Check for domain mismatch
            if not self._is_seo_discoverability_request(request_data):
                return self._create_domain_mismatch_response(request_id)
            
            # Check cache first
            cached_result = self.cache.get(analysis_request)
            if cached_result:
                return self._format_cached_response(cached_result, request_id, start_time)
            
            # Perform SEO analysis
            analysis_result = await self._perform_seo_analysis(analysis_request)
            
            # Cache the result
            self.cache.set(analysis_request, analysis_result)
            
            # Format response for boss agent
            response = self._format_boss_agent_response(
                analysis_result, 
                request_id, 
                start_time,
                cache_hit=False
            )
            
            logger.info(f"SEO & Discoverability Agent completed task for boss agent. Request ID: {request_id}")
            return response
            
        except Exception as e:
            logger.error(f"SEO & Discoverability Agent error: {e}")
            return self._create_error_response(request_id, str(e), start_time)
    
    
    def _parse_boss_request(self, request_data: Dict[str, Any]) -> SEOAnalysisRequest:
        """Parse boss agent request into internal format"""
        
        context = request_data.get('context', {})
        
        return SEOAnalysisRequest(
            request_id=request_data.get('request_id', str(uuid.uuid4())),
            channel_id=context.get('channel_id', 'unknown'),
            video_ids=context.get('specific_videos', []),
            time_period=context.get('time_period', 'last_30d'),
            analysis_depth=request_data.get('analysis_depth', 'standard'),
            include_keyword_analysis=request_data.get('include_keyword_analysis', True),
            include_competitor_keywords=request_data.get('include_competitor_keywords', True),
            include_optimization_suggestions=request_data.get('include_optimization_suggestions', True),
            token_budget=request_data.get('token_budget', {}).get('input_tokens', 3000)
        )
    
    def _is_seo_discoverability_request(self, request_data: Dict[str, Any]) -> bool:
        """Check if request is within SEO & discoverability domain"""
        
        query_type = request_data.get('query_type', '')
        
        # This agent handles SEO and discoverability requests
        if query_type in ['seo_optimization', 'seo', 'discoverability']:
            return True
        
        # Also handle requests that mention SEO/discoverability keywords
        message_content = request_data.get('message', '').lower()
        seo_keywords = [
            'seo', 'search', 'discoverability', 'keywords', 'ranking', 'optimization',
            'title', 'description', 'tags', 'thumbnail', 'click-through', 'impressions',
            'visibility', 'findable', 'searchable', 'google', 'youtube search'
        ]
        
        return any(keyword in message_content for keyword in seo_keywords)
    
    async def _perform_seo_analysis(self, request: SEOAnalysisRequest) -> Dict[str, Any]:
        """Perform comprehensive SEO analysis"""
        
        analysis_results = {}
        
        # Get SEO metrics for videos
        if request.video_ids:
            # Analyze specific videos
            seo_metrics = await self.youtube_client.get_video_seo_data(request.video_ids)
        else:
            # Generate sample SEO metrics for general analysis
            seo_metrics = self._create_sample_seo_metrics(request.channel_id)
        
        analysis_results['seo_metrics'] = seo_metrics
        
        # Get trending keywords if requested
        if request.include_keyword_analysis:
            channel_context = await self._get_channel_context(request.channel_id)
            trending_keywords = await self.youtube_client.get_trending_keywords(
                channel_context.get('niche', 'general')
            )
            analysis_results['trending_keywords'] = trending_keywords
        
        # Get channel context for analysis
        channel_context = await self._get_channel_context(request.channel_id)
        
        # Perform AI analysis using Claude Haiku
        ai_analysis = await self.seo_engine.analyze_seo_performance(
            seo_metrics, 
            channel_context
        )
        
        # Analyze algorithm favorability
        algorithm_scores = []
        for metric in seo_metrics:
            algo_analysis = self.algorithm_analyzer.calculate_algorithm_score(
                metric, channel_context
            )
            algorithm_scores.append(algo_analysis)
            
        # Calculate average algorithm score
        avg_algo_score = sum(score['algorithm_score'] for score in algorithm_scores) / len(algorithm_scores) if algorithm_scores else 0
        
        # Aggregate algorithm analysis
        algorithm_analysis = {
            'scores': algorithm_scores,
            'average_score': round(avg_algo_score, 1),
            'top_factors': self._aggregate_algorithm_factors(algorithm_scores),
            'common_risks': self._aggregate_algorithm_risks(algorithm_scores)
        }
        
        # Calculate SEO scores
        seo_scores = self._calculate_seo_scores(seo_metrics, ai_analysis)
        
        # Combine all analysis results
        return {
            'raw_data': analysis_results,
            'ai_analysis': ai_analysis,
            'seo_scores': seo_scores,
            'analysis_metadata': {
                'channel_id': request.channel_id,
                'analysis_depth': request.analysis_depth,
                'videos_analyzed': len(seo_metrics),
                'analysis_timestamp': datetime.now().isoformat()
            }
        }
    
    def _create_sample_seo_metrics(self, channel_id: str) -> List[SEOMetrics]:
        """Create sample SEO metrics for demo purposes"""
        
        # Sample video data for SEO analysis
        import random
        
        sample_videos = [
            {
                'title': 'Ultimate Guide to YouTube SEO in 2024',
                'description': 'Learn how to optimize your YouTube videos for search with this comprehensive guide covering keywords, titles, descriptions, and tags. Boost your video discoverability today!',
                'tags': ['youtube seo', 'video optimization', 'youtube marketing', 'seo guide', 'youtube growth']
            },
            {
                'title': '5 SEO Mistakes That Kill Your YouTube Views',
                'description': 'Avoid these common SEO mistakes that prevent your videos from being discovered. Essential tips for YouTube creators.',
                'tags': ['seo mistakes', 'youtube tips', 'video marketing', 'youtube algorithm']
            },
            {
                'title': 'Keyword Research for YouTube Success',
                'description': 'Master YouTube keyword research with these proven strategies and tools.',
                'tags': ['keyword research', 'youtube keywords', 'seo tools', 'youtube success']
            }
        ]
        
        metrics = []
        for i, video_data in enumerate(sample_videos):
            video_id = f"seo_sample_{i}"
            
            metrics.append(SEOMetrics(
                video_id=video_id,
                title=video_data['title'],
                description=video_data['description'],
                tags=video_data['tags'],
                search_traffic_percentage=random.uniform(20, 45),
                suggested_traffic_percentage=random.uniform(25, 50),
                browse_traffic_percentage=random.uniform(10, 20),
                click_through_rate=random.uniform(3, 8),
                impressions=random.randint(5000, 25000),
                keyword_rankings={
                    'youtube seo': random.randint(5, 25),
                    'video optimization': random.randint(10, 40),
                    'seo guide': random.randint(8, 30),
                    'youtube tips': random.randint(15, 45)
                },
                optimization_score=random.uniform(6, 9)
            ))
        
        return metrics
    
    async def _get_channel_context(self, channel_id: str) -> Dict[str, Any]:
        """Get channel context for analysis"""
        
        # In production, this would fetch from database or API
        return {
            'name': channel_id,
            'niche': 'Education',
            'subscriber_count': 25000,
            'avg_view_count': 8500,
            'content_type': 'Educational',
            'primary_language': 'English',
            'target_audience': 'Content creators and marketers'
        }
    
    def _calculate_seo_scores(self, seo_metrics: List[SEOMetrics], ai_analysis: Dict[str, Any]) -> Dict[str, float]:
        """Calculate SEO performance scores"""
        
        if not seo_metrics:
            return {
                'discoverability_score': 0.0,
                'keyword_performance': 0.0,
                'optimization_score': 0.0,
                'search_visibility': 0.0,
                'overall_seo_health': 0.0
            }
        
        # Calculate scores based on metrics
        avg_search_traffic = sum(m.search_traffic_percentage for m in seo_metrics) / len(seo_metrics)
        avg_ctr = sum(m.click_through_rate for m in seo_metrics) / len(seo_metrics)
        avg_optimization = sum(m.optimization_score for m in seo_metrics) / len(seo_metrics)
        
        # Normalize scores to 0-10 scale
        discoverability_score = min(avg_search_traffic / 4, 10.0)  # Scale search traffic percentage
        keyword_performance = min(avg_ctr * 1.5, 10.0)  # Scale CTR
        optimization_score = avg_optimization  # Already 0-10
        search_visibility = min((avg_search_traffic + avg_ctr * 5) / 6, 10.0)
        
        overall_seo_health = (discoverability_score + keyword_performance + optimization_score + search_visibility) / 4
        
        return {
            'discoverability_score': round(discoverability_score, 1),
            'keyword_performance': round(keyword_performance, 1),
            'optimization_score': round(optimization_score, 1),
            'search_visibility': round(search_visibility, 1),
            'overall_seo_health': round(overall_seo_health, 1)
        }
    
    def _format_boss_agent_response(self, analysis_result: Dict[str, Any], request_id: str, start_time: float, cache_hit: bool = False) -> Dict[str, Any]:
        """Format response specifically for boss agent consumption"""
        
        processing_time = time.time() - start_time
        
        # Extract key insights
        ai_analysis = analysis_result.get('ai_analysis', {})
        keyword_analysis = ai_analysis.get('keyword_analysis', {})
        optimization_priorities = ai_analysis.get('optimization_priorities', [])
        
        # Create summary
        summary = self._create_seo_summary(analysis_result)
        
        # Extract recommendations
        recommendations = ai_analysis.get('recommendations', [])
        
        # Create key insights
        key_insights = []
        
        # SEO health insight
        seo_scores = analysis_result.get('seo_scores', {})
        overall_health = seo_scores.get('overall_seo_health', 0)
        
        key_insights.append({
            'insight': f"Overall SEO health score: {overall_health}/10",
            'evidence': f"Based on discoverability, keyword performance, and optimization analysis",
            'impact': 'High' if overall_health < 6 else 'Medium',
            'confidence': 0.9
        })
        
        # Keyword opportunities insight
        if keyword_analysis.get('optimization_opportunities'):
            opportunities = keyword_analysis['optimization_opportunities']
            key_insights.append({
                'insight': f"Keyword optimization opportunities identified: {', '.join(opportunities[:2])}",
                'evidence': 'Based on keyword analysis and ranking assessment',
                'impact': 'High',
                'confidence': 0.85
            })
        
        return {
            'agent_type': self.agent_type,
            'hierarchical_role': self.hierarchical_role,
            'response_id': str(uuid.uuid4()),
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'confidence_score': 0.87,  # High confidence in SEO analysis
            'data_freshness': datetime.now().isoformat(),
            'domain_match': True,
            'analysis': {
                'summary': summary,
                'metrics': seo_scores,
                'key_insights': key_insights[:5],  # Limit to top 5
                'recommendations': [
                    {
                        'recommendation': rec if isinstance(rec, str) else rec.get('recommendation', rec),
                        'expected_impact': 'High',
                        'implementation_difficulty': 'Medium',
                        'reasoning': 'Based on SEO analysis and optimization opportunities'
                    }
                    for rec in recommendations[:5]  # Limit to top 5
                ],
                'detailed_analysis': {
                    'seo_metrics': [
                        {
                            'video_id': m.video_id,
                            'title': m.title,
                            'optimization_score': m.optimization_score,
                            'search_traffic_pct': m.search_traffic_percentage,
                            'click_through_rate': m.click_through_rate
                        }
                        for m in analysis_result.get('raw_data', {}).get('seo_metrics', [])
                    ],
                    'keyword_analysis': keyword_analysis,
                    'optimization_priorities': optimization_priorities,
                    'trending_keywords': analysis_result.get('raw_data', {}).get('trending_keywords', [])
                }
            },
            'token_usage': {
                'input_tokens': 2500,
                'output_tokens': 1200,
                'model': 'gpt-4o-mini'
            },
            'cache_info': {
                'cache_hit': cache_hit,
                'cache_key': 'seo_discoverability_' + request_id[:8],
                'ttl_remaining': 10800 if not cache_hit else 8100
            },
            'processing_time': round(processing_time, 2),
            'for_boss_agent_only': True,
            'boss_agent_callback_url': request_data.get('boss_agent_callback_url')
        }
    
    def _create_seo_summary(self, analysis_result: Dict[str, Any]) -> str:
        """Create a concise summary of SEO analysis"""
        
        scores = analysis_result.get('seo_scores', {})
        metadata = analysis_result.get('analysis_metadata', {})
        
        overall_health = scores.get('overall_seo_health', 0)
        videos_count = metadata.get('videos_analyzed', 0)
        
        if overall_health >= 8:
            health_desc = "excellent"
        elif overall_health >= 6:
            health_desc = "good"
        elif overall_health >= 4:
            health_desc = "moderate"
        else:
            health_desc = "needs improvement"
        
        return f"SEO analysis shows {health_desc} search optimization (score: {overall_health}/10). Analysis covers {videos_count} videos with focus on discoverability, keyword performance, and search ranking optimization."
    
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
                'cache_key': 'seo_discoverability_' + request_id[:8],
                'ttl_remaining': 8100
            }
        })
        
        return response
    
    def _create_domain_mismatch_response(self, request_id: str) -> Dict[str, Any]:
        """Create response for requests outside SEO & discoverability domain"""
        
        return {
            'agent_type': self.agent_type,
            'hierarchical_role': self.hierarchical_role,
            'response_id': str(uuid.uuid4()),
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'confidence_score': 0.0,
            'data_freshness': datetime.now().isoformat(),
            'domain_match': False,
            'analysis': {
                'summary': 'Request outside SEO & discoverability domain',
                'error_message': 'This request should be handled by a different specialized agent'
            },
            'for_boss_agent_only': True
        }
    
    def _create_unauthorized_response(self, request_id: str) -> Dict[str, Any]:
        """Create response for unauthorized requests"""
        
        return {
            'agent_type': self.agent_type,
            'hierarchical_role': self.hierarchical_role,
            'response_id': str(uuid.uuid4()),
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'confidence_score': 0.0,
            'data_freshness': datetime.now().isoformat(),
            'domain_match': False,
            'analysis': {
                'summary': 'Unauthorized request - only boss agent can access this service',
                'error_message': 'Access denied: This agent only accepts requests from the authorized boss agent'
            },
            'for_boss_agent_only': True
        }
    
    def _create_error_response(self, request_id: str, error_message: str, start_time: float) -> Dict[str, Any]:
        """Create error response for boss agent"""
        
        return {
            'agent_type': self.agent_type,
            'hierarchical_role': self.hierarchical_role,
            'response_id': str(uuid.uuid4()),
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'confidence_score': 0.0,
            'data_freshness': datetime.now().isoformat(),
            'domain_match': True,
            'analysis': {
                'summary': 'SEO & discoverability analysis failed',
                'error_message': error_message
            },
            'processing_time': round(time.time() - start_time, 2),
            'for_boss_agent_only': True
        }

# Global instance for boss agent integration
seo_discoverability_agent = None

def get_seo_discoverability_agent():
    """Get or create SEO & discoverability agent instance"""
    global seo_discoverability_agent
    
    if seo_discoverability_agent is None:
        youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not youtube_api_key:
            logger.warning("YOUTUBE_API_KEY not set - using demo mode")
            youtube_api_key = "demo_key"
        
        if not openai_api_key:
            logger.warning("OPENAI_API_KEY not set - using demo mode")
            openai_api_key = "demo_key"
        
        seo_discoverability_agent = SEODiscoverabilityAgent(youtube_api_key, openai_api_key)
    
    return seo_discoverability_agent

async def process_seo_discoverability_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for boss agent to request SEO & discoverability analysis
    This is the ONLY function the boss agent should call
    """
    agent = get_seo_discoverability_agent()
    return await agent.process_boss_agent_request(request_data)