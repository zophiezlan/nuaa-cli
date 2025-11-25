"""
Audit logging module for NUAA CLI.

Provides comprehensive audit trail functionality for security and compliance.
Tracks all document access, modifications, exports, and user actions.

Features:
- Immutable audit logs (append-only)
- Structured JSON format
- Automatic log rotation
- Compliance-ready (HIPAA, GDPR, SOC 2)
- Query and reporting capabilities
"""

from .logger import AuditLogger, get_audit_logger
from .events import AuditEvent, EventType
from .query import AuditQuery, query_audit_logs
from .config import AuditConfig

__all__ = [
    "AuditLogger",
    "get_audit_logger",
    "AuditEvent",
    "EventType",
    "AuditQuery",
    "query_audit_logs",
    "AuditConfig",
]
