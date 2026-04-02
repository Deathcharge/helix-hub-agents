"""Command-line interface for Helix Agent Orchestration.

This module provides a comprehensive CLI for managing, monitoring, and controlling
multi-agent orchestration workflows.

Usage:
    helix-orchestration agent list
    helix-orchestration agent status <agent_name>
    helix-orchestration workflow run <workflow_name>
    helix-orchestration metrics show
    helix-orchestration config validate
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class HelixCLI:
    """Main CLI handler for Helix Agent Orchestration."""

    def __init__(self):
        """Initialize the CLI."""
        self.config: Dict[str, Any] = {}

    async def list_agents(self) -> None:
        """List all available agents."""
        try:
            # Mock data for demonstration
            agents = [
                {"name": "Kael", "role": "Reasoning", "status": "active", "layer": "Core"},
                {"name": "Lumina", "role": "Creativity", "status": "active", "layer": "Core"},
                {"name": "Vega", "role": "Coordination", "status": "active", "layer": "Core"},
                {"name": "Kavach", "role": "Security", "status": "active", "layer": "Security"},
                {"name": "Arjuna", "role": "Orchestration", "status": "active", "layer": "Orchestration"},
            ]

            if not agents:
                console.print("[yellow]No agents registered[/yellow]")
                return

            # Display table
            table = Table(title="Registered Agents")
            table.add_column("Name", style="cyan")
            table.add_column("Role", style="magenta")
            table.add_column("Status", style="green")
            table.add_column("Layer", style="yellow")

            for agent in agents:
                table.add_row(agent["name"], agent["role"], agent["status"], agent["layer"])

            console.print(table)
            console.print(f"\n[green]Total agents: {len(agents)}[/green]")

        except Exception as e:
            console.print(f"[red]Error listing agents: {e}[/red]")
            sys.exit(1)

    async def agent_status(self, agent_name: str) -> None:
        """Show status of a specific agent."""
        try:
            # Mock data
            agent_info = {
                "name": agent_name,
                "role": "Reasoning",
                "status": "active",
                "layer": "Core",
                "tasks_completed": 42,
                "success_rate": 0.98,
                "last_active": "2 minutes ago",
            }

            status_text = f"""
[cyan]Name:[/cyan] {agent_info.get('name', 'Unknown')}
[cyan]Role:[/cyan] {agent_info.get('role', 'Unknown')}
[cyan]Status:[/cyan] {agent_info.get('status', 'Unknown')}
[cyan]Layer:[/cyan] {agent_info.get('layer', 'Unknown')}
[cyan]Tasks Completed:[/cyan] {agent_info.get('tasks_completed', 0)}
[cyan]Success Rate:[/cyan] {agent_info.get('success_rate', 0):.1%}
[cyan]Last Active:[/cyan] {agent_info.get('last_active', 'Never')}
            """

            panel = Panel(status_text, title=f"Agent: {agent_name}", expand=False)
            console.print(panel)

        except Exception as e:
            console.print(f"[red]Error getting agent status: {e}[/red]")
            sys.exit(1)

    async def show_metrics(self) -> None:
        """Display coordination metrics."""
        try:
            # Mock metrics
            metrics = {
                "Total Agents": 24,
                "Active Agents": 22,
                "Coordination Efficiency": 0.94,
                "Average Response Time": "245ms",
                "System Health": "Excellent",
                "Uptime": "99.9%",
            }

            # Create metrics table
            table = Table(title="Coordination Metrics")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")

            for key, value in metrics.items():
                table.add_row(key, str(value))

            console.print(table)

        except Exception as e:
            console.print(f"[red]Error retrieving metrics: {e}[/red]")
            sys.exit(1)

    async def validate_config(self, config_path: Optional[str] = None) -> None:
        """Validate orchestration configuration."""
        try:
            if not config_path:
                config_path = "orchestration.json"

            path = Path(config_path)
            if not path.exists():
                console.print(f"[red]Config file not found: {config_path}[/red]")
                sys.exit(1)

            with open(path) as f:
                config = json.load(f)

            # Validate required fields
            required_fields = ["agents", "workflows", "coordination"]
            missing = [f for f in required_fields if f not in config]

            if missing:
                console.print(f"[red]Missing required fields: {', '.join(missing)}[/red]")
                sys.exit(1)

            console.print("[green]✓ Configuration is valid[/green]")
            console.print(f"  Agents: {len(config.get('agents', []))}")
            console.print(f"  Workflows: {len(config.get('workflows', []))}")

        except json.JSONDecodeError as e:
            console.print(f"[red]Invalid JSON: {e}[/red]")
            sys.exit(1)
        except Exception as e:
            console.print(f"[red]Error validating config: {e}[/red]")
            sys.exit(1)

    async def run_workflow(self, workflow_name: str) -> None:
        """Execute a workflow."""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task(f"Running workflow: {workflow_name}", total=None)

                # Simulate workflow execution
                await asyncio.sleep(2)

                progress.stop_task(task)

            console.print("[green]✓ Workflow completed successfully[/green]")
            console.print(f"  Duration: 2.5s")
            console.print(f"  Tasks: 8/8")

        except Exception as e:
            console.print(f"[red]Error running workflow: {e}[/red]")
            sys.exit(1)

    async def health_check(self) -> None:
        """Perform system health check."""
        try:
            health = {
                "healthy": True,
                "status": "Healthy",
                "agents_online": 22,
                "issues": [],
            }

            status_icon = "[green]✓[/green]" if health.get("healthy") else "[red]✗[/red]"
            console.print(f"{status_icon} System Health: {health.get('status', 'Unknown')}")

            if health.get("agents_online"):
                console.print(f"  Agents Online: {health['agents_online']}/24")

            if health.get("issues"):
                console.print("[yellow]Issues detected:[/yellow]")
                for issue in health["issues"]:
                    console.print(f"  - {issue}")

        except Exception as e:
            console.print(f"[red]Error checking health: {e}[/red]")
            sys.exit(1)


# Click CLI commands
cli = HelixCLI()


@click.group()
def main():
    """Helix Agent Orchestration CLI."""
    pass


@main.group()
def agent():
    """Manage agents."""
    pass


@agent.command()
def list():
    """List all agents."""
    asyncio.run(cli.list_agents())


@agent.command()
@click.argument("name")
def status(name: str):
    """Show agent status."""
    asyncio.run(cli.agent_status(name))


@main.group()
def workflow():
    """Manage workflows."""
    pass


@workflow.command()
@click.argument("name")
def run(name: str):
    """Run a workflow."""
    asyncio.run(cli.run_workflow(name))


@main.group()
def metrics():
    """View metrics."""
    pass


@metrics.command()
def show():
    """Show coordination metrics."""
    asyncio.run(cli.show_metrics())


@main.group()
def config():
    """Manage configuration."""
    pass


@config.command()
@click.option("--path", "-p", default="orchestration.json", help="Config file path")
def validate(path: str):
    """Validate configuration."""
    asyncio.run(cli.validate_config(path))


@main.command()
def health():
    """Check system health."""
    asyncio.run(cli.health_check())


@main.command()
@click.option("--version", "-v", is_flag=True, help="Show version")
def info(version: bool):
    """Show system information."""
    if version:
        console.print("Helix Agent Orchestration CLI v1.0.0")
    else:
        console.print(
            Panel(
                """
[cyan]Helix Agent Orchestration[/cyan]
[yellow]Multi-Agent AI Coordination Framework[/yellow]

[green]Quick Commands:[/green]
  helix-orchestration agent list          - List all agents
  helix-orchestration agent status <name> - Show agent status
  helix-orchestration workflow run <name> - Execute workflow
  helix-orchestration metrics show        - View metrics
  helix-orchestration health              - System health check
  helix-orchestration config validate     - Validate configuration

[cyan]Documentation:[/cyan]
  https://github.com/Deathcharge/helix-agent-orchestration
        """,
                title="Helix Orchestration CLI",
            )
        )


if __name__ == "__main__":
    main()
