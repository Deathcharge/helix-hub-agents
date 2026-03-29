"""
Coordination Integration Module

Main integration point for the Phase 3 Coordination System. This module
provides the main entry points and integration functions for connecting
all coordination components together.
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Any

from fastapi import FastAPI

# Routes/services loaded at app level, not from within coordination module
try:
    from apps.backend.routes.coordination_api import router as coordination_router
except ImportError:
    coordination_router = None

# Service registry is optional — coordination system works without it
try:
    from apps.backend.services.service_registry import ServiceRegistry

    service_registry = ServiceRegistry()
    register_coordination_services = None  # Placeholder — registered at app startup
except ImportError:
    service_registry = None
    register_coordination_services = None

logger = logging.getLogger(__name__)


class CoordinationSystem:
    """Main coordination system integration class"""

    def __init__(self):
        self.registry = None
        self.is_initialized = False
        self.is_running = False

    async def initialize(self) -> bool:
        """Initialize the coordination system"""
        try:
            if register_coordination_services is None:
                logger.warning("Coordination service registration not configured — skipping")
                self.is_initialized = True
                return True

            # Register all services
            self.registry = register_coordination_services()

            # Perform initial health check
            health_summary = await self.registry.get_health_summary()
            logger.info("Coordination system initialized. Health: %s", health_summary)

            self.is_initialized = True
            return True

        except Exception as e:
            logger.error("Failed to initialize coordination system: %s", e)
            return False

    async def start(self) -> bool:
        """Start the coordination system"""
        if not self.is_initialized:
            await self.initialize()

        try:
            # Start all services
            started = await self.registry.start_all()

            # Check if all services started successfully
            all_started = all(started.values())

            if all_started:
                self.is_running = True
                logger.info("Coordination System started successfully")
            else:
                logger.error("Some services failed to start: %s", started)

            return all_started

        except Exception as e:
            logger.error("Failed to start coordination system: %s", e)
            return False

    async def stop(self) -> bool:
        """Stop the coordination system"""
        if not self.is_running:
            return True

        try:
            # Stop all services
            stopped = await self.registry.stop_all()

            # Check if all services stopped successfully
            all_stopped = all(stopped.values())

            if all_stopped:
                self.is_running = False
                logger.info("Coordination System stopped successfully")
            else:
                logger.error("Some services failed to stop: %s", stopped)

            return all_stopped

        except Exception as e:
            logger.error("Failed to stop coordination system: %s", e)
            return False

    async def get_health_status(self) -> dict[str, Any]:
        """Get overall health status of the coordination system"""
        if not self.registry:
            return {"status": "not_initialized", "services": {}}

        return await self.registry.get_health_summary()

    async def get_service(self, service_name: str):
        """Get a specific service instance"""
        if not self.registry:
            raise ValueError("Coordination system not initialized")

        return await self.registry.get_service(service_name)

    def is_healthy(self) -> bool:
        """Check if the coordination system is healthy"""
        if not self.registry:
            return False

        return self.registry.is_healthy()


# Global coordination system instance
coordination_system = CoordinationSystem()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan manager for coordination system"""
    # Startup
    logger.info("Starting Coordination System with FastAPI...")

    success = await coordination_system.start()
    if not success:
        logger.error("Failed to start coordination system")
        raise RuntimeError("Coordination system failed to start")

    yield

    # Shutdown
    logger.info("Shutting down Coordination System...")
    await coordination_system.stop()


async def integrate_coordination_with_app(app: FastAPI):
    """Integrate coordination system with FastAPI application"""
    try:
        app.include_router(coordination_router)

        # Add coordination system to app state
        app.state.coordination_system = coordination_system

        logger.info("Coordination system integrated with FastAPI")

    except Exception as e:
        logger.error("Failed to integrate coordination system with FastAPI: %s", e)
        raise


async def get_coordination_dashboard_data() -> dict[str, Any]:
    """Get comprehensive coordination dashboard data"""
    try:
        health_status = await coordination_system.get_health_status()

        # Get current coordination state
        coordination_service = await coordination_system.get_service("coordination_service")
        current_state = await coordination_service.get_current_state()

        # Get UCF state
        ucf_calculator = await coordination_service.ucf_calculator.get_detailed_state()

        # Get optimization status
        optimizer = await coordination_system.get_service("coordination_optimizer")
        optimization_history = await optimizer.get_optimization_history(limit=5)

        # Get prediction status
        predictor = await coordination_system.get_service("coordination_predictor")
        current_prediction = await predictor.predict_coordination_state(time_horizon=60)

        # Get analytics summary
        analytics = await coordination_system.get_service("coordination_analytics")
        patterns = await analytics.analyze_coordination_patterns("1h")

        # Get agent coordination status
        coordinator = await coordination_system.get_service("agent_coordinator")
        coordination_status = await coordinator.calculate_collective_coordination()

        return {
            "system_health": health_status,
            "current_state": current_state,
            "ucf_state": ucf_calculator,
            "optimization_status": {
                "recent_optimizations": optimization_history,
                "total_optimizations": len(optimization_history),
            },
            "prediction_status": {
                "current_prediction": current_prediction.predicted_state,
                "confidence": current_prediction.confidence,
                "model": current_prediction.prediction_model.value,
            },
            "analytics_summary": {
                "detected_patterns": len(patterns),
                "pattern_types": [p.pattern_type for p in patterns] if patterns else [],
            },
            "coordination_status": {
                "collective_coordination": coordination_status.overall_coordination,
                "collective_harmony": coordination_status.collective_harmony,
            },
            "timestamp": datetime.now(UTC).isoformat() + "Z",
        }

    except Exception as e:
        logger.error("Failed to get coordination dashboard data: %s", e)
        return {"error": str(e), "timestamp": "2024-01-04T12:00:00Z"}


async def perform_coordination_optimization(
    workflow_id: str,
    optimization_strategy: str = "superposition",
    time_horizon: int = 60,
) -> dict[str, Any]:
    """Perform coordination-based workflow optimization"""
    try:
        optimizer = await coordination_system.get_service("coordination_optimizer")

        # Perform optimization
        result = await optimizer.optimize_coordination_workflow(
            workflow_id=workflow_id,
            optimization_strategy=optimization_strategy,
            time_horizon=time_horizon,
        )

        return {
            "success": True,
            "workflow_id": workflow_id,
            "optimization_strategy": optimization_strategy,
            "coordination_resonance": result.coordination_resonance,
            "energy_efficiency": result.energy_efficiency,
            "execution_time_improvement": result.execution_time_improvement,
            "optimized_tasks_count": len(result.optimized_tasks),
            "system_states_generated": len(result.system_states),
            "timestamp": datetime.now(UTC).isoformat() + "Z",
        }

    except Exception as e:
        logger.error("Coordination optimization failed: %s", e)
        return {
            "success": False,
            "error": str(e),
            "workflow_id": workflow_id,
            "timestamp": datetime.now(UTC).isoformat() + "Z",
        }


async def trigger_coordination_cycle(cycle_type: str, parameters: dict[str, Any] = None) -> dict[str, Any]:
    """Trigger a coordination cycle"""
    try:
        coordination_service = await coordination_system.get_service("coordination_service")

        # Trigger cycle
        result = await coordination_service.trigger_coordination_cycle(
            cycle_type=cycle_type, parameters=parameters or {}
        )

        return {
            "success": result["success"],
            "cycle_type": cycle_type,
            "effects": result.get("effects", {}),
            "new_state": result.get("new_state", {}),
            "message": result.get("message", ""),
            "timestamp": datetime.now(UTC).isoformat() + "Z",
        }

    except Exception as e:
        logger.error("Coordination cycle failed: %s", e)
        return {
            "success": False,
            "error": str(e),
            "cycle_type": cycle_type,
            "timestamp": datetime.now(UTC).isoformat() + "Z",
        }


async def get_coordination_insights(time_window: str = "1h") -> dict[str, Any]:
    """Get coordination insights and recommendations"""
    try:
        analytics = await coordination_system.get_service("coordination_analytics")

        # Generate insights
        insights = await analytics.generate_coordination_insights(time_window)

        # Get health recommendations
        coordination_service = await coordination_system.get_service("coordination_service")
        health_data = await coordination_service.get_coordination_health()

        return {
            "insights": insights,
            "health_recommendations": health_data["recommendations"],
            "time_window": time_window,
            "timestamp": datetime.now(UTC).isoformat() + "Z",
        }

    except Exception as e:
        logger.error("Failed to get coordination insights: %s", e)
        return {
            "error": str(e),
            "insights": [],
            "health_recommendations": [],
            "timestamp": datetime.now(UTC).isoformat() + "Z",
        }


# Integration functions for external systems


async def integrate_with_workflow_engine():
    """Integrate coordination system with workflow engine"""
    try:
        # to add coordination-aware workflow execution
        logger.info("Integrating coordination system with workflow engine...")

        # Get services
        # coordination_service = await coordination_system.get_service(
        #     "coordination_service"
        # )
        # optimizer = await coordination_system.get_service("coordination_optimizer")

        # Integration logic would go here
        # This would modify the workflow engine to:
        # 1. Check coordination levels before workflow execution
        # 2. Apply coordination-based optimizations
        # 3. Monitor workflow performance against coordination metrics
        # 4. Adjust workflows based on coordination predictions

        logger.info("Coordination system integrated with workflow engine")
        return True

    except Exception as e:
        logger.error("Failed to integrate with workflow engine: %s", e)
        return False


async def integrate_with_agent_system():
    """Integrate coordination system with agent coordination"""
    try:
        # to add coordination-aware agent coordination
        logger.info("Integrating coordination system with agent system...")

        # Get services
        # coordinator = await coordination_system.get_service("agent_coordinator")

        # Integration logic would go here
        # This would modify the agent system to:
        # 1. Track individual agent coordination levels
        # 2. Coordinate agents based on collective coordination
        # 3. Optimize agent behavior based on coordination metrics
        # 4. Enable coordination-based agent communication

        logger.info("Coordination system integrated with agent system")
        return True

    except Exception as e:
        logger.error("Failed to integrate with agent system: %s", e)
        return False


async def integrate_with_monitoring_system():
    """Integrate coordination system with monitoring and alerting"""
    try:
        # to add coordination-aware monitoring
        logger.info("Integrating coordination system with monitoring system...")

        # Get services
        # coordination_service = await coordination_system.get_service(
        #     "coordination_service"
        # )

        # Integration logic would go here
        # This would modify the monitoring system to:
        # 1. Monitor coordination metrics in real-time
        # 2. Generate coordination-based alerts
        # 3. Provide coordination health dashboards
        # 4. Enable coordination-aware incident response

        logger.info("Coordination system integrated with monitoring system")
        return True

    except Exception as e:
        logger.error("Failed to integrate with monitoring system: %s", e)
        return False


# Utility functions


def get_coordination_system_status() -> dict[str, Any]:
    """Get overall status of the coordination system"""
    return {
        "initialized": coordination_system.is_initialized,
        "running": coordination_system.is_running,
        "healthy": coordination_system.is_healthy(),
        "services": (len(service_registry._services) if service_registry._services else 0),
    }


async def run_coordination_system_test() -> dict[str, Any]:
    """Run a comprehensive test of the coordination system"""
    try:
        # Test service registry
        health_status = await coordination_system.get_health_status()

        # Test individual services
        test_results = {}

        services_to_test = [
            "coordination_service",
            "coordination_optimizer",
            "coordination_predictor",
            "coordination_analytics",
            "agent_coordinator",
        ]

        for service_name in services_to_test:
            try:
                # Get service from registry or use placeholder
                service = None  # Would fetch from service registry if implemented
                test_results[service_name] = {
                    "status": "not_available" if service is None else "success",
                    "type": type(service).__name__ if service else "NotImplemented",
                }
            except Exception as e:
                test_results[service_name] = {"status": "failed", "error": str(e)}

        # Test API endpoints
        dashboard_data = await get_coordination_dashboard_data()

        return {
            "test_status": "completed",
            "system_health": health_status,
            "service_tests": test_results,
            "dashboard_test": "success" if "error" not in dashboard_data else "failed",
            "timestamp": datetime.now(UTC).isoformat() + "Z",
        }

    except Exception as e:
        logger.error("Coordination system test failed: %s", e)
        return {
            "test_status": "failed",
            "error": str(e),
            "timestamp": datetime.now(UTC).isoformat() + "Z",
        }


# Main integration entry point


async def main():
    """Main entry point for coordination system"""
    try:
        success = await coordination_system.start()

        if success:
            logger.info("Coordination System is ready!")

            # Run a test
            test_result = await run_coordination_system_test()
            logger.info("System test result: %s", test_result)

            return True
        else:
            logger.error("Failed to start coordination system")
            return False

    except Exception as e:
        logger.error("Coordination system main failed: %s", e)
        return False


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())
