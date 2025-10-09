"""
Cost Optimization Analyzer
AI-powered cost analysis and optimization recommendations for the multi-agent system
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import statistics

from .agent_performance_models import (
    CostOptimizationRecommendation, AgentType, ModelProvider
)
from .agent_performance_tracker import get_performance_tracker
from database import get_db_connection
from logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.MONITORING)

class OptimizationType(Enum):
    """Types of cost optimization strategies"""
    MODEL_SELECTION = "model_selection"
    CACHING_IMPROVEMENT = "caching_improvement" 
    REQUEST_BATCHING = "request_batching"
    ANALYSIS_DEPTH_TUNING = "analysis_depth_tuning"
    USAGE_PATTERN_OPTIMIZATION = "usage_pattern_optimization"
    FALLBACK_STRATEGY = "fallback_strategy"

@dataclass
class CostAnalysis:
    """Cost analysis results for an agent or system"""
    agent_type: Optional[AgentType]
    time_window_hours: int
    total_cost: float
    total_requests: int
    avg_cost_per_request: float
    cost_trend: str  # "increasing", "decreasing", "stable"
    primary_cost_drivers: List[str]
    optimization_potential: float  # Estimated savings percentage

@dataclass
class ModelCostData:
    """Cost data for a specific model"""
    model_name: str
    provider: ModelProvider
    input_cost_per_token: float
    output_cost_per_token: float
    avg_tokens_per_request: float
    performance_score: float  # Based on latency and success rate

class CostOptimizer:
    """Analyzes costs and generates optimization recommendations"""
    
    def __init__(self):
        self.model_costs = self._load_model_cost_data()
        self.optimization_history = {}
        
        logger.info("Cost optimizer initialized")
    
    def _load_model_cost_data(self) -> Dict[str, ModelCostData]:
        """Load current model pricing data"""
        return {
            # OpenAI GPT models
            "gpt-4o": ModelCostData(
                model_name="gpt-4o",
                provider=ModelProvider.OPENAI,
                input_cost_per_token=0.00001,  # $0.01 per 1K tokens
                output_cost_per_token=0.00003,  # $0.03 per 1K tokens
                avg_tokens_per_request=4000,
                performance_score=0.95
            ),
            "gpt-4o-mini": ModelCostData(
                model_name="gpt-4o-mini",
                provider=ModelProvider.OPENAI,
                input_cost_per_token=0.00000015,  # $0.15 per 1M tokens
                output_cost_per_token=0.0000006,   # $0.60 per 1M tokens
                avg_tokens_per_request=3500,
                performance_score=0.88
            ),
            
            # Anthropic Claude models
            "claude-3-5-sonnet-20241022": ModelCostData(
                model_name="claude-3-5-sonnet-20241022",
                provider=ModelProvider.ANTHROPIC,
                input_cost_per_token=0.000003,  # $3 per 1M tokens
                output_cost_per_token=0.000015,  # $15 per 1M tokens
                avg_tokens_per_request=4200,
                performance_score=0.92
            ),
            "claude-3-haiku-20240307": ModelCostData(
                model_name="claude-3-haiku-20240307",
                provider=ModelProvider.ANTHROPIC,
                input_cost_per_token=0.00000025,  # $0.25 per 1M tokens
                output_cost_per_token=0.00000125,  # $1.25 per 1M tokens
                avg_tokens_per_request=3000,
                performance_score=0.85
            ),
            
            # Google Gemini models
            "gemini-2.5-pro": ModelCostData(
                model_name="gemini-2.5-pro",
                provider=ModelProvider.GOOGLE,
                input_cost_per_token=0.00000125,  # $1.25 per 1M tokens
                output_cost_per_token=0.000005,   # $5 per 1M tokens
                avg_tokens_per_request=3800,
                performance_score=0.90
            ),
            "gemini-1.5-flash": ModelCostData(
                model_name="gemini-1.5-flash",
                provider=ModelProvider.GOOGLE,
                input_cost_per_token=0.000000075,  # $0.075 per 1M tokens
                output_cost_per_token=0.0000003,   # $0.30 per 1M tokens
                avg_tokens_per_request=2800,
                performance_score=0.82
            )
        }
    
    async def analyze_costs(self, time_window_hours: int = 24) -> List[CostAnalysis]:
        """Analyze costs for all agents"""
        try:
            performance_tracker = get_performance_tracker()
            
            # Get cost data for all agents
            cost_analyses = []
            
            for agent_type in AgentType:
                # Get agent health data
                agent_health = await performance_tracker.get_agent_health(
                    agent_type=agent_type,
                    time_window_minutes=time_window_hours * 60
                )
                
                if not agent_health:
                    continue
                
                agent_data = agent_health[0]  # Should be only one result per agent
                
                # Calculate cost trend
                cost_trend = await self._calculate_cost_trend(agent_type, time_window_hours)
                
                # Identify cost drivers
                cost_drivers = await self._identify_cost_drivers(agent_type, time_window_hours)
                
                # Estimate optimization potential
                optimization_potential = await self._estimate_optimization_potential(agent_type, agent_data)
                
                analysis = CostAnalysis(
                    agent_type=agent_type,
                    time_window_hours=time_window_hours,
                    total_cost=agent_data.total_cost_estimate,
                    total_requests=agent_data.total_requests,
                    avg_cost_per_request=(
                        agent_data.total_cost_estimate / agent_data.total_requests 
                        if agent_data.total_requests > 0 else 0
                    ),
                    cost_trend=cost_trend,
                    primary_cost_drivers=cost_drivers,
                    optimization_potential=optimization_potential
                )
                
                cost_analyses.append(analysis)
            
            return cost_analyses
            
        except Exception as e:
            logger.error(f"Failed to analyze costs: {e}", exc_info=True)
            return []
    
    async def _calculate_cost_trend(self, agent_type: AgentType, time_window_hours: int) -> str:
        """Calculate cost trend for an agent"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Get cost data in hourly buckets
                cursor.execute("""
                    SELECT 
                        strftime('%Y-%m-%d %H:00:00', timestamp) as hour,
                        SUM(cost_estimate) as hourly_cost
                    FROM agent_performance_metrics 
                    WHERE agent_type = ? 
                        AND timestamp >= ?
                    GROUP BY strftime('%Y-%m-%d %H:00:00', timestamp)
                    ORDER BY hour
                """, (agent_type.value, datetime.now() - timedelta(hours=time_window_hours)))
                
                hourly_costs = [row[1] for row in cursor.fetchall()]
                
                if len(hourly_costs) < 3:
                    return "insufficient_data"
                
                # Calculate trend using linear regression slope
                n = len(hourly_costs)
                x_values = list(range(n))
                
                # Simple linear regression
                x_mean = statistics.mean(x_values)
                y_mean = statistics.mean(hourly_costs)
                
                numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, hourly_costs))
                denominator = sum((x - x_mean) ** 2 for x in x_values)
                
                if denominator == 0:
                    return "stable"
                
                slope = numerator / denominator
                
                # Determine trend based on slope
                if slope > 0.01:  # Significant upward trend
                    return "increasing"
                elif slope < -0.01:  # Significant downward trend
                    return "decreasing"
                else:
                    return "stable"
                
        except Exception as e:
            logger.error(f"Failed to calculate cost trend: {e}")
            return "unknown"
    
    async def _identify_cost_drivers(self, agent_type: AgentType, time_window_hours: int) -> List[str]:
        """Identify primary cost drivers for an agent"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Analyze cost patterns
                cursor.execute("""
                    SELECT 
                        model_name,
                        analysis_depth,
                        AVG(cost_estimate) as avg_cost,
                        COUNT(*) as request_count,
                        SUM(cost_estimate) as total_cost,
                        AVG(input_tokens) as avg_input_tokens,
                        AVG(output_tokens) as avg_output_tokens,
                        AVG(CASE WHEN cache_hit = 1 THEN 0 ELSE 1 END) as cache_miss_rate
                    FROM agent_performance_metrics 
                    WHERE agent_type = ? 
                        AND timestamp >= ?
                    GROUP BY model_name, analysis_depth
                    ORDER BY total_cost DESC
                """, (agent_type.value, datetime.now() - timedelta(hours=time_window_hours)))
                
                results = cursor.fetchall()
                cost_drivers = []
                
                if not results:
                    return ["insufficient_data"]
                
                total_agent_cost = sum(row[4] for row in results)
                
                for row in results:
                    (model_name, analysis_depth, avg_cost, request_count, 
                     total_cost, avg_input_tokens, avg_output_tokens, cache_miss_rate) = row
                    
                    cost_percentage = (total_cost / total_agent_cost) * 100 if total_agent_cost > 0 else 0
                    
                    # Identify significant cost drivers (>20% of total cost)
                    if cost_percentage > 20:
                        if avg_cost > 0.05:  # High cost per request
                            cost_drivers.append(f"high_cost_model_{model_name}")
                        if analysis_depth == "deep" and cost_percentage > 30:
                            cost_drivers.append("excessive_deep_analysis")
                        if cache_miss_rate > 0.7:
                            cost_drivers.append("poor_cache_performance")
                        if avg_input_tokens > 5000:
                            cost_drivers.append("large_input_tokens")
                        if avg_output_tokens > 2000:
                            cost_drivers.append("large_output_tokens")
                
                # Add pattern-based drivers
                if len([r for r in results if r[1] == "deep"]) > len(results) * 0.5:
                    cost_drivers.append("overuse_of_deep_analysis")
                
                return cost_drivers[:5] if cost_drivers else ["standard_usage"]
                
        except Exception as e:
            logger.error(f"Failed to identify cost drivers: {e}")
            return ["analysis_error"]
    
    async def _estimate_optimization_potential(self, agent_type: AgentType, agent_data) -> float:
        """Estimate potential cost savings percentage"""
        try:
            # Base optimization potential on various factors
            potential = 0.0
            
            # Cache hit rate optimization
            if agent_data.cache_hit_rate < 0.5:
                potential += (0.5 - agent_data.cache_hit_rate) * 0.6  # Up to 30% savings
            
            # Model selection optimization
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT model_name, AVG(cost_estimate) as avg_cost
                    FROM agent_performance_metrics 
                    WHERE agent_type = ? 
                        AND timestamp >= ?
                    GROUP BY model_name
                """, (agent_type.value, datetime.now() - timedelta(hours=24)))
                
                model_costs = cursor.fetchall()
                
                if len(model_costs) > 1:
                    costs = [row[1] for row in model_costs]
                    cost_variation = (max(costs) - min(costs)) / max(costs) if max(costs) > 0 else 0
                    potential += cost_variation * 0.3  # Up to 30% savings from model optimization
                elif len(model_costs) == 1:
                    # Check if there's a cheaper alternative
                    current_model = model_costs[0][0]
                    if current_model in self.model_costs:
                        current_cost = self.model_costs[current_model]
                        cheaper_alternatives = [
                            model for model in self.model_costs.values()
                            if (model.provider == current_cost.provider and 
                                model.input_cost_per_token < current_cost.input_cost_per_token and
                                model.performance_score >= current_cost.performance_score * 0.9)
                        ]
                        if cheaper_alternatives:
                            potential += 0.25  # 25% potential savings
            
            # Request batching potential
            if agent_data.total_requests > 100:  # Only for high-volume agents
                potential += 0.15  # 15% potential from batching
            
            # Analysis depth optimization
            cursor.execute("""
                SELECT analysis_depth, COUNT(*) as count, AVG(cost_estimate) as avg_cost
                FROM agent_performance_metrics 
                WHERE agent_type = ? AND timestamp >= ?
                GROUP BY analysis_depth
            """, (agent_type.value, datetime.now() - timedelta(hours=24)))
            
            depth_analysis = cursor.fetchall()
            deep_analysis_ratio = 0
            total_requests = sum(row[1] for row in depth_analysis)
            
            for row in depth_analysis:
                if row[0] == "deep" and total_requests > 0:
                    deep_analysis_ratio = row[1] / total_requests
                    break
            
            if deep_analysis_ratio > 0.5:  # More than 50% deep analysis
                potential += 0.20  # 20% potential from depth optimization
            
            return min(potential, 0.8)  # Cap at 80% potential savings
            
        except Exception as e:
            logger.error(f"Failed to estimate optimization potential: {e}")
            return 0.0
    
    async def generate_recommendations(self, time_window_hours: int = 24) -> List[CostOptimizationRecommendation]:
        """Generate cost optimization recommendations"""
        try:
            cost_analyses = await self.analyze_costs(time_window_hours)
            recommendations = []
            
            for analysis in cost_analyses:
                agent_recommendations = await self._generate_agent_recommendations(analysis)
                recommendations.extend(agent_recommendations)
            
            # Generate system-wide recommendations
            system_recommendations = await self._generate_system_recommendations(cost_analyses)
            recommendations.extend(system_recommendations)
            
            # Sort by estimated savings
            recommendations.sort(key=lambda x: x.estimated_savings_per_day, reverse=True)
            
            return recommendations[:10]  # Return top 10 recommendations
            
        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}", exc_info=True)
            return []
    
    async def _generate_agent_recommendations(self, analysis: CostAnalysis) -> List[CostOptimizationRecommendation]:
        """Generate recommendations for a specific agent"""
        recommendations = []
        
        try:
            # Model selection recommendations
            if "high_cost_model" in str(analysis.primary_cost_drivers):
                current_daily_cost = analysis.total_cost * (24 / analysis.time_window_hours)
                
                rec = CostOptimizationRecommendation(
                    recommendation_id=f"model_opt_{analysis.agent_type.value}_{datetime.now().strftime('%Y%m%d')}",
                    type=OptimizationType.MODEL_SELECTION.value,
                    priority="high",
                    estimated_savings_per_day=current_daily_cost * 0.3,
                    implementation_effort="medium",
                    description=f"Switch {analysis.agent_type.value} to a more cost-effective model",
                    current_cost_per_day=current_daily_cost,
                    projected_cost_per_day=current_daily_cost * 0.7,
                    affected_agents=[analysis.agent_type],
                    implementation_steps=[
                        f"Evaluate performance of cheaper alternatives for {analysis.agent_type.value}",
                        "Run A/B test with new model on 10% of traffic",
                        "Monitor quality metrics for 48 hours",
                        "Gradually migrate if performance is acceptable"
                    ],
                    risks=[
                        "Potential slight decrease in response quality",
                        "Need to monitor performance closely during transition"
                    ]
                )
                recommendations.append(rec)
            
            # Cache optimization recommendations
            if "poor_cache_performance" in analysis.primary_cost_drivers:
                cache_savings = analysis.total_cost * 0.4 * (24 / analysis.time_window_hours)
                
                rec = CostOptimizationRecommendation(
                    recommendation_id=f"cache_opt_{analysis.agent_type.value}_{datetime.now().strftime('%Y%m%d')}",
                    type=OptimizationType.CACHING_IMPROVEMENT.value,
                    priority="high",
                    estimated_savings_per_day=cache_savings,
                    implementation_effort="low",
                    description=f"Improve cache performance for {analysis.agent_type.value}",
                    current_cost_per_day=analysis.total_cost * (24 / analysis.time_window_hours),
                    projected_cost_per_day=analysis.total_cost * (24 / analysis.time_window_hours) - cache_savings,
                    affected_agents=[analysis.agent_type],
                    implementation_steps=[
                        "Increase cache TTL for stable queries",
                        "Optimize cache key generation to improve hit rates",
                        "Implement cache warming for common requests",
                        "Monitor cache performance metrics"
                    ],
                    risks=[
                        "Slightly stale data in some responses",
                        "Increased memory usage"
                    ]
                )
                recommendations.append(rec)
            
            # Analysis depth optimization
            if "excessive_deep_analysis" in analysis.primary_cost_drivers:
                depth_savings = analysis.total_cost * 0.25 * (24 / analysis.time_window_hours)
                
                rec = CostOptimizationRecommendation(
                    recommendation_id=f"depth_opt_{analysis.agent_type.value}_{datetime.now().strftime('%Y%m%d')}",
                    type=OptimizationType.ANALYSIS_DEPTH_TUNING.value,
                    priority="medium",
                    estimated_savings_per_day=depth_savings,
                    implementation_effort="low",
                    description=f"Optimize analysis depth selection for {analysis.agent_type.value}",
                    current_cost_per_day=analysis.total_cost * (24 / analysis.time_window_hours),
                    projected_cost_per_day=analysis.total_cost * (24 / analysis.time_window_hours) - depth_savings,
                    affected_agents=[analysis.agent_type],
                    implementation_steps=[
                        "Implement intelligent depth selection based on request context",
                        "Use 'standard' depth as default, 'deep' only for complex queries",
                        "Add user preference for analysis depth",
                        "Monitor user satisfaction with shorter analyses"
                    ],
                    risks=[
                        "Some users may prefer more detailed analysis",
                        "Need to balance cost vs. insight quality"
                    ]
                )
                recommendations.append(rec)
            
        except Exception as e:
            logger.error(f"Failed to generate agent recommendations: {e}")
        
        return recommendations
    
    async def _generate_system_recommendations(self, analyses: List[CostAnalysis]) -> List[CostOptimizationRecommendation]:
        """Generate system-wide optimization recommendations"""
        recommendations = []
        
        try:
            total_daily_cost = sum(analysis.total_cost * (24 / analysis.time_window_hours) for analysis in analyses)
            
            # Request batching recommendation
            high_volume_agents = [a for a in analyses if a.total_requests > 50]
            if len(high_volume_agents) > 2:
                batching_savings = total_daily_cost * 0.15
                
                rec = CostOptimizationRecommendation(
                    recommendation_id=f"system_batching_{datetime.now().strftime('%Y%m%d')}",
                    type=OptimizationType.REQUEST_BATCHING.value,
                    priority="medium",
                    estimated_savings_per_day=batching_savings,
                    implementation_effort="high",
                    description="Implement request batching for high-volume agents",
                    current_cost_per_day=total_daily_cost,
                    projected_cost_per_day=total_daily_cost - batching_savings,
                    affected_agents=[a.agent_type for a in high_volume_agents],
                    implementation_steps=[
                        "Design request batching architecture",
                        "Implement batch processing for similar requests",
                        "Add batch optimization logic",
                        "Test and monitor batch performance"
                    ],
                    risks=[
                        "Increased system complexity",
                        "Potential latency for batched requests",
                        "Need for careful batch size optimization"
                    ]
                )
                recommendations.append(rec)
            
            # Usage pattern optimization
            peak_hours_optimization = total_daily_cost * 0.1
            
            rec = CostOptimizationRecommendation(
                recommendation_id=f"usage_pattern_{datetime.now().strftime('%Y%m%d')}",
                type=OptimizationType.USAGE_PATTERN_OPTIMIZATION.value,
                priority="low",
                estimated_savings_per_day=peak_hours_optimization,
                implementation_effort="medium",
                description="Optimize usage patterns and implement rate limiting during peak hours",
                current_cost_per_day=total_daily_cost,
                projected_cost_per_day=total_daily_cost - peak_hours_optimization,
                affected_agents=[a.agent_type for a in analyses],
                implementation_steps=[
                    "Analyze usage patterns by time of day",
                    "Implement intelligent rate limiting",
                    "Add request queuing for non-urgent requests",
                    "Provide usage analytics to users"
                ],
                risks=[
                    "User experience impact during rate limiting",
                    "Complexity in determining request urgency"
                ]
            )
            recommendations.append(rec)
            
        except Exception as e:
            logger.error(f"Failed to generate system recommendations: {e}")
        
        return recommendations
    
    async def track_optimization_implementation(self, recommendation_id: str) -> Dict[str, Any]:
        """Track the implementation and results of an optimization"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                
                # This would track actual savings vs. projected savings
                # Implementation would depend on specific optimization type
                
                return {
                    "recommendation_id": recommendation_id,
                    "implementation_status": "tracking",
                    "actual_savings": 0.0,
                    "tracking_start_date": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Failed to track optimization: {e}")
            return {}

# Global cost optimizer instance
_cost_optimizer = None

def get_cost_optimizer() -> CostOptimizer:
    """Get global cost optimizer instance"""
    global _cost_optimizer
    if _cost_optimizer is None:
        _cost_optimizer = CostOptimizer()
    return _cost_optimizer