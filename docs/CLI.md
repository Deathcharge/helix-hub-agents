# Helix Agent Orchestration CLI

A powerful command-line interface for managing, monitoring, and controlling multi-agent orchestration workflows.

## Installation

```bash
pip install helix-agent-orchestration
```

## Quick Start

### List All Agents

```bash
helix-orchestration agent list
```

Output:
```
┏━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
┃ Name      ┃ Role       ┃ Status ┃ Layer   ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
│ Kael      │ Reasoning  │ active │ Core    │
│ Lumina    │ Creativity │ active │ Core    │
│ Vega      │ Coord      │ active │ Core    │
│ Kavach    │ Security   │ active │ Security│
│ Arjuna    │ Orchestr   │ active │ Orch    │
└───────────┴────────────┴────────┴─────────┘

Total agents: 24
```

### Check Agent Status

```bash
helix-orchestration agent status Kael
```

Output:
```
┌─────────────────────────────────────────┐
│ Agent: Kael                             │
├─────────────────────────────────────────┤
│ Name: Kael                              │
│ Role: Reasoning                         │
│ Status: active                          │
│ Layer: Core                             │
│ Tasks Completed: 42                     │
│ Success Rate: 98.0%                     │
│ Last Active: 2 minutes ago              │
└─────────────────────────────────────────┘
```

### View Coordination Metrics

```bash
helix-orchestration metrics show
```

Output:
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Metric                  ┃ Value            ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ Total Agents            │ 24               │
│ Active Agents           │ 22               │
│ Coordination Efficiency │ 0.94             │
│ Average Response Time   │ 245ms            │
│ System Health           │ Excellent        │
│ Uptime                  │ 99.9%            │
└─────────────────────────┴──────────────────┘
```

### Run a Workflow

```bash
helix-orchestration workflow run my_workflow
```

Output:
```
⠋ Running workflow: my_workflow
✓ Workflow completed successfully
  Duration: 2.5s
  Tasks: 8/8
```

### Check System Health

```bash
helix-orchestration health
```

Output:
```
✓ System Health: Healthy
  Agents Online: 22/24
```

### Validate Configuration

```bash
helix-orchestration config validate --path orchestration.json
```

Output:
```
✓ Configuration is valid
  Agents: 24
  Workflows: 12
```

## Commands Reference

### Agent Commands

#### `agent list`
List all registered agents with their status and layer.

```bash
helix-orchestration agent list
```

#### `agent status <name>`
Show detailed status information for a specific agent.

```bash
helix-orchestration agent status Kael
```

**Options:**
- `<name>` - Agent name (required)

### Workflow Commands

#### `workflow run <name>`
Execute a workflow by name.

```bash
helix-orchestration workflow run my_workflow
```

**Options:**
- `<name>` - Workflow name (required)

### Metrics Commands

#### `metrics show`
Display current coordination metrics.

```bash
helix-orchestration metrics show
```

### Configuration Commands

#### `config validate`
Validate orchestration configuration file.

```bash
helix-orchestration config validate --path orchestration.json
```

**Options:**
- `--path, -p` - Path to config file (default: orchestration.json)

### System Commands

#### `health`
Perform system health check.

```bash
helix-orchestration health
```

#### `info`
Show system information.

```bash
helix-orchestration info
helix-orchestration info --version
```

**Options:**
- `--version, -v` - Show version number

## Configuration File Format

The CLI expects an `orchestration.json` configuration file with the following structure:

```json
{
  "agents": [
    {
      "name": "Kael",
      "role": "Reasoning",
      "layer": "Core",
      "enabled": true
    }
  ],
  "workflows": [
    {
      "name": "my_workflow",
      "description": "Example workflow",
      "steps": []
    }
  ],
  "coordination": {
    "mode": "distributed",
    "timeout": 30,
    "retry_policy": "exponential"
  }
}
```

## Advanced Usage

### Export Metrics to JSON

```bash
helix-orchestration metrics show > metrics.json
```

### Monitor Agent in Real-Time

```bash
watch -n 1 'helix-orchestration agent status Kael'
```

### Validate and Run Workflow

```bash
helix-orchestration config validate && helix-orchestration workflow run my_workflow
```

## Troubleshooting

### Command Not Found

If `helix-orchestration` command is not found, ensure the package is installed:

```bash
pip install helix-agent-orchestration
```

And that your Python scripts directory is in your PATH.

### Configuration Validation Fails

Check that your `orchestration.json` file contains all required fields:
- `agents` - Array of agent configurations
- `workflows` - Array of workflow definitions
- `coordination` - Coordination settings

### Agent Status Shows Offline

Ensure the agent is properly registered and the orchestration service is running.

## Environment Variables

- `HELIX_CONFIG_PATH` - Path to configuration file (default: orchestration.json)
- `HELIX_LOG_LEVEL` - Logging level (default: INFO)
- `HELIX_TIMEOUT` - Command timeout in seconds (default: 30)

## Examples

### Complete Workflow Management

```bash
# 1. Validate configuration
helix-orchestration config validate

# 2. Check system health
helix-orchestration health

# 3. List available agents
helix-orchestration agent list

# 4. Check specific agent
helix-orchestration agent status Kael

# 5. View metrics
helix-orchestration metrics show

# 6. Run workflow
helix-orchestration workflow run my_workflow
```

### Monitoring Setup

```bash
#!/bin/bash
# monitor.sh - Continuous monitoring script

while true; do
  clear
  echo "=== Helix Agent Orchestration Monitor ==="
  echo ""
  echo "System Health:"
  helix-orchestration health
  echo ""
  echo "Active Agents:"
  helix-orchestration agent list
  echo ""
  echo "Metrics:"
  helix-orchestration metrics show
  sleep 5
done
```

Run with:
```bash
chmod +x monitor.sh
./monitor.sh
```

## Integration with Scripts

```python
import subprocess
import json

def get_agent_status(agent_name):
    """Get agent status via CLI."""
    result = subprocess.run(
        ["helix-orchestration", "agent", "status", agent_name],
        capture_output=True,
        text=True
    )
    return result.stdout

def run_workflow(workflow_name):
    """Run a workflow via CLI."""
    result = subprocess.run(
        ["helix-orchestration", "workflow", "run", workflow_name],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

# Usage
status = get_agent_status("Kael")
print(status)

success = run_workflow("my_workflow")
print(f"Workflow {'succeeded' if success else 'failed'}")
```

## Performance Tips

1. **Batch Operations** - Use configuration files for bulk agent operations
2. **Caching** - Results are cached for 30 seconds by default
3. **Async Workflows** - Use `--async` flag for non-blocking execution
4. **Logging** - Enable debug logging with `--log-level DEBUG`

## Contributing

Found a bug or have a feature request? Please open an issue on GitHub:
https://github.com/Deathcharge/helix-agent-orchestration/issues

## License

Dual licensed under Apache 2.0 and Proprietary License.
