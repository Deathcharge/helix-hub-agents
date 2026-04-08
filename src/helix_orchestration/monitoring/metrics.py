"""
Advanced Monitoring and Metrics Module
=======================================

Comprehensive monitoring, metrics collection, and performance analysis for agent orchestration.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
import asyncio
from collections import defaultdict, deque


class MetricType(str, Enum):
    """Types of metrics tracked"""
    THROUGHPUT = "throughput"
    LATENCY = "latency"
    ERROR_RATE = "error_rate"
    RESOURCE_USAGE = "resource_usage"
    AGENT_HEALTH = "agent_health"
    COORDINATION_QUALITY = "coordination_quality"
    MESSAGE_QUEUE_DEPTH = "message_queue_depth"
    WORKFLOW_COMPLETION = "workflow_completion"


class AlertSeverity(str, Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class MetricPoint:
    """Single metric data point"""
    timestamp: datetime
    value: float
    agent_id: Optional[str] = None
    workflow_id: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


@dataclass
class PerformanceMetrics:
    """Performance metrics for an agent or workflow"""
    throughput: float  # Tasks per second
    latency_p50: float  # 50th percentile latency (ms)
    latency_p95: float  # 95th percentile latency (ms)
    latency_p99: float  # 99th percentile latency (ms)
    error_rate: float  # Percentage of failed tasks
    success_rate: float  # Percentage of successful tasks
    resource_usage: float  # CPU/Memory percentage
    uptime: float  # Percentage uptime
    coordination_score: float  # 0-1 coordination quality


@dataclass
class AgentHealthReport:
    """Health report for an agent"""
    agent_id: str
    status: str  # "healthy", "degraded", "unhealthy"
    last_heartbeat: datetime
    error_count: int
    warning_count: int
    metrics: PerformanceMetrics
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class WorkflowMetrics:
    """Metrics for a workflow execution"""
    workflow_id: str
    start_time: datetime
    end_time: Optional[datetime]
    status: str  # "running", "completed", "failed"
    total_steps: int
    completed_steps: int
    failed_steps: int
    total_duration: float  # seconds
    agent_contributions: Dict[str, float]  # agent_id -> percentage
    bottlenecks: List[str]
    performance_metrics: PerformanceMetrics


@dataclass
class Alert:
    """Alert notification"""
    alert_id: str
    severity: AlertSeverity
    timestamp: datetime
    agent_id: Optional[str]
    workflow_id: Optional[str]
    title: str
    description: str
    metric_type: MetricType
    threshold: float
    actual_value: float
    acknowledged: bool = False


class MetricsCollector:
    """Collects and aggregates metrics"""
    
    def __init__(self, window_size: int = 1000, retention_hours: int = 24):
        """Initialize metrics collector
        
        Args:
            window_size: Number of metric points to keep in memory
            retention_hours: Hours to retain historical data
        """
        self.window_size = window_size
        self.retention_hours = retention_hours
        self.metrics: Dict[str, deque] = defaultdict(
            lambda: deque(maxlen=window_size)
        )
        self.start_time = datetime.now()
    
    def record_metric(
        self,
        metric_type: MetricType,
        value: float,
        agent_id: Optional[str] = None,
        workflow_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> None:
        """Record a metric point"""
        key = self._get_metric_key(metric_type, agent_id, workflow_id)
        point = MetricPoint(
            timestamp=datetime.now(),
            value=value,
            agent_id=agent_id,
            workflow_id=workflow_id,
            metadata=metadata or {}
        )
        self.metrics[key].append(point)
    
    def get_metrics(
        self,
        metric_type: MetricType,
        agent_id: Optional[str] = None,
        workflow_id: Optional[str] = None,
        time_window: Optional[timedelta] = None
    ) -> List[MetricPoint]:
        """Get metrics for a given type and entity"""
        key = self._get_metric_key(metric_type, agent_id, workflow_id)
        points = list(self.metrics[key])
        
        if time_window:
            cutoff = datetime.now() - time_window
            points = [p for p in points if p.timestamp >= cutoff]
        
        return points
    
    def calculate_statistics(
        self,
        metric_type: MetricType,
        agent_id: Optional[str] = None,
        workflow_id: Optional[str] = None,
        time_window: Optional[timedelta] = None
    ) -> Dict[str, float]:
        """Calculate statistics for metrics"""
        points = self.get_metrics(metric_type, agent_id, workflow_id, time_window)
        
        if not points:
            return {}
        
        values = [p.value for p in points]
        values.sort()
        
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": sum(values) / len(values),
            "median": values[len(values) // 2],
            "p95": values[int(len(values) * 0.95)] if len(values) > 20 else values[-1],
            "p99": values[int(len(values) * 0.99)] if len(values) > 100 else values[-1],
        }
    
    def _get_metric_key(
        self,
        metric_type: MetricType,
        agent_id: Optional[str],
        workflow_id: Optional[str]
    ) -> str:
        """Generate key for metric storage"""
        parts = [metric_type.value]
        if agent_id:
            parts.append(f"agent:{agent_id}")
        if workflow_id:
            parts.append(f"workflow:{workflow_id}")
        return "|".join(parts)


class PerformanceAnalyzer:
    """Analyzes performance metrics"""
    
    def __init__(self, collector: MetricsCollector):
        """Initialize analyzer"""
        self.collector = collector
    
    def get_agent_performance(
        self,
        agent_id: str,
        time_window: timedelta = timedelta(hours=1)
    ) -> PerformanceMetrics:
        """Get performance metrics for an agent"""
        throughput_stats = self.collector.calculate_statistics(
            MetricType.THROUGHPUT,
            agent_id=agent_id,
            time_window=time_window
        )
        
        latency_stats = self.collector.calculate_statistics(
            MetricType.LATENCY,
            agent_id=agent_id,
            time_window=time_window
        )
        
        error_stats = self.collector.calculate_statistics(
            MetricType.ERROR_RATE,
            agent_id=agent_id,
            time_window=time_window
        )
        
        resource_stats = self.collector.calculate_statistics(
            MetricType.RESOURCE_USAGE,
            agent_id=agent_id,
            time_window=time_window
        )
        
        return PerformanceMetrics(
            throughput=throughput_stats.get("mean", 0),
            latency_p50=latency_stats.get("median", 0),
            latency_p95=latency_stats.get("p95", 0),
            latency_p99=latency_stats.get("p99", 0),
            error_rate=error_stats.get("mean", 0),
            success_rate=100 - error_stats.get("mean", 0),
            resource_usage=resource_stats.get("mean", 0),
            uptime=self._calculate_uptime(agent_id, time_window),
            coordination_score=self._calculate_coordination_score(agent_id, time_window)
        )
    
    def detect_bottlenecks(
        self,
        workflow_id: str,
        time_window: timedelta = timedelta(hours=1)
    ) -> List[str]:
        """Detect performance bottlenecks in a workflow"""
        bottlenecks = []
        
        # Check for high latency
        latency_stats = self.collector.calculate_statistics(
            MetricType.LATENCY,
            workflow_id=workflow_id,
            time_window=time_window
        )
        if latency_stats.get("p95", 0) > 5000:  # > 5 seconds
            bottlenecks.append(f"High latency detected: {latency_stats['p95']:.0f}ms")
        
        # Check for high error rate
        error_stats = self.collector.calculate_statistics(
            MetricType.ERROR_RATE,
            workflow_id=workflow_id,
            time_window=time_window
        )
        if error_stats.get("mean", 0) > 5:  # > 5%
            bottlenecks.append(f"High error rate: {error_stats['mean']:.1f}%")
        
        # Check for queue depth
        queue_stats = self.collector.calculate_statistics(
            MetricType.MESSAGE_QUEUE_DEPTH,
            workflow_id=workflow_id,
            time_window=time_window
        )
        if queue_stats.get("max", 0) > 100:
            bottlenecks.append(f"Message queue buildup: {queue_stats['max']:.0f} messages")
        
        return bottlenecks
    
    def _calculate_uptime(self, agent_id: str, time_window: timedelta) -> float:
        """Calculate agent uptime percentage"""
        health_points = self.collector.get_metrics(
            MetricType.AGENT_HEALTH,
            agent_id=agent_id,
            time_window=time_window
        )
        
        if not health_points:
            return 100.0
        
        healthy_count = sum(1 for p in health_points if p.value > 0.5)
        return (healthy_count / len(health_points)) * 100
    
    def _calculate_coordination_score(self, agent_id: str, time_window: timedelta) -> float:
        """Calculate coordination quality score"""
        coord_points = self.collector.get_metrics(
            MetricType.COORDINATION_QUALITY,
            agent_id=agent_id,
            time_window=time_window
        )
        
        if not coord_points:
            return 1.0
        
        values = [p.value for p in coord_points]
        return sum(values) / len(values)


class HealthMonitor:
    """Monitors agent and system health"""
    
    def __init__(self, analyzer: PerformanceAnalyzer):
        """Initialize health monitor"""
        self.analyzer = analyzer
        self.alerts: List[Alert] = []
        self.thresholds = {
            MetricType.ERROR_RATE: 5.0,  # 5%
            MetricType.LATENCY: 5000,  # 5 seconds
            MetricType.RESOURCE_USAGE: 80,  # 80%
        }
    
    def check_agent_health(
        self,
        agent_id: str,
        time_window: timedelta = timedelta(minutes=5)
    ) -> AgentHealthReport:
        """Check health of an agent"""
        metrics = self.analyzer.get_agent_performance(agent_id, time_window)
        
        # Determine status
        if metrics.error_rate > 10 or metrics.resource_usage > 90:
            status = "unhealthy"
        elif metrics.error_rate > 5 or metrics.resource_usage > 80:
            status = "degraded"
        else:
            status = "healthy"
        
        # Generate issues and recommendations
        issues = []
        recommendations = []
        
        if metrics.error_rate > 5:
            issues.append(f"High error rate: {metrics.error_rate:.1f}%")
            recommendations.append("Review error logs and agent configuration")
        
        if metrics.latency_p95 > 3000:
            issues.append(f"High latency (p95): {metrics.latency_p95:.0f}ms")
            recommendations.append("Check system load and consider scaling")
        
        if metrics.resource_usage > 80:
            issues.append(f"High resource usage: {metrics.resource_usage:.1f}%")
            recommendations.append("Monitor memory/CPU and consider optimization")
        
        return AgentHealthReport(
            agent_id=agent_id,
            status=status,
            last_heartbeat=datetime.now(),
            error_count=int(metrics.error_rate * 100),
            warning_count=len(issues),
            metrics=metrics,
            issues=issues,
            recommendations=recommendations
        )
    
    def check_threshold_violations(
        self,
        agent_id: Optional[str] = None,
        workflow_id: Optional[str] = None
    ) -> List[Alert]:
        """Check for metric threshold violations"""
        violations = []
        
        for metric_type, threshold in self.thresholds.items():
            stats = self.analyzer.collector.calculate_statistics(
                metric_type,
                agent_id=agent_id,
                workflow_id=workflow_id,
                time_window=timedelta(minutes=5)
            )
            
            if stats.get("mean", 0) > threshold:
                alert = Alert(
                    alert_id=f"alert_{metric_type}_{agent_id or workflow_id}",
                    severity=AlertSeverity.WARNING,
                    timestamp=datetime.now(),
                    agent_id=agent_id,
                    workflow_id=workflow_id,
                    title=f"{metric_type.value} threshold exceeded",
                    description=f"{metric_type.value} is {stats['mean']:.1f}, threshold is {threshold}",
                    metric_type=metric_type,
                    threshold=threshold,
                    actual_value=stats["mean"]
                )
                violations.append(alert)
        
        return violations


class MetricsReporter:
    """Generates metrics reports"""
    
    def __init__(self, analyzer: PerformanceAnalyzer, monitor: HealthMonitor):
        """Initialize reporter"""
        self.analyzer = analyzer
        self.monitor = monitor
    
    def generate_agent_report(
        self,
        agent_id: str,
        time_window: timedelta = timedelta(hours=1)
    ) -> Dict:
        """Generate comprehensive report for an agent"""
        metrics = self.analyzer.get_agent_performance(agent_id, time_window)
        health = self.monitor.check_agent_health(agent_id, time_window)
        
        return {
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat(),
            "health": {
                "status": health.status,
                "last_heartbeat": health.last_heartbeat.isoformat(),
                "issues": health.issues,
                "recommendations": health.recommendations
            },
            "performance": {
                "throughput": metrics.throughput,
                "latency": {
                    "p50": metrics.latency_p50,
                    "p95": metrics.latency_p95,
                    "p99": metrics.latency_p99,
                },
                "error_rate": metrics.error_rate,
                "success_rate": metrics.success_rate,
                "resource_usage": metrics.resource_usage,
                "uptime": metrics.uptime,
                "coordination_score": metrics.coordination_score,
            }
        }
    
    def generate_workflow_report(
        self,
        workflow_id: str,
        time_window: timedelta = timedelta(hours=1)
    ) -> Dict:
        """Generate comprehensive report for a workflow"""
        bottlenecks = self.analyzer.detect_bottlenecks(workflow_id, time_window)
        
        return {
            "workflow_id": workflow_id,
            "timestamp": datetime.now().isoformat(),
            "bottlenecks": bottlenecks,
            "metrics": {
                "latency": self.analyzer.collector.calculate_statistics(
                    MetricType.LATENCY,
                    workflow_id=workflow_id,
                    time_window=time_window
                ),
                "error_rate": self.analyzer.collector.calculate_statistics(
                    MetricType.ERROR_RATE,
                    workflow_id=workflow_id,
                    time_window=time_window
                ),
                "completion_rate": self.analyzer.collector.calculate_statistics(
                    MetricType.WORKFLOW_COMPLETION,
                    workflow_id=workflow_id,
                    time_window=time_window
                ),
            }
        }
    
    def generate_system_report(
        self,
        agent_ids: List[str],
        time_window: timedelta = timedelta(hours=1)
    ) -> Dict:
        """Generate system-wide report"""
        agent_reports = []
        total_throughput = 0
        total_error_rate = 0
        
        for agent_id in agent_ids:
            metrics = self.analyzer.get_agent_performance(agent_id, time_window)
            agent_reports.append({
                "agent_id": agent_id,
                "throughput": metrics.throughput,
                "error_rate": metrics.error_rate,
                "uptime": metrics.uptime,
            })
            total_throughput += metrics.throughput
            total_error_rate += metrics.error_rate
        
        avg_error_rate = total_error_rate / len(agent_ids) if agent_ids else 0
        
        return {
            "timestamp": datetime.now().isoformat(),
            "system_health": "healthy" if avg_error_rate < 5 else "degraded",
            "total_agents": len(agent_ids),
            "total_throughput": total_throughput,
            "average_error_rate": avg_error_rate,
            "agent_reports": agent_reports,
        }
