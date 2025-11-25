"""
Audit event types and structures.

Defines all auditable events in NUAA CLI for compliance tracking.
"""

from enum import Enum
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, Any, Dict
import uuid


class EventType(str, Enum):
    """Types of auditable events."""

    # Document operations
    DOCUMENT_CREATED = "document.created"
    DOCUMENT_READ = "document.read"
    DOCUMENT_UPDATED = "document.updated"
    DOCUMENT_DELETED = "document.deleted"
    DOCUMENT_EXPORTED = "document.exported"
    DOCUMENT_IMPORTED = "document.imported"
    DOCUMENT_VALIDATED = "document.validated"

    # Template operations
    TEMPLATE_ACCESSED = "template.accessed"
    TEMPLATE_MODIFIED = "template.modified"
    TEMPLATE_DOWNLOADED = "template.downloaded"

    # Configuration operations
    CONFIG_CHANGED = "config.changed"
    CONFIG_READ = "config.read"

    # User operations
    USER_LOGIN = "user.login"
    USER_LOGOUT = "user.logout"
    USER_ACTION = "user.action"

    # System operations
    SYSTEM_START = "system.start"
    SYSTEM_STOP = "system.stop"
    SYSTEM_ERROR = "system.error"

    # Agent operations
    AGENT_REGISTERED = "agent.registered"
    AGENT_INVOKED = "agent.invoked"
    AGENT_ERROR = "agent.error"

    # MCP operations
    MCP_TOOL_REGISTERED = "mcp.tool_registered"
    MCP_TOOL_INVOKED = "mcp.tool_invoked"

    # Data operations
    DATA_EXPORT = "data.export"
    DATA_IMPORT = "data.import"
    DATA_BACKUP = "data.backup"
    DATA_RESTORE = "data.restore"

    # Security events
    AUTH_SUCCESS = "auth.success"
    AUTH_FAILURE = "auth.failure"
    AUTH_DENIED = "auth.denied"
    PERMISSION_DENIED = "permission.denied"

    # Compliance events
    PII_ACCESSED = "compliance.pii_accessed"
    SENSITIVE_DATA_EXPORTED = "compliance.sensitive_exported"
    AUDIT_LOG_ACCESSED = "compliance.audit_accessed"


class Severity(str, Enum):
    """Severity levels for audit events."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class AuditEvent:
    """
    Represents a single auditable event.

    All events are immutable once created and contain comprehensive
    metadata for compliance and forensic analysis.
    """

    # Core fields
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    event_type: EventType = EventType.USER_ACTION
    severity: Severity = Severity.INFO

    # User/Actor information
    user_id: Optional[str] = None
    username: Optional[str] = None
    session_id: Optional[str] = None

    # Resource information
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    resource_path: Optional[str] = None

    # Action details
    action: Optional[str] = None
    description: Optional[str] = None
    status: str = "success"  # success, failure, error

    # Context
    metadata: Dict[str, Any] = field(default_factory=dict)

    # System information
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    process_id: Optional[int] = None

    # Compliance fields
    is_sensitive: bool = False
    contains_pii: bool = False
    retention_days: int = 365  # Default 1 year retention

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert event to dictionary for serialization.

        Returns:
            Dictionary representation of the event
        """
        data = asdict(self)
        # Convert datetime to ISO format
        data["timestamp"] = self.timestamp.isoformat()
        # Convert enums to strings
        data["event_type"] = self.event_type.value
        data["severity"] = self.severity.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuditEvent":
        """
        Create event from dictionary.

        Args:
            data: Dictionary containing event data

        Returns:
            AuditEvent instance
        """
        # Convert timestamp string to datetime
        if "timestamp" in data and isinstance(data["timestamp"], str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])

        # Convert enum strings to enums
        if "event_type" in data and isinstance(data["event_type"], str):
            data["event_type"] = EventType(data["event_type"])

        if "severity" in data and isinstance(data["severity"], str):
            data["severity"] = Severity(data["severity"])

        return cls(**data)

    def is_security_event(self) -> bool:
        """Check if this is a security-related event."""
        security_types = [
            EventType.AUTH_SUCCESS,
            EventType.AUTH_FAILURE,
            EventType.AUTH_DENIED,
            EventType.PERMISSION_DENIED,
        ]
        return self.event_type in security_types

    def is_compliance_event(self) -> bool:
        """Check if this is a compliance-related event."""
        return (
            self.event_type.value.startswith("compliance.")
            or self.contains_pii
            or self.is_sensitive
        )

    def requires_immediate_alert(self) -> bool:
        """Check if this event requires immediate alerting."""
        return self.severity in [Severity.ERROR, Severity.CRITICAL] or (
            self.event_type
            in [
                EventType.AUTH_FAILURE,
                EventType.PERMISSION_DENIED,
                EventType.SYSTEM_ERROR,
            ]
            and self.severity == Severity.WARNING
        )


def create_document_event(
    event_type: EventType,
    document_path: str,
    action: str,
    user: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> AuditEvent:
    """
    Create a document-related audit event.

    Args:
        event_type: Type of document event
        document_path: Path to the document
        action: Action performed
        user: User who performed the action
        metadata: Additional metadata

    Returns:
        AuditEvent instance
    """
    import os
    import socket

    return AuditEvent(
        event_type=event_type,
        resource_type="document",
        resource_path=document_path,
        action=action,
        username=user or os.getenv("USER") or os.getenv("USERNAME"),
        hostname=socket.gethostname(),
        process_id=os.getpid(),
        metadata=metadata or {},
    )


def create_system_event(
    event_type: EventType,
    description: str,
    severity: Severity = Severity.INFO,
    metadata: Optional[Dict[str, Any]] = None,
) -> AuditEvent:
    """
    Create a system-related audit event.

    Args:
        event_type: Type of system event
        description: Description of the event
        severity: Event severity
        metadata: Additional metadata

    Returns:
        AuditEvent instance
    """
    import os
    import socket

    return AuditEvent(
        event_type=event_type,
        severity=severity,
        description=description,
        hostname=socket.gethostname(),
        process_id=os.getpid(),
        metadata=metadata or {},
    )


def create_security_event(
    event_type: EventType,
    action: str,
    status: str,
    user: Optional[str] = None,
    severity: Severity = Severity.WARNING,
    metadata: Optional[Dict[str, Any]] = None,
) -> AuditEvent:
    """
    Create a security-related audit event.

    Args:
        event_type: Type of security event
        action: Action attempted
        status: Status of the action (success/failure)
        user: User who attempted the action
        severity: Event severity
        metadata: Additional metadata

    Returns:
        AuditEvent instance
    """
    import os
    import socket

    return AuditEvent(
        event_type=event_type,
        severity=severity,
        action=action,
        status=status,
        username=user or os.getenv("USER") or os.getenv("USERNAME"),
        hostname=socket.gethostname(),
        process_id=os.getpid(),
        metadata=metadata or {},
    )
