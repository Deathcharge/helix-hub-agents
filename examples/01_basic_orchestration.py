"""
Example 1: Basic Agent Orchestration
=====================================

Demonstrates basic agent orchestration with monitoring and communication.
"""

import asyncio
from helix_orchestration.monitoring import MetricsCollector, PerformanceAnalyzer, HealthMonitor, MetricsReporter, MetricType
from helix_orchestration.workflows import WorkflowTemplateLibrary, CommunicationPatternHandler
from helix_orchestration.communication import AgentCommunicationHub, Message, MessageType, MessagePriority


async def example_basic_agent_communication():
    """Basic agent-to-agent communication"""
    print("=" * 60)
    print("Example 1: Basic Agent Communication")
    print("=" * 60)
    
    hub = AgentCommunicationHub()
    
    # Register agents
    hub.register_agent("analyzer", {"role": "data_analyzer", "status": "active"})
    hub.register_agent("processor", {"role": "data_processor", "status": "active"})
    hub.register_agent("reporter", {"role": "report_generator", "status": "active"})
    
    print(f"Registered agents: {hub.list_agents()}")
    
    # Send a message
    message = Message(
        sender_id="analyzer",
        recipient_ids=["processor"],
        message_type=MessageType.REQUEST,
        priority=MessagePriority.HIGH,
        content={"action": "process", "data": [1, 2, 3, 4, 5]}
    )
    
    success = await hub.send_message(message)
    print(f"Message sent successfully: {success}")
    
    # Receive message
    received = await hub.receive_message(timeout=2)
    if received:
        print(f"Received message from {received.sender_id}: {received.content}")


async def example_workflow_execution():
    """Execute a pre-built workflow"""
    print("\n" + "=" * 60)
    print("Example 2: Workflow Execution")
    print("=" * 60)
    
    library = WorkflowTemplateLibrary()
    
    # Get a workflow template
    workflow = library.data_processing_pipeline()
    
    print(f"Workflow: {workflow.name}")
    print(f"Pattern: {workflow.pattern}")
    print(f"Steps: {len(workflow.steps)}")
    
    for step in workflow.steps:
        print(f"  - {step.name} (agent: {step.agent_id}, action: {step.action})")
    
    # Validate workflow
    is_valid = workflow.validate()
    print(f"Workflow is valid: {is_valid}")


async def example_metrics_collection():
    """Collect and analyze metrics"""
    print("\n" + "=" * 60)
    print("Example 3: Metrics Collection and Analysis")
    print("=" * 60)
    
    collector = MetricsCollector()
    analyzer = PerformanceAnalyzer(collector)
    
    # Record some metrics
    for i in range(100):
        collector.record_metric(
            MetricType.THROUGHPUT,
            value=10 + (i % 5),
            agent_id="agent_1"
        )
        collector.record_metric(
            MetricType.LATENCY,
            value=100 + (i % 50),
            agent_id="agent_1"
        )
        collector.record_metric(
            MetricType.ERROR_RATE,
            value=2 + (i % 3),
            agent_id="agent_1"
        )
    
    # Get performance metrics
    performance = analyzer.get_agent_performance("agent_1")
    
    print(f"Agent: agent_1")
    print(f"  Throughput: {performance.throughput:.2f} tasks/sec")
    print(f"  Latency (p50): {performance.latency_p50:.2f}ms")
    print(f"  Latency (p95): {performance.latency_p95:.2f}ms")
    print(f"  Latency (p99): {performance.latency_p99:.2f}ms")
    print(f"  Error Rate: {performance.error_rate:.2f}%")
    print(f"  Success Rate: {performance.success_rate:.2f}%")
    print(f"  Uptime: {performance.uptime:.2f}%")


async def example_health_monitoring():
    """Monitor agent health"""
    print("\n" + "=" * 60)
    print("Example 4: Agent Health Monitoring")
    print("=" * 60)
    
    collector = MetricsCollector()
    analyzer = PerformanceAnalyzer(collector)
    monitor = HealthMonitor(analyzer)
    
    # Record metrics
    for i in range(50):
        collector.record_metric(
            MetricType.ERROR_RATE,
            value=3 + (i % 2),
            agent_id="agent_2"
        )
        collector.record_metric(
            MetricType.RESOURCE_USAGE,
            value=60 + (i % 20),
            agent_id="agent_2"
        )
    
    # Check health
    health = monitor.check_agent_health("agent_2")
    
    print(f"Agent: agent_2")
    print(f"  Status: {health.status}")
    print(f"  Last Heartbeat: {health.last_heartbeat}")
    print(f"  Error Count: {health.error_count}")
    print(f"  Warning Count: {health.warning_count}")
    
    if health.issues:
        print(f"  Issues:")
        for issue in health.issues:
            print(f"    - {issue}")
    
    if health.recommendations:
        print(f"  Recommendations:")
        for rec in health.recommendations:
            print(f"    - {rec}")


async def example_metrics_reporting():
    """Generate metrics reports"""
    print("\n" + "=" * 60)
    print("Example 5: Metrics Reporting")
    print("=" * 60)
    
    collector = MetricsCollector()
    analyzer = PerformanceAnalyzer(collector)
    monitor = HealthMonitor(analyzer)
    reporter = MetricsReporter(analyzer, monitor)
    
    # Record metrics for multiple agents
    for agent_id in ["agent_1", "agent_2", "agent_3"]:
        for i in range(30):
            collector.record_metric(
                MetricType.THROUGHPUT,
                value=10 + (i % 5),
                agent_id=agent_id
            )
            collector.record_metric(
                MetricType.ERROR_RATE,
                value=2 + (i % 3),
                agent_id=agent_id
            )
    
    # Generate system report
    report = reporter.generate_system_report(["agent_1", "agent_2", "agent_3"])
    
    print(f"System Report:")
    print(f"  Timestamp: {report['timestamp']}")
    print(f"  System Health: {report['system_health']}")
    print(f"  Total Agents: {report['total_agents']}")
    print(f"  Total Throughput: {report['total_throughput']:.2f}")
    print(f"  Average Error Rate: {report['average_error_rate']:.2f}%")
    
    print(f"\n  Agent Reports:")
    for agent_report in report['agent_reports']:
        print(f"    - {agent_report['agent_id']}: throughput={agent_report['throughput']:.2f}, error_rate={agent_report['error_rate']:.2f}%")


async def example_communication_patterns():
    """Demonstrate communication patterns"""
    print("\n" + "=" * 60)
    print("Example 6: Communication Patterns")
    print("=" * 60)
    
    # Broadcast pattern
    print("Broadcast Pattern:")
    results = await CommunicationPatternHandler.broadcast(
        "coordinator",
        ["agent_1", "agent_2", "agent_3"],
        {"message": "Hello agents"}
    )
    print(f"  Broadcast to {len(results)} agents")
    
    # Consensus pattern
    print("\nConsensus Pattern:")
    consensus = await CommunicationPatternHandler.consensus(
        ["agent_1", "agent_2", "agent_3"],
        {"question": "Should we proceed?"},
        threshold=0.8
    )
    print(f"  Consensus reached: {consensus['consensus_reached']}")
    print(f"  Agreement ratio: {consensus['agreement_ratio']:.2f}")


async def main():
    """Run all examples"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Helix Agent Orchestration - Basic Examples  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    try:
        await example_basic_agent_communication()
        await example_workflow_execution()
        await example_metrics_collection()
        await example_health_monitoring()
        await example_metrics_reporting()
        await example_communication_patterns()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
    
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
