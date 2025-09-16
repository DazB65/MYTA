"""
Agent Performance Analytics System
Track and optimize agent collaboration effectiveness with comprehensive metrics
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import json
import uuid
import statistics
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)

class PerformanceMetric(Enum):
    SUCCESS_RATE = "success_rate"
    RESPONSE_TIME = "response_time"
    CONFIDENCE_SCORE = "confidence_score"
    USER_SATISFACTION = "user_satisfaction"
    COLLABORATION_EFFECTIVENESS = "collaboration_effectiveness"
    INSIGHT_QUALITY = "insight_quality"
    RECOMMENDATION_ACCURACY = "recommendation_accuracy"
    PROACTIVE_SUGGESTIONS = "proactive_suggestions"

class AnalyticsTimeframe(Enum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"

@dataclass
class AgentPerformanceRecord:
    record_id: str
    agent_name: str
    user_id: str
    execution_time: datetime
    success: bool
    response_time: float  # seconds
    confidence_score: float  # 0.0 to 1.0
    user_feedback_score: Optional[float]  # 1.0 to 5.0
    collaboration_partners: List[str]
    insights_generated: int
    recommendations_provided: int
    proactive_suggestions: int
    context: Dict[str, Any]

@dataclass
class CollaborationMetrics:
    collaboration_id: str
    participating_agents: List[str]
    execution_time: datetime
    total_duration: float
    success: bool
    synergy_score: float  # How well agents worked together
    handoff_efficiency: float  # How smoothly context was passed
    outcome_quality: float  # Quality of final result
    user_satisfaction: Optional[float]

@dataclass
class AgentAnalytics:
    agent_name: str
    timeframe: AnalyticsTimeframe
    period_start: datetime
    period_end: datetime
    total_executions: int
    successful_executions: int
    success_rate: float
    average_response_time: float
    average_confidence: float
    average_user_satisfaction: float
    collaboration_count: int
    insights_generated: int
    recommendations_provided: int
    proactive_suggestions: int
    top_collaboration_partners: List[Tuple[str, int]]
    performance_trend: str  # "improving", "stable", "declining"

class AgentPerformanceAnalytics:
    """Comprehensive analytics system for agent performance tracking"""
    
    def __init__(self):
        self.performance_records: List[AgentPerformanceRecord] = []
        self.collaboration_metrics: List[CollaborationMetrics] = []
        self.agent_analytics_cache: Dict[str, Dict[str, AgentAnalytics]] = {}
        self.performance_benchmarks = self._load_performance_benchmarks()
        
    def _load_performance_benchmarks(self) -> Dict[str, Dict[str, float]]:
        """Load performance benchmarks for different agents"""
        return {
            "content_analysis": {
                "target_success_rate": 0.95,
                "target_response_time": 30.0,
                "target_confidence": 0.85,
                "target_user_satisfaction": 4.2
            },
            "audience_insights": {
                "target_success_rate": 0.92,
                "target_response_time": 25.0,
                "target_confidence": 0.80,
                "target_user_satisfaction": 4.0
            },
            "seo_optimization": {
                "target_success_rate": 0.90,
                "target_response_time": 20.0,
                "target_confidence": 0.88,
                "target_user_satisfaction": 4.1
            },
            "competitive_analysis": {
                "target_success_rate": 0.88,
                "target_response_time": 35.0,
                "target_confidence": 0.82,
                "target_user_satisfaction": 4.0
            },
            "monetization": {
                "target_success_rate": 0.85,
                "target_response_time": 30.0,
                "target_confidence": 0.78,
                "target_user_satisfaction": 3.9
            }
        }
    
    async def record_agent_performance(
        self,
        agent_name: str,
        user_id: str,
        success: bool,
        response_time: float,
        confidence_score: float,
        collaboration_partners: List[str] = None,
        insights_generated: int = 0,
        recommendations_provided: int = 0,
        proactive_suggestions: int = 0,
        context: Dict[str, Any] = None
    ) -> str:
        """Record a single agent performance execution"""
        
        record = AgentPerformanceRecord(
            record_id=str(uuid.uuid4()),
            agent_name=agent_name,
            user_id=user_id,
            execution_time=datetime.now(),
            success=success,
            response_time=response_time,
            confidence_score=confidence_score,
            user_feedback_score=None,  # To be updated later
            collaboration_partners=collaboration_partners or [],
            insights_generated=insights_generated,
            recommendations_provided=recommendations_provided,
            proactive_suggestions=proactive_suggestions,
            context=context or {}
        )
        
        self.performance_records.append(record)
        
        # Clear analytics cache for this agent
        if agent_name in self.agent_analytics_cache:
            del self.agent_analytics_cache[agent_name]
        
        logger.info(f"📊 Recorded performance for {agent_name}: success={success}, time={response_time:.1f}s, confidence={confidence_score:.2f}")
        
        return record.record_id
    
    async def record_collaboration_metrics(
        self,
        participating_agents: List[str],
        total_duration: float,
        success: bool,
        synergy_score: float,
        handoff_efficiency: float,
        outcome_quality: float
    ) -> str:
        """Record collaboration performance metrics"""
        
        collaboration = CollaborationMetrics(
            collaboration_id=str(uuid.uuid4()),
            participating_agents=participating_agents,
            execution_time=datetime.now(),
            total_duration=total_duration,
            success=success,
            synergy_score=synergy_score,
            handoff_efficiency=handoff_efficiency,
            outcome_quality=outcome_quality,
            user_satisfaction=None  # To be updated later
        )
        
        self.collaboration_metrics.append(collaboration)
        
        logger.info(f"🤝 Recorded collaboration: {participating_agents}, synergy={synergy_score:.2f}, efficiency={handoff_efficiency:.2f}")
        
        return collaboration.collaboration_id
    
    async def update_user_feedback(self, record_id: str, feedback_score: float) -> bool:
        """Update user feedback score for a performance record"""
        
        for record in self.performance_records:
            if record.record_id == record_id:
                record.user_feedback_score = feedback_score
                logger.info(f"📝 Updated user feedback for {record.agent_name}: {feedback_score}/5.0")
                return True
        
        # Check collaboration metrics
        for collaboration in self.collaboration_metrics:
            if collaboration.collaboration_id == record_id:
                collaboration.user_satisfaction = feedback_score
                logger.info(f"📝 Updated collaboration feedback: {feedback_score}/5.0")
                return True
        
        return False
    
    async def get_agent_analytics(
        self, 
        agent_name: str, 
        timeframe: AnalyticsTimeframe,
        force_refresh: bool = False
    ) -> AgentAnalytics:
        """Get comprehensive analytics for a specific agent"""
        
        cache_key = f"{agent_name}_{timeframe.value}"
        
        # Check cache first
        if not force_refresh and cache_key in self.agent_analytics_cache.get(agent_name, {}):
            cached_analytics = self.agent_analytics_cache[agent_name][cache_key]
            # Check if cache is still fresh (within 1 hour)
            if (datetime.now() - cached_analytics.period_end).total_seconds() < 3600:
                return cached_analytics
        
        # Calculate time period
        period_end = datetime.now()
        if timeframe == AnalyticsTimeframe.HOUR:
            period_start = period_end - timedelta(hours=1)
        elif timeframe == AnalyticsTimeframe.DAY:
            period_start = period_end - timedelta(days=1)
        elif timeframe == AnalyticsTimeframe.WEEK:
            period_start = period_end - timedelta(weeks=1)
        elif timeframe == AnalyticsTimeframe.MONTH:
            period_start = period_end - timedelta(days=30)
        elif timeframe == AnalyticsTimeframe.QUARTER:
            period_start = period_end - timedelta(days=90)
        else:  # YEAR
            period_start = period_end - timedelta(days=365)
        
        # Filter records for this agent and timeframe
        agent_records = [
            record for record in self.performance_records
            if record.agent_name == agent_name and period_start <= record.execution_time <= period_end
        ]
        
        if not agent_records:
            # Return empty analytics
            return AgentAnalytics(
                agent_name=agent_name,
                timeframe=timeframe,
                period_start=period_start,
                period_end=period_end,
                total_executions=0,
                successful_executions=0,
                success_rate=0.0,
                average_response_time=0.0,
                average_confidence=0.0,
                average_user_satisfaction=0.0,
                collaboration_count=0,
                insights_generated=0,
                recommendations_provided=0,
                proactive_suggestions=0,
                top_collaboration_partners=[],
                performance_trend="stable"
            )
        
        # Calculate metrics
        total_executions = len(agent_records)
        successful_executions = len([r for r in agent_records if r.success])
        success_rate = successful_executions / total_executions
        
        average_response_time = statistics.mean([r.response_time for r in agent_records])
        average_confidence = statistics.mean([r.confidence_score for r in agent_records])
        
        # Calculate user satisfaction (only for records with feedback)
        feedback_records = [r for r in agent_records if r.user_feedback_score is not None]
        average_user_satisfaction = statistics.mean([r.user_feedback_score for r in feedback_records]) if feedback_records else 0.0
        
        # Count collaborations
        collaboration_count = len([r for r in agent_records if r.collaboration_partners])
        
        # Sum insights and recommendations
        insights_generated = sum(r.insights_generated for r in agent_records)
        recommendations_provided = sum(r.recommendations_provided for r in agent_records)
        proactive_suggestions = sum(r.proactive_suggestions for r in agent_records)
        
        # Find top collaboration partners
        partner_counts = Counter()
        for record in agent_records:
            for partner in record.collaboration_partners:
                partner_counts[partner] += 1
        top_collaboration_partners = partner_counts.most_common(5)
        
        # Calculate performance trend
        performance_trend = self._calculate_performance_trend(agent_name, agent_records, timeframe)
        
        analytics = AgentAnalytics(
            agent_name=agent_name,
            timeframe=timeframe,
            period_start=period_start,
            period_end=period_end,
            total_executions=total_executions,
            successful_executions=successful_executions,
            success_rate=success_rate,
            average_response_time=average_response_time,
            average_confidence=average_confidence,
            average_user_satisfaction=average_user_satisfaction,
            collaboration_count=collaboration_count,
            insights_generated=insights_generated,
            recommendations_provided=recommendations_provided,
            proactive_suggestions=proactive_suggestions,
            top_collaboration_partners=top_collaboration_partners,
            performance_trend=performance_trend
        )
        
        # Cache the analytics
        if agent_name not in self.agent_analytics_cache:
            self.agent_analytics_cache[agent_name] = {}
        self.agent_analytics_cache[agent_name][cache_key] = analytics
        
        return analytics

    def _calculate_performance_trend(
        self,
        agent_name: str,
        agent_records: List[AgentPerformanceRecord],
        timeframe: AnalyticsTimeframe
    ) -> str:
        """Calculate performance trend for an agent"""

        if len(agent_records) < 10:  # Need sufficient data for trend analysis
            return "stable"

        # Sort records by execution time
        sorted_records = sorted(agent_records, key=lambda r: r.execution_time)

        # Split into two halves for comparison
        mid_point = len(sorted_records) // 2
        first_half = sorted_records[:mid_point]
        second_half = sorted_records[mid_point:]

        # Calculate metrics for each half
        first_half_success_rate = len([r for r in first_half if r.success]) / len(first_half)
        second_half_success_rate = len([r for r in second_half if r.success]) / len(second_half)

        first_half_confidence = statistics.mean([r.confidence_score for r in first_half])
        second_half_confidence = statistics.mean([r.confidence_score for r in second_half])

        first_half_response_time = statistics.mean([r.response_time for r in first_half])
        second_half_response_time = statistics.mean([r.response_time for r in second_half])

        # Calculate improvement scores
        success_improvement = second_half_success_rate - first_half_success_rate
        confidence_improvement = second_half_confidence - first_half_confidence
        response_time_improvement = first_half_response_time - second_half_response_time  # Lower is better

        # Weighted overall improvement score
        overall_improvement = (
            success_improvement * 0.4 +
            confidence_improvement * 0.3 +
            (response_time_improvement / 10.0) * 0.3  # Normalize response time
        )

        if overall_improvement > 0.05:
            return "improving"
        elif overall_improvement < -0.05:
            return "declining"
        else:
            return "stable"

    async def get_collaboration_analytics(self, timeframe: AnalyticsTimeframe) -> Dict[str, Any]:
        """Get analytics for agent collaborations"""

        # Calculate time period
        period_end = datetime.now()
        if timeframe == AnalyticsTimeframe.HOUR:
            period_start = period_end - timedelta(hours=1)
        elif timeframe == AnalyticsTimeframe.DAY:
            period_start = period_end - timedelta(days=1)
        elif timeframe == AnalyticsTimeframe.WEEK:
            period_start = period_end - timedelta(weeks=1)
        elif timeframe == AnalyticsTimeframe.MONTH:
            period_start = period_end - timedelta(days=30)
        elif timeframe == AnalyticsTimeframe.QUARTER:
            period_start = period_end - timedelta(days=90)
        else:  # YEAR
            period_start = period_end - timedelta(days=365)

        # Filter collaboration metrics
        collaborations = [
            collab for collab in self.collaboration_metrics
            if period_start <= collab.execution_time <= period_end
        ]

        if not collaborations:
            return {
                "total_collaborations": 0,
                "success_rate": 0.0,
                "average_synergy_score": 0.0,
                "average_handoff_efficiency": 0.0,
                "average_outcome_quality": 0.0,
                "most_effective_pairs": [],
                "collaboration_patterns": {}
            }

        # Calculate metrics
        total_collaborations = len(collaborations)
        successful_collaborations = len([c for c in collaborations if c.success])
        success_rate = successful_collaborations / total_collaborations

        average_synergy_score = statistics.mean([c.synergy_score for c in collaborations])
        average_handoff_efficiency = statistics.mean([c.handoff_efficiency for c in collaborations])
        average_outcome_quality = statistics.mean([c.outcome_quality for c in collaborations])

        # Find most effective collaboration pairs
        pair_performance = defaultdict(list)
        for collab in collaborations:
            if len(collab.participating_agents) == 2:
                pair = tuple(sorted(collab.participating_agents))
                pair_performance[pair].append(collab.synergy_score)

        most_effective_pairs = []
        for pair, scores in pair_performance.items():
            if len(scores) >= 3:  # Need at least 3 collaborations
                avg_score = statistics.mean(scores)
                most_effective_pairs.append({
                    "agents": list(pair),
                    "average_synergy": avg_score,
                    "collaboration_count": len(scores)
                })

        most_effective_pairs.sort(key=lambda x: x["average_synergy"], reverse=True)

        # Analyze collaboration patterns
        collaboration_patterns = self._analyze_collaboration_patterns(collaborations)

        return {
            "timeframe": timeframe.value,
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "total_collaborations": total_collaborations,
            "successful_collaborations": successful_collaborations,
            "success_rate": success_rate,
            "average_synergy_score": average_synergy_score,
            "average_handoff_efficiency": average_handoff_efficiency,
            "average_outcome_quality": average_outcome_quality,
            "most_effective_pairs": most_effective_pairs[:5],
            "collaboration_patterns": collaboration_patterns
        }

    def _analyze_collaboration_patterns(self, collaborations: List[CollaborationMetrics]) -> Dict[str, Any]:
        """Analyze patterns in agent collaborations"""

        # Count collaboration sizes
        size_distribution = Counter()
        for collab in collaborations:
            size_distribution[len(collab.participating_agents)] += 1

        # Find most common agent combinations
        combination_counts = Counter()
        for collab in collaborations:
            if len(collab.participating_agents) <= 4:  # Only track smaller combinations
                combination = tuple(sorted(collab.participating_agents))
                combination_counts[combination] += 1

        # Calculate success rates by collaboration size
        success_by_size = {}
        for size in size_distribution.keys():
            size_collaborations = [c for c in collaborations if len(c.participating_agents) == size]
            successful = len([c for c in size_collaborations if c.success])
            success_by_size[size] = successful / len(size_collaborations) if size_collaborations else 0.0

        return {
            "size_distribution": dict(size_distribution),
            "most_common_combinations": [
                {"agents": list(combo), "count": count}
                for combo, count in combination_counts.most_common(10)
            ],
            "success_rate_by_size": success_by_size,
            "optimal_collaboration_size": max(success_by_size.keys(), key=success_by_size.get) if success_by_size else 2
        }

    async def get_performance_comparison(self, agent_names: List[str], timeframe: AnalyticsTimeframe) -> Dict[str, Any]:
        """Compare performance across multiple agents"""

        agent_analytics = {}
        for agent_name in agent_names:
            analytics = await self.get_agent_analytics(agent_name, timeframe)
            agent_analytics[agent_name] = analytics

        # Create comparison metrics
        comparison = {
            "timeframe": timeframe.value,
            "agents_compared": agent_names,
            "metrics_comparison": {},
            "rankings": {},
            "performance_gaps": {},
            "recommendations": []
        }

        # Compare each metric
        metrics = ["success_rate", "average_response_time", "average_confidence", "average_user_satisfaction"]

        for metric in metrics:
            values = {}
            for agent_name, analytics in agent_analytics.items():
                values[agent_name] = getattr(analytics, metric)

            comparison["metrics_comparison"][metric] = values

            # Create rankings (higher is better except for response_time)
            if metric == "average_response_time":
                sorted_agents = sorted(values.items(), key=lambda x: x[1])  # Lower is better
            else:
                sorted_agents = sorted(values.items(), key=lambda x: x[1], reverse=True)  # Higher is better

            comparison["rankings"][metric] = [agent for agent, value in sorted_agents]

        # Calculate performance gaps
        for metric in metrics:
            values = list(comparison["metrics_comparison"][metric].values())
            if values:
                max_val = max(values)
                min_val = min(values)
                comparison["performance_gaps"][metric] = {
                    "range": max_val - min_val,
                    "coefficient_of_variation": statistics.stdev(values) / statistics.mean(values) if statistics.mean(values) > 0 else 0
                }

        # Generate recommendations
        comparison["recommendations"] = self._generate_performance_recommendations(agent_analytics)

        return comparison

    def _generate_performance_recommendations(self, agent_analytics: Dict[str, AgentAnalytics]) -> List[str]:
        """Generate performance improvement recommendations"""

        recommendations = []

        for agent_name, analytics in agent_analytics.items():
            benchmarks = self.performance_benchmarks.get(agent_name, {})

            # Check success rate
            if analytics.success_rate < benchmarks.get("target_success_rate", 0.9):
                recommendations.append(f"🎯 {agent_name}: Improve success rate from {analytics.success_rate:.1%} to {benchmarks.get('target_success_rate', 0.9):.1%}")

            # Check response time
            if analytics.average_response_time > benchmarks.get("target_response_time", 30.0):
                recommendations.append(f"⚡ {agent_name}: Reduce response time from {analytics.average_response_time:.1f}s to {benchmarks.get('target_response_time', 30.0):.1f}s")

            # Check confidence
            if analytics.average_confidence < benchmarks.get("target_confidence", 0.8):
                recommendations.append(f"🎯 {agent_name}: Increase confidence from {analytics.average_confidence:.1%} to {benchmarks.get('target_confidence', 0.8):.1%}")

            # Check user satisfaction
            if analytics.average_user_satisfaction < benchmarks.get("target_user_satisfaction", 4.0):
                recommendations.append(f"😊 {agent_name}: Improve user satisfaction from {analytics.average_user_satisfaction:.1f}/5.0 to {benchmarks.get('target_user_satisfaction', 4.0):.1f}/5.0")

            # Check collaboration
            if analytics.collaboration_count == 0:
                recommendations.append(f"🤝 {agent_name}: Consider more collaboration opportunities to enhance analysis quality")

            # Check trend
            if analytics.performance_trend == "declining":
                recommendations.append(f"📉 {agent_name}: Performance is declining - investigate and address root causes")

        return recommendations[:10]  # Limit to top 10 recommendations

    async def generate_performance_report(
        self,
        agent_names: List[str],
        timeframe: AnalyticsTimeframe,
        include_recommendations: bool = True
    ) -> Dict[str, Any]:
        """Generate a comprehensive performance report"""

        report = {
            "report_id": str(uuid.uuid4()),
            "generated_at": datetime.now().isoformat(),
            "timeframe": timeframe.value,
            "agents_analyzed": agent_names,
            "executive_summary": {},
            "individual_analytics": {},
            "collaboration_analytics": {},
            "performance_comparison": {},
            "recommendations": [],
            "key_insights": []
        }

        # Get individual analytics
        for agent_name in agent_names:
            analytics = await self.get_agent_analytics(agent_name, timeframe)
            report["individual_analytics"][agent_name] = asdict(analytics)

        # Get collaboration analytics
        report["collaboration_analytics"] = await self.get_collaboration_analytics(timeframe)

        # Get performance comparison
        if len(agent_names) > 1:
            report["performance_comparison"] = await self.get_performance_comparison(agent_names, timeframe)

        # Generate executive summary
        report["executive_summary"] = self._generate_executive_summary(report)

        # Generate recommendations
        if include_recommendations:
            report["recommendations"] = self._generate_comprehensive_recommendations(report)

        # Generate key insights
        report["key_insights"] = self._generate_key_insights(report)

        return report

    def _generate_executive_summary(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary from report data"""

        individual_analytics = report["individual_analytics"]
        collaboration_analytics = report["collaboration_analytics"]

        # Calculate overall metrics
        total_executions = sum(analytics["total_executions"] for analytics in individual_analytics.values())
        overall_success_rate = sum(
            analytics["successful_executions"] for analytics in individual_analytics.values()
        ) / max(total_executions, 1)

        average_response_time = statistics.mean([
            analytics["average_response_time"] for analytics in individual_analytics.values()
            if analytics["total_executions"] > 0
        ]) if individual_analytics else 0.0

        average_confidence = statistics.mean([
            analytics["average_confidence"] for analytics in individual_analytics.values()
            if analytics["total_executions"] > 0
        ]) if individual_analytics else 0.0

        # Find top performing agent
        top_performer = None
        if individual_analytics:
            top_performer = max(
                individual_analytics.keys(),
                key=lambda agent: individual_analytics[agent]["success_rate"]
            )

        # Find most collaborative agent
        most_collaborative = None
        if individual_analytics:
            most_collaborative = max(
                individual_analytics.keys(),
                key=lambda agent: individual_analytics[agent]["collaboration_count"]
            )

        return {
            "total_executions": total_executions,
            "overall_success_rate": overall_success_rate,
            "average_response_time": average_response_time,
            "average_confidence": average_confidence,
            "total_collaborations": collaboration_analytics.get("total_collaborations", 0),
            "collaboration_success_rate": collaboration_analytics.get("success_rate", 0.0),
            "top_performing_agent": top_performer,
            "most_collaborative_agent": most_collaborative,
            "performance_status": "excellent" if overall_success_rate > 0.9 else "good" if overall_success_rate > 0.8 else "needs_improvement"
        }

    def _generate_comprehensive_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Generate comprehensive recommendations from report data"""

        recommendations = []

        # Add individual agent recommendations
        if "performance_comparison" in report and "recommendations" in report["performance_comparison"]:
            recommendations.extend(report["performance_comparison"]["recommendations"])

        # Add collaboration recommendations
        collaboration_analytics = report["collaboration_analytics"]
        if collaboration_analytics.get("success_rate", 0) < 0.85:
            recommendations.append("🤝 Improve collaboration success rate through better agent coordination")

        if collaboration_analytics.get("average_synergy_score", 0) < 0.7:
            recommendations.append("⚡ Enhance agent synergy through improved context sharing")

        # Add system-wide recommendations
        executive_summary = report["executive_summary"]
        if executive_summary.get("overall_success_rate", 0) < 0.9:
            recommendations.append("🎯 Focus on improving overall system success rate")

        if executive_summary.get("average_response_time", 0) > 30.0:
            recommendations.append("⚡ Optimize system performance to reduce response times")

        return recommendations

    def _generate_key_insights(self, report: Dict[str, Any]) -> List[str]:
        """Generate key insights from report data"""

        insights = []

        individual_analytics = report["individual_analytics"]
        collaboration_analytics = report["collaboration_analytics"]
        executive_summary = report["executive_summary"]

        # Performance insights
        if executive_summary.get("overall_success_rate", 0) > 0.95:
            insights.append("🎉 Exceptional performance: System achieving >95% success rate")

        # Collaboration insights
        if collaboration_analytics.get("total_collaborations", 0) > 0:
            optimal_size = collaboration_analytics.get("collaboration_patterns", {}).get("optimal_collaboration_size", 2)
            insights.append(f"🤝 Optimal collaboration size: {optimal_size} agents working together")

        # Trend insights
        improving_agents = [
            agent for agent, analytics in individual_analytics.items()
            if analytics["performance_trend"] == "improving"
        ]
        if improving_agents:
            insights.append(f"📈 Performance improving: {', '.join(improving_agents)}")

        declining_agents = [
            agent for agent, analytics in individual_analytics.items()
            if analytics["performance_trend"] == "declining"
        ]
        if declining_agents:
            insights.append(f"📉 Performance declining: {', '.join(declining_agents)} - needs attention")

        # Efficiency insights
        fastest_agent = min(
            individual_analytics.keys(),
            key=lambda agent: individual_analytics[agent]["average_response_time"]
        ) if individual_analytics else None

        if fastest_agent:
            time = individual_analytics[fastest_agent]["average_response_time"]
            insights.append(f"⚡ Fastest agent: {fastest_agent} ({time:.1f}s average)")

        return insights

# Global performance analytics instance
performance_analytics = AgentPerformanceAnalytics()

async def record_agent_performance(
    agent_name: str,
    user_id: str,
    success: bool,
    response_time: float,
    confidence_score: float,
    collaboration_partners: List[str] = None,
    insights_generated: int = 0,
    recommendations_provided: int = 0,
    proactive_suggestions: int = 0,
    context: Dict[str, Any] = None
) -> str:
    """Record agent performance metrics"""
    return await performance_analytics.record_agent_performance(
        agent_name, user_id, success, response_time, confidence_score,
        collaboration_partners, insights_generated, recommendations_provided,
        proactive_suggestions, context
    )

async def record_collaboration_metrics(
    participating_agents: List[str],
    total_duration: float,
    success: bool,
    synergy_score: float,
    handoff_efficiency: float,
    outcome_quality: float
) -> str:
    """Record collaboration performance metrics"""
    return await performance_analytics.record_collaboration_metrics(
        participating_agents, total_duration, success, synergy_score,
        handoff_efficiency, outcome_quality
    )

async def get_agent_analytics(agent_name: str, timeframe: AnalyticsTimeframe) -> AgentAnalytics:
    """Get analytics for a specific agent"""
    return await performance_analytics.get_agent_analytics(agent_name, timeframe)

async def get_collaboration_analytics(timeframe: AnalyticsTimeframe) -> Dict[str, Any]:
    """Get collaboration analytics"""
    return await performance_analytics.get_collaboration_analytics(timeframe)

async def get_performance_comparison(agent_names: List[str], timeframe: AnalyticsTimeframe) -> Dict[str, Any]:
    """Compare performance across agents"""
    return await performance_analytics.get_performance_comparison(agent_names, timeframe)

async def generate_performance_report(
    agent_names: List[str],
    timeframe: AnalyticsTimeframe,
    include_recommendations: bool = True
) -> Dict[str, Any]:
    """Generate comprehensive performance report"""
    return await performance_analytics.generate_performance_report(
        agent_names, timeframe, include_recommendations
    )

async def update_user_feedback(record_id: str, feedback_score: float) -> bool:
    """Update user feedback for a performance record"""
    return await performance_analytics.update_user_feedback(record_id, feedback_score)
