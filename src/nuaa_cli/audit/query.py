"""
Audit log querying and reporting.

Provides capabilities to search, filter, and analyze audit logs
for compliance reporting and forensic analysis.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any, Iterator
import re

from .events import AuditEvent, EventType, Severity
from .config import get_config


@dataclass
class AuditQuery:
    """
    Query parameters for searching audit logs.

    Attributes:
        start_time: Start of time range
        end_time: End of time range
        event_types: Filter by event types
        severities: Filter by severity levels
        username: Filter by username
        resource_path: Filter by resource path (supports wildcards)
        action: Filter by action
        status: Filter by status (success/failure)
        contains_pii: Filter events containing PII
        is_sensitive: Filter sensitive events
        limit: Maximum number of results
        offset: Number of results to skip
    """

    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    event_types: Optional[List[EventType]] = None
    severities: Optional[List[Severity]] = None
    username: Optional[str] = None
    resource_path: Optional[str] = None
    action: Optional[str] = None
    status: Optional[str] = None
    contains_pii: Optional[bool] = None
    is_sensitive: Optional[bool] = None
    limit: Optional[int] = None
    offset: int = 0
    sort_desc: bool = True  # Most recent first by default

    def matches(self, event: AuditEvent) -> bool:
        """
        Check if an event matches the query criteria.

        Args:
            event: AuditEvent to check

        Returns:
            True if event matches, False otherwise
        """
        # Time range
        if self.start_time and event.timestamp < self.start_time:
            return False
        if self.end_time and event.timestamp > self.end_time:
            return False

        # Event type
        if self.event_types and event.event_type not in self.event_types:
            return False

        # Severity
        if self.severities and event.severity not in self.severities:
            return False

        # Username
        if self.username and event.username != self.username:
            return False

        # Resource path (with wildcard support)
        if self.resource_path and event.resource_path:
            pattern = self.resource_path.replace("*", ".*")
            if not re.match(pattern, event.resource_path):
                return False

        # Action
        if self.action and event.action != self.action:
            return False

        # Status
        if self.status and event.status != self.status:
            return False

        # PII flag
        if self.contains_pii is not None and event.contains_pii != self.contains_pii:
            return False

        # Sensitive flag
        if self.is_sensitive is not None and event.is_sensitive != self.is_sensitive:
            return False

        return True


def query_audit_logs(
    query: Optional[AuditQuery] = None,
    log_file: Optional[Path] = None,
) -> List[AuditEvent]:
    """
    Query audit logs based on criteria.

    Args:
        query: AuditQuery with search criteria (None = all events)
        log_file: Path to log file (uses current log if None)

    Returns:
        List of matching AuditEvents
    """
    if query is None:
        query = AuditQuery()

    config = get_config()
    log_path = log_file or config.log_path

    if not log_path.exists():
        return []

    results = []

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue

                try:
                    entry = json.loads(line)

                    # Skip header
                    if entry.get("type") == "audit_log_header":
                        continue

                    # Convert to AuditEvent
                    # Remove audit-specific fields
                    entry.pop("_checksum", None)
                    entry.pop("_prev_checksum", None)

                    event = AuditEvent.from_dict(entry)

                    # Check if event matches query
                    if query.matches(event):
                        results.append(event)

                except (json.JSONDecodeError, Exception):
                    # Skip invalid entries
                    continue

        # Sort results
        results.sort(key=lambda e: e.timestamp, reverse=query.sort_desc)

        # Apply offset and limit
        if query.offset > 0:
            results = results[query.offset :]

        if query.limit:
            results = results[: query.limit]

        return results

    except Exception as e:
        import logging

        logging.error(f"Error querying audit logs: {e}")
        return []


def query_all_logs() -> List[AuditEvent]:
    """
    Query all audit logs (including rotated logs).

    Returns:
        List of all AuditEvents across all log files
    """
    config = get_config()
    all_events = []

    # Query current log
    all_events.extend(query_audit_logs())

    # Query rotated logs
    for i in range(1, config.max_files + 1):
        log_file = config.audit_dir / f"{config.log_file}.{i}"
        if log_file.exists():
            all_events.extend(query_audit_logs(log_file=log_file))

    # Sort by timestamp
    all_events.sort(key=lambda e: e.timestamp, reverse=True)

    return all_events


def get_events_by_date_range(
    start_date: datetime, end_date: datetime
) -> List[AuditEvent]:
    """
    Get all events within a date range.

    Args:
        start_date: Start of date range
        end_date: End of date range

    Returns:
        List of AuditEvents in the date range
    """
    query = AuditQuery(start_time=start_date, end_time=end_date)
    return query_audit_logs(query)


def get_events_by_user(username: str) -> List[AuditEvent]:
    """
    Get all events for a specific user.

    Args:
        username: Username to search for

    Returns:
        List of AuditEvents by the user
    """
    query = AuditQuery(username=username)
    return query_audit_logs(query)


def get_security_events() -> List[AuditEvent]:
    """
    Get all security-related events.

    Returns:
        List of security AuditEvents
    """
    security_types = [
        EventType.AUTH_SUCCESS,
        EventType.AUTH_FAILURE,
        EventType.AUTH_DENIED,
        EventType.PERMISSION_DENIED,
    ]
    query = AuditQuery(event_types=security_types)
    return query_audit_logs(query)


def get_failed_events() -> List[AuditEvent]:
    """
    Get all failed events.

    Returns:
        List of failed AuditEvents
    """
    query = AuditQuery(status="failure")
    return query_audit_logs(query)


def get_events_with_pii() -> List[AuditEvent]:
    """
    Get all events containing PII.

    Returns:
        List of AuditEvents containing PII
    """
    query = AuditQuery(contains_pii=True)
    return query_audit_logs(query)


def generate_compliance_report(
    start_date: datetime, end_date: datetime
) -> Dict[str, Any]:
    """
    Generate a compliance report for a date range.

    Args:
        start_date: Start of reporting period
        end_date: End of reporting period

    Returns:
        Dictionary containing compliance report data
    """
    query = AuditQuery(start_time=start_date, end_time=end_date)
    events = query_audit_logs(query)

    # Aggregate statistics
    event_counts = {}
    severity_counts = {}
    user_activity = {}
    failed_actions = []

    for event in events:
        # Count by event type
        event_type = event.event_type.value
        event_counts[event_type] = event_counts.get(event_type, 0) + 1

        # Count by severity
        severity = event.severity.value
        severity_counts[severity] = severity_counts.get(severity, 0) + 1

        # Track user activity
        if event.username:
            if event.username not in user_activity:
                user_activity[event.username] = {"total": 0, "failed": 0}
            user_activity[event.username]["total"] += 1
            if event.status == "failure":
                user_activity[event.username]["failed"] += 1

        # Track failures
        if event.status == "failure":
            failed_actions.append(
                {
                    "timestamp": event.timestamp.isoformat(),
                    "event_type": event.event_type.value,
                    "user": event.username,
                    "action": event.action,
                }
            )

    return {
        "report_period": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat(),
        },
        "summary": {
            "total_events": len(events),
            "unique_users": len(user_activity),
            "failed_actions": len(failed_actions),
        },
        "event_counts": event_counts,
        "severity_counts": severity_counts,
        "user_activity": user_activity,
        "failed_actions": failed_actions[:100],  # Limit to 100 most recent
        "compliance_flags": {
            "pii_access_count": len([e for e in events if e.contains_pii]),
            "sensitive_operations": len([e for e in events if e.is_sensitive]),
            "security_events": len([e for e in events if e.is_security_event()]),
        },
    }


def export_to_json(events: List[AuditEvent], output_file: Path) -> None:
    """
    Export audit events to JSON file.

    Args:
        events: List of AuditEvents to export
        output_file: Path to output file
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump([e.to_dict() for e in events], f, indent=2)


def export_to_csv(events: List[AuditEvent], output_file: Path) -> None:
    """
    Export audit events to CSV file.

    Args:
        events: List of AuditEvents to export
        output_file: Path to output file
    """
    import csv

    if not events:
        return

    # Get all field names
    fieldnames = list(events[0].to_dict().keys())

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for event in events:
            # Convert nested dicts to JSON strings for CSV
            row = event.to_dict()
            if "metadata" in row and isinstance(row["metadata"], dict):
                row["metadata"] = json.dumps(row["metadata"])
            writer.writerow(row)
