"""
Intelligent Agent Workflows System
Advanced task decomposition, dynamic agent chaining, and seamless context preservation
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import json

logger = logging.getLogger(__name__)

class WorkflowComplexity(Enum):
    SIMPLE = "simple"           # Single agent can handle
    MODERATE = "moderate"       # 2-3 agents needed
    COMPLEX = "complex"         # 4+ agents with dependencies
    ENTERPRISE = "enterprise"   # Full multi-agent orchestration

class TaskType(Enum):
    ANALYSIS = "analysis"
    OPTIMIZATION = "optimization"
    STRATEGY = "strategy"
    CREATION = "creation"
    MONITORING = "monitoring"

@dataclass
class WorkflowTask:
    task_id: str
    task_type: TaskType
    description: str
    required_agents: List[str]
    dependencies: List[str]  # Task IDs this depends on
    context_requirements: List[str]
    estimated_duration: int  # seconds
    priority: int  # 1-10, 10 being highest
    success_criteria: List[str]

@dataclass
class AgentHandoff:
    from_agent: str
    to_agent: str
    context_data: Dict[str, Any]
    handoff_reason: str
    timestamp: datetime
    success: bool

@dataclass
class WorkflowExecution:
    workflow_id: str
    user_id: str
    original_request: str
    decomposed_tasks: List[WorkflowTask]
    execution_plan: List[Dict[str, Any]]
    current_stage: int
    completed_tasks: List[str]
    active_tasks: List[str]
    agent_handoffs: List[AgentHandoff]
    accumulated_context: Dict[str, Any]
    start_time: datetime
    estimated_completion: datetime
    status: str  # "planning", "executing", "completed", "failed"

class IntelligentWorkflowEngine:
    """Advanced workflow engine for intelligent agent collaboration"""
    
    def __init__(self):
        self.active_workflows: Dict[str, WorkflowExecution] = {}
        self.workflow_templates = self._load_workflow_templates()
        self.agent_capabilities = self._load_agent_capabilities()
        
    def _load_workflow_templates(self) -> Dict[str, Any]:
        """Load pre-defined workflow templates for common tasks"""
        return {
            "video_optimization": {
                "name": "Complete Video Optimization",
                "description": "Full analysis and optimization of video content",
                "complexity": WorkflowComplexity.COMPLEX,
                "template_tasks": [
                    {
                        "task_type": TaskType.ANALYSIS,
                        "description": "Analyze video performance and content quality",
                        "required_agents": ["content_analysis"],
                        "dependencies": [],
                        "priority": 10
                    },
                    {
                        "task_type": TaskType.ANALYSIS,
                        "description": "Analyze audience engagement and demographics",
                        "required_agents": ["audience_insights"],
                        "dependencies": [],
                        "priority": 9
                    },
                    {
                        "task_type": TaskType.OPTIMIZATION,
                        "description": "Optimize SEO elements based on content analysis",
                        "required_agents": ["seo_optimization"],
                        "dependencies": ["content_analysis"],
                        "priority": 8
                    },
                    {
                        "task_type": TaskType.ANALYSIS,
                        "description": "Competitive landscape analysis",
                        "required_agents": ["competitive_analysis"],
                        "dependencies": ["content_analysis", "audience_insights"],
                        "priority": 7
                    },
                    {
                        "task_type": TaskType.STRATEGY,
                        "description": "Monetization strategy recommendations",
                        "required_agents": ["monetization"],
                        "dependencies": ["audience_insights", "competitive_analysis"],
                        "priority": 6
                    }
                ]
            },
            "content_strategy": {
                "name": "Comprehensive Content Strategy",
                "description": "Full content planning and strategy development",
                "complexity": WorkflowComplexity.COMPLEX,
                "template_tasks": [
                    {
                        "task_type": TaskType.ANALYSIS,
                        "description": "Audience behavior and preference analysis",
                        "required_agents": ["audience_insights"],
                        "dependencies": [],
                        "priority": 10
                    },
                    {
                        "task_type": TaskType.ANALYSIS,
                        "description": "Competitive content gap analysis",
                        "required_agents": ["competitive_analysis"],
                        "dependencies": [],
                        "priority": 9
                    },
                    {
                        "task_type": TaskType.STRATEGY,
                        "description": "SEO-optimized content topics and keywords",
                        "required_agents": ["seo_optimization"],
                        "dependencies": ["audience_insights", "competitive_analysis"],
                        "priority": 8
                    },
                    {
                        "task_type": TaskType.STRATEGY,
                        "description": "Content monetization and revenue optimization",
                        "required_agents": ["monetization"],
                        "dependencies": ["audience_insights", "seo_optimization"],
                        "priority": 7
                    },
                    {
                        "task_type": TaskType.CREATION,
                        "description": "Content calendar and production schedule",
                        "required_agents": ["content_analysis"],
                        "dependencies": ["seo_optimization", "monetization"],
                        "priority": 6
                    }
                ]
            },
            "channel_audit": {
                "name": "Complete Channel Audit",
                "description": "Comprehensive analysis of entire channel performance",
                "complexity": WorkflowComplexity.ENTERPRISE,
                "template_tasks": [
                    {
                        "task_type": TaskType.ANALYSIS,
                        "description": "Historical content performance analysis",
                        "required_agents": ["content_analysis"],
                        "dependencies": [],
                        "priority": 10
                    },
                    {
                        "task_type": TaskType.ANALYSIS,
                        "description": "Audience growth and engagement trends",
                        "required_agents": ["audience_insights"],
                        "dependencies": [],
                        "priority": 10
                    },
                    {
                        "task_type": TaskType.ANALYSIS,
                        "description": "SEO performance and optimization opportunities",
                        "required_agents": ["seo_optimization"],
                        "dependencies": ["content_analysis"],
                        "priority": 9
                    },
                    {
                        "task_type": TaskType.ANALYSIS,
                        "description": "Competitive positioning and market analysis",
                        "required_agents": ["competitive_analysis"],
                        "dependencies": ["content_analysis", "audience_insights"],
                        "priority": 8
                    },
                    {
                        "task_type": TaskType.ANALYSIS,
                        "description": "Revenue optimization and monetization audit",
                        "required_agents": ["monetization"],
                        "dependencies": ["audience_insights", "competitive_analysis"],
                        "priority": 7
                    }
                ]
            }
        }
    
    def _load_agent_capabilities(self) -> Dict[str, Any]:
        """Load agent capabilities and specializations"""
        return {
            "content_analysis": {
                "specializations": ["video_performance", "content_quality", "engagement_analysis"],
                "output_types": ["performance_metrics", "content_insights", "optimization_recommendations"],
                "processing_time": 30,  # seconds
                "dependencies": []
            },
            "audience_insights": {
                "specializations": ["demographics", "behavior_analysis", "engagement_patterns"],
                "output_types": ["audience_profiles", "engagement_insights", "growth_recommendations"],
                "processing_time": 25,
                "dependencies": []
            },
            "seo_optimization": {
                "specializations": ["keyword_research", "title_optimization", "description_optimization"],
                "output_types": ["seo_recommendations", "keyword_strategies", "optimization_plans"],
                "processing_time": 20,
                "dependencies": ["content_analysis"]
            },
            "competitive_analysis": {
                "specializations": ["competitor_tracking", "market_analysis", "opportunity_identification"],
                "output_types": ["competitive_insights", "market_opportunities", "strategic_recommendations"],
                "processing_time": 35,
                "dependencies": ["content_analysis", "audience_insights"]
            },
            "monetization": {
                "specializations": ["revenue_optimization", "sponsorship_opportunities", "product_placement"],
                "output_types": ["monetization_strategies", "revenue_projections", "partnership_opportunities"],
                "processing_time": 30,
                "dependencies": ["audience_insights"]
            }
        }
    
    async def analyze_request_complexity(self, user_request: str, context: Dict[str, Any]) -> WorkflowComplexity:
        """Analyze the complexity of a user request to determine workflow approach"""
        
        request_lower = user_request.lower()
        
        # Enterprise-level indicators
        enterprise_keywords = [
            "complete audit", "full analysis", "comprehensive review", 
            "entire channel", "everything", "all videos", "total optimization"
        ]
        
        # Complex task indicators
        complex_keywords = [
            "optimize", "strategy", "plan", "improve", "analyze and fix",
            "full optimization", "complete strategy", "comprehensive"
        ]
        
        # Moderate task indicators
        moderate_keywords = [
            "compare", "analyze", "review", "check", "evaluate", "assess"
        ]
        
        if any(keyword in request_lower for keyword in enterprise_keywords):
            return WorkflowComplexity.ENTERPRISE
        elif any(keyword in request_lower for keyword in complex_keywords):
            return WorkflowComplexity.COMPLEX
        elif any(keyword in request_lower for keyword in moderate_keywords):
            return WorkflowComplexity.MODERATE
        else:
            return WorkflowComplexity.SIMPLE
    
    async def decompose_task(self, user_request: str, context: Dict[str, Any]) -> List[WorkflowTask]:
        """Intelligently decompose a complex request into manageable agent tasks"""
        
        complexity = await self.analyze_request_complexity(user_request, context)
        
        # Check if we have a matching template
        template_match = self._find_matching_template(user_request)
        if template_match:
            return self._create_tasks_from_template(template_match, user_request, context)
        
        # Dynamic task decomposition based on request analysis
        return await self._dynamic_task_decomposition(user_request, context, complexity)

    def _find_matching_template(self, user_request: str) -> Optional[str]:
        """Find the best matching workflow template for the request"""

        request_lower = user_request.lower()

        # Template matching logic
        if any(keyword in request_lower for keyword in ["optimize video", "improve video", "video optimization"]):
            return "video_optimization"
        elif any(keyword in request_lower for keyword in ["content strategy", "content plan", "content calendar"]):
            return "content_strategy"
        elif any(keyword in request_lower for keyword in ["channel audit", "full analysis", "complete review"]):
            return "channel_audit"

        return None

    def _create_tasks_from_template(self, template_name: str, user_request: str, context: Dict[str, Any]) -> List[WorkflowTask]:
        """Create workflow tasks from a template"""

        template = self.workflow_templates[template_name]
        tasks = []

        for i, task_template in enumerate(template["template_tasks"]):
            task = WorkflowTask(
                task_id=f"{template_name}_{i+1}",
                task_type=TaskType(task_template["task_type"]),
                description=task_template["description"],
                required_agents=task_template["required_agents"],
                dependencies=task_template.get("dependencies", []),
                context_requirements=self._determine_context_requirements(task_template),
                estimated_duration=self._estimate_task_duration(task_template),
                priority=task_template.get("priority", 5),
                success_criteria=self._generate_success_criteria(task_template)
            )
            tasks.append(task)

        return tasks

    async def _dynamic_task_decomposition(self, user_request: str, context: Dict[str, Any], complexity: WorkflowComplexity) -> List[WorkflowTask]:
        """Dynamically decompose a request into tasks based on content analysis"""

        tasks = []
        request_lower = user_request.lower()

        # Analyze what the user is asking for
        needs_content_analysis = any(keyword in request_lower for keyword in [
            "analyze", "performance", "engagement", "views", "retention"
        ])

        needs_audience_insights = any(keyword in request_lower for keyword in [
            "audience", "viewers", "demographics", "subscribers", "growth"
        ])

        needs_seo = any(keyword in request_lower for keyword in [
            "seo", "search", "keywords", "title", "description", "tags"
        ])

        needs_competitive = any(keyword in request_lower for keyword in [
            "competitors", "competition", "market", "compare", "benchmark"
        ])

        needs_monetization = any(keyword in request_lower for keyword in [
            "monetize", "revenue", "money", "earnings", "sponsorship", "ads"
        ])

        task_counter = 1

        # Create tasks based on identified needs
        if needs_content_analysis:
            tasks.append(WorkflowTask(
                task_id=f"dynamic_content_{task_counter}",
                task_type=TaskType.ANALYSIS,
                description="Analyze content performance and quality metrics",
                required_agents=["content_analysis"],
                dependencies=[],
                context_requirements=["video_data", "performance_metrics"],
                estimated_duration=30,
                priority=10,
                success_criteria=["Performance metrics analyzed", "Content insights generated"]
            ))
            task_counter += 1

        if needs_audience_insights:
            tasks.append(WorkflowTask(
                task_id=f"dynamic_audience_{task_counter}",
                task_type=TaskType.ANALYSIS,
                description="Analyze audience behavior and engagement patterns",
                required_agents=["audience_insights"],
                dependencies=[],
                context_requirements=["audience_data", "engagement_metrics"],
                estimated_duration=25,
                priority=9,
                success_criteria=["Audience insights generated", "Engagement patterns identified"]
            ))
            task_counter += 1

        if needs_seo:
            dependencies = ["dynamic_content_1"] if needs_content_analysis else []
            tasks.append(WorkflowTask(
                task_id=f"dynamic_seo_{task_counter}",
                task_type=TaskType.OPTIMIZATION,
                description="Optimize SEO elements and keyword strategy",
                required_agents=["seo_optimization"],
                dependencies=dependencies,
                context_requirements=["content_data", "keyword_research"],
                estimated_duration=20,
                priority=8,
                success_criteria=["SEO recommendations provided", "Keyword strategy optimized"]
            ))
            task_counter += 1

        if needs_competitive:
            dependencies = []
            if needs_content_analysis:
                dependencies.append("dynamic_content_1")
            if needs_audience_insights:
                dependencies.append("dynamic_audience_2")

            tasks.append(WorkflowTask(
                task_id=f"dynamic_competitive_{task_counter}",
                task_type=TaskType.ANALYSIS,
                description="Analyze competitive landscape and opportunities",
                required_agents=["competitive_analysis"],
                dependencies=dependencies,
                context_requirements=["competitor_data", "market_analysis"],
                estimated_duration=35,
                priority=7,
                success_criteria=["Competitive analysis completed", "Market opportunities identified"]
            ))
            task_counter += 1

        if needs_monetization:
            dependencies = []
            if needs_audience_insights:
                dependencies.append("dynamic_audience_2")

            tasks.append(WorkflowTask(
                task_id=f"dynamic_monetization_{task_counter}",
                task_type=TaskType.STRATEGY,
                description="Develop monetization strategy and revenue optimization",
                required_agents=["monetization"],
                dependencies=dependencies,
                context_requirements=["revenue_data", "audience_insights"],
                estimated_duration=30,
                priority=6,
                success_criteria=["Monetization strategy developed", "Revenue opportunities identified"]
            ))

        return tasks

    def _determine_context_requirements(self, task_template: Dict[str, Any]) -> List[str]:
        """Determine what context data is needed for a task"""

        agent = task_template["required_agents"][0]
        agent_caps = self.agent_capabilities.get(agent, {})

        context_map = {
            "content_analysis": ["video_data", "performance_metrics", "engagement_data"],
            "audience_insights": ["audience_data", "demographic_data", "engagement_metrics"],
            "seo_optimization": ["content_data", "keyword_data", "search_metrics"],
            "competitive_analysis": ["competitor_data", "market_data", "industry_trends"],
            "monetization": ["revenue_data", "audience_insights", "market_opportunities"]
        }

        return context_map.get(agent, ["general_context"])

    def _estimate_task_duration(self, task_template: Dict[str, Any]) -> int:
        """Estimate how long a task will take to complete"""

        agent = task_template["required_agents"][0]
        base_duration = self.agent_capabilities.get(agent, {}).get("processing_time", 30)

        # Adjust based on task complexity
        complexity_multiplier = {
            TaskType.ANALYSIS: 1.0,
            TaskType.OPTIMIZATION: 1.2,
            TaskType.STRATEGY: 1.5,
            TaskType.CREATION: 1.8,
            TaskType.MONITORING: 0.8
        }

        task_type = TaskType(task_template["task_type"])
        return int(base_duration * complexity_multiplier.get(task_type, 1.0))

    def _generate_success_criteria(self, task_template: Dict[str, Any]) -> List[str]:
        """Generate success criteria for a task"""

        task_type = TaskType(task_template["task_type"])
        agent = task_template["required_agents"][0]

        criteria_map = {
            (TaskType.ANALYSIS, "content_analysis"): [
                "Performance metrics analyzed",
                "Content insights generated",
                "Optimization recommendations provided"
            ],
            (TaskType.ANALYSIS, "audience_insights"): [
                "Audience demographics analyzed",
                "Engagement patterns identified",
                "Growth recommendations provided"
            ],
            (TaskType.OPTIMIZATION, "seo_optimization"): [
                "SEO elements optimized",
                "Keyword strategy developed",
                "Search visibility improved"
            ],
            (TaskType.ANALYSIS, "competitive_analysis"): [
                "Competitive landscape mapped",
                "Market opportunities identified",
                "Strategic recommendations provided"
            ],
            (TaskType.STRATEGY, "monetization"): [
                "Monetization strategy developed",
                "Revenue opportunities identified",
                "Implementation plan created"
            ]
        }

        return criteria_map.get((task_type, agent), ["Task completed successfully"])

    async def create_workflow(self, user_id: str, user_request: str, context: Dict[str, Any]) -> WorkflowExecution:
        """Create a new intelligent workflow for a user request"""

        workflow_id = f"workflow_{user_id}_{int(datetime.now().timestamp())}"

        # Decompose the request into tasks
        tasks = await self.decompose_task(user_request, context)

        # Create execution plan with dependency resolution
        execution_plan = self._create_execution_plan(tasks)

        # Estimate completion time
        estimated_completion = self._estimate_workflow_completion(tasks)

        workflow = WorkflowExecution(
            workflow_id=workflow_id,
            user_id=user_id,
            original_request=user_request,
            decomposed_tasks=tasks,
            execution_plan=execution_plan,
            current_stage=0,
            completed_tasks=[],
            active_tasks=[],
            agent_handoffs=[],
            accumulated_context=context.copy(),
            start_time=datetime.now(),
            estimated_completion=estimated_completion,
            status="planning"
        )

        self.active_workflows[workflow_id] = workflow
        return workflow

    def _create_execution_plan(self, tasks: List[WorkflowTask]) -> List[Dict[str, Any]]:
        """Create an optimized execution plan considering dependencies and parallelization"""

        # Topological sort for dependency resolution
        execution_stages = []
        remaining_tasks = tasks.copy()
        completed_task_ids = set()

        while remaining_tasks:
            # Find tasks that can be executed (all dependencies met)
            ready_tasks = []
            for task in remaining_tasks:
                if all(dep in completed_task_ids for dep in task.dependencies):
                    ready_tasks.append(task)

            if not ready_tasks:
                # Circular dependency or error - break the cycle
                logger.warning("Potential circular dependency detected, forcing execution")
                ready_tasks = [remaining_tasks[0]]

            # Group ready tasks by priority and parallelization potential
            stage = {
                "stage_number": len(execution_stages) + 1,
                "parallel_tasks": [],
                "sequential_tasks": [],
                "estimated_duration": 0
            }

            # Sort by priority (highest first)
            ready_tasks.sort(key=lambda t: t.priority, reverse=True)

            # Determine which tasks can run in parallel
            for task in ready_tasks:
                if self._can_run_in_parallel(task, stage["parallel_tasks"]):
                    stage["parallel_tasks"].append(task.task_id)
                else:
                    stage["sequential_tasks"].append(task.task_id)

            # Calculate stage duration
            parallel_duration = max([self._get_task_duration(t) for t in ready_tasks if t.task_id in stage["parallel_tasks"]], default=0)
            sequential_duration = sum([self._get_task_duration(t) for t in ready_tasks if t.task_id in stage["sequential_tasks"]])
            stage["estimated_duration"] = parallel_duration + sequential_duration

            execution_stages.append(stage)

            # Mark tasks as completed for dependency resolution
            for task in ready_tasks:
                completed_task_ids.add(task.task_id)
                remaining_tasks.remove(task)

        return execution_stages

    def _can_run_in_parallel(self, task: WorkflowTask, current_parallel_tasks: List[str]) -> bool:
        """Determine if a task can run in parallel with currently scheduled tasks"""

        # Check if any of the required agents are already in use
        for parallel_task_id in current_parallel_tasks:
            parallel_task = self._get_task_by_id(parallel_task_id)
            if parallel_task and any(agent in parallel_task.required_agents for agent in task.required_agents):
                return False

        # Check resource constraints (for now, assume all tasks can run in parallel if agents are different)
        return True

    def _get_task_by_id(self, task_id: str) -> Optional[WorkflowTask]:
        """Get a task by its ID from active workflows"""
        for workflow in self.active_workflows.values():
            for task in workflow.decomposed_tasks:
                if task.task_id == task_id:
                    return task
        return None

    def _get_task_duration(self, task: WorkflowTask) -> int:
        """Get the estimated duration for a task"""
        return task.estimated_duration

    def _estimate_workflow_completion(self, tasks: List[WorkflowTask]) -> datetime:
        """Estimate when the workflow will complete"""

        total_duration = sum(task.estimated_duration for task in tasks)
        # Add 20% buffer for coordination overhead
        total_duration = int(total_duration * 1.2)

        return datetime.now() + timedelta(seconds=total_duration)

    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute an intelligent workflow with dynamic agent coordination"""

        if workflow_id not in self.active_workflows:
            raise ValueError(f"Workflow {workflow_id} not found")

        workflow = self.active_workflows[workflow_id]
        workflow.status = "executing"

        try:
            # Execute each stage of the workflow
            for stage_index, stage in enumerate(workflow.execution_plan):
                workflow.current_stage = stage_index + 1

                logger.info(f"Executing workflow stage {stage_index + 1} for workflow {workflow_id}")

                # Execute parallel tasks
                if stage["parallel_tasks"]:
                    await self._execute_parallel_tasks(workflow, stage["parallel_tasks"])

                # Execute sequential tasks
                if stage["sequential_tasks"]:
                    await self._execute_sequential_tasks(workflow, stage["sequential_tasks"])

                # Update workflow progress
                workflow.completed_tasks.extend(stage["parallel_tasks"] + stage["sequential_tasks"])
                workflow.active_tasks = []

            workflow.status = "completed"

            # Generate final synthesis
            final_result = await self._synthesize_workflow_results(workflow)

            return {
                "success": True,
                "workflow_id": workflow_id,
                "status": "completed",
                "results": final_result,
                "execution_time": (datetime.now() - workflow.start_time).total_seconds(),
                "tasks_completed": len(workflow.completed_tasks),
                "agent_handoffs": len(workflow.agent_handoffs)
            }

        except Exception as e:
            workflow.status = "failed"
            logger.error(f"Workflow {workflow_id} failed: {e}")

            return {
                "success": False,
                "workflow_id": workflow_id,
                "status": "failed",
                "error": str(e),
                "partial_results": workflow.accumulated_context
            }

    async def _execute_parallel_tasks(self, workflow: WorkflowExecution, task_ids: List[str]) -> None:
        """Execute multiple tasks in parallel"""

        tasks = [self._get_workflow_task(workflow, task_id) for task_id in task_ids]
        tasks = [t for t in tasks if t is not None]

        if not tasks:
            return

        workflow.active_tasks.extend(task_ids)

        # Create async tasks for parallel execution
        async_tasks = []
        for task in tasks:
            async_task = self._execute_single_task(workflow, task)
            async_tasks.append(async_task)

        # Execute all tasks in parallel
        results = await asyncio.gather(*async_tasks, return_exceptions=True)

        # Process results and handle any errors
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Task {tasks[i].task_id} failed: {result}")
            else:
                # Merge successful results into workflow context
                workflow.accumulated_context.update(result)

    def _get_workflow_task(self, workflow: WorkflowExecution, task_id: str) -> Optional[WorkflowTask]:
        """Get a specific task from a workflow"""
        for task in workflow.decomposed_tasks:
            if task.task_id == task_id:
                return task
        return None

    async def _execute_sequential_tasks(self, workflow: WorkflowExecution, task_ids: List[str]) -> None:
        """Execute tasks sequentially with context passing"""

        for task_id in task_ids:
            task = self._get_workflow_task(workflow, task_id)
            if task:
                workflow.active_tasks = [task_id]
                result = await self._execute_single_task(workflow, task)
                workflow.accumulated_context.update(result)
                workflow.active_tasks = []

    async def _execute_single_task(self, workflow: WorkflowExecution, task: WorkflowTask) -> Dict[str, Any]:
        """Execute a single task with intelligent agent coordination"""

        logger.info(f"Executing task {task.task_id}: {task.description}")

        # Prepare context for the task
        task_context = self._prepare_task_context(workflow, task)

        # Execute the task with the appropriate agent
        agent_id = task.required_agents[0]  # For now, use the first required agent

        try:
            # Import and use the appropriate agent
            if agent_id == "content_analysis":
                from .agent_coordinators import ContentAnalysisAgent
                agent = ContentAnalysisAgent()
            elif agent_id == "audience_insights":
                from .agent_coordinators import AudienceInsightsAgent
                agent = AudienceInsightsAgent()
            elif agent_id == "seo_optimization":
                from .seo_agent import get_seo_agent
                agent = get_seo_agent()
            elif agent_id == "competitive_analysis":
                from .competitive_intelligence_2 import CompetitiveIntelligence2Engine
                agent = CompetitiveIntelligence2Engine()
            elif agent_id == "monetization":
                from .monetization_agent import get_monetization_agent
                agent = get_monetization_agent()
            else:
                raise ValueError(f"Unknown agent: {agent_id}")

            # Create agent request
            from .agent_models import AgentRequest
            agent_request = AgentRequest(
                user_id=workflow.user_id,
                message=task.description,
                context=task_context,
                query_type=self._map_task_type_to_query_type(task.task_type)
            )

            # Execute the agent
            if hasattr(agent, 'process_request'):
                response = await agent.process_request(agent_request)
            elif hasattr(agent, 'analyze_competitive_landscape'):
                # Special handling for competitive intelligence
                response = await agent.analyze_competitive_landscape(workflow.user_id, task_context)
            else:
                # Fallback to a generic processing method
                response = {"analysis": f"Task {task.task_id} completed", "recommendations": []}

            # Create agent handoff record
            handoff = AgentHandoff(
                from_agent="workflow_engine",
                to_agent=agent_id,
                context_data=task_context,
                handoff_reason=f"Task execution: {task.description}",
                timestamp=datetime.now(),
                success=True
            )
            workflow.agent_handoffs.append(handoff)

            # Process and return results
            task_result = {
                f"{agent_id}_result": response,
                f"{agent_id}_task_id": task.task_id,
                f"{agent_id}_completion_time": datetime.now().isoformat()
            }

            logger.info(f"Task {task.task_id} completed successfully")
            return task_result

        except Exception as e:
            logger.error(f"Task {task.task_id} failed: {e}")

            # Create failed handoff record
            handoff = AgentHandoff(
                from_agent="workflow_engine",
                to_agent=agent_id,
                context_data=task_context,
                handoff_reason=f"Task execution failed: {task.description}",
                timestamp=datetime.now(),
                success=False
            )
            workflow.agent_handoffs.append(handoff)

            return {
                f"{agent_id}_error": str(e),
                f"{agent_id}_task_id": task.task_id,
                f"{agent_id}_failure_time": datetime.now().isoformat()
            }

    def _prepare_task_context(self, workflow: WorkflowExecution, task: WorkflowTask) -> Dict[str, Any]:
        """Prepare context for a specific task based on dependencies and requirements"""

        context = workflow.accumulated_context.copy()

        # Add task-specific context
        context.update({
            "task_id": task.task_id,
            "task_type": task.task_type.value,
            "task_description": task.description,
            "workflow_id": workflow.workflow_id,
            "original_request": workflow.original_request
        })

        # Add dependency results
        for dep_task_id in task.dependencies:
            for key, value in workflow.accumulated_context.items():
                if dep_task_id in key:
                    context[f"dependency_{dep_task_id}"] = value

        # Add context requirements
        for requirement in task.context_requirements:
            if requirement in workflow.accumulated_context:
                context[requirement] = workflow.accumulated_context[requirement]

        return context

    def _map_task_type_to_query_type(self, task_type: TaskType):
        """Map workflow task types to agent query types"""

        from .agent_models import QueryType

        mapping = {
            TaskType.ANALYSIS: QueryType.CONTENT_ANALYSIS,
            TaskType.OPTIMIZATION: QueryType.SEO_OPTIMIZATION,
            TaskType.STRATEGY: QueryType.MONETIZATION_STRATEGY,
            TaskType.CREATION: QueryType.CONTENT_ANALYSIS,
            TaskType.MONITORING: QueryType.COMPETITIVE_ANALYSIS
        }

        return mapping.get(task_type, QueryType.GENERAL)

    async def _synthesize_workflow_results(self, workflow: WorkflowExecution) -> Dict[str, Any]:
        """Synthesize all agent results into a comprehensive final result"""

        synthesis = {
            "workflow_summary": {
                "original_request": workflow.original_request,
                "tasks_completed": len(workflow.completed_tasks),
                "execution_time": (datetime.now() - workflow.start_time).total_seconds(),
                "agents_involved": list(set([handoff.to_agent for handoff in workflow.agent_handoffs if handoff.success]))
            },
            "key_insights": [],
            "recommendations": [],
            "action_plan": [],
            "agent_contributions": {}
        }

        # Extract insights and recommendations from each agent's results
        for key, value in workflow.accumulated_context.items():
            if "_result" in key:
                agent_name = key.replace("_result", "")
                synthesis["agent_contributions"][agent_name] = value

                # Extract insights
                if isinstance(value, dict):
                    if "insights" in value:
                        synthesis["key_insights"].extend(value["insights"] if isinstance(value["insights"], list) else [value["insights"]])
                    if "recommendations" in value:
                        synthesis["recommendations"].extend(value["recommendations"] if isinstance(value["recommendations"], list) else [value["recommendations"]])
                    if "analysis" in value:
                        synthesis["key_insights"].append(f"{agent_name}: {value['analysis']}")

        # Generate unified action plan
        synthesis["action_plan"] = self._generate_unified_action_plan(workflow, synthesis)

        # Add workflow metadata
        synthesis["workflow_metadata"] = {
            "workflow_id": workflow.workflow_id,
            "completion_time": datetime.now().isoformat(),
            "success_rate": len([h for h in workflow.agent_handoffs if h.success]) / max(len(workflow.agent_handoffs), 1),
            "total_handoffs": len(workflow.agent_handoffs)
        }

        return synthesis

    def _generate_unified_action_plan(self, workflow: WorkflowExecution, synthesis: Dict[str, Any]) -> List[str]:
        """Generate a unified action plan from all agent recommendations"""

        action_plan = []

        # Prioritize actions based on agent expertise and workflow goals
        if "content_analysis" in synthesis["agent_contributions"]:
            action_plan.append("📊 Implement content performance optimizations")

        if "audience_insights" in synthesis["agent_contributions"]:
            action_plan.append("👥 Apply audience engagement strategies")

        if "seo_optimization" in synthesis["agent_contributions"]:
            action_plan.append("🔍 Execute SEO optimization recommendations")

        if "competitive_analysis" in synthesis["agent_contributions"]:
            action_plan.append("🏆 Leverage competitive opportunities")

        if "monetization" in synthesis["agent_contributions"]:
            action_plan.append("💰 Implement monetization strategies")

        # Add workflow-specific actions
        action_plan.append("📈 Monitor progress and iterate based on results")
        action_plan.append("🔄 Schedule follow-up analysis in 30 days")

        return action_plan

# Global workflow engine instance
workflow_engine = IntelligentWorkflowEngine()

async def create_intelligent_workflow(user_id: str, user_request: str, context: Dict[str, Any]) -> WorkflowExecution:
    """Create and return a new intelligent workflow"""
    return await workflow_engine.create_workflow(user_id, user_request, context)

async def execute_intelligent_workflow(workflow_id: str) -> Dict[str, Any]:
    """Execute an intelligent workflow and return results"""
    return await workflow_engine.execute_workflow(workflow_id)

def get_workflow_status(workflow_id: str) -> Optional[Dict[str, Any]]:
    """Get the current status of a workflow"""
    if workflow_id in workflow_engine.active_workflows:
        workflow = workflow_engine.active_workflows[workflow_id]
        return {
            "workflow_id": workflow_id,
            "status": workflow.status,
            "current_stage": workflow.current_stage,
            "total_stages": len(workflow.execution_plan),
            "completed_tasks": len(workflow.completed_tasks),
            "total_tasks": len(workflow.decomposed_tasks),
            "estimated_completion": workflow.estimated_completion.isoformat(),
            "active_tasks": workflow.active_tasks
        }
    return None
