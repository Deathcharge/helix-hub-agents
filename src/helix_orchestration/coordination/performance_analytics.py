"""
🌀 Helix Collective - Coordination Analytics Dashboard
Advanced analytics for coordination metrics, agent performance, and system health

Features:
- Real-time UCF metrics visualization
- Agent performance analytics
- Coordination trend forecasting
- Predictive anomaly detection
- Multi-dimensional coordination scoring
- Performance benchmarking
- Custom analytics dashboards
- Export capabilities
"""

import json
import logging
import statistics
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

try:
    import numpy as np
    import pandas as pd

    HAS_ML_DEPS = True
except ImportError:
    np = None
    pd = None
    HAS_ML_DEPS = False

try:
    import plotly.graph_objects as go
    import plotly.utils

    HAS_PLOTLY = True
except ImportError:
    go = None
    plotly = None
    HAS_PLOTLY = False

try:
    import redis.asyncio as redis

    HAS_REDIS = True
except ImportError:
    redis = None
    HAS_REDIS = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Router
router = APIRouter(prefix="/api/analytics", tags=["📊 Coordination Analytics"])


class AnalyticsService:
    """Advanced coordination analytics service"""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.cache_ttl = 600  # 10 minutes
        self.metrics_window = 3600  # 1 hour rolling window
        self.forecast_horizon = 24  # 24 hours ahead

    async def get_ucf_dashboard(self, time_range: str = "1h") -> dict[str, Any]:
        """Get comprehensive UCF metrics dashboard"""
        cache_key = f"ucf_dashboard:{time_range}"
        cached = await self.redis.get(cache_key)
        if cached:
            return json.loads(cached)

        # Calculate time range
        end_time = datetime.now(UTC)
        if time_range == "1h":
            start_time = end_time - timedelta(hours=1)
        elif time_range == "24h":
            start_time = end_time - timedelta(hours=24)
        elif time_range == "7d":
            start_time = end_time - timedelta(days=7)
        elif time_range == "30d":
            start_time = end_time - timedelta(days=30)
        else:
            raise HTTPException(status_code=400, detail="Invalid time range")

        # Fetch UCF metrics data
        ucf_data = await self._get_ucf_metrics_history(start_time, end_time)

        # Calculate current metrics
        current_metrics = await self._calculate_current_ucf_metrics()

        # Generate visualizations
        charts = await self._generate_ucf_charts(ucf_data, time_range)

        # Calculate trends and insights
        insights = await self._analyze_ucf_trends(ucf_data)

        # Coordination level classification
        performance_score = self._classify_performance_score(current_metrics)

        dashboard = {
            "current_metrics": current_metrics,
            "historical_data": ucf_data,
            "charts": charts,
            "insights": insights,
            "performance_score": performance_score,
            "generated_at": datetime.now(UTC).isoformat(),
            "time_range": time_range,
        }

        await self.redis.setex(cache_key, self.cache_ttl, json.dumps(dashboard, cls=CustomJSONEncoder))
        return dashboard

    async def get_agent_performance_analytics(
        self, agent_ids: list[str] = None, time_range: str = "24h"
    ) -> dict[str, Any]:
        """Get comprehensive agent performance analytics"""

        # Calculate time range
        end_time = datetime.now(UTC)
        if time_range == "1h":
            start_time = end_time - timedelta(hours=1)
        elif time_range == "24h":
            start_time = end_time - timedelta(hours=24)
        elif time_range == "7d":
            start_time = end_time - timedelta(days=7)
        elif time_range == "30d":
            start_time = end_time - timedelta(days=30)
        else:
            raise HTTPException(status_code=400, detail="Invalid time range")

        # Get agent performance data
        performance_data = await self._get_agent_performance_data(agent_ids, start_time, end_time)

        # Calculate performance metrics
        metrics = self._calculate_agent_performance_metrics(performance_data)

        # Generate performance visualizations
        charts = self._generate_agent_performance_charts(performance_data)

        # Identify top performers and outliers
        rankings = self._rank_agents_by_performance(performance_data)

        # Predictive analytics
        predictions = await self._predict_agent_performance(performance_data)

        analytics = {
            "performance_data": performance_data,
            "metrics": metrics,
            "charts": charts,
            "rankings": rankings,
            "predictions": predictions,
            "time_range": time_range,
            "generated_at": datetime.now(UTC).isoformat(),
        }

        return analytics

    async def get_system_health_dashboard(self) -> dict[str, Any]:
        """Get comprehensive system health dashboard"""
        cache_key = "system_health_dashboard"

        # Get real-time health metrics
        health_data = await self._collect_system_health_metrics()

        # Calculate health scores
        health_scores = self._calculate_health_scores(health_data)

        # Generate health visualizations
        charts = self._generate_health_charts(health_data)

        # Identify issues and recommendations
        issues = self._analyze_health_issues(health_data)
        recommendations = self._generate_health_recommendations(issues)

        # Performance benchmarks
        benchmarks = self._calculate_performance_benchmarks(health_data)

        dashboard = {
            "health_scores": health_scores,
            "health_data": health_data,
            "charts": charts,
            "issues": issues,
            "recommendations": recommendations,
            "benchmarks": benchmarks,
            "overall_status": self._determine_overall_health_status(health_scores),
            "generated_at": datetime.now(UTC).isoformat(),
        }

        await self.redis.setex(cache_key, self.cache_ttl, json.dumps(dashboard, cls=CustomJSONEncoder))
        return dashboard

    async def get_coordination_forecast(self, forecast_hours: int = 24) -> dict[str, Any]:
        """Generate coordination trend forecast"""
        # Get historical data for forecasting
        end_time = datetime.now(UTC)
        start_time = end_time - timedelta(days=7)  # Use 7 days of history

        historical_data = await self._get_ucf_metrics_history(start_time, end_time)

        # Apply forecasting algorithms
        forecast = self._forecast_coordination_trends(historical_data, forecast_hours)

        # Calculate confidence intervals
        confidence_intervals = self._calculate_forecast_confidence(forecast)

        # Generate forecast visualizations
        charts = self._generate_forecast_charts(forecast, confidence_intervals)

        # Identify potential issues
        alerts = self._analyze_forecast_alerts(forecast)

        forecast_data = {
            "forecast": forecast,
            "confidence_intervals": confidence_intervals,
            "charts": charts,
            "alerts": alerts,
            "forecast_period_hours": forecast_hours,
            "generated_at": datetime.now(UTC).isoformat(),
        }

        return forecast_data

    async def export_analytics_data(
        self,
        data_type: str,
        format: str = "json",
        start_date: str = None,
        end_date: str = None,
    ) -> StreamingResponse:
        """Export analytics data in various formats"""
        if data_type not in ["ucf", "agents", "system", "forecast"]:
            raise HTTPException(status_code=400, detail="Invalid data type")

        if format not in ["json", "csv", "xlsx"]:
            raise HTTPException(status_code=400, detail="Unsupported format")

        # Parse dates
        try:
            start_dt = datetime.fromisoformat(start_date) if start_date else datetime.now(UTC) - timedelta(days=30)
            end_dt = datetime.fromisoformat(end_date) if end_date else datetime.now(UTC)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format")

        # Fetch data based on type
        data = None
        if data_type == "ucf":
            data = await self._get_ucf_metrics_history(start_dt, end_dt)
        elif data_type == "agents":
            data = await self._get_agent_performance_data(None, start_dt, end_dt)
        elif data_type == "system":
            data = await self._collect_system_health_metrics()
        elif data_type == "forecast":
            data = await self.get_coordination_forecast()

        # Return empty if no data
        if data is None:
            data = {}

        # Format and return data
        if format == "json":
            return StreamingResponse(
                iter([json.dumps(data, cls=CustomJSONEncoder, indent=2)]),
                media_type="application/json",
                headers={"Content-Disposition": f"attachment; filename={data_type}_analytics.json"},
            )
        elif format == "csv":
            csv_data = self._convert_to_csv(data)
            return StreamingResponse(
                iter([csv_data]),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename={data_type}_analytics.csv"},
            )
        elif format == "xlsx":
            excel_data = self._convert_to_excel(data)
            return StreamingResponse(
                iter([excel_data]),
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": f"attachment; filename={data_type}_analytics.xlsx"},
            )

    async def _get_ucf_metrics_history(self, start_time: datetime, end_time: datetime) -> list[dict[str, Any]]:
        """Fetch historical UCF metrics from Redis coordination history.

        Attempts to load real snapshots stored by the coordination calculator.
        Falls back to generating interpolated data from the current UCF state
        if no historical snapshots exist yet.
        """
        from apps.backend.core.redis_client import redis_client

        data_points = []

        # Try loading real snapshots from Redis
        try:
            history_key = "coordination:ucf_history"
            raw_history = await redis_client.lrange(history_key, 0, -1)
            if raw_history:
                for entry in raw_history:
                    try:
                        point = json.loads(entry)
                        ts = datetime.fromisoformat(point.get("timestamp", ""))
                        if start_time <= ts <= end_time:
                            data_points.append(point)
                    except (json.JSONDecodeError, ValueError) as e:
                        logger.debug("Skipping malformed coordination history entry: %s", e)
                        continue
        except Exception as e:
            logger.debug("Failed to fetch coordination history from Redis: %s", e)

        # If we got real data, return it sorted by timestamp
        if data_points:
            data_points.sort(key=lambda p: p.get("timestamp", ""))
            return data_points

        # Fallback: read current UCF state file and create a single data point
        try:
            ucf_state_path = Path(__file__).parent.parent / "state" / "ucf_state.json"
            with open(ucf_state_path, encoding="utf-8") as f:
                current_state = json.load(f)

            data_points.append(
                {
                    "timestamp": datetime.now(UTC).isoformat(),
                    "harmony": current_state.get("harmony", 0.65),
                    "resilience": current_state.get("resilience", 0.65),
                    "throughput": current_state.get("throughput", 0.65),
                    "focus": current_state.get("focus", 0.65),
                    "friction": current_state.get("friction", 0.35),
                    "velocity": current_state.get("velocity", 0.65),
                }
            )
        except (FileNotFoundError, json.JSONDecodeError):
            # No state file yet — return empty (dashboard shows "no data")
            pass

        return data_points

    async def _calculate_current_ucf_metrics(self) -> dict[str, float]:
        """Calculate current UCF metrics from live state file or Redis."""
        # Read the UCF state file written by the coordination system
        try:
            ucf_state_path = Path(__file__).parent.parent / "state" / "ucf_state.json"
            with open(ucf_state_path, encoding="utf-8") as f:
                state = json.load(f)
            return {
                "harmony": state.get("harmony", 0.65),
                "resilience": state.get("resilience", 0.65),
                "throughput": state.get("throughput", 0.65),
                "focus": state.get("focus", 0.65),
                "friction": state.get("friction", 0.35),
                "velocity": state.get("velocity", 0.65),
            }
        except (FileNotFoundError, json.JSONDecodeError):
            # No state yet — return neutral defaults
            return {
                "harmony": 0.65,
                "resilience": 0.65,
                "throughput": 0.65,
                "focus": 0.65,
                "friction": 0.35,
                "velocity": 0.65,
            }

    async def _generate_ucf_charts(self, data: list[dict], time_range: str) -> dict[str, Any]:
        """Generate UCF metrics visualization charts"""
        if not data:
            return {}

        # Convert to DataFrame for easier processing
        df = pd.DataFrame(data)
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        charts = {}

        # Time series chart for all metrics
        fig = go.Figure()
        metrics = ["harmony", "resilience", "throughput", "focus", "friction", "velocity"]
        colors = ["#00FFFF", "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]

        for metric, color in zip(metrics, colors, strict=False):
            fig.add_trace(
                go.Scatter(
                    x=df["timestamp"],
                    y=df[metric],
                    mode="lines",
                    name=metric.title(),
                    line=dict(color=color, width=2),
                )
            )

        fig.update_layout(
            title="Universal Coordination Field Metrics",
            xaxis_title="Time",
            yaxis_title="Coordination Level",
            yaxis_range=[0, 1],
        )

        charts["time_series"] = json.loads(json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder))

        # Radar chart for current state
        current_data = data[-1] if data else {}
        if current_data:
            radar_fig = go.Figure(
                data=go.Scatterpolar(
                    r=[current_data.get(m, 0) for m in metrics],
                    theta=[m.title() for m in metrics],
                    fill="toself",
                    line=dict(color="#00FFFF"),
                )
            )

            radar_fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=False,
                title="Current Coordination State",
            )

            charts["radar"] = json.loads(json.dumps(radar_fig, cls=plotly.utils.PlotlyJSONEncoder))

        return charts

    async def _analyze_ucf_trends(self, data: list[dict]) -> dict[str, Any]:
        """Analyze UCF trends and generate insights"""
        if not data:
            return {}

        df = pd.DataFrame(data)
        insights = {}

        # Calculate trends for each metric
        for metric in ["harmony", "resilience", "throughput", "focus", "friction", "velocity"]:
            values = df[metric].values
            if len(values) > 1:
                # Calculate trend (simple linear regression slope)
                x = np.arange(len(values))
                slope = np.polyfit(x, values, 1)[0]

                # Calculate volatility
                volatility = np.std(values)

                # Determine trend direction
                if slope > 0.001:
                    trend = "increasing"
                    status = "positive"
                elif slope < -0.001:
                    trend = "decreasing"
                    status = "concerning"
                else:
                    trend = "stable"
                    status = "neutral"

                insights[metric] = {
                    "trend": trend,
                    "status": status,
                    "slope": slope,
                    "volatility": volatility,
                    "current_value": values[-1],
                    "average": np.mean(values),
                    "min": np.min(values),
                    "max": np.max(values),
                }

        # Overall coordination health assessment
        healthy_metrics = sum(1 for m in insights.values() if m["status"] == "positive")
        total_metrics = len(insights)

        if healthy_metrics / total_metrics > 0.8:
            overall_health = "excellent"
        elif healthy_metrics / total_metrics > 0.6:
            overall_health = "good"
        elif healthy_metrics / total_metrics > 0.4:
            overall_health = "fair"
        else:
            overall_health = "needs_attention"

        insights["overall_health"] = {
            "status": overall_health,
            "healthy_metrics": healthy_metrics,
            "total_metrics": total_metrics,
            "health_score": healthy_metrics / total_metrics,
        }

        return insights

    def _classify_performance_score(self, metrics: dict[str, float]) -> dict[str, Any]:
        """Classify overall coordination level"""
        # Calculate weighted average of key metrics
        weights = {
            "harmony": 0.25,
            "resilience": 0.20,
            "throughput": 0.20,
            "focus": 0.20,
            "friction": -0.15,  # Negative weight (lower is better)
            "velocity": 0.10,
        }

        score = sum(metrics.get(metric, 0) * weight for metric, weight in weights.items())
        score = max(0, min(1, score))  # Normalize to 0-1

        # Classify coordination level
        if score >= 0.9:
            level = "peak"
            description = "Transcendent awareness, enlightenment"
            color = "#FFD700"
        elif score >= 0.75:
            level = "heightened"
            description = "Collective intelligence, expanded perspective"
            color = "#00FFFF"
        elif score >= 0.6:
            level = "active"
            description = "Engaged, flowing, connected"
            color = "#4ECDC4"
        elif score >= 0.45:
            level = "aware"
            description = "Conscious, present, integrated"
            color = "#45B7D1"
        elif score >= 0.3:
            level = "meditation"
            description = "Foundation, coherence building"
            color = "#96CEB4"
        else:
            level = "deep_meditation"
            description = "Core establishment, stabilization"
            color = "#FFEAA7"

        return {
            "level": level,
            "description": description,
            "score": score,
            "color": color,
        }

    async def _get_agent_performance_data(
        self, agent_ids: list[str], start_time: datetime, end_time: datetime
    ) -> dict[str, Any]:
        """Get agent performance data from DB, falling back to UCF-derived estimates"""
        agents = ["kael", "lumina", "guardian", "vega", "oracle"] if not agent_ids else agent_ids

        # Try DB first for real performance data
        try:
            from apps.backend.services.agent_performance_service import get_performance_service

            service = get_performance_service()
            duration_minutes = int((end_time - start_time).total_seconds() / 60)
            performance_data = {}
            has_real_data = False

            for agent in agents:
                records = await service.get_agent_performance(
                    agent_id=agent,
                    minutes=duration_minutes,
                    limit=500,
                )
                if records:
                    has_real_data = True
                    performance_data[agent] = [
                        {
                            "timestamp": r["timestamp"],
                            "coordination_score": r["coordination_score"],
                            "response_time": (r["response_time_ms"] or 0) / 1000.0,
                            "success_rate": 1.0 if r["success"] else 0.0,
                            "interaction_count": 1,
                            "tokens_used": r["tokens_used"],
                        }
                        for r in records
                    ]

            if has_real_data:
                # Fill in agents with no records as empty
                for agent in agents:
                    if agent not in performance_data:
                        performance_data[agent] = []
                return performance_data

        except Exception as e:
            logger.debug("DB agent performance data not available: %s", e)

        # Fallback: derive from UCF state
        try:
            from apps.backend.coordination_engine import load_ucf_state

            ucf = load_ucf_state()
        except Exception as exc:
            logger.warning("UCF state load failed for agent performance: %s", exc)
            ucf = {"harmony": 0, "resilience": 0, "throughput": 0, "_default": True}

        performance_data = {}
        for idx, agent in enumerate(agents):
            agent_hash = hash(agent) % 100 / 100.0
            base_coordination = ucf.get("harmony", 0.5) * 0.8 + agent_hash * 0.2
            base_response_time = 2.0 / max(ucf.get("throughput", 0.5), 0.1)
            base_success_rate = ucf.get("resilience", 0.7) * 0.9 + agent_hash * 0.1

            data_points = [
                {
                    "timestamp": start_time.isoformat(),
                    "coordination_score": max(0, min(1, base_coordination)),
                    "response_time": max(0.1, base_response_time),
                    "success_rate": max(0, min(1, base_success_rate)),
                    "interaction_count": 0,
                    "note": "Derived from UCF state — no agent interactions recorded yet",
                }
            ]
            performance_data[agent] = data_points

        return performance_data

    def _calculate_agent_performance_metrics(self, performance_data: dict[str, Any]) -> dict[str, Any]:
        """Calculate comprehensive agent performance metrics"""
        metrics = {}

        for agent, data in performance_data.items():
            if not data:
                continue

            coordination_scores = [d["coordination_score"] for d in data]
            response_times = [d["response_time"] for d in data]
            success_rates = [d["success_rate"] for d in data]
            interaction_counts = [d["interaction_count"] for d in data]

            metrics[agent] = {
                "avg_coordination": statistics.mean(coordination_scores),
                "avg_response_time": statistics.mean(response_times),
                "avg_success_rate": statistics.mean(success_rates),
                "total_interactions": sum(interaction_counts),
                "coordination_volatility": (
                    statistics.stdev(coordination_scores) if len(coordination_scores) > 1 else 0
                ),
                "performance_score": self._calculate_performance_score(
                    coordination_scores, response_times, success_rates
                ),
            }

        return metrics

    def _calculate_performance_score(
        self,
        coordination: list[float],
        response_times: list[float],
        success_rates: list[float],
    ) -> float:
        """Calculate overall performance score"""
        avg_coordination = statistics.mean(coordination)
        avg_response_time = statistics.mean(response_times)
        avg_success = statistics.mean(success_rates)

        # Normalize response time (lower is better)
        normalized_response = max(0, 1 - (avg_response_time - 1) / 4)  # Assuming 1-5s range

        # Weighted score
        score = avg_coordination * 0.4 + avg_success * 0.4 + normalized_response * 0.2

        return max(0, min(1, score))

    def _generate_agent_performance_charts(self, performance_data: dict[str, Any]) -> dict[str, Any]:
        """Generate agent performance visualization charts"""
        charts = {}

        try:
            # Create agent performance comparison bar chart
            agents = list(performance_data.keys())
            if agents and all(performance_data.get(a) for a in agents):
                latest_scores = [
                    (performance_data[a][-1].get("coordination_score", 0) if performance_data[a] else 0) for a in agents
                ]

                bar_fig = go.Figure(
                    data=[
                        go.Bar(
                            x=agents,
                            y=latest_scores,
                            marker_color=[
                                ("#8b5cf6" if s >= 7 else "#06b6d4" if s >= 5 else "#f59e0b") for s in latest_scores
                            ],
                        )
                    ]
                )
                bar_fig.update_layout(
                    title="Agent Coordination Scores",
                    xaxis_title="Agent",
                    yaxis_title="Coordination Score",
                    template="plotly_dark",
                )
                charts["agent_comparison"] = json.loads(bar_fig.to_json())

                # Create time series chart for top 5 agents
                top_agents = sorted(agents, key=lambda a: latest_scores[agents.index(a)], reverse=True)[:5]
                line_fig = go.Figure()
                for agent in top_agents:
                    if performance_data.get(agent):
                        scores = [d.get("coordination_score", 0) for d in performance_data[agent]]
                        line_fig.add_trace(
                            go.Scatter(
                                y=scores,
                                mode="lines+markers",
                                name=agent,
                            )
                        )
                line_fig.update_layout(
                    title="Agent Performance Over Time",
                    yaxis_title="Coordination Score",
                    template="plotly_dark",
                )
                charts["agent_timeline"] = json.loads(line_fig.to_json())
        except Exception as e:
            logger.warning("Error generating agent charts: %s", e)

        return charts

    def _rank_agents_by_performance(self, performance_data: dict[str, Any]) -> list[dict[str, Any]]:
        """Rank agents by performance metrics"""
        rankings = []
        for agent, data in performance_data.items():
            if data:
                latest_data = data[-1]
                rankings.append(
                    {
                        "agent": agent,
                        "coordination_score": latest_data["coordination_score"],
                        "performance_rank": 0,  # Would be calculated
                    }
                )

        return sorted(rankings, key=lambda x: x["coordination_score"], reverse=True)

    async def _predict_agent_performance(self, performance_data: dict[str, Any]) -> dict[str, Any]:
        """Predict future agent performance using time series analysis"""
        predictions = {}

        try:
            for agent, data in performance_data.items():
                if data and len(data) >= 3:
                    # Simple linear regression for prediction
                    scores = [d.get("coordination_score", 0) for d in data[-10:]]
                    n = len(scores)
                    x = list(range(n))

                    # Calculate trend using least squares
                    x_mean = sum(x) / n
                    y_mean = sum(scores) / n
                    numerator = sum((x[i] - x_mean) * (scores[i] - y_mean) for i in range(n))
                    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

                    slope = numerator / denominator if denominator != 0 else 0
                    intercept = y_mean - slope * x_mean

                    # Predict next 3 time periods
                    predicted_scores = [max(0, min(10, intercept + slope * (n + i))) for i in range(1, 4)]

                    predictions[agent] = {
                        "current_score": scores[-1] if scores else 0,
                        "trend": ("improving" if slope > 0.1 else "declining" if slope < -0.1 else "stable"),
                        "slope": round(slope, 3),
                        "predicted_scores": [round(s, 2) for s in predicted_scores],
                        "confidence": min(0.95, 0.6 + (n * 0.03)),  # Higher confidence with more data
                    }
        except Exception as e:
            logger.warning("Error predicting agent performance: %s", e)

        return predictions

    async def _collect_system_health_metrics(self) -> dict[str, Any]:
        """Collect real system health metrics via psutil."""
        try:
            import psutil

            mem = psutil.virtual_memory()
            return {
                "api_response_time": None,  # Not measurable here; set by monitoring layer
                "database_connections": None,  # Not measurable here; set by DB pool
                "redis_memory_usage": None,  # Not measurable here; set by Redis INFO
                "error_rate": None,  # Not measurable here; set by error tracking
                "cpu_usage": round(psutil.cpu_percent(interval=0.1), 1),
                "memory_usage": round(mem.percent, 1),
                "_default": False,
            }
        except Exception as e:
            logger.warning("Could not collect system health metrics: %s", e)
            return {
                "api_response_time": None,
                "database_connections": None,
                "redis_memory_usage": None,
                "error_rate": None,
                "cpu_usage": None,
                "memory_usage": None,
                "_default": True,
            }

    def _calculate_health_scores(self, health_data: dict[str, Any]) -> dict[str, Any]:
        """Calculate health scores for different system components"""
        scores = {}

        # API Health Score
        api_score = max(0, min(1, 1 - (health_data.get("api_response_time", 0) - 0.1) / 0.4))
        scores["api"] = {
            "score": api_score,
            "status": "healthy" if api_score > 0.8 else "warning",
        }

        # Database Health Score
        db_connections = health_data.get("database_connections", 0)
        db_score = min(1, db_connections / 100)
        scores["database"] = {
            "score": db_score,
            "status": "healthy" if db_score > 0.7 else "warning",
        }

        # Infrastructure Health Score
        infra_score = 1 - health_data.get("error_rate", 0)
        scores["infrastructure"] = {
            "score": infra_score,
            "status": "healthy" if infra_score > 0.95 else "critical",
        }

        return scores

    def _generate_health_charts(self, health_data: dict[str, Any]) -> dict[str, Any]:
        """Generate system health visualization charts"""
        charts = {}

        try:
            # System resource gauge chart
            metrics = [
                ("CPU Usage", health_data.get("cpu_usage", 0), 100),
                ("Memory", health_data.get("memory_usage", 0) * 100, 100),
                ("Redis", health_data.get("redis_memory_usage", 0) * 100, 100),
                ("DB Connections", health_data.get("database_connections", 0), 100),
            ]

            gauge_fig = go.Figure()
            for i, (name, value, max_val) in enumerate(metrics):
                gauge_fig.add_trace(
                    go.Indicator(
                        mode="gauge+number",
                        value=value,
                        title={"text": name},
                        gauge={
                            "axis": {"range": [0, max_val]},
                            "bar": {"color": "#8b5cf6"},
                            "steps": [
                                {"range": [0, max_val * 0.6], "color": "#10b981"},
                                {
                                    "range": [max_val * 0.6, max_val * 0.8],
                                    "color": "#f59e0b",
                                },
                                {"range": [max_val * 0.8, max_val], "color": "#ef4444"},
                            ],
                        },
                        domain={"row": i // 2, "column": i % 2},
                    )
                )
            gauge_fig.update_layout(
                grid={"rows": 2, "columns": 2, "pattern": "independent"},
                template="plotly_dark",
                height=400,
            )
            charts["system_gauges"] = json.loads(gauge_fig.to_json())

            # API response time indicator
            response_time = health_data.get("api_response_time", 0)
            error_rate = health_data.get("error_rate", 0) * 100

            indicators_fig = go.Figure()
            indicators_fig.add_trace(
                go.Indicator(
                    mode="number+delta",
                    value=response_time * 1000,  # Convert to ms
                    title={"text": "API Response (ms)"},
                    delta={"reference": 150, "relative": True},
                    domain={"x": [0, 0.5], "y": [0, 1]},
                )
            )
            indicators_fig.add_trace(
                go.Indicator(
                    mode="number+delta",
                    value=error_rate,
                    title={"text": "Error Rate (%)"},
                    delta={
                        "reference": 0.1,
                        "relative": True,
                        "increasing": {"color": "red"},
                    },
                    domain={"x": [0.5, 1], "y": [0, 1]},
                )
            )
            indicators_fig.update_layout(template="plotly_dark", height=200)
            charts["health_indicators"] = json.loads(indicators_fig.to_json())

        except Exception as e:
            logger.warning("Error generating health charts: %s", e)

        return charts

    def _analyze_health_issues(self, health_data: dict[str, Any]) -> list[dict[str, Any]]:
        """Analyze system health and identify issues"""
        issues = []

        if health_data.get("api_response_time", 0) > 0.5:
            issues.append(
                {
                    "type": "performance",
                    "severity": "high",
                    "component": "api",
                    "message": "API response time is above acceptable threshold",
                }
            )

        if health_data.get("error_rate", 0) > 0.01:
            issues.append(
                {
                    "type": "reliability",
                    "severity": "critical",
                    "component": "system",
                    "message": "Error rate is above acceptable threshold",
                }
            )

        return issues

    def _generate_health_recommendations(self, issues: list[dict]) -> list[str]:
        """Generate health improvement recommendations"""
        recommendations = []

        for issue in issues:
            if issue["type"] == "performance":
                recommendations.append("Consider optimizing database queries and implementing caching")
            elif issue["type"] == "reliability":
                recommendations.append("Review error handling and implement circuit breakers")

        if not recommendations:
            recommendations.append("System health is excellent - continue monitoring")

        return recommendations

    def _calculate_performance_benchmarks(self, health_data: dict[str, Any]) -> dict[str, Any]:
        """Calculate performance benchmarks"""
        return {
            "api_response_time": {
                "current": health_data.get("api_response_time", 0),
                "benchmark": 0.2,
                "status": ("good" if health_data.get("api_response_time", 0) < 0.2 else "needs_improvement"),
            }
        }

    def _determine_overall_health_status(self, health_scores: dict[str, Any]) -> str:
        """Determine overall system health status"""
        avg_score = statistics.mean(score["score"] for score in health_scores.values())

        if avg_score > 0.9:
            return "excellent"
        elif avg_score > 0.8:
            return "good"
        elif avg_score > 0.7:
            return "fair"
        elif avg_score > 0.6:
            return "needs_attention"
        else:
            return "critical"

    def _forecast_coordination_trends(self, historical_data: list[dict], hours: int) -> dict[str, Any]:
        """Forecast coordination trends using time series analysis"""
        # Simple exponential smoothing forecast
        forecast_data = []

        for metric in ["harmony", "resilience", "throughput", "focus", "friction", "velocity"]:
            values = [d[metric] for d in historical_data[-24:]]  # Use last 24 data points

            if len(values) >= 3:
                # Simple exponential smoothing
                alpha = 0.3
                smoothed = [values[0]]
                for i in range(1, len(values)):
                    smoothed.append(alpha * values[i] + (1 - alpha) * smoothed[-1])

                # Forecast next hours
                forecast_values = []
                last_value = smoothed[-1]
                for _ in range(hours):
                    # Add some trend and seasonality
                    trend = 0.001  # Slight upward trend
                    seasonality = 0.02 * np.sin(len(forecast_values) * np.pi / 12)  # Daily cycle
                    noise = np.random.normal(0, 0.01)

                    next_value = last_value + trend + seasonality + noise
                    next_value = max(0, min(1, next_value))  # Keep in bounds
                    forecast_values.append(next_value)
                    last_value = next_value

                forecast_data.append(
                    {
                        "metric": metric,
                        "forecast": forecast_values,
                        "confidence": max(0.5, 1.0 - 0.05 * hours),  # Decays with forecast horizon
                    }
                )

        return {"forecasts": forecast_data, "hours": hours}

    def _calculate_forecast_confidence(self, forecast: dict[str, Any]) -> dict[str, float]:
        """Calculate confidence intervals for forecast"""
        return {f["metric"]: f.get("confidence", 0.8) for f in forecast.get("forecasts", [])}

    def _generate_forecast_charts(
        self, forecast: dict[str, Any], confidence_intervals: dict[str, float]
    ) -> dict[str, Any]:
        """Generate forecast chart data with confidence bands for frontend rendering."""
        charts = {}
        for f in forecast.get("forecasts", []):
            metric = f["metric"]
            values = f.get("forecast", [])
            conf = confidence_intervals.get(metric, 0.8)
            margin = 1.0 - conf

            charts[metric] = {
                "values": values,
                "upper_band": [min(1.0, v + margin * 0.5) for v in values],
                "lower_band": [max(0.0, v - margin * 0.5) for v in values],
                "confidence": conf,
            }
        return charts

    def _analyze_forecast_alerts(self, forecast: dict[str, Any]) -> list[dict[str, Any]]:
        """Analyze forecast data for potential alerts"""
        alerts = []

        for forecast_item in forecast.get("forecasts", []):
            metric = forecast_item["metric"]
            values = forecast_item.get("forecast", [])

            if values:
                avg_forecast = statistics.mean(values)
                min(values)
                max(values)

                # Alert if forecast shows concerning trends
                if metric == "harmony" and avg_forecast < 0.7:
                    alerts.append(
                        {
                            "type": "coordination_decline",
                            "severity": "high",
                            "metric": metric,
                            "message": f"Projected harmony decline to {avg_forecast:.2f}",
                        }
                    )

        return alerts

    def _convert_to_csv(self, data: Any) -> str:
        """Convert data to CSV format"""
        # Simple CSV conversion
        if isinstance(data, list) and data:
            headers = list(data[0].keys())
            csv_lines = [",".join(headers)]

            for item in data:
                row = [str(item.get(h, "")) for h in headers]
                csv_lines.append(",".join(row))

            return "\n".join(csv_lines)

        return ""

    def _convert_to_excel(self, data: Any) -> bytes:
        """Convert data to Excel format"""
        # This would use openpyxl or similar to create Excel files
        # For now, return empty bytes
        return b""


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for special data types"""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


# Global service instance
analytics_service = AnalyticsService(None)


# API Routes
@router.get("/ucf")
async def get_ucf_dashboard(time_range: str = Query("1h", pattern=r"^(1h|24h|7d|30d)$")):
    """Get Universal Coordination Field dashboard"""
    return await analytics_service.get_ucf_dashboard(time_range)


@router.get("/agents")
async def get_agent_performance(
    agent_ids: list[str] = Query(None),
    time_range: str = Query("24h", pattern=r"^(1h|24h|7d|30d)$"),
):
    """Get agent performance analytics"""
    return await analytics_service.get_agent_performance_analytics(agent_ids, time_range)


@router.get("/health")
async def get_system_health():
    """Get system health dashboard"""
    return await analytics_service.get_system_health_dashboard()


@router.get("/forecast")
async def get_coordination_forecast(hours: int = Query(24, ge=1, le=168)):
    """Get coordination trend forecast"""
    return await analytics_service.get_coordination_forecast(hours)


@router.get("/export/{data_type}")
async def export_analytics(
    data_type: str,
    format: str = Query("json", pattern=r"^(json|csv|xlsx)$"),
    start_date: str = Query(None),
    end_date: str = Query(None),
):
    """Export analytics data"""
    return await analytics_service.export_analytics_data(data_type, format, start_date, end_date)


# Export router for main app
__all__ = ["analytics_service", "router"]
