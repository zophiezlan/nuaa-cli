"""
Core audit logging implementation.

Provides thread-safe, append-only audit logging with automatic rotation.
"""

import json
import threading
from pathlib import Path
from typing import Optional
from datetime import datetime
import hashlib

from .events import AuditEvent
from .config import AuditConfig, get_config


class AuditLogger:
    """
    Thread-safe audit logger with immutable log entries.

    Features:
    - Append-only logging (no modifications or deletions)
    - Automatic log rotation based on file size
    - JSON-formatted structured logs
    - Thread-safe operations
    - Integrity verification via checksums
    """

    def __init__(self, config: Optional[AuditConfig] = None):
        """
        Initialize audit logger.

        Args:
            config: AuditConfig instance (uses global config if None)
        """
        self.config = config or get_config()
        self._lock = threading.Lock()
        self._last_checksum: Optional[str] = None

        # Initialize log file
        if self.config.enabled:
            self._init_log_file()

    def _init_log_file(self) -> None:
        """Initialize the audit log file and directory."""
        # Ensure directory exists
        self.config.audit_dir.mkdir(parents=True, exist_ok=True)

        # Create log file if it doesn't exist
        if not self.config.log_path.exists():
            self._write_header()

    def _write_header(self) -> None:
        """Write log file header."""
        header = {
            "type": "audit_log_header",
            "version": "1.0",
            "created": datetime.utcnow().isoformat(),
            "description": "NUAA CLI Audit Log",
            "format": "JSON Lines (JSONL)",
        }
        with open(self.config.log_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(header) + "\n")

    def log(self, event: AuditEvent) -> bool:
        """
        Log an audit event.

        Args:
            event: AuditEvent to log

        Returns:
            True if event was logged successfully, False otherwise
        """
        if not self.config.enabled:
            return False

        # Check if event type is allowed
        if not self.config.is_event_allowed(event.event_type.value):
            return False

        # Filter PII if not allowed
        if event.contains_pii and not self.config.include_pii:
            event.metadata = {"_pii_filtered": True}

        with self._lock:
            try:
                # Check for rotation
                self._check_rotation()

                # Convert event to dict
                event_dict = event.to_dict()

                # Add checksum for integrity
                event_json = json.dumps(event_dict, sort_keys=True)
                checksum = hashlib.sha256(event_json.encode()).hexdigest()
                event_dict["_checksum"] = checksum
                event_dict["_prev_checksum"] = self._last_checksum

                # Write to log file (append-only)
                with open(self.config.log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(event_dict) + "\n")
                    f.flush()  # Ensure immediate write

                self._last_checksum = checksum

                # Send to syslog if enabled
                if self.config.syslog_enabled:
                    self._send_to_syslog(event)

                # Check for alerts
                if event.requires_immediate_alert() and self.config.alert_on_critical:
                    self._send_alert(event)

                return True

            except Exception as e:
                # Log to standard logging but don't raise
                # (audit failures shouldn't break the application)
                import logging

                logging.error(f"Failed to write audit log: {e}")
                return False

    def _check_rotation(self) -> None:
        """Check if log rotation is needed and perform it."""
        if not self.config.log_path.exists():
            self._write_header()
            return

        # Check file size
        file_size = self.config.log_path.stat().st_size
        if file_size >= self.config.max_file_size:
            self._rotate_logs()

    def _rotate_logs(self) -> None:
        """Rotate audit logs."""
        # Rotate existing logs
        for i in range(self.config.max_files - 1, 0, -1):
            old_file = self.config.audit_dir / f"{self.config.log_file}.{i}"
            new_file = self.config.audit_dir / f"{self.config.log_file}.{i + 1}"

            if old_file.exists():
                if new_file.exists():
                    new_file.unlink()  # Delete oldest log
                old_file.rename(new_file)

        # Rotate current log to .1
        rotated_file = self.config.audit_dir / f"{self.config.log_file}.1"
        if rotated_file.exists():
            rotated_file.unlink()
        self.config.log_path.rename(rotated_file)

        # Create new log file
        self._write_header()
        self._last_checksum = None

    def _send_to_syslog(self, event: AuditEvent) -> None:
        """
        Send audit event to syslog.

        Args:
            event: AuditEvent to send
        """
        if not self.config.syslog_host:
            return

        try:
            import logging.handlers

            syslog = logging.handlers.SysLogHandler(
                address=(self.config.syslog_host, self.config.syslog_port)
            )

            # Format as syslog message
            message = f"NUAA_AUDIT: {event.event_type.value} - {event.action or event.description}"
            syslog.emit(
                logging.LogRecord(
                    name="nuaa_audit",
                    level=logging.INFO,
                    pathname="",
                    lineno=0,
                    msg=message,
                    args=(),
                    exc_info=None,
                )
            )
        except Exception:
            pass  # Fail silently if syslog is unavailable

    def _send_alert(self, event: AuditEvent) -> None:
        """
        Send alert for critical event.

        Args:
            event: AuditEvent that triggered the alert
        """
        # In a production system, this would send email/SMS/etc.
        # For now, just log to stderr
        import sys

        print(
            f"[AUDIT ALERT] {event.severity.value.upper()}: {event.event_type.value}",
            file=sys.stderr,
        )

    def verify_integrity(self, log_file: Optional[Path] = None) -> bool:
        """
        Verify integrity of audit log using checksums.

        Args:
            log_file: Path to log file (uses current log if None)

        Returns:
            True if integrity is verified, False otherwise
        """
        log_path = log_file or self.config.log_path

        if not log_path.exists():
            return True  # Empty log is valid

        try:
            prev_checksum = None

            with open(log_path, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    if not line.strip():
                        continue

                    try:
                        entry = json.loads(line)

                        # Skip header
                        if entry.get("type") == "audit_log_header":
                            continue

                        # Verify checksum chain
                        if "_checksum" in entry:
                            stored_checksum = entry.pop("_checksum")
                            stored_prev = entry.pop("_prev_checksum", None)

                            # Verify previous checksum chain
                            if stored_prev != prev_checksum:
                                print(f"Integrity violation at line {line_num}: broken checksum chain")
                                return False

                            # Verify current checksum
                            event_json = json.dumps(entry, sort_keys=True)
                            calculated = hashlib.sha256(event_json.encode()).hexdigest()

                            if calculated != stored_checksum:
                                print(
                                    f"Integrity violation at line {line_num}: checksum mismatch"
                                )
                                return False

                            prev_checksum = stored_checksum

                    except json.JSONDecodeError:
                        print(f"Invalid JSON at line {line_num}")
                        return False

            return True

        except Exception as e:
            print(f"Error verifying integrity: {e}")
            return False


# Global logger instance
_logger: Optional[AuditLogger] = None
_logger_lock = threading.Lock()


def get_audit_logger() -> AuditLogger:
    """
    Get the global audit logger instance (thread-safe singleton).

    Returns:
        AuditLogger instance
    """
    global _logger

    if _logger is None:
        with _logger_lock:
            if _logger is None:
                _logger = AuditLogger()

    return _logger


def log_event(event: AuditEvent) -> bool:
    """
    Log an audit event using the global logger.

    Args:
        event: AuditEvent to log

    Returns:
        True if logged successfully, False otherwise
    """
    logger = get_audit_logger()
    return logger.log(event)
