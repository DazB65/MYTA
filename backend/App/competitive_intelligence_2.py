"""
Competitive Intelligence 2.0 Engine
Advanced market positioning and competitive strategy analysis
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import json
import statistics

from .enhanced_user_context import EnhancedUserContextManager
from .advanced_prediction_engine import get_prediction_engine

logger = logging.getLogger(__name__)

class CompetitorTier(Enum):
    DIRECT = "direct"           # Same niche, similar size
    ASPIRATIONAL = "aspirational"  # Same niche, larger
    ADJACENT = "adjacent"       # Related niche, similar size
    EMERGING = "emerging"       # Same niche, smaller but growing

class OpportunityType(Enum):
    CONTENT_GAP = "content_gap"
    TIMING_ADVANTAGE = "timing_advantage"
    FORMAT_INNOVATION = "format_innovation"
    AUDIENCE_OVERLAP = "audience_overlap"
    TRENDING_TOPIC = "trending_topic"
    BLUE_OCEAN = "blue_ocean"

class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class CompetitorProfile:
    """Comprehensive competitor analysis profile"""
    competitor_id: str
    name: str
    channel_url: str
    tier: CompetitorTier
    subscriber_count: int
    avg_views: float
    upload_frequency: float
    content_categories: List[str]
    top_performing_content: List[Dict[str, Any]]
    growth_rate: float
    engagement_rate: float
    posting_schedule: Dict[str, Any]
    content_strategy: Dict[str, Any]
    strengths: List[str]
    weaknesses: List[str]
    last_analyzed: datetime

@dataclass
class ContentGap:
    """Identified content gap opportunity"""
    gap_id: str
    topic: str
    search_volume: int
    competition_level: str  # low, medium, high
    opportunity_score: float
    missing_competitors: List[str]
    potential_views: int
    difficulty_rating: float
    suggested_approach: str
    keywords: List[str]
    content_format: str
    estimated_effort: str

@dataclass
class MarketOpportunity:
    """Strategic market opportunity"""
    opportunity_id: str
    type: OpportunityType
    title: str
    description: str
    opportunity_score: float
    effort_required: str
    time_sensitivity: str
    potential_impact: str
    action_steps: List[str]
    success_metrics: List[str]
    competitors_missing: List[str]
    market_size: Optional[int]

@dataclass
class CompetitiveThreat:
    """Identified competitive threat"""
    threat_id: str
    competitor_name: str
    threat_level: ThreatLevel
    threat_type: str
    description: str
    impact_assessment: str
    timeline: str
    mitigation_strategies: List[str]
    monitoring_metrics: List[str]
    detected_at: datetime

@dataclass
class BlueOceanOpportunity:
    """Untapped market opportunity"""
    ocean_id: str
    market_name: str
    market_size: int
    competition_density: float
    entry_difficulty: str
    potential_roi: float
    unique_value_proposition: str
    target_audience: Dict[str, Any]
    content_strategy: Dict[str, Any]
    success_probability: float
    investment_required: str

class CompetitiveIntelligence2Engine:
    """Advanced competitive intelligence and market analysis engine"""
    
    def __init__(self):
        self.context_service = EnhancedUserContextManager()
        self.prediction_engine = get_prediction_engine()
        
        # Competitive data storage
        self.competitor_profiles = {}
        self.content_gaps = {}
        self.market_opportunities = {}
        self.competitive_threats = {}
        self.blue_ocean_opportunities = {}
        
        logger.info("Competitive Intelligence 2.0 Engine initialized")
    
    async def analyze_competitive_landscape(
        self, 
        user_id: str, 
        analysis_depth: str = "comprehensive"
    ) -> Dict[str, Any]:
        """
        Perform comprehensive competitive landscape analysis
        
        Args:
            user_id: User identifier
            analysis_depth: Level of analysis (quick, standard, comprehensive)
        
        Returns:
            Complete competitive intelligence report
        """
        try:
            logger.info(f"🔍 Analyzing competitive landscape for user {user_id}")
            
            # Get enhanced user context
            enhanced_context = await self.context_service.get_enhanced_context(user_id)
            
            # Identify and analyze competitors
            competitors = await self._identify_competitors(user_id, enhanced_context)
            competitor_analysis = await self._analyze_competitors(competitors, enhanced_context)
            
            # Find content gaps and opportunities
            content_gaps = await self._identify_content_gaps(user_id, competitors, enhanced_context)
            market_opportunities = await self._identify_market_opportunities(user_id, competitors, enhanced_context)
            
            # Assess competitive threats
            threats = await self._assess_competitive_threats(user_id, competitors, enhanced_context)
            
            # Discover blue ocean opportunities
            blue_oceans = await self._discover_blue_ocean_opportunities(user_id, enhanced_context)
            
            # Generate strategic recommendations
            strategic_recommendations = await self._generate_strategic_recommendations(
                user_id, competitor_analysis, content_gaps, market_opportunities, threats, blue_oceans
            )
            
            # Compile comprehensive report
            intelligence_report = {
                'analysis_timestamp': datetime.now().isoformat(),
                'analysis_depth': analysis_depth,
                'competitive_landscape': {
                    'total_competitors': len(competitors),
                    'direct_competitors': len([c for c in competitors if c.tier == CompetitorTier.DIRECT]),
                    'aspirational_targets': len([c for c in competitors if c.tier == CompetitorTier.ASPIRATIONAL]),
                    'market_position': await self._calculate_market_position(user_id, competitors, enhanced_context)
                },
                'competitor_profiles': [asdict(comp) for comp in competitor_analysis],
                'content_gaps': [asdict(gap) for gap in content_gaps],
                'market_opportunities': [asdict(opp) for opp in market_opportunities],
                'competitive_threats': [asdict(threat) for threat in threats],
                'blue_ocean_opportunities': [asdict(ocean) for ocean in blue_oceans],
                'strategic_recommendations': strategic_recommendations,
                'next_analysis_date': (datetime.now() + timedelta(days=7)).isoformat()
            }
            
            logger.info(f"✅ Competitive analysis completed: {len(competitors)} competitors, {len(content_gaps)} gaps, {len(market_opportunities)} opportunities")
            return intelligence_report
            
        except Exception as e:
            logger.error(f"Error in competitive landscape analysis: {e}")
            return {
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat(),
                'status': 'failed'
            }
    
    async def _identify_competitors(
        self, 
        user_id: str, 
        enhanced_context: Dict[str, Any]
    ) -> List[CompetitorProfile]:
        """Identify and categorize competitors"""
        
        # Get user's niche and characteristics
        channel_info = enhanced_context.get('channel_info', {})
        user_niche = channel_info.get('niche', 'general')
        user_subscribers = channel_info.get('subscriber_count', 0)
        
        # Mock competitor data (in production, would use YouTube API, Social Blade, etc.)
        mock_competitors = [
            {
                'name': 'TechReview Pro',
                'channel_url': 'https://youtube.com/techreviewpro',
                'subscriber_count': user_subscribers * 2.5,
                'avg_views': 45000,
                'upload_frequency': 3.5,
                'niche': user_niche,
                'growth_rate': 0.15
            },
            {
                'name': 'Digital Creator Hub',
                'channel_url': 'https://youtube.com/digitalcreatorhub',
                'subscriber_count': user_subscribers * 0.8,
                'avg_views': 25000,
                'upload_frequency': 5.2,
                'niche': user_niche,
                'growth_rate': 0.25
            },
            {
                'name': 'Content Master',
                'channel_url': 'https://youtube.com/contentmaster',
                'subscriber_count': user_subscribers * 1.2,
                'avg_views': 35000,
                'upload_frequency': 2.8,
                'niche': user_niche,
                'growth_rate': 0.08
            }
        ]
        
        competitors = []
        for i, comp_data in enumerate(mock_competitors):
            # Determine competitor tier
            tier = self._determine_competitor_tier(user_subscribers, comp_data['subscriber_count'], comp_data['growth_rate'])
            
            competitor = CompetitorProfile(
                competitor_id=f"comp_{i+1}",
                name=comp_data['name'],
                channel_url=comp_data['channel_url'],
                tier=tier,
                subscriber_count=comp_data['subscriber_count'],
                avg_views=comp_data['avg_views'],
                upload_frequency=comp_data['upload_frequency'],
                content_categories=[user_niche, 'tutorials', 'reviews'],
                top_performing_content=[],
                growth_rate=comp_data['growth_rate'],
                engagement_rate=0.045,  # 4.5% average
                posting_schedule={'peak_days': ['tuesday', 'thursday'], 'peak_hours': [19, 20]},
                content_strategy={'focus': 'educational', 'format': 'long-form'},
                strengths=['consistent uploads', 'high production quality'],
                weaknesses=['limited audience interaction', 'slow trend adoption'],
                last_analyzed=datetime.now()
            )
            competitors.append(competitor)
        
        return competitors
    
    def _determine_competitor_tier(self, user_subs: int, comp_subs: int, growth_rate: float) -> CompetitorTier:
        """Determine competitor tier based on size and growth"""
        
        size_ratio = comp_subs / max(user_subs, 1)
        
        if 0.7 <= size_ratio <= 1.5:
            return CompetitorTier.DIRECT
        elif size_ratio > 1.5:
            return CompetitorTier.ASPIRATIONAL
        elif size_ratio < 0.7 and growth_rate > 0.2:
            return CompetitorTier.EMERGING
        else:
            return CompetitorTier.ADJACENT
    
    async def _analyze_competitors(
        self, 
        competitors: List[CompetitorProfile], 
        enhanced_context: Dict[str, Any]
    ) -> List[CompetitorProfile]:
        """Perform detailed analysis of each competitor"""
        
        analyzed_competitors = []
        
        for competitor in competitors:
            # Analyze content strategy
            competitor.content_strategy = await self._analyze_content_strategy(competitor)
            
            # Identify strengths and weaknesses
            competitor.strengths, competitor.weaknesses = await self._analyze_strengths_weaknesses(competitor)
            
            # Analyze top performing content
            competitor.top_performing_content = await self._analyze_top_content(competitor)
            
            analyzed_competitors.append(competitor)
        
        return analyzed_competitors
    
    async def _analyze_content_strategy(self, competitor: CompetitorProfile) -> Dict[str, Any]:
        """Analyze competitor's content strategy"""
        
        # Mock analysis (in production, would analyze actual content)
        strategies = {
            'TechReview Pro': {
                'focus': 'in-depth product reviews',
                'format': 'long-form tutorials',
                'posting_pattern': 'consistent weekly schedule',
                'audience_engagement': 'moderate',
                'monetization': 'affiliate marketing + sponsorships'
            },
            'Digital Creator Hub': {
                'focus': 'quick tips and hacks',
                'format': 'short-form + live streams',
                'posting_pattern': 'high frequency daily posts',
                'audience_engagement': 'high community interaction',
                'monetization': 'course sales + memberships'
            },
            'Content Master': {
                'focus': 'comprehensive guides',
                'format': 'series-based content',
                'posting_pattern': 'bi-weekly deep dives',
                'audience_engagement': 'expert positioning',
                'monetization': 'consulting + premium content'
            }
        }
        
        return strategies.get(competitor.name, {
            'focus': 'general content',
            'format': 'mixed formats',
            'posting_pattern': 'irregular',
            'audience_engagement': 'standard',
            'monetization': 'ad revenue'
        })
    
    async def _analyze_strengths_weaknesses(self, competitor: CompetitorProfile) -> Tuple[List[str], List[str]]:
        """Identify competitor strengths and weaknesses"""
        
        strengths = []
        weaknesses = []
        
        # Analyze based on metrics
        if competitor.upload_frequency > 4:
            strengths.append("High content output")
        elif competitor.upload_frequency < 1:
            weaknesses.append("Inconsistent posting schedule")
        
        if competitor.engagement_rate > 0.05:
            strengths.append("Strong audience engagement")
        elif competitor.engagement_rate < 0.03:
            weaknesses.append("Low audience interaction")
        
        if competitor.growth_rate > 0.15:
            strengths.append("Rapid channel growth")
        elif competitor.growth_rate < 0.05:
            weaknesses.append("Stagnant growth")
        
        # Add specific strengths/weaknesses based on competitor
        competitor_specific = {
            'TechReview Pro': {
                'strengths': ['Professional production quality', 'Detailed analysis', 'Industry credibility'],
                'weaknesses': ['Slow to cover trending topics', 'Limited format variety']
            },
            'Digital Creator Hub': {
                'strengths': ['Quick trend adoption', 'High engagement rate', 'Community building'],
                'weaknesses': ['Inconsistent quality', 'Over-reliance on trends']
            },
            'Content Master': {
                'strengths': ['Expert authority', 'Comprehensive content', 'Premium positioning'],
                'weaknesses': ['Low posting frequency', 'Limited audience reach']
            }
        }
        
        specific = competitor_specific.get(competitor.name, {'strengths': [], 'weaknesses': []})
        strengths.extend(specific['strengths'])
        weaknesses.extend(specific['weaknesses'])
        
        return strengths, weaknesses

    async def _analyze_top_content(self, competitor: CompetitorProfile) -> List[Dict[str, Any]]:
        """Analyze competitor's top performing content"""

        # Mock top content analysis (in production, would use YouTube API)
        top_content_templates = {
            'TechReview Pro': [
                {'title': 'Complete Guide to [Product] - Everything You Need to Know', 'views': 125000, 'engagement': 0.067},
                {'title': 'Why [Product] is Better Than [Competitor Product]', 'views': 98000, 'engagement': 0.054},
                {'title': '[Product] After 6 Months - Honest Review', 'views': 87000, 'engagement': 0.071}
            ],
            'Digital Creator Hub': [
                {'title': '5 Secrets [Platform] Doesn\'t Want You to Know', 'views': 156000, 'engagement': 0.089},
                {'title': 'I Tried [Trend] for 30 Days - Here\'s What Happened', 'views': 134000, 'engagement': 0.076},
                {'title': 'How to [Skill] in 10 Minutes (Beginner Friendly)', 'views': 112000, 'engagement': 0.082}
            ],
            'Content Master': [
                {'title': 'The Ultimate [Topic] Masterclass (2+ Hours)', 'views': 89000, 'engagement': 0.045},
                {'title': 'Advanced [Technique] - Professional Level Tutorial', 'views': 76000, 'engagement': 0.038},
                {'title': '[Topic] Mistakes That Are Killing Your Results', 'views': 94000, 'engagement': 0.052}
            ]
        }

        return top_content_templates.get(competitor.name, [
            {'title': 'Generic Popular Video', 'views': 50000, 'engagement': 0.04}
        ])

    async def _identify_content_gaps(
        self,
        user_id: str,
        competitors: List[CompetitorProfile],
        enhanced_context: Dict[str, Any]
    ) -> List[ContentGap]:
        """Identify content gaps in the market"""

        channel_info = enhanced_context.get('channel_info', {})
        user_niche = channel_info.get('niche', 'general')

        # Mock content gap analysis
        potential_gaps = [
            {
                'topic': f'{user_niche} for Complete Beginners',
                'search_volume': 12000,
                'competition_level': 'low',
                'missing_competitors': ['TechReview Pro', 'Content Master'],
                'content_format': 'step-by-step tutorial series'
            },
            {
                'topic': f'Advanced {user_niche} Techniques',
                'search_volume': 8500,
                'competition_level': 'medium',
                'missing_competitors': ['Digital Creator Hub'],
                'content_format': 'in-depth masterclass'
            },
            {
                'topic': f'{user_niche} Tools Comparison 2024',
                'search_volume': 15000,
                'competition_level': 'low',
                'missing_competitors': ['TechReview Pro', 'Digital Creator Hub'],
                'content_format': 'comparison review'
            },
            {
                'topic': f'Common {user_niche} Mistakes to Avoid',
                'search_volume': 9800,
                'competition_level': 'medium',
                'missing_competitors': ['Content Master'],
                'content_format': 'educational breakdown'
            }
        ]

        content_gaps = []
        for i, gap_data in enumerate(potential_gaps):
            # Calculate opportunity score
            opportunity_score = self._calculate_opportunity_score(
                gap_data['search_volume'],
                gap_data['competition_level'],
                len(gap_data['missing_competitors'])
            )

            gap = ContentGap(
                gap_id=f"gap_{i+1}",
                topic=gap_data['topic'],
                search_volume=gap_data['search_volume'],
                competition_level=gap_data['competition_level'],
                opportunity_score=opportunity_score,
                missing_competitors=gap_data['missing_competitors'],
                potential_views=int(gap_data['search_volume'] * 0.15),  # 15% capture rate
                difficulty_rating=self._calculate_difficulty_rating(gap_data['competition_level']),
                suggested_approach=f"Create comprehensive {gap_data['content_format']} covering this topic",
                keywords=self._generate_keywords(gap_data['topic']),
                content_format=gap_data['content_format'],
                estimated_effort=self._estimate_effort(gap_data['content_format'])
            )
            content_gaps.append(gap)

        # Sort by opportunity score
        content_gaps.sort(key=lambda x: x.opportunity_score, reverse=True)
        return content_gaps[:10]  # Return top 10 gaps

    def _calculate_opportunity_score(self, search_volume: int, competition_level: str, missing_count: int) -> float:
        """Calculate opportunity score for content gap"""

        # Base score from search volume
        volume_score = min(search_volume / 20000, 1.0)  # Normalize to 1.0

        # Competition multiplier
        competition_multipliers = {'low': 1.5, 'medium': 1.0, 'high': 0.6}
        competition_score = competition_multipliers.get(competition_level, 1.0)

        # Missing competitors bonus
        missing_bonus = min(missing_count * 0.2, 0.8)

        opportunity_score = (volume_score * competition_score + missing_bonus) * 100
        return round(min(opportunity_score, 100), 1)

    def _calculate_difficulty_rating(self, competition_level: str) -> float:
        """Calculate difficulty rating for content gap"""
        difficulty_map = {'low': 2.5, 'medium': 5.0, 'high': 8.0}
        return difficulty_map.get(competition_level, 5.0)

    def _generate_keywords(self, topic: str) -> List[str]:
        """Generate relevant keywords for topic"""
        base_keywords = topic.lower().split()
        additional_keywords = ['tutorial', 'guide', 'how to', 'tips', 'best', '2024']
        return base_keywords + additional_keywords[:3]

    def _estimate_effort(self, content_format: str) -> str:
        """Estimate effort required for content format"""
        effort_map = {
            'step-by-step tutorial series': 'High (10-15 hours)',
            'in-depth masterclass': 'Very High (20+ hours)',
            'comparison review': 'Medium (5-8 hours)',
            'educational breakdown': 'Medium (4-6 hours)'
        }
        return effort_map.get(content_format, 'Medium (5-8 hours)')

    async def _identify_market_opportunities(
        self,
        user_id: str,
        competitors: List[CompetitorProfile],
        enhanced_context: Dict[str, Any]
    ) -> List[MarketOpportunity]:
        """Identify strategic market opportunities"""

        opportunities = []

        # Timing advantage opportunities
        timing_opp = MarketOpportunity(
            opportunity_id="timing_001",
            type=OpportunityType.TIMING_ADVANTAGE,
            title="Early Trend Adoption Opportunity",
            description="Competitors are slow to adopt new trends. You can gain first-mover advantage.",
            opportunity_score=85.0,
            effort_required="Medium",
            time_sensitivity="High - Act within 2 weeks",
            potential_impact="High - 40-60% view increase",
            action_steps=[
                "Monitor trending topics daily",
                "Create content within 24-48 hours of trend emergence",
                "Use trending hashtags and keywords",
                "Engage with trend-related comments"
            ],
            success_metrics=["View count increase", "Subscriber growth rate", "Engagement rate"],
            competitors_missing=["TechReview Pro", "Content Master"],
            market_size=50000
        )
        opportunities.append(timing_opp)

        # Format innovation opportunity
        format_opp = MarketOpportunity(
            opportunity_id="format_001",
            type=OpportunityType.FORMAT_INNOVATION,
            title="Interactive Content Format Gap",
            description="No competitors are using interactive formats like polls, Q&A, or live collaboration.",
            opportunity_score=78.0,
            effort_required="Medium",
            time_sensitivity="Medium - 1-2 months",
            potential_impact="Medium - 25-35% engagement increase",
            action_steps=[
                "Experiment with YouTube polls and community posts",
                "Host live Q&A sessions",
                "Create collaborative content with audience",
                "Use interactive elements in videos"
            ],
            success_metrics=["Engagement rate", "Community post interactions", "Live stream attendance"],
            competitors_missing=["TechReview Pro", "Digital Creator Hub", "Content Master"],
            market_size=30000
        )
        opportunities.append(format_opp)

        # Audience overlap opportunity
        audience_opp = MarketOpportunity(
            opportunity_id="audience_001",
            type=OpportunityType.AUDIENCE_OVERLAP,
            title="Cross-Niche Audience Capture",
            description="Opportunity to capture audience from adjacent niches that competitors ignore.",
            opportunity_score=72.0,
            effort_required="Low",
            time_sensitivity="Low - 3-6 months",
            potential_impact="Medium - 20-30% audience expansion",
            action_steps=[
                "Create content bridging your niche with adjacent topics",
                "Collaborate with creators in adjacent niches",
                "Use cross-niche keywords in content",
                "Engage with adjacent niche communities"
            ],
            success_metrics=["Subscriber diversity", "Cross-niche engagement", "Collaboration success"],
            competitors_missing=["Content Master"],
            market_size=75000
        )
        opportunities.append(audience_opp)

        return opportunities

    async def _assess_competitive_threats(
        self,
        user_id: str,
        competitors: List[CompetitorProfile],
        enhanced_context: Dict[str, Any]
    ) -> List[CompetitiveThreat]:
        """Assess potential competitive threats"""

        threats = []

        # High growth competitor threat
        for competitor in competitors:
            if competitor.growth_rate > 0.2:  # 20% growth rate
                threat = CompetitiveThreat(
                    threat_id=f"threat_{competitor.competitor_id}",
                    competitor_name=competitor.name,
                    threat_level=ThreatLevel.HIGH,
                    threat_type="Rapid Growth Competitor",
                    description=f"{competitor.name} is growing at {competitor.growth_rate*100:.1f}% monthly and may capture market share.",
                    impact_assessment="Potential 15-25% audience overlap loss",
                    timeline="3-6 months",
                    mitigation_strategies=[
                        "Accelerate content production",
                        "Focus on unique value proposition",
                        "Improve content quality and engagement",
                        "Strengthen community building"
                    ],
                    monitoring_metrics=["Relative growth rate", "Audience overlap", "Content similarity"],
                    detected_at=datetime.now()
                )
                threats.append(threat)

        # Content saturation threat
        saturation_threat = CompetitiveThreat(
            threat_id="threat_saturation",
            competitor_name="Market Saturation",
            threat_level=ThreatLevel.MEDIUM,
            threat_type="Market Saturation",
            description="Increasing number of creators in your niche may lead to audience fragmentation.",
            impact_assessment="Potential 10-20% view decrease due to increased competition",
            timeline="6-12 months",
            mitigation_strategies=[
                "Develop unique content angles",
                "Build stronger audience loyalty",
                "Expand into adjacent niches",
                "Focus on premium content quality"
            ],
            monitoring_metrics=["Market competition density", "Audience retention", "Unique value metrics"],
            detected_at=datetime.now()
        )
        threats.append(saturation_threat)

        return threats

    async def _discover_blue_ocean_opportunities(
        self,
        user_id: str,
        enhanced_context: Dict[str, Any]
    ) -> List[BlueOceanOpportunity]:
        """Discover untapped blue ocean market opportunities"""

        channel_info = enhanced_context.get('channel_info', {})
        user_niche = channel_info.get('niche', 'general')

        blue_oceans = []

        # Micro-niche opportunity
        micro_niche = BlueOceanOpportunity(
            ocean_id="blue_001",
            market_name=f"Beginner-Friendly {user_niche} for Non-Tech Audience",
            market_size=25000,
            competition_density=0.2,  # Very low competition
            entry_difficulty="Low",
            potential_roi=3.5,
            unique_value_proposition="Simplify complex topics for complete beginners with zero technical background",
            target_audience={
                "demographics": "35-55 years old, non-technical professionals",
                "pain_points": ["Intimidated by technical jargon", "Need practical applications"],
                "content_preferences": ["Step-by-step guides", "Real-world examples", "Patient explanations"]
            },
            content_strategy={
                "format": "Ultra-beginner friendly tutorials",
                "tone": "Patient and encouraging",
                "structure": "Small digestible steps with lots of encouragement",
                "examples": "Real-world scenarios they can relate to"
            },
            success_probability=0.85,
            investment_required="Low - Adjust existing content approach"
        )
        blue_oceans.append(micro_niche)

        # Cross-industry application
        cross_industry = BlueOceanOpportunity(
            ocean_id="blue_002",
            market_name=f"{user_niche} Applications in Healthcare/Education",
            market_size=40000,
            competition_density=0.1,  # Almost no competition
            entry_difficulty="Medium",
            potential_roi=4.2,
            unique_value_proposition="Bridge technology with traditional industries that are underserved",
            target_audience={
                "demographics": "Healthcare/education professionals, 28-50 years old",
                "pain_points": ["Industry-specific challenges", "Limited tech resources", "Compliance requirements"],
                "content_preferences": ["Industry-specific examples", "Compliance-aware solutions", "ROI-focused content"]
            },
            content_strategy={
                "format": "Industry-specific case studies and tutorials",
                "tone": "Professional and authoritative",
                "structure": "Problem-solution format with industry context",
                "examples": "Real healthcare/education scenarios"
            },
            success_probability=0.75,
            investment_required="Medium - Requires industry research and partnerships"
        )
        blue_oceans.append(cross_industry)

        # Accessibility-focused market
        accessibility_market = BlueOceanOpportunity(
            ocean_id="blue_003",
            market_name=f"Accessible {user_niche} for People with Disabilities",
            market_size=15000,
            competition_density=0.05,  # Virtually no competition
            entry_difficulty="Medium",
            potential_roi=5.0,
            unique_value_proposition="First creator to make technology truly accessible for people with disabilities",
            target_audience={
                "demographics": "People with visual, hearing, or motor disabilities",
                "pain_points": ["Inaccessible content", "Lack of adaptive solutions", "Limited representation"],
                "content_preferences": ["Audio descriptions", "Closed captions", "Adaptive technology focus"]
            },
            content_strategy={
                "format": "Fully accessible tutorials with multiple format options",
                "tone": "Inclusive and empowering",
                "structure": "Multiple accessibility options for each piece of content",
                "examples": "Adaptive technology demonstrations"
            },
            success_probability=0.90,
            investment_required="Medium - Accessibility tools and training required"
        )
        blue_oceans.append(accessibility_market)

        return blue_oceans

    async def _calculate_market_position(
        self,
        user_id: str,
        competitors: List[CompetitorProfile],
        enhanced_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate user's current market position relative to competitors"""

        channel_info = enhanced_context.get('channel_info', {})
        user_subscribers = channel_info.get('subscriber_count', 0)
        user_avg_views = channel_info.get('avg_views', 0)
        user_growth_rate = channel_info.get('growth_rate', 0.05)

        # Calculate percentile rankings
        competitor_subs = [comp.subscriber_count for comp in competitors]
        competitor_views = [comp.avg_views for comp in competitors]
        competitor_growth = [comp.growth_rate for comp in competitors]

        sub_percentile = self._calculate_percentile(user_subscribers, competitor_subs)
        view_percentile = self._calculate_percentile(user_avg_views, competitor_views)
        growth_percentile = self._calculate_percentile(user_growth_rate, competitor_growth)

        # Overall market position
        overall_score = (sub_percentile + view_percentile + growth_percentile) / 3

        # Position category
        if overall_score >= 80:
            position_category = "Market Leader"
        elif overall_score >= 60:
            position_category = "Strong Competitor"
        elif overall_score >= 40:
            position_category = "Growing Player"
        elif overall_score >= 20:
            position_category = "Emerging Creator"
        else:
            position_category = "New Entrant"

        return {
            'overall_score': round(overall_score, 1),
            'position_category': position_category,
            'subscriber_percentile': round(sub_percentile, 1),
            'view_percentile': round(view_percentile, 1),
            'growth_percentile': round(growth_percentile, 1),
            'competitive_advantages': self._identify_competitive_advantages(
                user_subscribers, user_avg_views, user_growth_rate, competitors
            ),
            'improvement_areas': self._identify_improvement_areas(
                user_subscribers, user_avg_views, user_growth_rate, competitors
            )
        }

    def _calculate_percentile(self, user_value: float, competitor_values: List[float]) -> float:
        """Calculate percentile ranking against competitors"""
        if not competitor_values:
            return 50.0

        all_values = competitor_values + [user_value]
        all_values.sort()

        user_rank = all_values.index(user_value) + 1
        percentile = (user_rank / len(all_values)) * 100

        return percentile

    def _identify_competitive_advantages(
        self,
        user_subs: int,
        user_views: float,
        user_growth: float,
        competitors: List[CompetitorProfile]
    ) -> List[str]:
        """Identify user's competitive advantages"""

        advantages = []

        # Growth rate advantage
        avg_competitor_growth = statistics.mean([comp.growth_rate for comp in competitors])
        if user_growth > avg_competitor_growth * 1.2:
            advantages.append("Above-average growth rate")

        # Engagement advantage (mock calculation)
        user_engagement = 0.055  # Mock user engagement rate
        avg_competitor_engagement = statistics.mean([comp.engagement_rate for comp in competitors])
        if user_engagement > avg_competitor_engagement * 1.1:
            advantages.append("Strong audience engagement")

        # Consistency advantage (mock)
        advantages.append("Consistent content quality")

        return advantages

    def _identify_improvement_areas(
        self,
        user_subs: int,
        user_views: float,
        user_growth: float,
        competitors: List[CompetitorProfile]
    ) -> List[str]:
        """Identify areas for improvement"""

        improvements = []

        # Subscriber count
        max_competitor_subs = max([comp.subscriber_count for comp in competitors])
        if user_subs < max_competitor_subs * 0.5:
            improvements.append("Increase subscriber acquisition")

        # View count
        max_competitor_views = max([comp.avg_views for comp in competitors])
        if user_views < max_competitor_views * 0.6:
            improvements.append("Improve content discoverability")

        # Upload frequency (mock)
        improvements.append("Consider increasing upload frequency")

        return improvements

    async def _generate_strategic_recommendations(
        self,
        user_id: str,
        competitors: List[CompetitorProfile],
        content_gaps: List[ContentGap],
        opportunities: List[MarketOpportunity],
        threats: List[CompetitiveThreat],
        blue_oceans: List[BlueOceanOpportunity]
    ) -> Dict[str, Any]:
        """Generate comprehensive strategic recommendations"""

        recommendations = {
            'immediate_actions': [],
            'short_term_strategy': [],
            'long_term_vision': [],
            'competitive_positioning': [],
            'content_strategy': [],
            'growth_tactics': []
        }

        # Immediate actions (next 2 weeks)
        if content_gaps:
            top_gap = content_gaps[0]
            recommendations['immediate_actions'].append({
                'action': f"Create content for '{top_gap.topic}'",
                'priority': 'High',
                'effort': top_gap.estimated_effort,
                'expected_impact': f"{top_gap.potential_views:,} potential views"
            })

        if opportunities:
            top_opportunity = max(opportunities, key=lambda x: x.opportunity_score)
            recommendations['immediate_actions'].append({
                'action': f"Execute {top_opportunity.title}",
                'priority': 'High',
                'effort': top_opportunity.effort_required,
                'expected_impact': top_opportunity.potential_impact
            })

        # Short-term strategy (1-3 months)
        recommendations['short_term_strategy'].extend([
            {
                'strategy': 'Content Gap Exploitation',
                'description': f"Target top {min(3, len(content_gaps))} content gaps for quick wins",
                'timeline': '1-2 months',
                'success_metrics': ['View count increase', 'Subscriber growth', 'Search ranking improvement']
            },
            {
                'strategy': 'Competitive Differentiation',
                'description': 'Develop unique content angles that competitors are missing',
                'timeline': '2-3 months',
                'success_metrics': ['Brand recognition', 'Audience loyalty', 'Content uniqueness score']
            }
        ])

        # Long-term vision (6-12 months)
        if blue_oceans:
            top_blue_ocean = max(blue_oceans, key=lambda x: x.potential_roi)
            recommendations['long_term_vision'].append({
                'vision': f"Blue Ocean Market Leadership in {top_blue_ocean.market_name}",
                'description': top_blue_ocean.unique_value_proposition,
                'timeline': '6-12 months',
                'investment_required': top_blue_ocean.investment_required,
                'success_probability': f"{top_blue_ocean.success_probability*100:.0f}%"
            })

        # Competitive positioning
        direct_competitors = [comp for comp in competitors if comp.tier == CompetitorTier.DIRECT]
        if direct_competitors:
            recommendations['competitive_positioning'].append({
                'positioning': 'Differentiation Strategy',
                'description': f"Position against {len(direct_competitors)} direct competitors through unique value proposition",
                'key_differentiators': ['Content quality', 'Audience engagement', 'Innovation'],
                'monitoring_required': ['Competitor content analysis', 'Market share tracking']
            })

        # Content strategy
        recommendations['content_strategy'].extend([
            {
                'strategy': 'Content Gap Prioritization',
                'description': 'Focus on high-opportunity, low-competition topics',
                'implementation': 'Use content gap analysis for content calendar planning'
            },
            {
                'strategy': 'Format Innovation',
                'description': 'Experiment with content formats competitors are not using',
                'implementation': 'Test interactive content, live streams, collaborative formats'
            }
        ])

        # Growth tactics
        recommendations['growth_tactics'].extend([
            {
                'tactic': 'First-Mover Advantage',
                'description': 'Be first to cover trending topics in your niche',
                'implementation': 'Set up trend monitoring and rapid content creation workflow'
            },
            {
                'tactic': 'Cross-Niche Expansion',
                'description': 'Capture audience from adjacent niches',
                'implementation': 'Create bridge content connecting your niche to related topics'
            }
        ])

        return recommendations

# Utility functions for the competitive intelligence engine
def get_competitive_intelligence_engine():
    """Get singleton instance of competitive intelligence engine"""
    if not hasattr(get_competitive_intelligence_engine, '_instance'):
        get_competitive_intelligence_engine._instance = CompetitiveIntelligence2Engine()
    return get_competitive_intelligence_engine._instance
