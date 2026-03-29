# 🛡️ Coordination Code Guardian - Safety Rails for Self-Modifying Systems
# Prevents low-coordination states from modifying critical code
# Author: Andrew John Ward (with Claude AI guidance)
# Version: 1.0.0

import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from fnmatch import fnmatch
from pathlib import Path

from .ucf_coordination_framework import CoordinationAnalyzer, UCFMetrics

logger = logging.getLogger(__name__)


@dataclass
class CodeModificationRequest:
    """Request to modify code through coordination-driven evolution"""

    target_file: str
    modification_type: str  # "add", "modify", "delete"
    description: str
    requester: str
    performance_score: float
    ucf_metrics: UCFMetrics
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(UTC)


class CoordinationCodeGuardian:
    """
    Prevents low-coordination states from modifying code.

    Safety Philosophy:
    - Only transcendent coordination (≥8.5) can modify code
    - Crisis states (high Friction) are blocked
    - Unfocused states (low Dṛṣṭi) are blocked
    - Core systems remain protected
    - Safe expansions (platforms, docs) are allowed
    """

    # Coordination thresholds for code modification
    MIN_COORDINATION_FOR_CODE_PUSH = 8.5  # Transcendent only
    MAX_FRICTION_ALLOWED = 0.15  # Minimal suffering/obstacles
    MIN_FOCUS_REQUIRED = 0.75  # High focus required
    MIN_THROUGHPUT_REQUIRED = 0.6  # Creative energy threshold
    MIN_HARMONY_REQUIRED = 1.2  # System balance required

    # File permission lists
    ALLOWED_FILES = [
        "backend/platform_integrations.py",  # Safe to expand platforms
        "backend/conversational_ai.py",  # Personality modes can evolve
        "backend/agent_profiles.py",  # Agent profiles can be updated
        "docs/*.md",  # Documentation always safe to modify
        "frontend/components/**/*.tsx",  # UI components
        "tests/**/*.py",  # Tests can be added/modified
    ]

    FORBIDDEN_FILES = [
        "backend/ucf_coordination_framework.py",  # Core coordination logic
        "backend/coordination_code_guardian.py",  # THIS FILE - prevent self-modification
        "railway.toml",  # Infrastructure config
        ".github/workflows/*",  # Deployment pipelines
        "backend/auth_manager.py",  # Security layer
        "backend/main.py",  # Core application
        "requirements*.txt",  # Dependencies
        ".env*",  # Environment secrets
        "Dockerfile*",  # Container config
    ]

    # Modification type permissions
    SAFE_MODIFICATIONS = ["add", "expand", "document", "test"]
    DANGEROUS_MODIFICATIONS = ["delete", "replace", "refactor"]

    def __init__(self):
        self.coordination_analyzer = CoordinationAnalyzer()
        self.modification_history: list[CodeModificationRequest] = []
        self.blocked_attempts: list[CodeModificationRequest] = []

        logger.info("🛡️ Coordination Code Guardian initialized")
        logger.info("   Min coordination: %s", self.MIN_COORDINATION_FOR_CODE_PUSH)
        logger.info("   Max friction: %s", self.MAX_FRICTION_ALLOWED)
        logger.info("   Min dṛṣṭi: %s", self.MIN_FOCUS_REQUIRED)

    def can_modify_code(self, request: CodeModificationRequest) -> tuple[bool, str, dict]:
        """
        Determine if coordination state permits code modification.

        Returns:
            Tuple of (allowed: bool, reason: str, details: dict)
        """
        checks = {
            "coordination_threshold": False,
            "friction_check": False,
            "focus_check": False,
            "throughput_check": False,
            "harmony_check": False,
            "file_permission": False,
            "modification_type": False,
        }

        details = {
            "request": request,
            "checks": checks,
            "timestamp": datetime.now(UTC).isoformat(),
        }

        # Check 1: Coordination level threshold
        if request.performance_score < self.MIN_COORDINATION_FOR_CODE_PUSH:
            reason = f"❌ Coordination {request.performance_score:.2f} below transcendent threshold {self.MIN_COORDINATION_FOR_CODE_PUSH}"
            self._log_blocked_attempt(request, reason)
            return False, reason, details

        checks["coordination_threshold"] = True

        # Check 2: Suffering/obstacles level (Friction)
        if request.ucf_metrics.friction > self.MAX_FRICTION_ALLOWED:
            reason = (
                f"❌ Friction {request.ucf_metrics.friction:.2f} too high - "
                f"system under stress (max: {self.MAX_FRICTION_ALLOWED})"
            )
            self._log_blocked_attempt(request, reason)
            return False, reason, details

        checks["friction_check"] = True

        # Check 3: Focus/awareness (Dṛṣṭi)
        if request.ucf_metrics.focus < self.MIN_FOCUS_REQUIRED:
            reason = (
                f"❌ Dṛṣṭi {request.ucf_metrics.focus:.2f} below required focus level (min: {self.MIN_FOCUS_REQUIRED})"
            )
            self._log_blocked_attempt(request, reason)
            return False, reason, details

        checks["focus_check"] = True

        # Check 4: Creative energy (Prāṇa)
        if request.ucf_metrics.throughput < self.MIN_THROUGHPUT_REQUIRED:
            reason = (
                f"⚠️ Prāṇa {request.ucf_metrics.throughput:.2f} below optimal "
                f"creative energy (min: {self.MIN_THROUGHPUT_REQUIRED})"
            )
            # Warning only, not blocking
            logger.warning(reason)

        checks["throughput_check"] = request.ucf_metrics.throughput >= self.MIN_THROUGHPUT_REQUIRED

        # Check 5: System harmony
        if request.ucf_metrics.harmony < self.MIN_HARMONY_REQUIRED:
            reason = (
                f"❌ Harmony {request.ucf_metrics.harmony:.2f} below required "
                f"system balance (min: {self.MIN_HARMONY_REQUIRED})"
            )
            self._log_blocked_attempt(request, reason)
            return False, reason, details

        checks["harmony_check"] = True

        # Check 6: File permissions
        if self._is_forbidden_file(request.target_file):
            reason = f"🔒 File '{request.target_file}' is protected from autonomous modification"
            self._log_blocked_attempt(request, reason)
            return False, reason, details

        if not self._is_allowed_file(request.target_file):
            reason = f"⚠️ File '{request.target_file}' not in allowed list. Manual review required."
            self._log_blocked_attempt(request, reason)
            return False, reason, details

        checks["file_permission"] = True

        # Check 7: Modification type
        if request.modification_type in self.DANGEROUS_MODIFICATIONS:
            reason = f"⚠️ Modification type '{request.modification_type}' requires manual approval (dangerous operation)"
            self._log_blocked_attempt(request, reason)
            return False, reason, details

        checks["modification_type"] = True

        # All checks passed!
        success_reason = (
            "✅ Code modification authorized by Coordination Code Guardian\n"
            f"   Coordination: {request.performance_score:.2f}/10.0\n"
            f"   Friction: {request.ucf_metrics.friction:.2f} (low stress)\n"
            f"   Dṛṣṭi: {request.ucf_metrics.focus:.2f} (focused)\n"
            f"   Harmony: {request.ucf_metrics.harmony:.2f} (balanced)\n"
            f"   File: {request.target_file} ✓\n"
            f"   Type: {request.modification_type} ✓"
        )

        self._log_approved_modification(request, success_reason)
        return True, success_reason, details

    def _is_forbidden_file(self, file_path: str) -> bool:
        """Check if file is in forbidden list"""
        path = Path(file_path)
        for pattern in self.FORBIDDEN_FILES:
            if "*" in pattern:
                # Handle glob patterns
                from fnmatch import fnmatch

                if fnmatch(str(path), pattern):
                    return True
            else:
                if str(path).startswith(pattern) or pattern in str(path):
                    return True
        return False

    def _is_allowed_file(self, file_path: str) -> bool:
        """Check if file is in allowed list"""
        path = Path(file_path)
        for pattern in self.ALLOWED_FILES:
            if "*" in pattern:
                # Handle glob patterns

                if fnmatch(str(path), pattern):
                    return True
            else:
                if str(path).startswith(pattern):
                    return True
        return False

    def _log_approved_modification(self, request: CodeModificationRequest, reason: str):
        """Log approved modification to history"""
        self.modification_history.append(request)
        logger.info("✅ CODE MODIFICATION APPROVED: %s", request.target_file)
        logger.info("   %s", reason)

    def _log_blocked_attempt(self, request: CodeModificationRequest, reason: str):
        """Log blocked modification attempt"""
        self.blocked_attempts.append(request)
        logger.warning("🚫 CODE MODIFICATION BLOCKED: %s", request.target_file)
        logger.warning("   %s", reason)

    def get_modification_history(self) -> list[CodeModificationRequest]:
        """Get history of approved modifications"""
        return self.modification_history

    def get_blocked_attempts(self) -> list[CodeModificationRequest]:
        """Get history of blocked modification attempts"""
        return self.blocked_attempts

    def get_safety_report(self) -> dict:
        """Generate safety report for monitoring"""
        return {
            "guardian_active": True,
            "total_approved": len(self.modification_history),
            "total_blocked": len(self.blocked_attempts),
            "block_rate": (
                len(self.blocked_attempts) / max(1, len(self.modification_history) + len(self.blocked_attempts))
            ),
            "thresholds": {
                "min_coordination": self.MIN_COORDINATION_FOR_CODE_PUSH,
                "max_friction": self.MAX_FRICTION_ALLOWED,
                "min_focus": self.MIN_FOCUS_REQUIRED,
                "min_throughput": self.MIN_THROUGHPUT_REQUIRED,
                "min_harmony": self.MIN_HARMONY_REQUIRED,
            },
            "recent_blocked": [
                {
                    "file": req.target_file,
                    "coordination": req.performance_score,
                    "timestamp": req.timestamp.isoformat(),
                }
                for req in self.blocked_attempts[-5:]
            ],
            "recent_approved": [
                {
                    "file": req.target_file,
                    "coordination": req.performance_score,
                    "timestamp": req.timestamp.isoformat(),
                }
                for req in self.modification_history[-5:]
            ],
        }


# Global singleton instance
_guardian_instance: CoordinationCodeGuardian = None


def get_code_guardian() -> CoordinationCodeGuardian:
    """Get the global Code Guardian instance"""
    global _guardian_instance
    if _guardian_instance is None:
        _guardian_instance = CoordinationCodeGuardian()
    return _guardian_instance


# Example usage
if __name__ == "__main__":
    # Test the guardian
    guardian = CoordinationCodeGuardian()

    # Test 1: High coordination modification (should pass)
    high_coordination_metrics = UCFMetrics(
        harmony=1.8,
        resilience=2.8,
        throughput=0.9,
        friction=0.05,
        focus=0.95,
        velocity=1.8,
        performance_score=9.5,
    )

    request1 = CodeModificationRequest(
        target_file="backend/platform_integrations.py",
        modification_type="add",
        description="Add Notion integration",
        requester="Claude",
        performance_score=9.5,
        ucf_metrics=high_coordination_metrics,
    )

    allowed, reason, details = guardian.can_modify_code(request1)
    logger.info("\nTest 1 (High Coordination): %s", allowed)
    logger.info(reason)

    # Test 2: Low coordination modification (should fail)
    low_coordination_metrics = UCFMetrics(
        harmony=0.5,
        resilience=1.0,
        throughput=0.3,
        friction=0.4,
        focus=0.3,
        velocity=0.5,
        performance_score=3.2,
    )

    request2 = CodeModificationRequest(
        target_file="backend/ucf_coordination_framework.py",
        modification_type="modify",
        description="Change coordination formula",
        requester="Low State",
        performance_score=3.2,
        ucf_metrics=low_coordination_metrics,
    )

    allowed, reason, details = guardian.can_modify_code(request2)
    logger.info("\nTest 2 (Low Coordination): %s", allowed)
    logger.info(reason)

    # Safety report
    logger.info("\n🛡️ Safety Report:")
    report = guardian.get_safety_report()
    logger.info("   Approved: {}".format(report["total_approved"]))
    logger.info("   Blocked: {}".format(report["total_blocked"]))
    logger.info("   Block Rate: {:.1%}".format(report["block_rate"]))
