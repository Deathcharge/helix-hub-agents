"""Integration examples with other Helix packages.

This module demonstrates how to integrate Helix Agent Orchestration
with other packages in the Helix Collective ecosystem.
"""

import asyncio
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class IntegrationExample:
    """Base class for integration examples."""

    name: str
    description: str
    packages: List[str]


class UnifiedLLMIntegration:
    """Integration with helix-unified-llm package.

    Demonstrates how to use the Unified LLM package for agent reasoning.
    """

    @staticmethod
    async def example_agent_reasoning():
        """Example: Use Unified LLM for agent reasoning.

        This shows how to integrate the Unified LLM package to provide
        advanced reasoning capabilities to orchestration agents.
        """
        print("🧠 Unified LLM Integration Example")
        print("-" * 50)

        # Pseudo-code showing integration pattern
        example_code = """
from helix_unified_llm import UnifiedLLM
from helix_agent_orchestration import AgentOrchestrator

# Initialize LLM
llm = UnifiedLLM(
    model="gpt-4",
    temperature=0.7,
    max_tokens=2048
)

# Initialize orchestrator
orchestrator = AgentOrchestrator()

# Agent with LLM reasoning
class ReasoningAgent:
    def __init__(self, name, llm):
        self.name = name
        self.llm = llm

    async def reason(self, prompt):
        # Use LLM for reasoning
        response = await self.llm.generate(prompt)
        return response

    async def execute_task(self, task):
        # Reason about task
        reasoning = await self.reason(f"How should I approach: {task}?")
        # Execute based on reasoning
        return await self.perform_action(reasoning)

# Register agent with orchestrator
kael = ReasoningAgent("Kael", llm)
orchestrator.register_agent(kael)

# Run workflow using LLM-powered reasoning
result = await orchestrator.execute_workflow("analysis_pipeline")
        """
        print(example_code)

        print("\n✅ Integration Pattern:")
        print("  1. Initialize UnifiedLLM with desired model")
        print("  2. Create agents that use LLM for reasoning")
        print("  3. Register agents with orchestrator")
        print("  4. Execute workflows with LLM-powered decision making\n")


class NotificationsIntegration:
    """Integration with helix-notifications package.

    Demonstrates how to use notifications for agent communication.
    """

    @staticmethod
    async def example_agent_notifications():
        """Example: Use Notifications for agent communication.

        Shows how to integrate the Notifications package for inter-agent
        communication and event propagation.
        """
        print("📢 Notifications Integration Example")
        print("-" * 50)

        example_code = """
from helix_notifications import NotificationManager
from helix_agent_orchestration import AgentOrchestrator, Agent

# Initialize notification manager
notifier = NotificationManager(
    providers=["slack", "email", "discord"],
    config={
        "slack": {"webhook_url": "..."},
        "email": {"smtp_server": "..."},
    }
)

# Agent with notification support
class NotificationAgent(Agent):
    def __init__(self, name, notifier):
        super().__init__(name)
        self.notifier = notifier

    async def on_task_complete(self, task, result):
        # Send notification
        await self.notifier.notify(
            channel="slack",
            message=f"Task {task} completed: {result}",
            severity="info"
        )

    async def on_error(self, error):
        # Alert on error
        await self.notifier.notify(
            channel="email",
            message=f"Agent {self.name} encountered error: {error}",
            severity="critical"
        )

# Register agent with orchestrator
orchestrator = AgentOrchestrator()
agent = NotificationAgent("Aria", notifier)
orchestrator.register_agent(agent)

# Workflows now send notifications
result = await orchestrator.execute_workflow("data_pipeline")
        """
        print(example_code)

        print("\n✅ Integration Pattern:")
        print("  1. Initialize NotificationManager with providers")
        print("  2. Create agents that inherit notification support")
        print("  3. Send notifications on task completion/errors")
        print("  4. Multi-channel notification delivery\n")


class TokenCostIntegration:
    """Integration with helix-token-cost-manager package.

    Demonstrates how to track and manage token costs.
    """

    @staticmethod
    async def example_token_tracking():
        """Example: Track token costs across agents.

        Shows how to integrate the Token Cost Manager for monitoring
        and optimizing LLM token usage.
        """
        print("💰 Token Cost Manager Integration Example")
        print("-" * 50)

        example_code = """
from helix_token_cost_manager import TokenCostManager
from helix_agent_orchestration import AgentOrchestrator

# Initialize token cost manager
cost_manager = TokenCostManager(
    models={
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5": {"input": 0.0005, "output": 0.0015},
    },
    budget_limit=1000.0  # $1000 daily budget
)

# Orchestrator with cost tracking
class CostTrackingOrchestrator(AgentOrchestrator):
    def __init__(self, cost_manager):
        super().__init__()
        self.cost_manager = cost_manager

    async def execute_workflow(self, workflow_name):
        # Track costs during execution
        with self.cost_manager.track_session(workflow_name):
            result = await super().execute_workflow(workflow_name)
            
            # Get cost report
            costs = self.cost_manager.get_session_costs()
            print(f"Workflow {workflow_name} cost: ${costs['total']:.2f}")
            
            return result

    async def optimize_agent_routing(self, task):
        # Route to cheapest capable agent
        agents = self.get_capable_agents(task)
        costs = [self.cost_manager.estimate_cost(agent) for agent in agents]
        return agents[costs.index(min(costs))]

# Use cost-aware orchestrator
orchestrator = CostTrackingOrchestrator(cost_manager)
result = await orchestrator.execute_workflow("analysis")

# Get cost analytics
analytics = cost_manager.get_analytics()
print(f"Total costs: ${analytics['total']:.2f}")
print(f"Budget remaining: ${analytics['remaining']:.2f}")
        """
        print(example_code)

        print("\n✅ Integration Pattern:")
        print("  1. Initialize TokenCostManager with pricing")
        print("  2. Create cost-tracking orchestrator")
        print("  3. Track costs per workflow/agent")
        print("  4. Optimize routing based on costs\n")


class IntegrationIntegration:
    """Integration with helix-integration package.

    Demonstrates how to integrate with external APIs and services.
    """

    @staticmethod
    async def example_external_api_integration():
        """Example: Integrate with external APIs.

        Shows how to use the Integration package to connect agents
        with external services and APIs.
        """
        print("🔗 External API Integration Example")
        print("-" * 50)

        example_code = """
from helix_integration import APIConnector, IntegrationManager
from helix_agent_orchestration import Agent, AgentOrchestrator

# Initialize integration manager
integrations = IntegrationManager()

# Register external APIs
integrations.register_api(
    "slack",
    APIConnector(
        base_url="https://slack.com/api",
        auth_type="bearer",
        token="${SLACK_TOKEN}"
    )
)

integrations.register_api(
    "github",
    APIConnector(
        base_url="https://api.github.com",
        auth_type="bearer",
        token="${GITHUB_TOKEN}"
    )
)

# Agent that uses external APIs
class IntegrationAgent(Agent):
    def __init__(self, name, integrations):
        super().__init__(name)
        self.integrations = integrations

    async def post_to_slack(self, message):
        response = await self.integrations.call(
            "slack",
            "POST",
            "/chat.postMessage",
            json={"text": message, "channel": "#helix"}
        )
        return response

    async def create_github_issue(self, title, body):
        response = await self.integrations.call(
            "github",
            "POST",
            "/repos/Deathcharge/helix/issues",
            json={"title": title, "body": body}
        )
        return response

# Register agent
orchestrator = AgentOrchestrator()
agent = IntegrationAgent("Aria", integrations)
orchestrator.register_agent(agent)

# Use agent to interact with external services
await agent.post_to_slack("Workflow completed successfully!")
await agent.create_github_issue("New analysis results", "Check dashboard")
        """
        print(example_code)

        print("\n✅ Integration Pattern:")
        print("  1. Initialize IntegrationManager")
        print("  2. Register external APIs with credentials")
        print("  3. Create agents that use APIs")
        print("  4. Call external services from agents\n")


class RoutineEngineIntegration:
    """Integration with helix-routine-engine package.

    Demonstrates how to schedule and manage routine tasks.
    """

    @staticmethod
    async def example_routine_scheduling():
        """Example: Schedule routine tasks.

        Shows how to use the Routine Engine to schedule recurring
        orchestration workflows.
        """
        print("⏰ Routine Engine Integration Example")
        print("-" * 50)

        example_code = """
from helix_routine_engine import RoutineScheduler, RoutineTask
from helix_agent_orchestration import AgentOrchestrator

# Initialize routine scheduler
scheduler = RoutineScheduler()

# Initialize orchestrator
orchestrator = AgentOrchestrator()

# Define routine workflows
async def daily_analysis():
    \"\"\"Run daily analysis workflow.\"\"\"
    return await orchestrator.execute_workflow("daily_analysis")

async def hourly_monitoring():
    \"\"\"Run hourly monitoring workflow.\"\"\"
    return await orchestrator.execute_workflow("hourly_monitoring")

async def weekly_report():
    \"\"\"Generate weekly report.\"\"\"
    return await orchestrator.execute_workflow("weekly_report")

# Schedule routines
scheduler.schedule(
    RoutineTask(
        name="daily_analysis",
        func=daily_analysis,
        schedule="0 2 * * *",  # 2 AM daily
        timezone="UTC"
    )
)

scheduler.schedule(
    RoutineTask(
        name="hourly_monitoring",
        func=hourly_monitoring,
        schedule="0 * * * *",  # Every hour
        timezone="UTC"
    )
)

scheduler.schedule(
    RoutineTask(
        name="weekly_report",
        func=weekly_report,
        schedule="0 9 * * 1",  # 9 AM Monday
        timezone="UTC"
    )
)

# Start scheduler
await scheduler.start()

# Monitor routine execution
status = scheduler.get_status()
print(f"Active routines: {len(status['active'])}")
for routine in status['active']:
    print(f"  - {routine['name']}: {routine['next_run']}")
        """
        print(example_code)

        print("\n✅ Integration Pattern:")
        print("  1. Initialize RoutineScheduler")
        print("  2. Define async workflow functions")
        print("  3. Schedule with cron expressions")
        print("  4. Monitor routine execution\n")


class NeuralMeshIntegration:
    """Integration with neural-mesh package.

    Demonstrates how to use distributed neural networks.
    """

    @staticmethod
    async def example_distributed_inference():
        """Example: Distributed neural inference.

        Shows how to use the Neural Mesh package for distributed
        machine learning inference across agents.
        """
        print("🧠 Neural Mesh Integration Example")
        print("-" * 50)

        example_code = """
from neural_mesh import NeuralMesh, MeshNode
from helix_agent_orchestration import Agent, AgentOrchestrator

# Initialize neural mesh
mesh = NeuralMesh(
    nodes=["node1:8000", "node2:8000", "node3:8000"],
    model="ensemble-transformer",
    strategy="distributed"
)

# Agent with neural inference
class NeuralAgent(Agent):
    def __init__(self, name, mesh):
        super().__init__(name)
        self.mesh = mesh

    async def predict(self, input_data):
        # Distributed inference across mesh
        result = await self.mesh.infer(input_data)
        return result

    async def train_batch(self, training_data):
        # Distributed training
        result = await self.mesh.train(training_data)
        return result

# Register agents with mesh
orchestrator = AgentOrchestrator()
agents = [
    NeuralAgent(f"Node-{i}", mesh)
    for i in range(3)
]
for agent in agents:
    orchestrator.register_agent(agent)

# Execute distributed inference workflow
result = await orchestrator.execute_workflow("neural_analysis")
        """
        print(example_code)

        print("\n✅ Integration Pattern:")
        print("  1. Initialize NeuralMesh with nodes")
        print("  2. Create agents with mesh inference")
        print("  3. Distribute inference across nodes")
        print("  4. Aggregate results from mesh\n")


class PolicyEngineIntegration:
    """Integration with policy-engine package.

    Demonstrates how to enforce policies and constraints.
    """

    @staticmethod
    async def example_policy_enforcement():
        """Example: Enforce policies on agents.

        Shows how to use the Policy Engine to enforce constraints
        and policies on agent behavior.
        """
        print("📋 Policy Engine Integration Example")
        print("-" * 50)

        example_code = """
from policy_engine import PolicyEngine, Policy
from helix_agent_orchestration import AgentOrchestrator

# Initialize policy engine
policy_engine = PolicyEngine()

# Define policies
policies = [
    Policy(
        name="rate_limit",
        rule="requests_per_minute < 1000",
        action="throttle"
    ),
    Policy(
        name="cost_limit",
        rule="daily_cost < 1000",
        action="deny"
    ),
    Policy(
        name="data_retention",
        rule="data_age < 90_days",
        action="archive"
    ),
]

# Register policies
for policy in policies:
    policy_engine.register_policy(policy)

# Orchestrator with policy enforcement
class PolicyAwareOrchestrator(AgentOrchestrator):
    def __init__(self, policy_engine):
        super().__init__()
        self.policy_engine = policy_engine

    async def execute_workflow(self, workflow_name):
        # Check policies before execution
        if not self.policy_engine.evaluate_all():
            raise Exception("Policy violation detected")
        
        return await super().execute_workflow(workflow_name)

# Use policy-aware orchestrator
orchestrator = PolicyAwareOrchestrator(policy_engine)
result = await orchestrator.execute_workflow("analysis")
        """
        print(example_code)

        print("\n✅ Integration Pattern:")
        print("  1. Initialize PolicyEngine")
        print("  2. Define policies with rules")
        print("  3. Register policies")
        print("  4. Evaluate policies before execution\n")


async def main():
    """Run all integration examples."""
    print("🔗 Helix Agent Orchestration - Integration Examples\n")
    print("=" * 70)
    print()

    # Run all integration examples
    await UnifiedLLMIntegration.example_agent_reasoning()
    await NotificationsIntegration.example_agent_notifications()
    await TokenCostIntegration.example_token_tracking()
    await IntegrationIntegration.example_external_api_integration()
    await RoutineEngineIntegration.example_routine_scheduling()
    await NeuralMeshIntegration.example_distributed_inference()
    await PolicyEngineIntegration.example_policy_enforcement()

    print("=" * 70)
    print("\n✅ All integration examples completed!")
    print("\n📚 For more information, visit:")
    print("   https://github.com/Deathcharge/helix-agent-orchestration")


if __name__ == "__main__":
    asyncio.run(main())
