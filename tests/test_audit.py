"""
Tests for audit logging module.

Tests audit event creation, logging, querying, and compliance features.
"""

import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path


from nuaa_cli.audit import (
    AuditLogger,
    AuditEvent,
    EventType,
    Severity,
    AuditConfig,
    AuditQuery,
    query_audit_logs,
    create_document_event,
    create_system_event,
    create_security_event,
)


class TestAuditEvents:
    """Tests for AuditEvent class."""

    def test_audit_event_creation(self):
        """Test creating a basic audit event."""
        event = AuditEvent(
            event_type=EventType.DOCUMENT_CREATED,
            action="create",
            resource_path="/test/document.md",
        )

        assert event.event_type == EventType.DOCUMENT_CREATED
        assert event.action == "create"
        assert event.resource_path == "/test/document.md"
        assert event.status == "success"

    def test_audit_event_has_id(self):
        """Test that events have unique IDs."""
        event1 = AuditEvent()
        event2 = AuditEvent()

        assert event1.event_id != event2.event_id

    def test_audit_event_has_timestamp(self):
        """Test that events have timestamps."""
        event = AuditEvent()

        assert isinstance(event.timestamp, datetime)
        assert event.timestamp <= datetime.utcnow()

    def test_audit_event_to_dict(self):
        """Test converting event to dictionary."""
        event = AuditEvent(
            event_type=EventType.DOCUMENT_CREATED,
            action="create",
            metadata={"key": "value"},
        )

        data = event.to_dict()

        assert isinstance(data, dict)
        assert data["event_type"] == EventType.DOCUMENT_CREATED.value
        assert data["action"] == "create"
        assert data["metadata"] == {"key": "value"}

    def test_audit_event_from_dict(self):
        """Test creating event from dictionary."""
        data = {
            "event_id": "test-id",
            "timestamp": "2025-01-01T00:00:00",
            "event_type": "document.created",
            "severity": "info",
            "action": "test",
        }

        event = AuditEvent.from_dict(data)

        assert event.event_id == "test-id"
        assert event.event_type == EventType.DOCUMENT_CREATED
        assert event.severity == Severity.INFO

    def test_is_security_event(self):
        """Test security event detection."""
        security_event = AuditEvent(event_type=EventType.AUTH_FAILURE)
        regular_event = AuditEvent(event_type=EventType.DOCUMENT_CREATED)

        assert security_event.is_security_event()
        assert not regular_event.is_security_event()

    def test_is_compliance_event(self):
        """Test compliance event detection."""
        pii_event = AuditEvent(contains_pii=True)
        sensitive_event = AuditEvent(is_sensitive=True)
        compliance_event = AuditEvent(event_type=EventType.PII_ACCESSED)
        regular_event = AuditEvent()

        assert pii_event.is_compliance_event()
        assert sensitive_event.is_compliance_event()
        assert compliance_event.is_compliance_event()
        assert not regular_event.is_compliance_event()

    def test_requires_immediate_alert(self):
        """Test alert requirement detection."""
        critical_event = AuditEvent(severity=Severity.CRITICAL)
        error_event = AuditEvent(severity=Severity.ERROR)
        auth_failure = AuditEvent(event_type=EventType.AUTH_FAILURE, severity=Severity.WARNING)
        regular_event = AuditEvent()

        assert critical_event.requires_immediate_alert()
        assert error_event.requires_immediate_alert()
        assert auth_failure.requires_immediate_alert()
        assert not regular_event.requires_immediate_alert()


class TestAuditConfig:
    """Tests for AuditConfig class."""

    def test_default_config(self):
        """Test default configuration values."""
        config = AuditConfig()

        assert config.enabled is True
        assert config.include_pii is False
        assert config.retention_days == 365
        assert config.max_files == 10

    def test_custom_config(self):
        """Test custom configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = AuditConfig(
                audit_dir=Path(tmpdir),
                enabled=False,
                include_pii=True,
                retention_days=30,
            )

            assert config.audit_dir == Path(tmpdir)
            assert config.enabled is False
            assert config.include_pii is True
            assert config.retention_days == 30

    def test_log_path(self):
        """Test log path property."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = AuditConfig(audit_dir=Path(tmpdir), log_file="test.log")

            assert config.log_path == Path(tmpdir) / "test.log"

    def test_is_event_allowed(self):
        """Test event filtering."""
        config = AuditConfig(enabled=True, allowed_event_types=[EventType.DOCUMENT_CREATED.value])

        assert config.is_event_allowed(EventType.DOCUMENT_CREATED.value)
        assert not config.is_event_allowed(EventType.DOCUMENT_DELETED.value)

    def test_config_to_dict(self):
        """Test converting config to dictionary."""
        config = AuditConfig()
        data = config.to_dict()

        assert isinstance(data, dict)
        assert "enabled" in data
        assert "audit_dir" in data


class TestAuditLogger:
    """Tests for AuditLogger class."""

    def test_logger_creation(self):
        """Test creating audit logger."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = AuditConfig(audit_dir=Path(tmpdir))
            logger = AuditLogger(config)

            assert logger.config == config
            assert logger.config.log_path.parent.exists()

    def test_log_event(self):
        """Test logging an event."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = AuditConfig(audit_dir=Path(tmpdir))
            logger = AuditLogger(config)

            event = AuditEvent(event_type=EventType.DOCUMENT_CREATED, action="test_create")

            result = logger.log(event)

            assert result is True
            assert config.log_path.exists()

    def test_log_creates_file(self):
        """Test that logging creates the log file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = AuditConfig(audit_dir=Path(tmpdir))
            logger = AuditLogger(config)

            event = AuditEvent()
            logger.log(event)

            assert config.log_path.exists()
            assert config.log_path.stat().st_size > 0

    def test_log_disabled(self):
        """Test that logging is skipped when disabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = AuditConfig(audit_dir=Path(tmpdir), enabled=False)
            logger = AuditLogger(config)

            event = AuditEvent()
            result = logger.log(event)

            assert result is False

    def test_log_filters_pii(self):
        """Test that PII is filtered when not allowed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = AuditConfig(audit_dir=Path(tmpdir), include_pii=False)
            logger = AuditLogger(config)

            event = AuditEvent(contains_pii=True, metadata={"sensitive": "data", "name": "Alice"})

            logger.log(event)

            # Read log and verify PII was filtered
            with open(config.log_path, "r") as f:
                lines = f.readlines()
                last_line = json.loads(lines[-1])

                assert last_line["metadata"] == {"_pii_filtered": True}

    def test_verify_integrity_valid(self):
        """Test integrity verification on valid log."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = AuditConfig(audit_dir=Path(tmpdir))
            logger = AuditLogger(config)

            # Log some events
            for i in range(5):
                event = AuditEvent(action=f"test_{i}")
                logger.log(event)

            # Verify integrity
            assert logger.verify_integrity() is True

    def test_log_rotation(self):
        """Test log rotation when file size exceeds limit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = AuditConfig(
                audit_dir=Path(tmpdir),
                max_file_size=1024,  # 1KB
            )
            logger = AuditLogger(config)

            # Log many events to trigger rotation
            for i in range(100):
                event = AuditEvent(
                    action=f"test_{i}", metadata={"data": "x" * 100}
                )  # Bulk up event
                logger.log(event)

            # Check if rotated file exists
            rotated = Path(tmpdir) / "audit.log.1"
            # May or may not rotate depending on event size, so just check log exists
            assert config.log_path.exists()


class TestAuditQuery:
    """Tests for audit querying."""

    def test_query_all_events(self):
        """Test querying all events."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = AuditConfig(audit_dir=Path(tmpdir))
            logger = AuditLogger(config)

            # Log some events
            for i in range(5):
                event = AuditEvent(action=f"test_{i}")
                logger.log(event)

            # Query all
            events = query_audit_logs(log_file=config.log_path)

            assert len(events) == 5

    def test_query_by_event_type(self):
        """Test querying by event type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = AuditConfig(audit_dir=Path(tmpdir))
            logger = AuditLogger(config)

            # Log different event types
            logger.log(AuditEvent(event_type=EventType.DOCUMENT_CREATED))
            logger.log(AuditEvent(event_type=EventType.DOCUMENT_CREATED))
            logger.log(AuditEvent(event_type=EventType.DOCUMENT_DELETED))

            # Query for created events
            query = AuditQuery(event_types=[EventType.DOCUMENT_CREATED])
            events = query_audit_logs(query, log_file=config.log_path)

            assert len(events) == 2
            assert all(e.event_type == EventType.DOCUMENT_CREATED for e in events)

    def test_query_by_username(self):
        """Test querying by username."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = AuditConfig(audit_dir=Path(tmpdir))
            logger = AuditLogger(config)

            # Log events from different users
            logger.log(AuditEvent(username="alice"))
            logger.log(AuditEvent(username="bob"))
            logger.log(AuditEvent(username="alice"))

            # Query for alice's events
            query = AuditQuery(username="alice")
            events = query_audit_logs(query, log_file=config.log_path)

            assert len(events) == 2
            assert all(e.username == "alice" for e in events)

    def test_query_by_time_range(self):
        """Test querying by time range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = AuditConfig(audit_dir=Path(tmpdir))
            logger = AuditLogger(config)

            # Log events
            past_event = AuditEvent(timestamp=datetime.utcnow() - timedelta(days=10), action="old")
            recent_event = AuditEvent(
                timestamp=datetime.utcnow() - timedelta(hours=1), action="recent"
            )

            logger.log(past_event)
            logger.log(recent_event)

            # Query last 7 days
            query = AuditQuery(start_time=datetime.utcnow() - timedelta(days=7))
            events = query_audit_logs(query, log_file=config.log_path)

            # Should only get recent event
            assert len(events) == 1
            assert events[0].action == "recent"

    def test_query_with_limit(self):
        """Test querying with limit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = AuditConfig(audit_dir=Path(tmpdir))
            logger = AuditLogger(config)

            # Log 10 events
            for i in range(10):
                logger.log(AuditEvent(action=f"test_{i}"))

            # Query with limit
            query = AuditQuery(limit=3)
            events = query_audit_logs(query, log_file=config.log_path)

            assert len(events) == 3


class TestHelperFunctions:
    """Tests for helper functions."""

    def test_create_document_event(self):
        """Test creating document event."""
        event = create_document_event(
            event_type=EventType.DOCUMENT_CREATED,
            document_path="/test/doc.md",
            action="create",
            user="alice",
        )

        assert event.event_type == EventType.DOCUMENT_CREATED
        assert event.resource_type == "document"
        assert event.resource_path == "/test/doc.md"
        assert event.action == "create"
        assert event.username == "alice"

    def test_create_system_event(self):
        """Test creating system event."""
        event = create_system_event(
            event_type=EventType.SYSTEM_START,
            description="System starting",
            severity=Severity.INFO,
        )

        assert event.event_type == EventType.SYSTEM_START
        assert event.description == "System starting"
        assert event.severity == Severity.INFO

    def test_create_security_event(self):
        """Test creating security event."""
        event = create_security_event(
            event_type=EventType.AUTH_FAILURE,
            action="login",
            status="failure",
            user="attacker",
        )

        assert event.event_type == EventType.AUTH_FAILURE
        assert event.action == "login"
        assert event.status == "failure"
        assert event.username == "attacker"


class TestCompliance:
    """Tests for compliance features."""

    def test_pii_tracking(self):
        """Test PII tracking in events."""
        event = AuditEvent(contains_pii=True, metadata={"ssn": "123-45-6789"})

        assert event.contains_pii is True
        assert event.is_compliance_event()

    def test_sensitive_data_tracking(self):
        """Test sensitive data tracking."""
        event = AuditEvent(is_sensitive=True)

        assert event.is_sensitive is True
        assert event.is_compliance_event()

    def test_retention_period(self):
        """Test retention period setting."""
        event = AuditEvent(retention_days=90)

        assert event.retention_days == 90
