"""
Team configurations for NUAA Web Interface
"""

TEAMS = {
    "outreach": {
        "name": "Outreach Team",
        "icon": "🚶",
        "templates": [
            "session-report-simple.md",
            "safety-incident.md",
            "engagement-statistics.md",
        ],
        "description": "Quick field reports and session documentation",
        "color": "#3498db",
    },
    "festival-dancewize": {
        "name": "Festival/DanceWize",
        "icon": "🎵",
        "templates": [
            "festival-session-report.md",
            "drug-checking-report.md",
            "volunteer-roster.md",
        ],
        "description": "Event planning and session reports",
        "color": "#9b59b6",
    },
    "peer-distributors": {
        "name": "Peer Distributors",
        "icon": "🤝",
        "templates": ["distribution-log-simple.md", "resupply-request.md"],
        "description": "Distribution tracking and resupply requests",
        "color": "#2ecc71",
    },
    "nsp-warehouse": {
        "name": "NSP Warehouse",
        "icon": "📦",
        "templates": [
            "distribution-shipment-simple.md",
            "inventory-check.md",
            "supplier-order.md",
        ],
        "description": "Inventory and distribution management",
        "color": "#e67e22",
    },
    "peerline": {
        "name": "Peerline",
        "icon": "📞",
        "templates": ["call-log-simple.md", "resource-request.md"],
        "description": "Call logging and peer support",
        "color": "#e74c3c",
    },
    "board-management": {
        "name": "Board/Management",
        "icon": "📊",
        "templates": [
            "funding-proposal-email-friendly.md",
            "strategic-plan.md",
            "impact-report.md",
        ],
        "description": "Strategic planning and proposals",
        "color": "#34495e",
    },
    "comms-advocacy": {
        "name": "Communications/Advocacy",
        "icon": "📢",
        "templates": [
            "campaign-strategy.md",
            "media-release.md",
            "stakeholder-briefing.md",
        ],
        "description": "Campaign planning and media",
        "color": "#1abc9c",
    },
    "training": {
        "name": "Training Team",
        "icon": "📚",
        "templates": [
            "training-curriculum.md",
            "participant-materials.md",
            "evaluation-framework.md",
        ],
        "description": "Training and education materials",
        "color": "#f1c40f",
    },
    "bbv-testing": {
        "name": "BBV Testing",
        "icon": "🏥",
        "templates": [
            "testing-session.md",
            "client-education.md",
            "referral-protocol.md",
        ],
        "description": "Testing protocols and education",
        "color": "#c0392b",
    },
    "workforce-dev": {
        "name": "Workforce Development",
        "icon": "👥",
        "templates": [
            "pd-plan.md",
            "supervision-record.md",
            "team-meeting.md",
        ],
        "description": "Staff development and supervision",
        "color": "#7f8c8d",
    },
}
