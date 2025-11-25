"""
Audit logging configuration.

Manages configuration for the audit logging system including
storage location, rotation, and retention policies.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List
from platformdirs import user_data_dir


@dataclass
class AuditConfig:
    """
    Configuration for audit logging system.

    Attributes:
        audit_dir: Directory for storing audit logs
        log_file: Primary audit log file name
        max_file_size: Maximum size of a single log file in bytes (default: 100MB)
        max_files: Maximum number of rotated log files to keep (default: 10)
        retention_days: Default retention period in days (default: 365)
        enabled: Whether audit logging is enabled (default: True)
        include_pii: Whether to log PII (default: False for privacy)
        encrypt_logs: Whether to encrypt audit logs (default: False)
        syslog_enabled: Whether to send logs to syslog (default: False)
        syslog_host: Syslog server host
        syslog_port: Syslog server port
        alert_on_critical: Send alerts for critical events (default: True)
        alert_email: Email address for alerts
        compliance_mode: Enable strict compliance mode (default: False)
        allowed_event_types: Filter to only log specific event types (None = all)
    """

    # Storage configuration
    audit_dir: Path = field(default_factory=lambda: Path(user_data_dir("nuaa-cli", "NUAA")) / "audit")
    log_file: str = "audit.log"

    # Rotation configuration
    max_file_size: int = 100 * 1024 * 1024  # 100 MB
    max_files: int = 10
    retention_days: int = 365

    # Feature flags
    enabled: bool = True
    include_pii: bool = False
    encrypt_logs: bool = False
    syslog_enabled: bool = False

    # Syslog configuration
    syslog_host: Optional[str] = None
    syslog_port: int = 514

    # Alerting configuration
    alert_on_critical: bool = True
    alert_email: Optional[str] = None

    # Compliance
    compliance_mode: bool = False
    allowed_event_types: Optional[List[str]] = None

    def __post_init__(self):
        """Initialize configuration from environment variables."""
        # Override from environment variables
        if env_dir := os.getenv("NUAA_AUDIT_DIR"):
            self.audit_dir = Path(env_dir)

        if env_enabled := os.getenv("NUAA_AUDIT_ENABLED"):
            self.enabled = env_enabled.lower() in ("true", "1", "yes")

        if env_pii := os.getenv("NUAA_AUDIT_INCLUDE_PII"):
            self.include_pii = env_pii.lower() in ("true", "1", "yes")

        if env_compliance := os.getenv("NUAA_AUDIT_COMPLIANCE_MODE"):
            self.compliance_mode = env_compliance.lower() in ("true", "1", "yes")

        if env_max_size := os.getenv("NUAA_AUDIT_MAX_FILE_SIZE"):
            try:
                self.max_file_size = int(env_max_size)
            except ValueError:
                pass

        if env_retention := os.getenv("NUAA_AUDIT_RETENTION_DAYS"):
            try:
                self.retention_days = int(env_retention)
            except ValueError:
                pass

        if env_syslog := os.getenv("NUAA_AUDIT_SYSLOG_ENABLED"):
            self.syslog_enabled = env_syslog.lower() in ("true", "1", "yes")

        if env_syslog_host := os.getenv("NUAA_AUDIT_SYSLOG_HOST"):
            self.syslog_host = env_syslog_host

        if env_alert_email := os.getenv("NUAA_AUDIT_ALERT_EMAIL"):
            self.alert_email = env_alert_email

        # Ensure audit directory exists
        if self.enabled:
            self.audit_dir.mkdir(parents=True, exist_ok=True)

    @property
    def log_path(self) -> Path:
        """Get the full path to the audit log file."""
        return self.audit_dir / self.log_file

    def is_event_allowed(self, event_type: str) -> bool:
        """
        Check if an event type should be logged.

        Args:
            event_type: Event type to check

        Returns:
            True if event should be logged, False otherwise
        """
        if not self.enabled:
            return False

        if self.allowed_event_types is None:
            return True

        return event_type in self.allowed_event_types

    def get_retention_path(self) -> Path:
        """Get path for retention policy configuration."""
        return self.audit_dir / "retention_policy.json"

    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        return {
            "audit_dir": str(self.audit_dir),
            "log_file": self.log_file,
            "max_file_size": self.max_file_size,
            "max_files": self.max_files,
            "retention_days": self.retention_days,
            "enabled": self.enabled,
            "include_pii": self.include_pii,
            "encrypt_logs": self.encrypt_logs,
            "syslog_enabled": self.syslog_enabled,
            "syslog_host": self.syslog_host,
            "syslog_port": self.syslog_port,
            "alert_on_critical": self.alert_on_critical,
            "alert_email": self.alert_email,
            "compliance_mode": self.compliance_mode,
            "allowed_event_types": self.allowed_event_types,
        }


# Global configuration instance
_config: Optional[AuditConfig] = None


def get_config() -> AuditConfig:
    """
    Get the global audit configuration.

    Returns:
        AuditConfig instance
    """
    global _config
    if _config is None:
        _config = AuditConfig()
    return _config


def set_config(config: AuditConfig) -> None:
    """
    Set the global audit configuration.

    Args:
        config: AuditConfig instance to use
    """
    global _config
    _config = config


def reset_config() -> None:
    """Reset configuration to defaults."""
    global _config
    _config = None
