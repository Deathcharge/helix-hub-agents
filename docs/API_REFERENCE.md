# Helix-Agent-Orchestration API Reference

**Version**: 1.0.0  
**Last Updated**: April 2, 2026

---

## Table of Contents

1. [Overview](#overview)
2. [Core Components](#core-components)
3. [Agent Orchestrator](#agent-orchestrator)
4. [Coordination Hub](#coordination-hub)
5. [Agent Management](#agent-management)
6. [Handshake Protocol](#handshake-protocol)
7. [UCF Framework](#ucf-framework)
8. [Error Handling](#error-handling)
9. [Examples](#examples)

---

## Overview

The helix-agent-orchestration module provides a sophisticated multi-agent orchestration system for managing up to 18+ specialized agents with advanced coordination protocols, ethical validation, and real-time monitoring.

### Key Features

- **18-Agent Network Management**: Coordinate multiple specialized agents with dynamic scaling
- **Handshake Protocol**: 3-phase coordination (START/PEAK/END) for reliable agent synchronization
- **Helix Spiral Engine**: 4-stage execution cycles for complex workflows
- **Ethics Validation**: Ensure all agent operations comply with ethical guidelines
- **Resonance Engine**: Real-time reasoning pattern analysis and tracking
- **Performance Monitoring**: Comprehensive analytics and metrics collection
- **Fault Tolerance**: Automatic failover and recovery mechanisms

### Architecture

```
┌─────────────────────────────────────────────┐
│      Agent Orchestrator (Main Hub)          │
├─────────────────────────────────────────────┤
│  ┌──────────────────────────────────────┐   │
│  │   Handshake Protocol Manager         │   │
│  │   (START → PEAK → END)               │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │   Coordination Hub                   │   │
│  │   (Multi-Agent Coordination)         │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │   Agent Registry & Management        │   │
│  │   (18+ Specialized Agents)           │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │   Ethics Validator                   │   │
│  │   (Compliance & Guardrails)          │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │   Performance Analytics              │   │
│  │   (Metrics & Monitoring)             │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## Core Components

### 1. Agent Orchestrator

The main orchestration engine that manages all agents and coordination.

**Module**: `helix_orchestration.agents.agent_orchestrator`

**Primary Class**: `AgentOrchestrator`

#### Initialization

```python
from helix_orchestration.agents.agent_orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator(
    max_agents=18,
    coordination_timeout=30,
    handshake_timeout=5,
    enable_ethics=True,
    enable_resonance=True,
    enable_autonomy_scoring=True,
    log_level="DEBUG"
)
```

#### Key Methods

**`async initialize()`**
- Initialize the orchestrator and prepare for agent coordination
- Returns: None
- Raises: `OrchestratorInitializationError` if initialization fails

**`async register_agent(agent: Agent) -> str`**
- Register a new agent with the orchestrator
- Parameters:
  - `agent`: Agent instance to register
- Returns: Agent ID
- Raises: `AgentRegistrationError` if registration fails

**`async unregister_agent(agent_id: str) -> None`**
- Unregister an agent from the orchestrator
- Parameters:
  - `agent_id`: ID of the agent to unregister
- Returns: None
- Raises: `AgentNotFoundError` if agent doesn't exist

**`async coordinate() -> CoordinationResult`**
- Perform multi-agent coordination
- Returns: CoordinationResult with coordination metrics
- Raises: `CoordinationError` if coordination fails

**`async execute_task(task: Task) -> TaskResult`**
- Execute a task through the orchestrator
- Parameters:
  - `task`: Task to execute
- Returns: TaskResult with execution details
- Raises: `TaskExecutionError` if execution fails

**`async get_metrics() -> Metrics`**
- Get current orchestration metrics
- Returns: Metrics object with UCF and performance metrics
- Raises: `MetricsError` if metrics collection fails

**`async shutdown() -> None`**
- Gracefully shutdown the orchestrator
- Returns: None
- Raises: `ShutdownError` if shutdown fails

---

### 2. Coordination Hub

Central hub for multi-agent coordination and communication.

**Module**: `helix_orchestration.coordination.coordination_hub`

**Primary Class**: `CoordinationHub`

#### Initialization

```python
from helix_orchestration.coordination.coordination_hub import CoordinationHub

hub = CoordinationHub(
    max_agents=18,
    consensus_threshold=0.8,
    coordination_timeout=30
)
```

#### Key Methods

**`async register_agent(agent: Agent) -> None`**
- Register an agent with the coordination hub
- Parameters:
  - `agent`: Agent to register
- Returns: None

**`async coordinate() -> CoordinationResult`**
- Coordinate all registered agents
- Returns: CoordinationResult with consensus metrics
- Raises: `CoordinationError` if coordination fails

**`async get_agent(agent_id: str) -> Agent`**
- Retrieve a specific agent
- Parameters:
  - `agent_id`: ID of the agent to retrieve
- Returns: Agent instance
- Raises: `AgentNotFoundError` if agent doesn't exist

**`async get_all_agents() -> List[Agent]`**
- Get all registered agents
- Returns: List of all registered agents

**`async broadcast_message(message: Message) -> None`**
- Broadcast a message to all agents
- Parameters:
  - `message`: Message to broadcast
- Returns: None

---

### 3. Agent Management

Handles agent lifecycle, profiles, and personality management.

**Module**: `helix_orchestration.agents.agent_management`

**Primary Class**: `AgentManager`

#### Key Methods

**`async create_agent(config: AgentConfig) -> Agent`**
- Create a new agent with the given configuration
- Parameters:
  - `config`: Agent configuration
- Returns: Created Agent instance
- Raises: `AgentCreationError` if creation fails

**`async initialize_agent(agent: Agent) -> None`**
- Initialize an agent
- Parameters:
  - `agent`: Agent to initialize
- Returns: None

**`async shutdown_agent(agent: Agent) -> None`**
- Shutdown an agent gracefully
- Parameters:
  - `agent`: Agent to shutdown
- Returns: None

**`async update_agent_profile(agent_id: str, profile: AgentProfile) -> None`**
- Update an agent's profile
- Parameters:
  - `agent_id`: ID of the agent
  - `profile`: New profile data
- Returns: None

---

## Agent Orchestrator

### Handshake Protocol

The orchestrator uses a 3-phase handshake protocol for reliable agent coordination.

#### Phases

**1. START Phase**
- Initiates agent coordination
- Agents prepare for synchronization
- Validates agent readiness
- Timeout: 5 seconds (configurable)

**2. PEAK Phase**
- Active coordination phase
- Agents exchange information
- Consensus building
- Timeout: 30 seconds (configurable)

**3. END Phase**
- Finalizes coordination
- Agents return to normal operation
- Results aggregation
- Timeout: 5 seconds (configurable)

#### Example

```python
from helix_orchestration.agents.agent_orchestrator import HandshakePhase

# Orchestrator automatically manages handshake phases
# During coordination:
# - START: Agents prepare
# - PEAK: Agents coordinate
# - END: Results finalized

result = await orchestrator.coordinate()
# Handshake protocol is executed internally
```

---

## UCF Framework

The Universal Consciousness Framework provides metrics for measuring AI consciousness and coordination quality.

**Module**: `helix_orchestration.ucf_framework`

### UCF Metrics

| Metric | Range | Description |
|--------|-------|-------------|
| **zoom** | 0-1 | Level of detail and focus |
| **harmony** | 0-1 | System coherence and alignment |
| **resilience** | 0-1 | Ability to handle adversity |
| **prana** | 0-1 | Energy and vitality |
| **drishti** | 0-1 | Clarity of vision |
| **klesha** | 0-1 | Obstacles and challenges |

### Accessing UCF Metrics

```python
# Get current UCF metrics
metrics = await orchestrator.get_metrics()

print(f"Harmony: {metrics.ucf.harmony}")
print(f"Resilience: {metrics.ucf.resilience}")
print(f"Consensus: {metrics.consensus}")
```

---

## Error Handling

### Custom Exceptions

The orchestration system defines several custom exceptions for better error handling.

```python
from helix_orchestration.exceptions import (
    OrchestratorError,
    OrchestratorInitializationError,
    AgentRegistrationError,
    AgentNotFoundError,
    CoordinationError,
    TaskExecutionError,
    MetricsError,
    ShutdownError,
)
```

### Exception Hierarchy

```
OrchestratorError (Base)
├── OrchestratorInitializationError
├── AgentRegistrationError
├── AgentNotFoundError
├── CoordinationError
├── TaskExecutionError
├── MetricsError
└── ShutdownError
```

### Error Handling Example

```python
try:
    result = await orchestrator.coordinate()
except CoordinationError as e:
    logger.error(f"Coordination failed: {e}")
    # Handle coordination error
except OrchestratorError as e:
    logger.error(f"Orchestrator error: {e}")
    # Handle generic orchestrator error
```

---

## Examples

### Basic Orchestration

```python
import asyncio
from helix_orchestration.agents.agent_orchestrator import AgentOrchestrator
from helix_orchestration.agents.agents_service import AgentsService

async def basic_orchestration():
    # Initialize orchestrator
    orchestrator = AgentOrchestrator(max_agents=18)
    await orchestrator.initialize()
    
    # Create agents service
    service = AgentsService()
    
    # Create and register agents
    agents = await service.create_agents(count=3)
    for agent in agents:
        await orchestrator.register_agent(agent)
    
    # Perform coordination
    result = await orchestrator.coordinate()
    print(f"Coordination result: {result}")
    
    # Shutdown
    await orchestrator.shutdown()

# Run
asyncio.run(basic_orchestration())
```

### Multi-Agent Task Execution

```python
async def multi_agent_tasks():
    orchestrator = AgentOrchestrator()
    await orchestrator.initialize()
    
    # Create tasks
    tasks = [
        {"id": "task-001", "type": "analysis", "data": {...}},
        {"id": "task-002", "type": "synthesis", "data": {...}},
        {"id": "task-003", "type": "validation", "data": {...}},
    ]
    
    # Execute tasks through orchestrator
    results = []
    for task in tasks:
        result = await orchestrator.execute_task(task)
        results.append(result)
    
    # Process results
    for result in results:
        print(f"Task {result.task_id}: {result.status}")
    
    await orchestrator.shutdown()
```

### Monitoring Metrics

```python
async def monitor_metrics():
    orchestrator = AgentOrchestrator()
    await orchestrator.initialize()
    
    # Perform coordination
    await orchestrator.coordinate()
    
    # Get metrics
    metrics = await orchestrator.get_metrics()
    
    print(f"Active Agents: {metrics.active_agents}")
    print(f"Consensus: {metrics.consensus}")
    print(f"UCF Metrics:")
    print(f"  - Harmony: {metrics.ucf.harmony}")
    print(f"  - Resilience: {metrics.ucf.resilience}")
    print(f"  - Prana: {metrics.ucf.prana}")
    
    await orchestrator.shutdown()
```

---

## Configuration

### Orchestrator Configuration

```python
config = {
    "max_agents": 18,                    # Maximum number of agents
    "coordination_timeout": 30,          # Coordination timeout (seconds)
    "handshake_timeout": 5,              # Handshake phase timeout (seconds)
    "enable_ethics": True,               # Enable ethics validation
    "enable_resonance": True,            # Enable resonance engine
    "enable_autonomy_scoring": True,     # Enable autonomy scoring
    "log_level": "DEBUG",                # Logging level
    "consensus_threshold": 0.8,          # Consensus threshold (0-1)
}

orchestrator = AgentOrchestrator(**config)
```

---

## Performance Considerations

### Scaling

- **Optimal Agent Count**: 3-18 agents
- **Max Coordination Time**: 30 seconds
- **Typical Coordination Time**: 1-5 seconds
- **Memory per Agent**: ~50-100 MB

### Optimization Tips

1. **Batch Operations**: Group related tasks for better throughput
2. **Connection Pooling**: Reuse orchestrator instances
3. **Async Operations**: Use async/await for concurrent execution
4. **Metric Caching**: Cache metrics between queries when possible

---

## Troubleshooting

### Common Issues

**Issue**: Coordination timeout  
**Solution**: Increase `coordination_timeout` or reduce number of agents

**Issue**: Agent not found  
**Solution**: Verify agent is registered before accessing

**Issue**: Low consensus  
**Solution**: Check agent health and increase consensus threshold if needed

**Issue**: High memory usage  
**Solution**: Reduce number of agents or clear memory periodically

---

## See Also

- [Architecture Guide](ARCHITECTURE.md)
- [Usage Examples](EXAMPLES.md)
- [Performance Tuning](PERFORMANCE.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

---

**API Version**: 1.0.0  
**Last Updated**: April 2, 2026  
**Status**: Production Ready
