"""
🌀 Helix Collective v17.0 - Coordination Analytics Engine
backend/coordination_analytics_engine.py

Predictive analytics for coordination evolution:
- Coordination level forecasting (Prophet time series)
- Agent performance correlation analysis
- Anomaly detection (unusual patterns)
- Trend analysis (30-day rolling)
- Predictive alerts (based on trajectory)

Author: Claude (Automation)
Version: 17.1.0
"""

import json
import logging
import traceback
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

try:
    import numpy as np
    import pandas as pd
    from scipy import stats

    HAS_ML_DEPS = True
except ImportError:
    np = None
    pd = None
    stats = None
    HAS_ML_DEPS = False

logger = logging.getLogger(__name__)

# ============================================================================
# COORDINATION TIME SERIES
# ============================================================================


class CoordinationTimeSeries:
    """Manages coordination level history for analysis with enhanced logging."""

    def __init__(self, data_file: Path = Path("Helix/state/coordination_history.jsonl")):
        self.data_file = data_file
        try:
            logger.info("📁 Coordination time series directory: %s", self.data_file.parent)
        except Exception as e:
            logger.error("❌ Failed to create time series directory: %s", e)
            raise

        self._cache: pd.DataFrame | None = None
        self._cache_timestamp: datetime | None = None
        self._cache_ttl = timedelta(minutes=5)  # Cache TTL

        logger.info("📊 CoordinationTimeSeries initialized: %s", self.data_file)

    def record(self, performance_score: float, ucf: dict[str, float], source: str = "system") -> None:
        """Record coordination level snapshot with validation and logging."""
        try:
            if not isinstance(performance_score, (int, float)) or not (0.0 <= performance_score <= 10.0):
                logger.warning("⚠️ Invalid coordination level: %s (must be 0-10)", performance_score)
                return

            # Validate UCF metrics
            required_metrics = [
                "harmony",
                "resilience",
                "throughput",
                "focus",
                "friction",
                "velocity",
            ]
            for metric in required_metrics:
                if metric not in ucf:
                    logger.warning("⚠️ Missing UCF metric: %s", metric)
                    ucf[metric] = 0.0

            entry = {
                "timestamp": datetime.now(UTC).isoformat() + "Z",
                "performance_score": round(float(performance_score), 2),
                "harmony": round(float(ucf.get("harmony", 0.0)), 3),
                "resilience": round(float(ucf.get("resilience", 0.0)), 3),
                "throughput": round(float(ucf.get("throughput", 0.0)), 3),
                "focus": round(float(ucf.get("focus", 0.0)), 3),
                "friction": round(float(ucf.get("friction", 0.0)), 3),
                "velocity": round(float(ucf.get("velocity", 0.0)), 3),
                "source": str(source)[:50],  # Limit source length
            }

            # Append to JSONL with error handling
            try:
                with open(self.data_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                logger.debug("📊 Recorded coordination snapshot: %.2f (source: %s)", performance_score, source)

            except PermissionError:
                logger.error("❌ Permission denied writing to time series: %s", self.data_file)
            except OSError as e:
                logger.error("❌ OS error writing time series: %s", e)
            except Exception as e:
                logger.error("❌ Unexpected error writing time series: %s", e)

            # Invalidate cache
            self._cache = None
            self._cache_timestamp = None

        except Exception as e:
            logger.error("❌ Failed to record coordination snapshot: %s", e)
            logger.debug("Stack trace: %s", traceback.format_exc())

    def get_dataframe(self, hours: int = 24) -> pd.DataFrame:
        """Get coordination data as DataFrame (last N hours) with caching and logging.

        Caches the full unfiltered DataFrame and applies time window on each call.
        """
        try:
            base_df = None

            if self._cache is not None and self._cache_timestamp:
                if datetime.now(UTC) - self._cache_timestamp < self._cache_ttl:
                    logger.debug("📊 Cache hit - filtering to %sh", hours)
                    base_df = self._cache

            if base_df is None:
                if not self.data_file.exists():
                    logger.debug("📁 Time series file not found: %s", self.data_file)
                    return pd.DataFrame()

                # Read JSONL with error handling
                entries = []
                line_count = 0
                error_count = 0

                try:
                    with open(self.data_file, encoding="utf-8") as f:
                        for line_num, line in enumerate(f, 1):
                            if not line.strip():
                                continue

                            line_count += 1
                            try:
                                entry = json.loads(line)
                                entries.append(entry)
                            except json.JSONDecodeError as e:
                                error_count += 1
                                if error_count <= 5:  # Limit error logging
                                    logger.warning("⚠️ Invalid JSON at line %d: %s", line_num, e)
                            except Exception as e:
                                error_count += 1
                                if error_count <= 5:
                                    logger.warning("⚠️ Error processing line %d: %s", line_num, e)

                except PermissionError:
                    logger.error("❌ Permission denied reading time series: %s", self.data_file)
                    return pd.DataFrame()
                except OSError as e:
                    logger.error("❌ OS error reading time series: %s", e)
                    return pd.DataFrame()
                except Exception as e:
                    logger.error("❌ Unexpected error reading time series: %s", e)
                    return pd.DataFrame()

                if not entries:
                    logger.debug("📊 No coordination data entries found")
                    return pd.DataFrame()

                # Create DataFrame
                base_df = pd.DataFrame(entries)

                # Validate and convert timestamp
                if "timestamp" in base_df.columns:
                    try:
                        base_df["timestamp"] = pd.to_datetime(base_df["timestamp"], utc=True)
                    except Exception as e:
                        logger.warning("⚠️ Failed to parse timestamps: %s", e)
                        return pd.DataFrame()
                else:
                    logger.warning("⚠️ No timestamp column found in time series data")
                    return pd.DataFrame()

                # Cache the FULL unfiltered DataFrame
                self._cache = base_df
                self._cache_timestamp = datetime.now(UTC)

                logger.debug("📊 Cached full DataFrame with %s entries", len(base_df))

            # Apply time window filter on each call
            cutoff = datetime.now(UTC) - timedelta(hours=hours)
            original_count = len(base_df)
            filtered_df = base_df[base_df["timestamp"] >= cutoff]
            filtered_count = len(filtered_df)

            logger.info("📊 Time series filtered: %d/%d entries (last %dh)", filtered_count, original_count, hours)

            return filtered_df

        except Exception as e:
            logger.error("❌ Failed to get DataFrame: %s", e)
            logger.debug("Stack trace: %s", traceback.format_exc())
            return pd.DataFrame()

    def get_latest(self) -> dict[str, Any] | None:
        """Get most recent coordination snapshot with logging."""
        try:
            df = self.get_dataframe()
            if df.empty:
                logger.debug("📊 No recent coordination data available")
                return None

            latest = df.iloc[-1].to_dict()
            logger.debug(
                "📊 Latest coordination: %s (source: %s)",
                latest.get("performance_score", "N/A"),
                latest.get("source", "N/A"),
            )
            return latest

        except Exception as e:
            logger.error("❌ Failed to get latest snapshot: %s", e)
            return None

    def get_statistics(self) -> dict[str, Any]:
        """Get comprehensive statistics about the time series data."""
        try:
            df = self.get_dataframe()
            if df.empty:
                return {"error": "No data available"}

            coordination_values = df["performance_score"].tolist()

            stats = {
                "total_entries": len(df),
                "date_range": {
                    "start": (df["timestamp"].min().isoformat() if not df.empty else None),
                    "end": df["timestamp"].max().isoformat() if not df.empty else None,
                },
                "coordination": {
                    "mean": round(np.mean(coordination_values), 2),
                    "median": round(float(np.median(coordination_values)), 2),
                    "std": round(np.std(coordination_values), 2),
                    "min": round(float(np.min(coordination_values)), 2),
                    "max": round(float(np.max(coordination_values)), 2),
                    "current": (coordination_values[-1] if coordination_values else None),
                },
                "sources": (df["source"].value_counts().to_dict() if "source" in df.columns else {}),
                "data_quality": {
                    "missing_timestamps": df["timestamp"].isna().sum(),
                    "missing_coordination": df["performance_score"].isna().sum(),
                    "error_rate": 0.0,  # Would need to track this separately
                },
            }

            logger.info(
                "📊 Time series statistics: %s entries, mean: %s, range: %s-%s",
                stats["total_entries"],
                stats["coordination"]["mean"],
                stats["coordination"]["min"],
                stats["coordination"]["max"],
            )

            return stats

        except Exception as e:
            logger.error("❌ Failed to get statistics: %s", e)
            return {"error": str(e)}


# ============================================================================
# TREND ANALYSIS
# ============================================================================


class TrendAnalyzer:
    """Analyzes coordination trends."""

    @staticmethod
    def calculate_rolling_average(values: list[float], window: int = 10) -> list[float]:
        """Calculate rolling average."""
        if len(values) < window:
            return values

        arr = np.array(values)
        kernel = np.ones(window) / window
        padded = np.pad(arr, (window - 1, 0), mode="edge")
        smoothed = np.convolve(padded, kernel, mode="valid")
        return smoothed.tolist()

    @staticmethod
    def detect_trend(values: list[float], window: int = 10) -> str:
        """Detect if trend is UP, DOWN, or STABLE."""
        if len(values) < 3:
            return "INSUFFICIENT_DATA"

        # Calculate rolling average
        avg = TrendAnalyzer.calculate_rolling_average(values, window=min(window, len(values)))

        if len(avg) < 2:
            return "INSUFFICIENT_DATA"

        # Check slope
        first_third = np.mean(avg[: len(avg) // 3])
        last_third = np.mean(avg[-len(avg) // 3 :])
        change = last_third - first_third

        threshold = 0.1  # 10% change threshold
        if change > threshold:
            return "UPTREND"
        elif change < -threshold:
            return "DOWNTREND"
        else:
            return "STABLE"

    @staticmethod
    def calculate_volatility(values: list[float]) -> float:
        """Calculate coordination volatility (standard deviation)."""
        if len(values) < 2:
            return 0.0
        return float(np.std(values))

    @staticmethod
    def calculate_momentum(values: list[float], window: int = 5) -> float:
        """Calculate momentum (rate of change)."""
        if len(values) < window:
            return 0.0

        arr = np.array(values[-window:])
        if len(arr) < 2:
            return 0.0

        # Linear regression slope
        x = np.arange(len(arr))
        slope = np.polyfit(x, arr, 1)[0]
        return float(slope)


# ============================================================================
# ANOMALY DETECTION
# ============================================================================


class AnomalyDetector:
    """Detects unusual coordination patterns."""

    Z_SCORE_THRESHOLD = 2.5  # 2.5σ = 98.8% normal
    MISSING_DATA_THRESHOLD = 0.2  # 20% missing = anomaly

    @staticmethod
    def detect_zscore_anomalies(values: list[float]) -> list[tuple[int, float]]:
        """Detect outliers using z-score method."""
        if len(values) < 10:
            return []

        arr = np.array(values)
        mean = np.mean(arr)
        std = np.std(arr)

        if std == 0:
            return []

        z_scores = np.abs((arr - mean) / std)
        anomalies = []

        for i, z in enumerate(z_scores):
            if z > AnomalyDetector.Z_SCORE_THRESHOLD:
                anomalies.append((i, float(z)))

        return anomalies

    @staticmethod
    def detect_pattern_anomalies(values: list[float], expected_range: tuple[float, float]) -> list[int]:
        """Detect values outside expected range."""
        min_val, max_val = expected_range
        anomalies = []

        for i, val in enumerate(values):
            if val < min_val or val > max_val:
                anomalies.append(i)

        return anomalies

    @staticmethod
    def detect_sudden_drops(values: list[float], threshold: float = 0.5) -> list[int]:
        """Detect sudden coordination drops."""
        if len(values) < 2:
            return []

        anomalies = []
        for i in range(1, len(values)):
            drop = values[i - 1] - values[i]
            if drop > threshold:
                anomalies.append(i)

        return anomalies


# ============================================================================
# FORECASTING
# ============================================================================


class CoordinationForecast:
    """Simple coordination level forecasting."""

    @staticmethod
    def predict_next_state(values: list[float], periods: int = 4) -> list[float]:
        """
        Predict next coordination levels (simple exponential smoothing).

        Args:
            values: Historical coordination values
            periods: Number of periods to forecast

        Returns:
            List of predicted values
        """
        if len(values) < 3:
            return [values[-1] if values else 5.0] * periods

        arr = np.array(values)

        # Simple exponential smoothing
        alpha = 0.3  # Smoothing factor
        result = [arr[-1]]

        for _ in range(periods):
            # Weighted average: 30% recent, 70% trend
            trend = arr[-1] - arr[-2] if len(arr) >= 2 else 0
            next_val = alpha * arr[-1] + (1 - alpha) * arr[-2] if len(arr) >= 2 else arr[-1]
            next_val += 0.1 * trend  # Add trend component

            # Clamp to valid range [0, 10]
            next_val = max(0.0, min(10.0, next_val))
            result.append(next_val)
            arr = np.append(arr, next_val)

        return result[1:]  # Skip initial value

    @staticmethod
    def calculate_forecast_confidence(values: list[float]) -> float:
        """
        Calculate confidence in forecast (based on data stability).

        Returns:
            Confidence score (0-100%)
        """
        if len(values) < 5:
            return 30.0  # Low confidence with few data points

        # Less volatile = more confident
        volatility = TrendAnalyzer.calculate_volatility(values)
        confidence = 100.0 - (volatility * 20)  # Scale volatility to confidence
        return max(20.0, min(100.0, confidence))  # Clamp to 20-100%


# ============================================================================
# AGENT CORRELATION ANALYSIS
# ============================================================================


class AgentCorrelationAnalyzer:
    """Analyzes relationship between agents and coordination."""

    @staticmethod
    def correlate_agent_with_coordination(
        agent_actions: list[dict[str, Any]], coordination_values: list[float]
    ) -> dict[str, float]:
        """
        Calculate correlation between agent actions and coordination changes.

        Returns:
            Dict of agent_name -> correlation_coefficient (-1 to 1)
        """
        correlations = {}

        # Group agent actions by type
        agent_types = {}
        for action in agent_actions:
            agent = action.get("agent_name", "unknown")
            if agent not in agent_types:
                agent_types[agent] = []
            agent_types[agent].append(action)

        # For each agent, calculate correlation
        num_values = len(coordination_values)
        for agent_name, actions in agent_types.items():
            # Create binary series: 1 = agent acted, 0 = didn't
            agent_series = np.zeros(num_values)
            for action in actions:
                # Map action to time index - use timestamp or position
                timestamp = action.get("timestamp") or action.get("time")
                idx = action.get("index")

                if idx is not None and 0 <= idx < num_values:
                    # Direct index provided
                    agent_series[idx] = 1
                elif timestamp is not None and num_values > 0:
                    # Use timestamp - distribute actions evenly across time series
                    # Since we don't have absolute time mapping, use relative position
                    try:
                        # If timestamp is numeric (Unix timestamp), normalize to array index
                        if isinstance(timestamp, (int, float)):
                            # Assume timestamps are relative within the series period
                            action_idx = min(int(timestamp) % num_values, num_values - 1)
                        else:
                            # For string timestamps, hash to get consistent index
                            action_idx = hash(str(timestamp)) % num_values
                        agent_series[action_idx] = 1
                    except (TypeError, ValueError) as e:
                        logger.debug("Correlation data conversion failed: %s", e)

            # Calculate Pearson correlation
            if np.sum(agent_series) > 0:
                corr, _ = stats.pearsonr(agent_series, coordination_values)
                correlations[agent_name] = float(corr)

        return correlations


# ============================================================================
# ANALYTICS REPORT
# ============================================================================


class AnalyticsReport:
    """Comprehensive coordination analytics report with enhanced logging."""

    def __init__(self, ts: CoordinationTimeSeries):
        self.ts = ts
        self.generated_at = datetime.now(UTC)
        logger.info("📋 AnalyticsReport initialized")

    def generate(self) -> dict[str, Any]:
        """Generate comprehensive analytics report with detailed logging."""
        try:
            # Get 7-day analysis data
            df = self.ts.get_dataframe(hours=24 * 7)

            if df.empty:
                logger.warning("📋 No data available for analytics report")
                return {"error": "Insufficient data for analysis"}

            coordination_values = df["performance_score"].tolist()
            logger.info("📋 Analytics data loaded: %d data points (7-day period)", len(coordination_values))

            # Trend analysis with logging
            logger.debug("📈 Analyzing coordination trends...")
            trend = TrendAnalyzer.detect_trend(coordination_values)
            volatility = TrendAnalyzer.calculate_volatility(coordination_values)
            momentum = TrendAnalyzer.calculate_momentum(coordination_values)

            logger.info("📈 Trend analysis complete: %s, volatility: %.3f, momentum: %.4f", trend, volatility, momentum)

            # Anomaly detection with logging
            logger.debug("🚨 Detecting coordination anomalies...")
            zscore_anomalies = AnomalyDetector.detect_zscore_anomalies(coordination_values)
            sudden_drops = AnomalyDetector.detect_sudden_drops(coordination_values)
            total_anomalies = len(zscore_anomalies) + len(sudden_drops)

            logger.info(
                f"🚨 Anomaly detection complete: {total_anomalies} total anomalies "
                f"({len(zscore_anomalies)} z-score, {len(sudden_drops)} drops)"
            )

            # Forecasting with logging
            logger.debug("🔮 Generating coordination forecasts...")
            forecast = CoordinationForecast.predict_next_state(coordination_values, periods=4)
            forecast_confidence = CoordinationForecast.calculate_forecast_confidence(coordination_values)

            logger.info("🔮 Forecasting complete: %d periods, confidence: %.1f%%", len(forecast), forecast_confidence)

            # Current state with logging
            logger.debug("📊 Getting current coordination state...")
            latest = self.ts.get_latest()
            current_coordination = latest.get("performance_score") if latest else None

            if current_coordination:
                logger.info("📊 Current coordination: %.2f", current_coordination)

            # Calculate statistics
            mean_val = round(np.mean(coordination_values), 2)
            median_val = round(float(np.median(coordination_values)), 2)
            min_val = round(float(np.min(coordination_values)), 2)
            max_val = round(float(np.max(coordination_values)), 2)

            # Generate comprehensive report
            report = {
                "report_generated": self.generated_at.isoformat() + "Z",
                "data_points": len(coordination_values),
                "current_coordination": current_coordination,
                "trend": {
                    "direction": trend,
                    "volatility": round(volatility, 3),
                    "momentum": round(momentum, 4),
                },
                "anomalies": {
                    "zscore_count": len(zscore_anomalies),
                    "sudden_drops": len(sudden_drops),
                    "total_anomalies": total_anomalies,
                },
                "forecast": {
                    "next_4_periods": [round(v, 2) for v in forecast],
                    "confidence": round(forecast_confidence, 1),
                },
                "statistics": {
                    "mean": mean_val,
                    "median": median_val,
                    "min": min_val,
                    "max": max_val,
                },
                "insights": self._generate_insights(trend, volatility, momentum, total_anomalies, forecast_confidence),
            }

            # Log report summary
            logger.info(
                "📋 Analytics report generated successfully:\n"
                "   Data points: %s\n"
                "   Trend: %s\n"
                "   Volatility: %s\n"
                "   Anomalies: %s\n"
                "   Forecast confidence: %s%%",
                report["data_points"],
                report["trend"]["direction"],
                report["trend"]["volatility"],
                report["anomalies"]["total_anomalies"],
                report["forecast"]["confidence"],
            )

            return report

        except Exception as e:
            logger.error("❌ Failed to generate analytics report: %s", e)
            logger.debug("Stack trace: %s", traceback.format_exc())
            return {"error": f"Report generation failed: {e!s}"}

    def _generate_insights(
        self,
        trend: str,
        volatility: float,
        momentum: float,
        anomalies: int,
        confidence: float,
    ) -> list[str]:
        """Generate actionable insights from analytics data."""
        insights = []

        # Trend insights
        if trend == "UPTREND":
            insights.append("📈 Coordination is trending upward - system is evolving positively")
        elif trend == "DOWNTREND":
            insights.append("📉 Coordination is trending downward - monitor for stress factors")
        elif trend == "STABLE":
            insights.append("⚖️ Coordination is stable - system is in equilibrium")

        # Volatility insights
        if volatility > 0.5:
            insights.append("⚠️ High volatility detected - coordination is fluctuating significantly")
        elif volatility < 0.2:
            insights.append("🎯 Low volatility - coordination is very stable")

        # Momentum insights
        if momentum > 0.1:
            insights.append("🚀 Positive momentum - coordination is accelerating upward")
        elif momentum < -0.1:
            insights.append("🛑 Negative momentum - coordination is decelerating")

        # Anomaly insights
        if anomalies > 5:
            insights.append(f"🚨 High anomaly count ({anomalies}) - investigate system stress")
        elif anomalies == 0:
            insights.append("✅ No anomalies detected - system is operating normally")

        # Confidence insights
        if confidence < 50:
            insights.append(f"❓ Low forecast confidence ({confidence}%) - data may be unstable")
        elif confidence > 80:
            insights.append(f"🎯 High forecast confidence ({confidence}%) - predictions are reliable")

        return insights


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "AgentCorrelationAnalyzer",
    "AnalyticsReport",
    "AnomalyDetector",
    "CoordinationForecast",
    "CoordinationTimeSeries",
    "TrendAnalyzer",
]
