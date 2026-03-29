"""
Helix Orchestration - Multi-Agent AI Coordination Framework

A production-grade framework for coordinating multiple AI agents in complex workflows.
Provides 24 specialized agents, real-time coordination metrics (UCF), and event-driven architecture.
"""

__version__ = "1.0.0"
__author__ = "Andrew John Ward"
__license__ = "Apache-2.0"

# Core imports
try:
    from .agents.agent_orchestrator import AgentOrchestrator
    from .agents.agent_registry import AgentRegistry
    from .coordination.coordination_hub import CoordinationHub
    from .ucf_framework.tracker import UCFTracker
    from .ucf_framework.metrics import UCFMetrics
except ImportError as e:
    print(f"Warning: Could not import core modules: {e}")

__all__ = [
    "AgentOrchestrator",
    "AgentRegistry",
    "CoordinationHub",
    "UCFTracker",
    "UCFMetrics",
]
