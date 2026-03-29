"""
Helix Unified Coordination Module

This module provides coordination-related utilities including:
- UCF (Universal Coordination Field) protocol
- System coordination integration
- Affective intelligence
- Kael coordination core
- Coordination analytics and visualization
"""

import logging

logger = logging.getLogger(__name__)

# UCF Protocol
try:
    from .ucf_protocol import UCFMetrics, UCFProtocol
except ImportError as e:
    logger.debug("UCF Protocol not available: %s", e)

# UCF State
try:
    from .ucf_state_loader import UCFStateLoader
except ImportError as e:
    logger.debug("UCF State Loader not available: %s", e)

# UCF Tracker
try:
    from .ucf_tracker import UCFTracker
except ImportError as e:
    logger.debug("UCF Tracker not available: %s", e)

# UCF Framework
try:
    from .ucf_coordination_framework import UCFCoordinationFramework
except ImportError as e:
    logger.debug("UCF Coordination Framework not available: %s", e)

# System Core
try:
    from .system_core import SystemAgentState
except ImportError as e:
    logger.debug("System Coordination Core not available: %s", e)

# Kael Core
try:
    from .kael_core import KaelCoreIntegration
except ImportError as e:
    logger.debug("Kael Core not available: %s", e)

# Affective Intelligence
try:
    from .affective_intelligence import AffectiveIntelligence
except ImportError as e:
    logger.debug("Affective Intelligence not available: %s", e)

# Analytics
try:
    from .performance_analytics import PerformanceAnalytics
except ImportError as e:
    logger.debug("Coordination Analytics not available: %s", e)

__all__ = [
    "AffectiveIntelligence",
    "KaelCoreIntegration",
    "PerformanceAnalytics",
    "SystemAgentState",
    "UCFCoordinationFramework",
    "UCFMetrics",
    "UCFProtocol",
    "UCFStateLoader",
    "UCFTracker",
]
