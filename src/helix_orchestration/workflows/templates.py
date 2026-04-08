"""
Workflow Templates and Patterns
================================

Pre-built workflow templates and communication patterns for common orchestration scenarios.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
from enum import Enum
import asyncio


class CommunicationPattern(str, Enum):
    """Agent communication patterns"""
    BROADCAST = "broadcast"  # One agent to many
    CONSENSUS = "consensus"  # All agents agree
    HIERARCHICAL = "hierarchical"  # Chain of command
    MESH = "mesh"  # Peer-to-peer
    PIPELINE = "pipeline"  # Sequential processing
    MAP_REDUCE = "map_reduce"  # Distributed processing


@dataclass
class WorkflowStep:
    """Single step in a workflow"""
    name: str
    agent_id: str
    action: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    timeout: int = 30  # seconds
    retry_count: int = 3
    dependencies: List[str] = field(default_factory=list)
    error_handler: Optional[Callable] = None


@dataclass
class WorkflowTemplate:
    """Template for a workflow"""
    name: str
    description: str
    pattern: CommunicationPattern
    steps: List[WorkflowStep]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> bool:
        """Validate workflow template"""
        # Check for circular dependencies
        visited = set()
        
        def has_cycle(step_name: str, path: set) -> bool:
            if step_name in path:
                return True
            if step_name in visited:
                return False
            
            visited.add(step_name)
            path.add(step_name)
            
            step = next((s for s in self.steps if s.name == step_name), None)
            if not step:
                return False
            
            for dep in step.dependencies:
                if has_cycle(dep, path.copy()):
                    return True
            
            return False
        
        for step in self.steps:
            if has_cycle(step.name, set()):
                return False
        
        return True


class WorkflowTemplateLibrary:
    """Library of pre-built workflow templates"""
    
    @staticmethod
    def data_processing_pipeline() -> WorkflowTemplate:
        """Template for data processing workflows"""
        return WorkflowTemplate(
            name="Data Processing Pipeline",
            description="Sequential data processing with validation and error handling",
            pattern=CommunicationPattern.PIPELINE,
            steps=[
                WorkflowStep(
                    name="validate_input",
                    agent_id="validator",
                    action="validate",
                    parameters={"schema": "data_schema"},
                    dependencies=[]
                ),
                WorkflowStep(
                    name="transform_data",
                    agent_id="transformer",
                    action="transform",
                    parameters={"rules": "transform_rules"},
                    dependencies=["validate_input"]
                ),
                WorkflowStep(
                    name="enrich_data",
                    agent_id="enricher",
                    action="enrich",
                    parameters={"sources": ["external_api", "cache"]},
                    dependencies=["transform_data"]
                ),
                WorkflowStep(
                    name="store_data",
                    agent_id="storage",
                    action="store",
                    parameters={"destination": "database"},
                    dependencies=["enrich_data"]
                ),
            ]
        )
    
    @staticmethod
    def content_generation_workflow() -> WorkflowTemplate:
        """Template for content generation workflows"""
        return WorkflowTemplate(
            name="Content Generation Workflow",
            description="Multi-stage content creation with review and refinement",
            pattern=CommunicationPattern.PIPELINE,
            steps=[
                WorkflowStep(
                    name="research",
                    agent_id="researcher",
                    action="research",
                    parameters={"topic": "input_topic"},
                    dependencies=[]
                ),
                WorkflowStep(
                    name="generate_draft",
                    agent_id="writer",
                    action="generate",
                    parameters={"style": "professional"},
                    dependencies=["research"]
                ),
                WorkflowStep(
                    name="review_draft",
                    agent_id="reviewer",
                    action="review",
                    parameters={"criteria": ["clarity", "accuracy", "tone"]},
                    dependencies=["generate_draft"]
                ),
                WorkflowStep(
                    name="refine_content",
                    agent_id="editor",
                    action="refine",
                    parameters={"improvements": "review_feedback"},
                    dependencies=["review_draft"]
                ),
                WorkflowStep(
                    name="publish",
                    agent_id="publisher",
                    action="publish",
                    parameters={"channels": ["web", "social"]},
                    dependencies=["refine_content"]
                ),
            ]
        )
    
    @staticmethod
    def decision_making_workflow() -> WorkflowTemplate:
        """Template for consensus-based decision making"""
        return WorkflowTemplate(
            name="Decision Making Workflow",
            description="Multi-agent consensus for complex decisions",
            pattern=CommunicationPattern.CONSENSUS,
            steps=[
                WorkflowStep(
                    name="gather_perspectives",
                    agent_id="coordinator",
                    action="broadcast",
                    parameters={"question": "decision_question"},
                    dependencies=[]
                ),
                WorkflowStep(
                    name="analyze_perspectives",
                    agent_id="analyst",
                    action="analyze",
                    parameters={"perspectives": "all_responses"},
                    dependencies=["gather_perspectives"]
                ),
                WorkflowStep(
                    name="reach_consensus",
                    agent_id="mediator",
                    action="consensus",
                    parameters={"threshold": 0.8},
                    dependencies=["analyze_perspectives"]
                ),
                WorkflowStep(
                    name="execute_decision",
                    agent_id="executor",
                    action="execute",
                    parameters={"decision": "consensus_result"},
                    dependencies=["reach_consensus"]
                ),
            ]
        )
    
    @staticmethod
    def distributed_processing_workflow() -> WorkflowTemplate:
        """Template for map-reduce style distributed processing"""
        return WorkflowTemplate(
            name="Distributed Processing Workflow",
            description="Parallel processing with aggregation",
            pattern=CommunicationPattern.MAP_REDUCE,
            steps=[
                WorkflowStep(
                    name="partition_data",
                    agent_id="partitioner",
                    action="partition",
                    parameters={"partition_count": 4},
                    dependencies=[]
                ),
                WorkflowStep(
                    name="process_partition_1",
                    agent_id="worker_1",
                    action="process",
                    parameters={"partition": 1},
                    dependencies=["partition_data"]
                ),
                WorkflowStep(
                    name="process_partition_2",
                    agent_id="worker_2",
                    action="process",
                    parameters={"partition": 2},
                    dependencies=["partition_data"]
                ),
                WorkflowStep(
                    name="process_partition_3",
                    agent_id="worker_3",
                    action="process",
                    parameters={"partition": 3},
                    dependencies=["partition_data"]
                ),
                WorkflowStep(
                    name="process_partition_4",
                    agent_id="worker_4",
                    action="process",
                    parameters={"partition": 4},
                    dependencies=["partition_data"]
                ),
                WorkflowStep(
                    name="aggregate_results",
                    agent_id="aggregator",
                    action="aggregate",
                    parameters={"combine_strategy": "merge"},
                    dependencies=[
                        "process_partition_1",
                        "process_partition_2",
                        "process_partition_3",
                        "process_partition_4",
                    ]
                ),
            ]
        )
    
    @staticmethod
    def error_recovery_workflow() -> WorkflowTemplate:
        """Template for error handling and recovery"""
        return WorkflowTemplate(
            name="Error Recovery Workflow",
            description="Graceful error handling with fallback strategies",
            pattern=CommunicationPattern.PIPELINE,
            steps=[
                WorkflowStep(
                    name="execute_primary",
                    agent_id="primary_agent",
                    action="execute",
                    parameters={"strategy": "primary"},
                    dependencies=[],
                    retry_count=2
                ),
                WorkflowStep(
                    name="execute_fallback",
                    agent_id="fallback_agent",
                    action="execute",
                    parameters={"strategy": "fallback"},
                    dependencies=["execute_primary"]
                ),
                WorkflowStep(
                    name="log_error",
                    agent_id="logger",
                    action="log",
                    parameters={"level": "error"},
                    dependencies=["execute_fallback"]
                ),
                WorkflowStep(
                    name="notify_admin",
                    agent_id="notifier",
                    action="notify",
                    parameters={"channel": "admin_channel"},
                    dependencies=["log_error"]
                ),
            ]
        )
    
    @staticmethod
    def hierarchical_approval_workflow() -> WorkflowTemplate:
        """Template for hierarchical approval processes"""
        return WorkflowTemplate(
            name="Hierarchical Approval Workflow",
            description="Multi-level approval chain",
            pattern=CommunicationPattern.HIERARCHICAL,
            steps=[
                WorkflowStep(
                    name="submit_request",
                    agent_id="requester",
                    action="submit",
                    parameters={"request_type": "approval"},
                    dependencies=[]
                ),
                WorkflowStep(
                    name="manager_review",
                    agent_id="manager",
                    action="review",
                    parameters={"level": 1},
                    dependencies=["submit_request"]
                ),
                WorkflowStep(
                    name="director_review",
                    agent_id="director",
                    action="review",
                    parameters={"level": 2},
                    dependencies=["manager_review"]
                ),
                WorkflowStep(
                    name="executive_review",
                    agent_id="executive",
                    action="review",
                    parameters={"level": 3},
                    dependencies=["director_review"]
                ),
                WorkflowStep(
                    name="execute_approved",
                    agent_id="executor",
                    action="execute",
                    parameters={"approval_status": "approved"},
                    dependencies=["executive_review"]
                ),
            ]
        )
    
    @staticmethod
    def monitoring_and_alerting_workflow() -> WorkflowTemplate:
        """Template for system monitoring and alerting"""
        return WorkflowTemplate(
            name="Monitoring and Alerting Workflow",
            description="Continuous monitoring with intelligent alerting",
            pattern=CommunicationPattern.BROADCAST,
            steps=[
                WorkflowStep(
                    name="collect_metrics",
                    agent_id="monitor",
                    action="collect",
                    parameters={"interval": 60},
                    dependencies=[]
                ),
                WorkflowStep(
                    name="analyze_metrics",
                    agent_id="analyzer",
                    action="analyze",
                    parameters={"thresholds": "default"},
                    dependencies=["collect_metrics"]
                ),
                WorkflowStep(
                    name="detect_anomalies",
                    agent_id="anomaly_detector",
                    action="detect",
                    parameters={"sensitivity": 0.8},
                    dependencies=["analyze_metrics"]
                ),
                WorkflowStep(
                    name="generate_alerts",
                    agent_id="alerter",
                    action="alert",
                    parameters={"severity_levels": ["info", "warning", "critical"]},
                    dependencies=["detect_anomalies"]
                ),
                WorkflowStep(
                    name="notify_stakeholders",
                    agent_id="notifier",
                    action="notify",
                    parameters={"channels": ["email", "slack", "pagerduty"]},
                    dependencies=["generate_alerts"]
                ),
            ]
        )


class CommunicationPatternHandler:
    """Handles different communication patterns"""
    
    @staticmethod
    async def broadcast(
        sender_agent: str,
        recipient_agents: List[str],
        message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Broadcast pattern: one to many"""
        results = {}
        tasks = []
        
        for agent in recipient_agents:
            tasks.append(
                CommunicationPatternHandler._send_to_agent(agent, message)
            )
        
        responses = await asyncio.gather(*tasks)
        
        for agent, response in zip(recipient_agents, responses):
            results[agent] = response
        
        return results
    
    @staticmethod
    async def consensus(
        agents: List[str],
        question: Dict[str, Any],
        threshold: float = 0.8
    ) -> Dict[str, Any]:
        """Consensus pattern: all agents agree"""
        responses = await CommunicationPatternHandler.broadcast(
            "coordinator",
            agents,
            question
        )
        
        # Count agreement
        agreements = sum(1 for r in responses.values() if r.get("agree", False))
        agreement_ratio = agreements / len(agents) if agents else 0
        
        return {
            "consensus_reached": agreement_ratio >= threshold,
            "agreement_ratio": agreement_ratio,
            "responses": responses,
        }
    
    @staticmethod
    async def pipeline(
        steps: List[WorkflowStep],
        initial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Pipeline pattern: sequential processing"""
        current_data = initial_data
        results = {}
        
        for step in steps:
            # Execute step
            result = await CommunicationPatternHandler._execute_step(step, current_data)
            results[step.name] = result
            current_data = result
        
        return results
    
    @staticmethod
    async def map_reduce(
        partitions: List[Dict[str, Any]],
        map_agents: List[str],
        reduce_agent: str
    ) -> Dict[str, Any]:
        """Map-reduce pattern: distributed processing"""
        # Map phase
        map_tasks = []
        for partition, agent in zip(partitions, map_agents):
            map_tasks.append(
                CommunicationPatternHandler._send_to_agent(agent, partition)
            )
        
        mapped_results = await asyncio.gather(*map_tasks)
        
        # Reduce phase
        reduce_result = await CommunicationPatternHandler._send_to_agent(
            reduce_agent,
            {"data": mapped_results}
        )
        
        return reduce_result
    
    @staticmethod
    async def _send_to_agent(
        agent_id: str,
        message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send message to agent (mock)"""
        # In real implementation, this would use actual agent communication
        await asyncio.sleep(0.1)  # Simulate network delay
        return {"agent": agent_id, "status": "success", "data": message}
    
    @staticmethod
    async def _execute_step(
        step: WorkflowStep,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a workflow step"""
        # In real implementation, this would execute the actual step
        await asyncio.sleep(0.1)  # Simulate processing
        return {"step": step.name, "status": "completed", "data": data}


class WorkflowComposer:
    """Composes workflows from templates and custom steps"""
    
    def __init__(self):
        """Initialize composer"""
        self.templates = WorkflowTemplateLibrary()
    
    def create_custom_workflow(
        self,
        name: str,
        pattern: CommunicationPattern,
        steps: List[WorkflowStep]
    ) -> WorkflowTemplate:
        """Create a custom workflow"""
        workflow = WorkflowTemplate(
            name=name,
            description="Custom workflow",
            pattern=pattern,
            steps=steps
        )
        
        if not workflow.validate():
            raise ValueError("Workflow has circular dependencies")
        
        return workflow
    
    def combine_workflows(
        self,
        name: str,
        workflows: List[WorkflowTemplate],
        pattern: CommunicationPattern = CommunicationPattern.PIPELINE
    ) -> WorkflowTemplate:
        """Combine multiple workflows into one"""
        combined_steps = []
        
        for workflow in workflows:
            combined_steps.extend(workflow.steps)
        
        combined = WorkflowTemplate(
            name=name,
            description=f"Combined workflow of {len(workflows)} workflows",
            pattern=pattern,
            steps=combined_steps
        )
        
        if not combined.validate():
            raise ValueError("Combined workflow has circular dependencies")
        
        return combined
