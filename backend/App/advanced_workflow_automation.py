"""
Advanced Workflow Automation System
Pre-built collaboration templates and one-click complex workflows
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import json
import uuid

from backend.App.intelligent_agent_workflows import create_intelligent_workflow, execute_intelligent_workflow
from backend.App.proactive_agent_collaboration import create_collaboration_session

logger = logging.getLogger(__name__)

class WorkflowCategory(Enum):
    CONTENT_OPTIMIZATION = "content_optimization"
    CHANNEL_GROWTH = "channel_growth"
    MONETIZATION = "monetization"
    COMPETITIVE_ANALYSIS = "competitive_analysis"
    AUDIENCE_DEVELOPMENT = "audience_development"
    CRISIS_MANAGEMENT = "crisis_management"

class AutomationTrigger(Enum):
    MANUAL = "manual"                    # User-initiated
    SCHEDULED = "scheduled"              # Time-based
    PERFORMANCE_BASED = "performance"    # Triggered by metrics
    EVENT_BASED = "event"               # Triggered by specific events
    THRESHOLD_BASED = "threshold"       # Triggered by crossing thresholds

@dataclass
class WorkflowTemplate:
    template_id: str
    name: str
    description: str
    category: WorkflowCategory
    estimated_duration: int  # minutes
    complexity_level: str    # "beginner", "intermediate", "advanced", "expert"
    required_agents: List[str]
    workflow_steps: List[Dict[str, Any]]
    success_metrics: List[str]
    automation_triggers: List[AutomationTrigger]
    prerequisites: List[str]
    expected_outcomes: List[str]

@dataclass
class AutomatedWorkflow:
    workflow_id: str
    template_id: str
    user_id: str
    trigger_type: AutomationTrigger
    trigger_conditions: Dict[str, Any]
    schedule: Optional[Dict[str, Any]]
    status: str  # "active", "paused", "completed", "failed"
    last_execution: Optional[datetime]
    next_execution: Optional[datetime]
    execution_count: int
    success_rate: float
    created_at: datetime

class AdvancedWorkflowAutomation:
    """Advanced workflow automation with pre-built templates and smart triggers"""
    
    def __init__(self):
        self.workflow_templates = self._load_workflow_templates()
        self.automated_workflows: Dict[str, AutomatedWorkflow] = {}
        self.execution_history: List[Dict[str, Any]] = []
        
    def _load_workflow_templates(self) -> Dict[str, WorkflowTemplate]:
        """Load pre-built workflow templates"""
        
        templates = {}
        
        # 1. Complete Video Optimization Workflow
        templates["complete_video_optimization"] = WorkflowTemplate(
            template_id="complete_video_optimization",
            name="Complete Video Optimization",
            description="Comprehensive analysis and optimization of a specific video",
            category=WorkflowCategory.CONTENT_OPTIMIZATION,
            estimated_duration=15,
            complexity_level="intermediate",
            required_agents=["content_analysis", "seo_optimization", "audience_insights", "competitive_analysis"],
            workflow_steps=[
                {
                    "step": 1,
                    "name": "Content Performance Analysis",
                    "agent": "content_analysis",
                    "action": "analyze_video_performance",
                    "parameters": {"include_engagement": True, "include_retention": True}
                },
                {
                    "step": 2,
                    "name": "SEO Optimization Analysis",
                    "agent": "seo_optimization",
                    "action": "analyze_seo_elements",
                    "parameters": {"include_keywords": True, "include_metadata": True},
                    "depends_on": [1]
                },
                {
                    "step": 3,
                    "name": "Audience Engagement Analysis",
                    "agent": "audience_insights",
                    "action": "analyze_audience_response",
                    "parameters": {"include_demographics": True, "include_behavior": True},
                    "depends_on": [1]
                },
                {
                    "step": 4,
                    "name": "Competitive Positioning",
                    "agent": "competitive_analysis",
                    "action": "analyze_competitive_position",
                    "parameters": {"include_benchmarking": True},
                    "depends_on": [1, 2, 3]
                }
            ],
            success_metrics=["engagement_improvement", "seo_score_increase", "competitive_advantage"],
            automation_triggers=[AutomationTrigger.MANUAL, AutomationTrigger.PERFORMANCE_BASED],
            prerequisites=["video_data_available", "youtube_connected"],
            expected_outcomes=[
                "Detailed performance analysis",
                "SEO optimization recommendations",
                "Audience engagement insights",
                "Competitive positioning strategy"
            ]
        )
        
        # 2. Channel Growth Strategy Workflow
        templates["channel_growth_strategy"] = WorkflowTemplate(
            template_id="channel_growth_strategy",
            name="Channel Growth Strategy",
            description="Comprehensive strategy for accelerating channel growth",
            category=WorkflowCategory.CHANNEL_GROWTH,
            estimated_duration=25,
            complexity_level="advanced",
            required_agents=["audience_insights", "competitive_analysis", "seo_optimization", "content_analysis", "monetization"],
            workflow_steps=[
                {
                    "step": 1,
                    "name": "Audience Growth Analysis",
                    "agent": "audience_insights",
                    "action": "analyze_growth_potential",
                    "parameters": {"include_demographics": True, "include_trends": True}
                },
                {
                    "step": 2,
                    "name": "Market Opportunity Analysis",
                    "agent": "competitive_analysis",
                    "action": "identify_market_opportunities",
                    "parameters": {"include_gaps": True, "include_trends": True}
                },
                {
                    "step": 3,
                    "name": "Content Strategy Optimization",
                    "agent": "content_analysis",
                    "action": "optimize_content_strategy",
                    "parameters": {"include_performance": True, "include_recommendations": True},
                    "depends_on": [1, 2]
                },
                {
                    "step": 4,
                    "name": "SEO Growth Strategy",
                    "agent": "seo_optimization",
                    "action": "develop_seo_growth_plan",
                    "parameters": {"include_keywords": True, "include_optimization": True},
                    "depends_on": [2, 3]
                },
                {
                    "step": 5,
                    "name": "Monetization Alignment",
                    "agent": "monetization",
                    "action": "align_monetization_with_growth",
                    "parameters": {"include_revenue_projections": True},
                    "depends_on": [1, 3, 4]
                }
            ],
            success_metrics=["subscriber_growth_rate", "engagement_rate", "content_performance", "revenue_growth"],
            automation_triggers=[AutomationTrigger.MANUAL, AutomationTrigger.SCHEDULED],
            prerequisites=["channel_data_available", "growth_goals_defined"],
            expected_outcomes=[
                "Comprehensive growth strategy",
                "Content optimization plan",
                "SEO growth roadmap",
                "Monetization alignment strategy"
            ]
        )
        
        # 3. Crisis Management Workflow
        templates["crisis_management"] = WorkflowTemplate(
            template_id="crisis_management",
            name="Crisis Management Response",
            description="Rapid response workflow for performance drops or issues",
            category=WorkflowCategory.CRISIS_MANAGEMENT,
            estimated_duration=10,
            complexity_level="expert",
            required_agents=["content_analysis", "audience_insights", "competitive_analysis"],
            workflow_steps=[
                {
                    "step": 1,
                    "name": "Performance Drop Analysis",
                    "agent": "content_analysis",
                    "action": "analyze_performance_drop",
                    "parameters": {"urgent": True, "include_recent_changes": True}
                },
                {
                    "step": 2,
                    "name": "Audience Reaction Analysis",
                    "agent": "audience_insights",
                    "action": "analyze_audience_sentiment",
                    "parameters": {"urgent": True, "include_engagement_changes": True},
                    "depends_on": [1]
                },
                {
                    "step": 3,
                    "name": "Competitive Impact Assessment",
                    "agent": "competitive_analysis",
                    "action": "assess_competitive_impact",
                    "parameters": {"urgent": True, "include_market_changes": True},
                    "depends_on": [1, 2]
                }
            ],
            success_metrics=["issue_identification", "recovery_plan", "implementation_speed"],
            automation_triggers=[AutomationTrigger.THRESHOLD_BASED, AutomationTrigger.PERFORMANCE_BASED],
            prerequisites=["performance_monitoring_active"],
            expected_outcomes=[
                "Root cause identification",
                "Immediate action plan",
                "Recovery strategy",
                "Prevention recommendations"
            ]
        )
        
        # 4. Monetization Optimization Workflow
        templates["monetization_optimization"] = WorkflowTemplate(
            template_id="monetization_optimization",
            name="Monetization Optimization",
            description="Comprehensive revenue optimization and strategy development",
            category=WorkflowCategory.MONETIZATION,
            estimated_duration=20,
            complexity_level="advanced",
            required_agents=["monetization", "audience_insights", "competitive_analysis", "content_analysis"],
            workflow_steps=[
                {
                    "step": 1,
                    "name": "Revenue Analysis",
                    "agent": "monetization",
                    "action": "analyze_current_revenue",
                    "parameters": {"include_all_streams": True, "include_trends": True}
                },
                {
                    "step": 2,
                    "name": "Audience Value Analysis",
                    "agent": "audience_insights",
                    "action": "analyze_audience_value",
                    "parameters": {"include_purchasing_behavior": True, "include_engagement_value": True}
                },
                {
                    "step": 3,
                    "name": "Content Monetization Analysis",
                    "agent": "content_analysis",
                    "action": "analyze_content_monetization",
                    "parameters": {"include_performance_correlation": True},
                    "depends_on": [1, 2]
                },
                {
                    "step": 4,
                    "name": "Competitive Revenue Analysis",
                    "agent": "competitive_analysis",
                    "action": "analyze_competitive_monetization",
                    "parameters": {"include_strategies": True, "include_opportunities": True},
                    "depends_on": [1, 2, 3]
                }
            ],
            success_metrics=["revenue_increase", "monetization_efficiency", "new_revenue_streams"],
            automation_triggers=[AutomationTrigger.MANUAL, AutomationTrigger.SCHEDULED],
            prerequisites=["monetization_data_available", "revenue_goals_defined"],
            expected_outcomes=[
                "Revenue optimization plan",
                "New monetization opportunities",
                "Audience value maximization",
                "Competitive monetization insights"
            ]
        )
        
        # 5. Weekly Performance Review Workflow
        templates["weekly_performance_review"] = WorkflowTemplate(
            template_id="weekly_performance_review",
            name="Weekly Performance Review",
            description="Automated weekly analysis of channel performance",
            category=WorkflowCategory.CONTENT_OPTIMIZATION,
            estimated_duration=12,
            complexity_level="beginner",
            required_agents=["content_analysis", "audience_insights", "seo_optimization"],
            workflow_steps=[
                {
                    "step": 1,
                    "name": "Weekly Content Performance",
                    "agent": "content_analysis",
                    "action": "analyze_weekly_performance",
                    "parameters": {"timeframe": "7_days", "include_trends": True}
                },
                {
                    "step": 2,
                    "name": "Audience Engagement Review",
                    "agent": "audience_insights",
                    "action": "review_weekly_engagement",
                    "parameters": {"timeframe": "7_days", "include_growth": True}
                },
                {
                    "step": 3,
                    "name": "SEO Performance Review",
                    "agent": "seo_optimization",
                    "action": "review_seo_performance",
                    "parameters": {"timeframe": "7_days", "include_rankings": True}
                }
            ],
            success_metrics=["performance_tracking", "trend_identification", "optimization_opportunities"],
            automation_triggers=[AutomationTrigger.SCHEDULED],
            prerequisites=["performance_data_available"],
            expected_outcomes=[
                "Weekly performance summary",
                "Trend analysis",
                "Optimization recommendations",
                "Next week planning insights"
            ]
        )
        
        return templates

    async def execute_one_click_workflow(
        self,
        template_id: str,
        user_id: str,
        context: Dict[str, Any],
        custom_parameters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute a pre-built workflow template with one click"""

        if template_id not in self.workflow_templates:
            raise ValueError(f"Workflow template {template_id} not found")

        template = self.workflow_templates[template_id]

        logger.info(f"🚀 Executing one-click workflow: {template.name} for user {user_id}")

        try:
            # Create enhanced context with template information
            enhanced_context = context.copy()
            enhanced_context.update({
                "workflow_template": template_id,
                "workflow_name": template.name,
                "workflow_category": template.category.value,
                "custom_parameters": custom_parameters or {}
            })

            # Create intelligent workflow based on template
            workflow_request = f"Execute {template.name}: {template.description}"
            workflow = await create_intelligent_workflow(user_id, workflow_request, enhanced_context)

            # Execute the workflow
            execution_result = await execute_intelligent_workflow(workflow.workflow_id)

            # Record execution
            execution_record = {
                "execution_id": str(uuid.uuid4()),
                "template_id": template_id,
                "workflow_id": workflow.workflow_id,
                "user_id": user_id,
                "execution_time": datetime.now(),
                "success": execution_result.get("success", False),
                "duration": execution_result.get("execution_time", 0),
                "agents_used": execution_result.get("results", {}).get("workflow_summary", {}).get("agents_involved", [])
            }

            self.execution_history.append(execution_record)

            # Format results for one-click workflow response
            if execution_result.get("success", False):
                results = execution_result["results"]

                formatted_response = {
                    "success": True,
                    "workflow_name": template.name,
                    "execution_time": execution_result.get("execution_time", 0),
                    "agents_involved": results.get("workflow_summary", {}).get("agents_involved", []),
                    "key_insights": results.get("key_insights", [])[:5],
                    "recommendations": results.get("recommendations", [])[:5],
                    "action_plan": results.get("action_plan", []),
                    "success_metrics": template.success_metrics,
                    "expected_outcomes_achieved": self._evaluate_outcomes(template, results),
                    "workflow_id": workflow.workflow_id,
                    "execution_id": execution_record["execution_id"]
                }

                logger.info(f"✅ One-click workflow completed: {template.name} in {execution_result.get('execution_time', 0):.1f}s")

                return formatted_response
            else:
                logger.error(f"❌ One-click workflow failed: {template.name}")
                return {
                    "success": False,
                    "workflow_name": template.name,
                    "error": execution_result.get("error", "Unknown error"),
                    "execution_id": execution_record["execution_id"]
                }

        except Exception as e:
            logger.error(f"One-click workflow execution failed for {template_id}: {e}")
            return {
                "success": False,
                "workflow_name": template.name,
                "error": str(e)
            }

    def _evaluate_outcomes(self, template: WorkflowTemplate, results: Dict[str, Any]) -> List[str]:
        """Evaluate which expected outcomes were achieved"""

        achieved_outcomes = []

        # Simple heuristic evaluation based on results content
        for outcome in template.expected_outcomes:
            outcome_lower = outcome.lower()

            # Check if outcome-related content exists in results
            if any(outcome_lower in str(value).lower() for value in results.values() if isinstance(value, (str, list))):
                achieved_outcomes.append(outcome)
            elif "analysis" in outcome_lower and results.get("key_insights"):
                achieved_outcomes.append(outcome)
            elif "strategy" in outcome_lower and results.get("action_plan"):
                achieved_outcomes.append(outcome)
            elif "recommendations" in outcome_lower and results.get("recommendations"):
                achieved_outcomes.append(outcome)

        return achieved_outcomes

    async def create_automated_workflow(
        self,
        template_id: str,
        user_id: str,
        trigger_type: AutomationTrigger,
        trigger_conditions: Dict[str, Any],
        schedule: Optional[Dict[str, Any]] = None
    ) -> AutomatedWorkflow:
        """Create an automated workflow that runs based on triggers"""

        if template_id not in self.workflow_templates:
            raise ValueError(f"Workflow template {template_id} not found")

        template = self.workflow_templates[template_id]

        if trigger_type not in template.automation_triggers:
            raise ValueError(f"Trigger type {trigger_type.value} not supported for template {template_id}")

        automated_workflow = AutomatedWorkflow(
            workflow_id=str(uuid.uuid4()),
            template_id=template_id,
            user_id=user_id,
            trigger_type=trigger_type,
            trigger_conditions=trigger_conditions,
            schedule=schedule,
            status="active",
            last_execution=None,
            next_execution=self._calculate_next_execution(trigger_type, schedule),
            execution_count=0,
            success_rate=0.0,
            created_at=datetime.now()
        )

        self.automated_workflows[automated_workflow.workflow_id] = automated_workflow

        logger.info(f"🤖 Created automated workflow: {template.name} with {trigger_type.value} trigger")

        return automated_workflow

    def _calculate_next_execution(self, trigger_type: AutomationTrigger, schedule: Optional[Dict[str, Any]]) -> Optional[datetime]:
        """Calculate when the next execution should occur"""

        if trigger_type == AutomationTrigger.SCHEDULED and schedule:
            if schedule.get("frequency") == "daily":
                return datetime.now() + timedelta(days=1)
            elif schedule.get("frequency") == "weekly":
                return datetime.now() + timedelta(weeks=1)
            elif schedule.get("frequency") == "monthly":
                return datetime.now() + timedelta(days=30)
            elif schedule.get("custom_interval_hours"):
                return datetime.now() + timedelta(hours=schedule["custom_interval_hours"])

        return None

    async def check_and_execute_automated_workflows(self, user_id: str, current_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check triggers and execute automated workflows"""

        executed_workflows = []

        for workflow in self.automated_workflows.values():
            if workflow.user_id != user_id or workflow.status != "active":
                continue

            should_execute = False

            # Check different trigger types
            if workflow.trigger_type == AutomationTrigger.SCHEDULED:
                if workflow.next_execution and datetime.now() >= workflow.next_execution:
                    should_execute = True

            elif workflow.trigger_type == AutomationTrigger.THRESHOLD_BASED:
                should_execute = self._check_threshold_triggers(workflow.trigger_conditions, current_metrics)

            elif workflow.trigger_type == AutomationTrigger.PERFORMANCE_BASED:
                should_execute = self._check_performance_triggers(workflow.trigger_conditions, current_metrics)

            elif workflow.trigger_type == AutomationTrigger.EVENT_BASED:
                should_execute = self._check_event_triggers(workflow.trigger_conditions, current_metrics)

            if should_execute:
                try:
                    # Execute the automated workflow
                    execution_result = await self.execute_one_click_workflow(
                        workflow.template_id,
                        workflow.user_id,
                        {"automated_execution": True, "trigger_type": workflow.trigger_type.value}
                    )

                    # Update workflow statistics
                    workflow.last_execution = datetime.now()
                    workflow.execution_count += 1

                    if execution_result.get("success", False):
                        workflow.success_rate = ((workflow.success_rate * (workflow.execution_count - 1)) + 1.0) / workflow.execution_count
                    else:
                        workflow.success_rate = (workflow.success_rate * (workflow.execution_count - 1)) / workflow.execution_count

                    # Calculate next execution for scheduled workflows
                    if workflow.trigger_type == AutomationTrigger.SCHEDULED:
                        workflow.next_execution = self._calculate_next_execution(workflow.trigger_type, workflow.schedule)

                    executed_workflows.append({
                        "workflow_id": workflow.workflow_id,
                        "template_id": workflow.template_id,
                        "execution_result": execution_result,
                        "trigger_type": workflow.trigger_type.value
                    })

                    logger.info(f"🤖 Automated workflow executed: {workflow.template_id}")

                except Exception as e:
                    logger.error(f"Automated workflow execution failed for {workflow.workflow_id}: {e}")
                    workflow.success_rate = (workflow.success_rate * (workflow.execution_count - 1)) / max(workflow.execution_count, 1)

        return executed_workflows

    def _check_threshold_triggers(self, trigger_conditions: Dict[str, Any], current_metrics: Dict[str, Any]) -> bool:
        """Check if threshold-based triggers are met"""

        for metric, threshold_config in trigger_conditions.items():
            current_value = current_metrics.get(metric, 0)
            threshold_value = threshold_config.get("threshold", 0)
            operator = threshold_config.get("operator", "less_than")  # "less_than", "greater_than", "equals"

            if operator == "less_than" and current_value < threshold_value:
                return True
            elif operator == "greater_than" and current_value > threshold_value:
                return True
            elif operator == "equals" and current_value == threshold_value:
                return True

        return False

    def _check_performance_triggers(self, trigger_conditions: Dict[str, Any], current_metrics: Dict[str, Any]) -> bool:
        """Check if performance-based triggers are met"""

        # Check for performance drops
        if "performance_drop" in trigger_conditions:
            drop_config = trigger_conditions["performance_drop"]
            metric = drop_config.get("metric", "engagement_rate")
            drop_percentage = drop_config.get("drop_percentage", 20)  # 20% drop

            current_value = current_metrics.get(metric, 0)
            baseline_value = current_metrics.get(f"{metric}_baseline", current_value)

            if baseline_value > 0:
                drop_percent = ((baseline_value - current_value) / baseline_value) * 100
                if drop_percent >= drop_percentage:
                    return True

        # Check for performance improvements
        if "performance_improvement" in trigger_conditions:
            improvement_config = trigger_conditions["performance_improvement"]
            metric = improvement_config.get("metric", "views")
            improvement_percentage = improvement_config.get("improvement_percentage", 50)  # 50% improvement

            current_value = current_metrics.get(metric, 0)
            baseline_value = current_metrics.get(f"{metric}_baseline", current_value)

            if baseline_value > 0:
                improvement_percent = ((current_value - baseline_value) / baseline_value) * 100
                if improvement_percent >= improvement_percentage:
                    return True

        return False

    def _check_event_triggers(self, trigger_conditions: Dict[str, Any], current_metrics: Dict[str, Any]) -> bool:
        """Check if event-based triggers are met"""

        # Check for specific events
        events_to_check = trigger_conditions.get("events", [])
        current_events = current_metrics.get("recent_events", [])

        for event in events_to_check:
            if event in current_events:
                return True

        # Check for milestone achievements
        if "milestone" in trigger_conditions:
            milestone_config = trigger_conditions["milestone"]
            metric = milestone_config.get("metric", "subscribers")
            milestone_value = milestone_config.get("value", 1000)

            current_value = current_metrics.get(metric, 0)
            if current_value >= milestone_value:
                return True

        return False

    def get_available_templates(self, category: Optional[WorkflowCategory] = None) -> List[Dict[str, Any]]:
        """Get available workflow templates, optionally filtered by category"""

        templates = []

        for template in self.workflow_templates.values():
            if category is None or template.category == category:
                templates.append({
                    "template_id": template.template_id,
                    "name": template.name,
                    "description": template.description,
                    "category": template.category.value,
                    "estimated_duration": template.estimated_duration,
                    "complexity_level": template.complexity_level,
                    "required_agents": template.required_agents,
                    "success_metrics": template.success_metrics,
                    "automation_triggers": [trigger.value for trigger in template.automation_triggers],
                    "expected_outcomes": template.expected_outcomes
                })

        return templates

    def get_automation_statistics(self, user_id: str) -> Dict[str, Any]:
        """Get automation statistics for a user"""

        user_workflows = [w for w in self.automated_workflows.values() if w.user_id == user_id]
        user_executions = [e for e in self.execution_history if e["user_id"] == user_id]

        if not user_workflows and not user_executions:
            return {
                "total_automated_workflows": 0,
                "total_executions": 0,
                "average_success_rate": 0.0,
                "most_used_template": None,
                "automation_savings_hours": 0.0
            }

        # Calculate statistics
        total_executions = len(user_executions)
        successful_executions = len([e for e in user_executions if e["success"]])
        average_success_rate = (successful_executions / total_executions) if total_executions > 0 else 0.0

        # Find most used template
        template_usage = {}
        for execution in user_executions:
            template_id = execution["template_id"]
            template_usage[template_id] = template_usage.get(template_id, 0) + 1

        most_used_template = max(template_usage.keys(), key=template_usage.get) if template_usage else None

        # Calculate time savings (estimated)
        total_duration_saved = sum(
            self.workflow_templates[e["template_id"]].estimated_duration
            for e in user_executions
            if e["template_id"] in self.workflow_templates
        )
        automation_savings_hours = total_duration_saved / 60.0  # Convert minutes to hours

        return {
            "total_automated_workflows": len(user_workflows),
            "active_automated_workflows": len([w for w in user_workflows if w.status == "active"]),
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "average_success_rate": average_success_rate,
            "most_used_template": most_used_template,
            "template_usage": template_usage,
            "automation_savings_hours": automation_savings_hours,
            "recent_executions": user_executions[-5:] if user_executions else []
        }

# Global workflow automation instance
workflow_automation = AdvancedWorkflowAutomation()

async def execute_one_click_workflow(
    template_id: str,
    user_id: str,
    context: Dict[str, Any],
    custom_parameters: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Execute a one-click workflow template"""
    return await workflow_automation.execute_one_click_workflow(
        template_id, user_id, context, custom_parameters
    )

async def create_automated_workflow(
    template_id: str,
    user_id: str,
    trigger_type: AutomationTrigger,
    trigger_conditions: Dict[str, Any],
    schedule: Optional[Dict[str, Any]] = None
) -> AutomatedWorkflow:
    """Create an automated workflow"""
    return await workflow_automation.create_automated_workflow(
        template_id, user_id, trigger_type, trigger_conditions, schedule
    )

async def check_and_execute_automated_workflows(user_id: str, current_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Check and execute automated workflows for a user"""
    return await workflow_automation.check_and_execute_automated_workflows(user_id, current_metrics)

def get_available_workflow_templates(category: Optional[WorkflowCategory] = None) -> List[Dict[str, Any]]:
    """Get available workflow templates"""
    return workflow_automation.get_available_templates(category)

def get_automation_statistics(user_id: str) -> Dict[str, Any]:
    """Get automation statistics for a user"""
    return workflow_automation.get_automation_statistics(user_id)
