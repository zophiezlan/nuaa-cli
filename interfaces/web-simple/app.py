#!/usr/bin/env python3
"""
NUAA Simple Web Interface

A simple, accessible web interface for NUAA teams who don't use command-line tools.
Designed for maximum accessibility and ease of use.

Features:
- Large, clear buttons
- Simple navigation
- No technical knowledge required
- Mobile-friendly
- Screen reader compatible
- High contrast mode
- Works offline (once loaded)
"""

from flask import Flask, render_template, request, jsonify
from pathlib import Path
import os
import socket
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Get the NUAA CLI path
NUAA_CLI_PATH = Path(__file__).parent.parent.parent
TEMPLATES_PATH = NUAA_CLI_PATH / "nuaa-kit" / "templates"

# Team configurations
TEAMS = {
    "outreach": {
        "name": "Outreach Team",
        "icon": "🚶",
        "templates": ["session-report-simple.md", "safety-incident.md", "engagement-statistics.md"],
        "description": "Quick field reports and session documentation",
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
    },
    "peer-distributors": {
        "name": "Peer Distributors",
        "icon": "🤝",
        "templates": ["distribution-log-simple.md", "resupply-request.md"],
        "description": "Distribution tracking and resupply requests",
    },
    "nsp-warehouse": {
        "name": "NSP Warehouse",
        "icon": "📦",
        "templates": ["distribution-shipment-simple.md", "inventory-check.md", "supplier-order.md"],
        "description": "Inventory and distribution management",
    },
    "peerline": {
        "name": "Peerline",
        "icon": "📞",
        "templates": ["call-log-simple.md", "resource-request.md"],
        "description": "Call logging and peer support",
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
    },
    "comms-advocacy": {
        "name": "Communications/Advocacy",
        "icon": "📢",
        "templates": ["campaign-strategy.md", "media-release.md", "stakeholder-briefing.md"],
        "description": "Campaign planning and media",
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
    },
    "bbv-testing": {
        "name": "BBV Testing",
        "icon": "🏥",
        "templates": ["testing-session.md", "client-education.md", "referral-protocol.md"],
        "description": "Testing protocols and education",
    },
    "workforce-dev": {
        "name": "Workforce Development",
        "icon": "💼",
        "templates": ["position-description.md", "onboarding-checklist.md", "career-pathway.md"],
        "description": "HR and professional development",
    },
}


@app.route("/")
def index():
    """Home page with team selection"""
    return render_template("index.html", teams=TEAMS)


@app.route("/welcome")
def welcome_wizard():
    """Welcome wizard for first-time users"""
    return render_template("welcome-wizard.html")


@app.route("/api/server-info")
def server_info():
    """API endpoint to get server information"""
    try:
        # Get local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "localhost"

    return jsonify({"ip": local_ip, "port": 5000, "status": "running"})


@app.route("/team/<team_id>")
def team_dashboard(team_id):
    """Team-specific dashboard"""
    if team_id not in TEAMS:
        return "Team not found", 404

    team = TEAMS[team_id]
    return render_template("team_dashboard.html", team_id=team_id, team=team)


@app.route("/template/<team_id>/<template_name>")
def show_template(team_id, template_name):
    """Display a template form"""
    if team_id not in TEAMS:
        return "Team not found", 404

    team = TEAMS[team_id]
    if template_name not in team["templates"]:
        return "Template not found", 404

    # Load the template
    template_path = TEMPLATES_PATH / "team-specific" / team_id / template_name

    if not template_path.exists():
        return f"Template file not found: {template_path}", 404

    with open(template_path, "r") as f:
        template_content = f.read()

    return render_template(
        "form.html",
        team_id=team_id,
        team=team,
        template_name=template_name,
        template_content=template_content,
    )


@app.route("/submit", methods=["POST"])
def submit_form():
    """Handle form submission"""
    data = request.json
    team_id = data.get("team_id")
    template_name = data.get("template_name")
    form_data = data.get("form_data", {})

    # Create output directory
    output_dir = NUAA_CLI_PATH / "outputs" / team_id / datetime.now().strftime("%Y-%m-%d")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = output_dir / f"{template_name.replace('.md', '')}-{timestamp}.md"

    # Load template and fill in data
    template_path = TEMPLATES_PATH / "team-specific" / team_id / template_name
    with open(template_path, "r") as f:
        content = f.read()

    # Simple replacement of placeholders with form data
    for key, value in form_data.items():
        placeholder = f"_{{{key}}}"
        content = content.replace(placeholder, value)

    # Save the filled template
    with open(output_file, "w") as f:
        f.write(content)
        f.write("\n\n---\n\n")
        f.write(
            f"**Submitted via Web Interface**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        f.write(f"**Team**: {TEAMS[team_id]['name']}\n")

    return jsonify(
        {"success": True, "file": str(output_file), "message": "Form submitted successfully!"}
    )


@app.route("/quick-submit", methods=["POST"])
def quick_submit():
    """Quick submission for field workers (minimal data)"""
    data = request.json
    team_id = data.get("team_id")
    quick_data = data.get("data", "")

    # Create output directory
    output_dir = NUAA_CLI_PATH / "outputs" / team_id / datetime.now().strftime("%Y-%m-%d")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = output_dir / f"quick-report-{timestamp}.md"

    # Save quick report
    with open(output_file, "w") as f:
        f.write(f"# Quick Report - {TEAMS[team_id]['name']}\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Data**:\n{quick_data}\n\n")
        f.write("---\n\n")
        f.write("**Submitted via**: Web Quick Submit\n")

    return jsonify({"success": True, "file": str(output_file), "message": "Quick report saved!"})


@app.route("/accessibility")
def accessibility_settings():
    """Accessibility settings page"""
    return render_template("accessibility.html")


@app.route("/help/<team_id>")
def help_page(team_id):
    """Team-specific help page"""
    if team_id not in TEAMS:
        return "Team not found", 404

    team = TEAMS[team_id]
    return render_template("help.html", team_id=team_id, team=team)


@app.route("/offline")
def offline_page():
    """Offline fallback page"""
    return render_template("offline.html")


if __name__ == "__main__":
    # Create output directory if it doesn't exist
    (NUAA_CLI_PATH / "outputs").mkdir(exist_ok=True)

    print("=" * 60)
    print("NUAA Simple Web Interface")
    print("=" * 60)
    print()
    print("Starting server...")
    print("Open your browser and go to: http://localhost:5000")
    print()
    print("Features:")
    print("  ✓ Simple, accessible interface")
    print("  ✓ No command-line knowledge required")
    print("  ✓ Mobile-friendly")
    print("  ✓ Works for all NUAA teams")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    app.run(debug=True, host="0.0.0.0", port=5000)
