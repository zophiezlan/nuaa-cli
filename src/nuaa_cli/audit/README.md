# NUAA CLI Audit Logging System

Comprehensive audit logging for security, compliance, and forensic analysis.

## Overview

The audit logging system provides:
- **Immutable audit trail** - Append-only logs with integrity verification
- **Comprehensive event tracking** - Documents, security, system, and user events
- **Compliance-ready** - HIPAA, GDPR, SOC 2 compliant logging
- **Thread-safe operations** - Safe for concurrent use
- **Automatic log rotation** - Size-based rotation with retention policies
- **Query and reporting** - Flexible search and compliance reports
- **Integrity verification** - Cryptographic checksums verify log integrity

## Quick Start

### Basic Usage

```python
from nuaa_cli.audit import get_audit_logger, create_document_event, EventType

# Get the global audit logger
logger = get_audit_logger()

# Log a document creation event
event = create_document_event(
    event_type=EventType.DOCUMENT_CREATED,
    document_path="/path/to/document.md",
    action="create",
    user="alice",
    metadata={"template": "program-design", "size": 1024}
)

logger.log(event)
```

### Querying Logs

```python
from nuaa_cli.audit import query_audit_logs, AuditQuery, EventType
from datetime import datetime, timedelta

# Query events from the last 7 days
query = AuditQuery(
    start_time=datetime.utcnow() - timedelta(days=7),
    event_types=[EventType.DOCUMENT_CREATED, EventType.DOCUMENT_MODIFIED]
)

events = query_audit_logs(query)

for event in events:
    print(f"{event.timestamp}: {event.event_type} - {event.resource_path}")
```

### Compliance Reports

```python
from nuaa_cli.audit import generate_compliance_report
from datetime import datetime, timedelta

# Generate monthly compliance report
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=30)

report = generate_compliance_report(start_date, end_date)

print(f"Total events: {report['summary']['total_events']}")
print(f"Failed actions: {report['summary']['failed_actions']}")
print(f"PII access count: {report['compliance_flags']['pii_access_count']}")
```

## Event Types

### Document Operations
- `DOCUMENT_CREATED` - Document created
- `DOCUMENT_READ` - Document accessed/read
- `DOCUMENT_UPDATED` - Document modified
- `DOCUMENT_DELETED` - Document deleted
- `DOCUMENT_EXPORTED` - Document exported
- `DOCUMENT_IMPORTED` - Document imported
- `DOCUMENT_VALIDATED` - Document validated

### Security Events
- `AUTH_SUCCESS` - Authentication succeeded
- `AUTH_FAILURE` - Authentication failed
- `AUTH_DENIED` - Authorization denied
- `PERMISSION_DENIED` - Permission denied

### System Events
- `SYSTEM_START` - System started
- `SYSTEM_STOP` - System stopped
- `SYSTEM_ERROR` - System error occurred

### Agent Events
- `AGENT_REGISTERED` - AI agent registered
- `AGENT_INVOKED` - AI agent invoked
- `AGENT_ERROR` - Agent error occurred

### Compliance Events
- `PII_ACCESSED` - Personal Identifiable Information accessed
- `SENSITIVE_DATA_EXPORTED` - Sensitive data exported
- `AUDIT_LOG_ACCESSED` - Audit log accessed

## Configuration

### Environment Variables

```bash
# Enable/disable audit logging
export NUAA_AUDIT_ENABLED=true

# Set audit log directory
export NUAA_AUDIT_DIR=/var/log/nuaa/audit

# Include PII in logs (careful!)
export NUAA_AUDIT_INCLUDE_PII=false

# Enable compliance mode (stricter logging)
export NUAA_AUDIT_COMPLIANCE_MODE=true

# Set maximum file size (bytes)
export NUAA_AUDIT_MAX_FILE_SIZE=104857600  # 100MB

# Set retention period (days)
export NUAA_AUDIT_RETENTION_DAYS=365  # 1 year

# Enable syslog forwarding
export NUAA_AUDIT_SYSLOG_ENABLED=true
export NUAA_AUDIT_SYSLOG_HOST=syslog.example.com

# Alert email for critical events
export NUAA_AUDIT_ALERT_EMAIL=security@example.com
```

### Programmatic Configuration

```python
from nuaa_cli.audit import AuditConfig, set_config
from pathlib import Path

config = AuditConfig(
    audit_dir=Path("/var/log/nuaa/audit"),
    max_file_size=100 * 1024 * 1024,  # 100MB
    max_files=10,
    retention_days=365,
    compliance_mode=True,
    include_pii=False,
)

set_config(config)
```

## Features

### 1. Immutable Audit Trail

All audit logs are append-only. Entries cannot be modified or deleted once written.

```python
# Events are immutable
event = AuditEvent(...)
logger.log(event)
# Event is now permanently recorded
```

### 2. Integrity Verification

Each log entry includes cryptographic checksums that form a tamper-evident chain.

```python
from nuaa_cli.audit import get_audit_logger

logger = get_audit_logger()

# Verify log integrity
is_valid = logger.verify_integrity()
if is_valid:
    print("✓ Audit log integrity verified")
else:
    print("✗ Audit log has been tampered with!")
```

### 3. Automatic Log Rotation

Logs automatically rotate when they reach the configured size limit.

```python
config = AuditConfig(
    max_file_size=100 * 1024 * 1024,  # 100MB
    max_files=10,  # Keep 10 rotated logs
)
# Old logs: audit.log.1, audit.log.2, ..., audit.log.10
```

### 4. Flexible Querying

Search logs by time, event type, user, severity, and more.

```python
from nuaa_cli.audit import AuditQuery, Severity

# Find all critical errors from user 'bob'
query = AuditQuery(
    username="bob",
    severities=[Severity.CRITICAL, Severity.ERROR],
    status="failure"
)

events = query_audit_logs(query)
```

### 5. Compliance Reports

Generate compliance reports for audits and regulatory requirements.

```python
# Monthly report
report = generate_compliance_report(
    start_date=datetime(2025, 1, 1),
    end_date=datetime(2025, 1, 31)
)

# Export to JSON
import json
with open("compliance_report.json", "w") as f:
    json.dump(report, f, indent=2)
```

### 6. Export Capabilities

Export audit logs for external analysis.

```python
from nuaa_cli.audit import query_all_logs, export_to_json, export_to_csv

# Get all events
events = query_all_logs()

# Export to JSON
export_to_json(events, Path("audit_export.json"))

# Export to CSV for spreadsheet analysis
export_to_csv(events, Path("audit_export.csv"))
```

## Security Considerations

### PII Handling

By default, PII is **not** logged. Enable only when required and ensure proper access controls.

```python
config = AuditConfig(
    include_pii=False,  # Default: do not log PII
)
```

### Access Control

Audit log files should have restricted permissions:

```bash
# Set proper permissions
chmod 600 /path/to/audit.log
chown root:root /path/to/audit.log
```

### Encryption (Future)

Future versions will support encrypted audit logs:

```python
config = AuditConfig(
    encrypt_logs=True,
    encryption_key_path="/path/to/key"
)
```

## Compliance Standards

### HIPAA Compliance

The audit system meets HIPAA requirements for:
- §164.308(a)(1)(ii)(D) - Information System Activity Review
- §164.312(b) - Audit Controls

```python
# Track all PHI access
from nuaa_cli.audit import create_document_event, EventType

event = create_document_event(
    event_type=EventType.PII_ACCESSED,
    document_path="/patient/records/12345.md",
    action="read",
    metadata={"contains_phi": True}
)
event.contains_pii = True
event.is_sensitive = True

logger.log(event)
```

### GDPR Compliance

Supports GDPR requirements for:
- Article 30 - Records of processing activities
- Article 32 - Security of processing

```python
# Track data processing
event = create_document_event(
    event_type=EventType.DATA_EXPORT,
    document_path="/exports/user_data.csv",
    action="export",
    metadata={"gdpr_legal_basis": "consent", "data_subject": "user@example.com"}
)
event.contains_pii = True

logger.log(event)
```

### SOC 2 Compliance

Meets SOC 2 criteria for:
- CC7.2 - System monitoring
- CC7.3 - Evaluation and response to security events

```python
# Log security events
from nuaa_cli.audit import create_security_event, EventType, Severity

event = create_security_event(
    event_type=EventType.AUTH_FAILURE,
    action="login",
    status="failure",
    user="attacker@evil.com",
    severity=Severity.WARNING,
    metadata={"ip_address": "192.168.1.100", "attempts": 3}
)

logger.log(event)
```

## Integration Examples

### Integration with Commands

```python
from nuaa_cli.audit import get_audit_logger, create_document_event, EventType

def design_command(program_name: str, output_path: str):
    """Create a program design document."""
    logger = get_audit_logger()

    # Log start
    event = create_document_event(
        event_type=EventType.DOCUMENT_CREATED,
        document_path=output_path,
        action="design_start",
        metadata={"program_name": program_name}
    )
    logger.log(event)

    try:
        # Create document
        create_design_document(program_name, output_path)

        # Log success
        event = create_document_event(
            event_type=EventType.DOCUMENT_CREATED,
            document_path=output_path,
            action="design_complete",
            metadata={"program_name": program_name, "status": "success"}
        )
        logger.log(event)

    except Exception as e:
        # Log failure
        event = create_document_event(
            event_type=EventType.SYSTEM_ERROR,
            document_path=output_path,
            action="design_failed",
            metadata={"error": str(e)}
        )
        event.status = "failure"
        event.severity = Severity.ERROR
        logger.log(event)
        raise
```

### Integration with Web API

```python
from fastapi import FastAPI, Request
from nuaa_cli.audit import get_audit_logger, create_security_event, EventType

app = FastAPI()
logger = get_audit_logger()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all API requests."""
    # Log request
    event = create_security_event(
        event_type=EventType.USER_ACTION,
        action=f"{request.method} {request.url.path}",
        status="pending",
        metadata={
            "client_ip": request.client.host,
            "user_agent": request.headers.get("user-agent")
        }
    )
    logger.log(event)

    # Process request
    response = await call_next(request)

    # Log response
    event.status = "success" if response.status_code < 400 else "failure"
    event.metadata["status_code"] = response.status_code
    logger.log(event)

    return response
```

## Troubleshooting

### Logs Not Being Created

```python
from nuaa_cli.audit import get_config

config = get_config()
print(f"Audit enabled: {config.enabled}")
print(f"Audit directory: {config.audit_dir}")
print(f"Log file: {config.log_path}")

# Check if directory is writable
if not config.audit_dir.exists():
    config.audit_dir.mkdir(parents=True)
```

### Verify Log Integrity

```python
from nuaa_cli.audit import get_audit_logger

logger = get_audit_logger()
is_valid = logger.verify_integrity()

if not is_valid:
    print("WARNING: Audit log integrity check failed!")
    print("The log may have been tampered with.")
```

### Query Specific Events

```python
from nuaa_cli.audit import get_failed_events, get_security_events

# Find all failures
failures = get_failed_events()
print(f"Found {len(failures)} failed operations")

# Find security events
security = get_security_events()
print(f"Found {len(security)} security events")
```

## Performance Considerations

- Audit logging is asynchronous and should not impact application performance
- Log files are append-only for maximum throughput
- Automatic rotation prevents excessive file sizes
- Queries can be slow on very large log files - use date range filters

## Roadmap

Future enhancements:
- [ ] Log encryption at rest
- [ ] Remote log forwarding (rsyslog, Splunk, ELK)
- [ ] Real-time alerting via email/SMS
- [ ] Web-based audit log viewer
- [ ] Advanced analytics and anomaly detection
- [ ] Integration with SIEM systems

## Support

For issues or questions about audit logging:
- GitHub Issues: https://github.com/zophiezlan/nuaa-cli/issues
- Tag with: `audit`, `security`, `compliance`

## License

Same as NUAA CLI main project.
