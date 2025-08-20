"""
Agent Collaboration System for MYTA
Enables multiple agents to work together on complex problems
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import json
import asyncio

from backend.App.channel_analyzer import ChannelProfile
from backend.App.agent_tools import get_agent_tools, AnalysisResult
from backend.App.dynamic_response_engine import get_dynamic_response_engine, ResponseContext
from backend.App.agent_personalities import get_agent_personality
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.AGENT)

@dataclass
class CollaborationRequest:
    """Request for agent collaboration"""
    primary_agent_id: str
    user_message: str
    user_id: str
    channel_profile: ChannelProfile
    complexity_level: str
    required_perspectives: List[str]
    collaboration_type: str
    context: Dict[str, Any]

@dataclass
class AgentContribution:
    """Individual agent's contribution to collaboration"""
    agent_id: str
    agent_name: str
    perspective: str
    analysis: Dict[str, Any]
    recommendations: List[str]
    concerns: List[str]
    supporting_data: Dict[str, Any]
    confidence_score: float
    collaboration_notes: List[str]

@dataclass
class CollaborationResult:
    """Result of agent collaboration"""
    primary_agent_id: str
    participating_agents: List[str]
    problem_analysis: Dict[str, Any]
    unified_recommendations: List[str]
    perspective_breakdown: List[AgentContribution]
    consensus_areas: List[str]
    debate_points: List[Dict[str, Any]]
    action_plan: Dict[str, Any]
    confidence_score: float
    collaboration_summary: str

class AgentCollaborationEngine:
    """Engine for coordinating agent collaboration"""
    
    def __init__(self):
        self.agent_tools = get_agent_tools()
        self.dynamic_engine = get_dynamic_response_engine()
        self.collaboration_patterns = self._load_collaboration_patterns()
        self.agent_relationships = self._load_agent_relationships()
    
    def _load_collaboration_patterns(self) -> Dict[str, Any]:
        """Load collaboration patterns for different problem types"""
        return {
            "comprehensive_analysis": {
                "description": "Full multi-agent analysis of complex problems",
                "required_agents": ["1", "2", "3", "4", "5"],
                "coordination_style": "sequential_with_synthesis",
                "debate_enabled": True
            },
            "performance_optimization": {
                "description": "Focus on performance metrics and optimization",
                "required_agents": ["1", "2", "4"],  # Alex, Levi, Zara
                "coordination_style": "parallel_analysis",
                "debate_enabled": True
            },
            "content_strategy": {
                "description": "Content creation and optimization focus",
                "required_agents": ["2", "3", "5"],  # Levi, Maya, Kai
                "coordination_style": "collaborative_refinement",
                "debate_enabled": False
            },
            "growth_acceleration": {
                "description": "Rapid growth strategies and scaling",
                "required_agents": ["1", "4", "5"],  # Alex, Zara, Kai
                "coordination_style": "strategic_planning",
                "debate_enabled": True
            },
            "crisis_response": {
                "description": "Urgent problem solving and damage control",
                "required_agents": ["1", "2", "4"],  # Alex, Levi, Zara
                "coordination_style": "rapid_response",
                "debate_enabled": False
            },
            "monetization_strategy": {
                "description": "Revenue optimization and business development",
                "required_agents": ["1", "3", "4"],  # Alex, Maya, Zara
                "coordination_style": "business_planning",
                "debate_enabled": True
            }
        }
    
    def _load_agent_relationships(self) -> Dict[str, Any]:
        """Load agent relationship dynamics and expertise overlaps"""
        return {
            "expertise_overlaps": {
                "analytics_content": ["1", "2"],  # Alex & Levi
                "content_engagement": ["2", "3"],  # Levi & Maya
                "engagement_growth": ["3", "4"],  # Maya & Zara
                "growth_technical": ["4", "5"],   # Zara & Kai
                "analytics_technical": ["1", "5"] # Alex & Kai
            },
            "collaboration_strengths": {
                "1": {  # Alex
                    "leads_well_with": ["4", "5"],  # Zara, Kai
                    "supports_well": ["2", "3"],    # Levi, Maya
                    "challenges_constructively": ["4"], # Zara
                    "expertise_areas": ["data_analysis", "performance_metrics", "benchmarking"]
                },
                "2": {  # Levi
                    "leads_well_with": ["3", "5"],  # Maya, Kai
                    "supports_well": ["1", "4"],    # Alex, Zara
                    "challenges_constructively": ["1"], # Alex
                    "expertise_areas": ["content_creation", "creative_strategy", "audience_appeal"]
                },
                "3": {  # Maya
                    "leads_well_with": ["2", "4"],  # Levi, Zara
                    "supports_well": ["1", "5"],    # Alex, Kai
                    "challenges_constructively": ["2"], # Levi
                    "expertise_areas": ["community_building", "engagement_strategy", "audience_psychology"]
                },
                "4": {  # Zara
                    "leads_well_with": ["1", "3"],  # Alex, Maya
                    "supports_well": ["2", "5"],    # Levi, Kai
                    "challenges_constructively": ["1"], # Alex
                    "expertise_areas": ["growth_strategy", "scaling", "algorithm_optimization"]
                },
                "5": {  # Kai
                    "leads_well_with": ["1", "2"],  # Alex, Levi
                    "supports_well": ["3", "4"],    # Maya, Zara
                    "challenges_constructively": ["4"], # Zara
                    "expertise_areas": ["technical_optimization", "seo", "platform_mechanics"]
                }
            },
            "debate_dynamics": {
                "analytics_vs_creative": {
                    "agents": ["1", "2"],
                    "common_tensions": ["data_driven_vs_intuitive", "metrics_vs_creativity"],
                    "resolution_approach": "balanced_synthesis"
                },
                "growth_vs_quality": {
                    "agents": ["4", "2"],
                    "common_tensions": ["speed_vs_quality", "scale_vs_craft"],
                    "resolution_approach": "phased_approach"
                },
                "technical_vs_engagement": {
                    "agents": ["5", "3"],
                    "common_tensions": ["optimization_vs_authenticity", "technical_vs_human"],
                    "resolution_approach": "user_centric_balance"
                }
            }
        }
    
    async def initiate_collaboration(self, request: CollaborationRequest) -> CollaborationResult:
        """Initiate collaboration between agents"""
        
        try:
            # Determine collaboration pattern
            collaboration_pattern = self._determine_collaboration_pattern(request)
            
            # Select participating agents
            participating_agents = self._select_participating_agents(request, collaboration_pattern)
            
            # Coordinate agent contributions
            agent_contributions = await self._coordinate_agent_contributions(
                request, participating_agents, collaboration_pattern
            )
            
            # Facilitate debates if enabled
            if collaboration_pattern.get("debate_enabled", False):
                debate_results = await self._facilitate_debates(
                    request, agent_contributions, collaboration_pattern
                )
            else:
                debate_results = []
            
            # Synthesize unified recommendations
            unified_recommendations = await self._synthesize_recommendations(
                request, agent_contributions, debate_results
            )
            
            # Identify consensus and conflicts
            consensus_areas = self._identify_consensus_areas(agent_contributions)
            
            # Create action plan
            action_plan = await self._create_unified_action_plan(
                request, agent_contributions, unified_recommendations
            )
            
            # Calculate overall confidence
            confidence_score = self._calculate_collaboration_confidence(agent_contributions)
            
            # Generate collaboration summary
            summary = self._generate_collaboration_summary(
                request, agent_contributions, unified_recommendations
            )
            
            return CollaborationResult(
                primary_agent_id=request.primary_agent_id,
                participating_agents=participating_agents,
                problem_analysis=self._synthesize_problem_analysis(agent_contributions),
                unified_recommendations=unified_recommendations,
                perspective_breakdown=agent_contributions,
                consensus_areas=consensus_areas,
                debate_points=debate_results,
                action_plan=action_plan,
                confidence_score=confidence_score,
                collaboration_summary=summary
            )
        
        except Exception as e:
            logger.error(f"Error in agent collaboration: {e}")
            return self._generate_fallback_collaboration(request)
    
    def _determine_collaboration_pattern(self, request: CollaborationRequest) -> Dict[str, Any]:
        """Determine the best collaboration pattern for the request"""
        
        message_lower = request.user_message.lower()
        
        # Pattern matching based on keywords and context
        if any(word in message_lower for word in ["crisis", "emergency", "urgent", "broken"]):
            return self.collaboration_patterns["crisis_response"]
        elif any(word in message_lower for word in ["comprehensive", "full analysis", "everything"]):
            return self.collaboration_patterns["comprehensive_analysis"]
        elif any(word in message_lower for word in ["performance", "metrics", "analytics"]):
            return self.collaboration_patterns["performance_optimization"]
        elif any(word in message_lower for word in ["content", "video", "create"]):
            return self.collaboration_patterns["content_strategy"]
        elif any(word in message_lower for word in ["grow", "scale", "expand"]):
            return self.collaboration_patterns["growth_acceleration"]
        elif any(word in message_lower for word in ["money", "revenue", "monetize"]):
            return self.collaboration_patterns["monetization_strategy"]
        else:
            # Default to comprehensive analysis
            return self.collaboration_patterns["comprehensive_analysis"]
    
    def _select_participating_agents(
        self, 
        request: CollaborationRequest, 
        pattern: Dict[str, Any]
    ) -> List[str]:
        """Select which agents should participate"""
        
        required_agents = pattern.get("required_agents", ["1", "2", "3", "4", "5"])
        
        # Always include the primary agent
        if request.primary_agent_id not in required_agents:
            required_agents.insert(0, request.primary_agent_id)
        
        # Filter based on channel size for efficiency
        if request.channel_profile.channel_size_tier == "micro":
            # For micro channels, focus on essential agents
            essential_agents = ["1", "2", "4"]  # Alex, Levi, Zara
            required_agents = [agent for agent in required_agents if agent in essential_agents]
        
        return required_agents[:4]  # Limit to 4 agents for manageable collaboration
    
    async def _coordinate_agent_contributions(
        self, 
        request: CollaborationRequest, 
        agents: List[str], 
        pattern: Dict[str, Any]
    ) -> List[AgentContribution]:
        """Coordinate contributions from participating agents"""
        
        contributions = []
        coordination_style = pattern.get("coordination_style", "parallel_analysis")
        
        if coordination_style == "sequential_with_synthesis":
            # Agents contribute in sequence, building on previous insights
            contributions = await self._sequential_contributions(request, agents)
        elif coordination_style == "parallel_analysis":
            # Agents analyze independently, then compare
            contributions = await self._parallel_contributions(request, agents)
        else:
            # Default to parallel
            contributions = await self._parallel_contributions(request, agents)
        
        return contributions
    
    async def _sequential_contributions(
        self, 
        request: CollaborationRequest, 
        agents: List[str]
    ) -> List[AgentContribution]:
        """Get sequential contributions from agents"""
        
        contributions = []
        accumulated_context = {}
        
        for agent_id in agents:
            try:
                # Add previous insights to context
                context = {**request.context, "previous_insights": accumulated_context}
                
                contribution = await self._get_agent_contribution(
                    request, agent_id, context
                )
                contributions.append(contribution)
                
                # Add this agent's insights to accumulated context
                accumulated_context[agent_id] = {
                    "recommendations": contribution.recommendations,
                    "key_insights": contribution.analysis.get("key_insights", [])
                }
                
            except Exception as e:
                logger.error(f"Error getting contribution from agent {agent_id}: {e}")
        
        return contributions
    
    async def _parallel_contributions(
        self, 
        request: CollaborationRequest, 
        agents: List[str]
    ) -> List[AgentContribution]:
        """Get parallel contributions from agents"""
        
        contributions = []
        
        # Create tasks for parallel execution
        tasks = []
        for agent_id in agents:
            task = self._get_agent_contribution(request, agent_id, request.context)
            tasks.append(task)
        
        # Execute in parallel
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, AgentContribution):
                    contributions.append(result)
                else:
                    logger.error(f"Error in parallel contribution: {result}")
        
        except Exception as e:
            logger.error(f"Error in parallel contributions: {e}")
        
        return contributions
    
    async def _get_agent_contribution(
        self, 
        request: CollaborationRequest, 
        agent_id: str, 
        context: Dict[str, Any]
    ) -> AgentContribution:
        """Get contribution from a specific agent"""
        
        try:
            agent = get_agent_personality(agent_id)
            
            # Determine agent's perspective on the problem
            perspective = self._determine_agent_perspective(agent_id, request.user_message)
            
            # Get agent's analysis using their tools
            analysis = await self._get_agent_analysis(agent_id, request, context)
            
            # Generate agent-specific recommendations
            recommendations = self._generate_agent_recommendations(
                agent_id, request, analysis
            )
            
            # Identify potential concerns from this agent's perspective
            concerns = self._identify_agent_concerns(agent_id, request, analysis)
            
            # Add collaboration notes
            collaboration_notes = self._generate_collaboration_notes(
                agent_id, request, context
            )
            
            return AgentContribution(
                agent_id=agent_id,
                agent_name=agent["name"],
                perspective=perspective,
                analysis=analysis,
                recommendations=recommendations,
                concerns=concerns,
                supporting_data=analysis.get("supporting_data", {}),
                confidence_score=analysis.get("confidence_score", 0.8),
                collaboration_notes=collaboration_notes
            )
        
        except Exception as e:
            logger.error(f"Error getting contribution from agent {agent_id}: {e}")
            return self._get_fallback_contribution(agent_id)
    
    def _determine_agent_perspective(self, agent_id: str, user_message: str) -> str:
        """Determine agent's unique perspective on the problem"""
        
        perspectives = {
            "1": "Data-driven performance analysis and metrics optimization",
            "2": "Creative content strategy and audience engagement",
            "3": "Community building and audience relationship management",
            "4": "Strategic growth planning and algorithm optimization",
            "5": "Technical implementation and platform optimization"
        }
        
        return perspectives.get(agent_id, "General optimization perspective")
    
    async def _get_agent_analysis(
        self, 
        agent_id: str, 
        request: CollaborationRequest, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get detailed analysis from agent using their tools"""
        
        try:
            # Get the most relevant tool for this agent and problem
            suggested_tool = self.agent_tools.suggest_best_tool(
                agent_id, request.user_message, request.channel_profile
            )
            
            # Execute the tool
            tool_result = self.agent_tools.execute_tool(
                agent_id, suggested_tool, request.channel_profile, context
            )
            
            return {
                "tool_used": suggested_tool,
                "analysis": tool_result.analysis,
                "confidence_score": tool_result.confidence_score,
                "key_insights": self._extract_key_insights(tool_result.analysis),
                "supporting_data": tool_result.analysis
            }
        
        except Exception as e:
            logger.error(f"Error getting analysis from agent {agent_id}: {e}")
            return {
                "tool_used": "general_analysis",
                "analysis": {"error": str(e)},
                "confidence_score": 0.5,
                "key_insights": [],
                "supporting_data": {}
            }
    
    def _generate_agent_recommendations(
        self, 
        agent_id: str, 
        request: CollaborationRequest, 
        analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations from agent's perspective"""
        
        base_recommendations = []
        
        # Agent-specific recommendation patterns
        if agent_id == "1":  # Alex - Analytics
            base_recommendations = [
                "Analyze performance metrics to identify optimization opportunities",
                "Compare current performance against industry benchmarks",
                "Implement data-driven optimization strategies"
            ]
        elif agent_id == "2":  # Levi - Content
            base_recommendations = [
                "Optimize content strategy for better audience engagement",
                "Improve video structure and creative elements",
                "Develop content series for sustained audience interest"
            ]
        elif agent_id == "3":  # Maya - Engagement
            base_recommendations = [
                "Strengthen community engagement and interaction",
                "Implement audience retention strategies",
                "Build deeper audience relationships"
            ]
        elif agent_id == "4":  # Zara - Growth
            base_recommendations = [
                "Implement systematic growth strategies",
                "Optimize for algorithm performance and reach",
                "Scale content production efficiently"
            ]
        elif agent_id == "5":  # Kai - Technical
            base_recommendations = [
                "Optimize technical aspects for better discoverability",
                "Implement SEO best practices",
                "Improve platform-specific optimizations"
            ]
        
        # Customize based on analysis results
        if analysis.get("confidence_score", 0) > 0.8:
            base_recommendations.insert(0, "High-confidence recommendation based on strong data")
        
        return base_recommendations[:3]  # Top 3 recommendations
    
    def _identify_agent_concerns(
        self, 
        agent_id: str, 
        request: CollaborationRequest, 
        analysis: Dict[str, Any]
    ) -> List[str]:
        """Identify concerns from agent's perspective"""
        
        concerns = []
        
        # Agent-specific concern patterns
        if agent_id == "1":  # Alex - Analytics
            if request.channel_profile.metrics.avg_ctr < 0.04:
                concerns.append("Low CTR indicates thumbnail/title optimization needed")
            if request.channel_profile.metrics.avg_retention < 0.40:
                concerns.append("Poor retention suggests content structure issues")
        
        elif agent_id == "2":  # Levi - Content
            if "quality" in request.user_message.lower():
                concerns.append("Content quality improvements may require production investment")
            if request.channel_profile.channel_size_tier == "micro":
                concerns.append("Limited resources may constrain content production options")
        
        elif agent_id == "4":  # Zara - Growth
            if request.channel_profile.recent_performance.get("trend") == "declining":
                concerns.append("Declining trend requires immediate intervention")
            if request.channel_profile.channel_size_tier == "large":
                concerns.append("Scaling challenges may require team expansion")
        
        return concerns[:2]  # Top 2 concerns
    
    def _generate_collaboration_notes(
        self, 
        agent_id: str, 
        request: CollaborationRequest, 
        context: Dict[str, Any]
    ) -> List[str]:
        """Generate notes about collaboration dynamics"""
        
        notes = []
        
        # Check for previous insights from other agents
        previous_insights = context.get("previous_insights", {})
        
        if previous_insights:
            notes.append(f"Building on insights from {len(previous_insights)} previous agents")
        
        # Add agent-specific collaboration notes
        agent_relationships = self.agent_relationships["collaboration_strengths"].get(agent_id, {})
        
        if agent_relationships.get("challenges_constructively"):
            notes.append("May provide alternative perspective to challenge assumptions")
        
        if agent_relationships.get("supports_well"):
            notes.append("Provides supporting analysis for comprehensive solution")
        
        return notes
    
    async def _facilitate_debates(
        self, 
        request: CollaborationRequest, 
        contributions: List[AgentContribution], 
        pattern: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Facilitate debates between agents with different perspectives"""
        
        debates = []
        
        try:
            # Identify potential debate points
            debate_opportunities = self._identify_debate_opportunities(contributions)
            
            for debate_topic in debate_opportunities:
                debate_result = await self._conduct_debate(
                    request, contributions, debate_topic
                )
                debates.append(debate_result)
        
        except Exception as e:
            logger.error(f"Error facilitating debates: {e}")
        
        return debates
    
    def _identify_debate_opportunities(
        self, 
        contributions: List[AgentContribution]
    ) -> List[Dict[str, Any]]:
        """Identify opportunities for constructive debate"""
        
        opportunities = []
        
        # Look for conflicting recommendations
        all_recommendations = []
        for contrib in contributions:
            for rec in contrib.recommendations:
                all_recommendations.append({
                    "agent_id": contrib.agent_id,
                    "agent_name": contrib.agent_name,
                    "recommendation": rec
                })
        
        # Simple conflict detection (could be enhanced)
        conflicts = []
        for i, rec1 in enumerate(all_recommendations):
            for rec2 in all_recommendations[i+1:]:
                if self._recommendations_conflict(rec1["recommendation"], rec2["recommendation"]):
                    conflicts.append({
                        "topic": "Strategy Approach",
                        "agent1": rec1["agent_id"],
                        "agent2": rec2["agent_id"],
                        "position1": rec1["recommendation"],
                        "position2": rec2["recommendation"]
                    })
        
        return conflicts[:2]  # Limit to 2 debates for manageable discussion
    
    def _recommendations_conflict(self, rec1: str, rec2: str) -> bool:
        """Check if two recommendations conflict"""
        
        # Simple conflict detection based on keywords
        conflict_pairs = [
            (["fast", "quick", "rapid"], ["slow", "careful", "gradual"]),
            (["scale", "expand", "grow"], ["focus", "narrow", "specialize"]),
            (["data", "metrics", "analytics"], ["creative", "intuitive", "artistic"])
        ]
        
        rec1_lower = rec1.lower()
        rec2_lower = rec2.lower()
        
        for group1, group2 in conflict_pairs:
            has_group1_in_rec1 = any(word in rec1_lower for word in group1)
            has_group2_in_rec2 = any(word in rec2_lower for word in group2)
            
            if has_group1_in_rec1 and has_group2_in_rec2:
                return True
        
        return False
    
    async def _conduct_debate(
        self, 
        request: CollaborationRequest, 
        contributions: List[AgentContribution], 
        debate_topic: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Conduct a structured debate between agents"""
        
        try:
            agent1_id = debate_topic["agent1"]
            agent2_id = debate_topic["agent2"]
            
            # Get agent personalities
            agent1 = get_agent_personality(agent1_id)
            agent2 = get_agent_personality(agent2_id)
            
            # Simulate debate resolution
            resolution = self._resolve_debate(debate_topic, request.channel_profile)
            
            return {
                "topic": debate_topic["topic"],
                "participants": [
                    {"id": agent1_id, "name": agent1["name"], "position": debate_topic["position1"]},
                    {"id": agent2_id, "name": agent2["name"], "position": debate_topic["position2"]}
                ],
                "resolution": resolution,
                "synthesis": f"Balanced approach combining {agent1['name']}'s {debate_topic['position1'][:30]}... with {agent2['name']}'s {debate_topic['position2'][:30]}..."
            }
        
        except Exception as e:
            logger.error(f"Error conducting debate: {e}")
            return {
                "topic": "General Strategy",
                "participants": [],
                "resolution": "Collaborative approach recommended",
                "synthesis": "Multiple perspectives considered for optimal solution"
            }
    
    def _resolve_debate(self, debate_topic: Dict[str, Any], profile: ChannelProfile) -> str:
        """Resolve debate based on channel context"""
        
        # Simple resolution logic based on channel characteristics
        if profile.channel_size_tier == "micro":
            return "Focus approach recommended for micro channels"
        elif profile.channel_size_tier == "large":
            return "Scaling approach recommended for large channels"
        else:
            return "Balanced approach combining both perspectives"
    
    async def _synthesize_recommendations(
        self, 
        request: CollaborationRequest, 
        contributions: List[AgentContribution], 
        debates: List[Dict[str, Any]]
    ) -> List[str]:
        """Synthesize unified recommendations from all contributions"""
        
        unified = []
        
        try:
            # Collect all recommendations
            all_recommendations = []
            for contrib in contributions:
                all_recommendations.extend(contrib.recommendations)
            
            # Group similar recommendations
            grouped_recommendations = self._group_similar_recommendations(all_recommendations)
            
            # Create unified recommendations
            for group in grouped_recommendations:
                if len(group) >= 2:  # If multiple agents agree
                    unified.append(f"Multi-agent consensus: {group[0]}")
                else:
                    unified.append(group[0])
            
            # Add debate resolutions
            for debate in debates:
                unified.append(f"Collaborative resolution: {debate['synthesis']}")
            
            # Prioritize based on channel needs
            prioritized = self._prioritize_recommendations(unified, request.channel_profile)
            
            return prioritized[:5]  # Top 5 unified recommendations
        
        except Exception as e:
            logger.error(f"Error synthesizing recommendations: {e}")
            return ["Comprehensive multi-agent analysis completed", "Collaborative approach recommended"]
    
    def _group_similar_recommendations(self, recommendations: List[str]) -> List[List[str]]:
        """Group similar recommendations together"""
        
        groups = []
        used_indices = set()
        
        for i, rec1 in enumerate(recommendations):
            if i in used_indices:
                continue
            
            group = [rec1]
            used_indices.add(i)
            
            for j, rec2 in enumerate(recommendations[i+1:], i+1):
                if j in used_indices:
                    continue
                
                if self._recommendations_similar(rec1, rec2):
                    group.append(rec2)
                    used_indices.add(j)
            
            groups.append(group)
        
        return groups
    
    def _recommendations_similar(self, rec1: str, rec2: str) -> bool:
        """Check if two recommendations are similar"""
        
        # Simple similarity check based on common keywords
        rec1_words = set(rec1.lower().split())
        rec2_words = set(rec2.lower().split())
        
        common_words = rec1_words & rec2_words
        total_words = rec1_words | rec2_words
        
        similarity = len(common_words) / len(total_words) if total_words else 0
        
        return similarity > 0.3  # 30% similarity threshold
    
    def _prioritize_recommendations(
        self, 
        recommendations: List[str], 
        profile: ChannelProfile
    ) -> List[str]:
        """Prioritize recommendations based on channel needs"""
        
        prioritized = []
        
        # High priority for urgent issues
        if profile.metrics.avg_ctr < 0.03:
            urgent_recs = [rec for rec in recommendations if "ctr" in rec.lower() or "thumbnail" in rec.lower()]
            prioritized.extend(urgent_recs)
        
        # Add remaining recommendations
        for rec in recommendations:
            if rec not in prioritized:
                prioritized.append(rec)
        
        return prioritized
    
    def _identify_consensus_areas(self, contributions: List[AgentContribution]) -> List[str]:
        """Identify areas where agents agree"""
        
        consensus = []
        
        # Look for common themes in recommendations
        all_recommendations = []
        for contrib in contributions:
            all_recommendations.extend(contrib.recommendations)
        
        # Simple consensus detection
        word_counts = {}
        for rec in all_recommendations:
            words = rec.lower().split()
            for word in words:
                if len(word) > 4:  # Only count meaningful words
                    word_counts[word] = word_counts.get(word, 0) + 1
        
        # Find words mentioned by multiple agents
        consensus_words = [word for word, count in word_counts.items() if count >= 2]
        
        if consensus_words:
            consensus.append(f"Strong agreement on: {', '.join(consensus_words[:3])}")
        
        return consensus
    
    async def _create_unified_action_plan(
        self, 
        request: CollaborationRequest, 
        contributions: List[AgentContribution], 
        recommendations: List[str]
    ) -> Dict[str, Any]:
        """Create a unified action plan"""
        
        action_plan = {
            "immediate_actions": [],
            "short_term_goals": [],
            "long_term_strategy": [],
            "success_metrics": [],
            "timeline": "4-6 weeks for initial implementation"
        }
        
        try:
            # Extract actions from recommendations
            for rec in recommendations[:3]:  # Top 3 recommendations
                if any(word in rec.lower() for word in ["immediate", "urgent", "now"]):
                    action_plan["immediate_actions"].append(rec)
                elif any(word in rec.lower() for word in ["strategy", "plan", "long"]):
                    action_plan["long_term_strategy"].append(rec)
                else:
                    action_plan["short_term_goals"].append(rec)
            
            # Add success metrics based on agent contributions
            for contrib in contributions:
                if contrib.agent_id == "1":  # Alex - Analytics
                    action_plan["success_metrics"].append("Performance metrics improvement")
                elif contrib.agent_id == "4":  # Zara - Growth
                    action_plan["success_metrics"].append("Growth rate acceleration")
        
        except Exception as e:
            logger.error(f"Error creating action plan: {e}")
        
        return action_plan
    
    def _calculate_collaboration_confidence(self, contributions: List[AgentContribution]) -> float:
        """Calculate overall confidence in collaboration result"""
        
        if not contributions:
            return 0.5
        
        # Average confidence scores
        total_confidence = sum(contrib.confidence_score for contrib in contributions)
        avg_confidence = total_confidence / len(contributions)
        
        # Boost for multiple agent agreement
        if len(contributions) >= 3:
            avg_confidence += 0.1
        
        return min(avg_confidence, 1.0)
    
    def _generate_collaboration_summary(
        self, 
        request: CollaborationRequest, 
        contributions: List[AgentContribution], 
        recommendations: List[str]
    ) -> str:
        """Generate summary of collaboration"""
        
        agent_names = [contrib.agent_name for contrib in contributions]
        
        summary = f"Collaborative analysis by {', '.join(agent_names)} "
        summary += f"addressing '{request.user_message[:50]}...' "
        summary += f"resulted in {len(recommendations)} unified recommendations "
        summary += f"with {len(contributions)} expert perspectives considered."
        
        return summary
    
    def _synthesize_problem_analysis(self, contributions: List[AgentContribution]) -> Dict[str, Any]:
        """Synthesize problem analysis from all contributions"""
        
        analysis = {
            "problem_scope": "Multi-faceted challenge requiring diverse expertise",
            "key_factors": [],
            "root_causes": [],
            "impact_assessment": "Moderate to high impact on channel performance"
        }
        
        # Extract key factors from contributions
        for contrib in contributions:
            if contrib.analysis.get("key_insights"):
                analysis["key_factors"].extend(contrib.analysis["key_insights"][:2])
        
        return analysis
    
    def _get_fallback_contribution(self, agent_id: str) -> AgentContribution:
        """Get fallback contribution when agent analysis fails"""
        
        agent = get_agent_personality(agent_id)
        
        return AgentContribution(
            agent_id=agent_id,
            agent_name=agent["name"],
            perspective="General optimization perspective",
            analysis={"error": "Analysis unavailable"},
            recommendations=[f"{agent['name']} recommends comprehensive optimization"],
            concerns=["Limited analysis available"],
            supporting_data={},
            confidence_score=0.5,
            collaboration_notes=["Fallback contribution due to analysis limitation"]
        )
    
    def _generate_fallback_collaboration(self, request: CollaborationRequest) -> CollaborationResult:
        """Generate fallback collaboration result"""
        
        return CollaborationResult(
            primary_agent_id=request.primary_agent_id,
            participating_agents=[request.primary_agent_id],
            problem_analysis={"error": "Collaboration analysis unavailable"},
            unified_recommendations=["Comprehensive analysis recommended"],
            perspective_breakdown=[],
            consensus_areas=["General optimization approach"],
            debate_points=[],
            action_plan={"immediate_actions": ["Seek detailed analysis"]},
            confidence_score=0.5,
            collaboration_summary="Fallback collaboration due to system limitation"
        )
    
    def _extract_key_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """Extract key insights from analysis"""
        
        insights = []
        
        # Extract insights from different analysis sections
        if "overall_score" in analysis:
            insights.append(f"Overall performance score: {analysis['overall_score']}")
        
        if "ctr_analysis" in analysis:
            ctr_status = analysis["ctr_analysis"].get("status", "unknown")
            insights.append(f"CTR performance: {ctr_status}")
        
        if "retention_analysis" in analysis:
            retention_status = analysis["retention_analysis"].get("status", "unknown")
            insights.append(f"Retention performance: {retention_status}")
        
        return insights[:3]  # Top 3 insights

# Global collaboration engine instance
_collaboration_engine: Optional[AgentCollaborationEngine] = None

def get_collaboration_engine() -> AgentCollaborationEngine:
    """Get or create global collaboration engine instance"""
    global _collaboration_engine
    if _collaboration_engine is None:
        _collaboration_engine = AgentCollaborationEngine()
    return _collaboration_engine
