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

from flask import Flask, render_template, request, jsonify, send_file, make_response
from pathlib import Path
import os
import socket
from datetime import datetime, timedelta
import json
import glob
from collections import defaultdict
import io

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


@app.route("/api/stats/<team_id>")
def api_stats(team_id):
    """API endpoint for dashboard statistics"""
    if team_id not in TEAMS:
        return jsonify({"error": "Team not found"}), 404

    output_dir = NUAA_CLI_PATH / "outputs" / team_id

    # Count total documents
    total_docs = 0
    recent_docs = 0
    drafts = 0

    if output_dir.exists():
        # Count all markdown files
        all_files = list(output_dir.rglob("*.md"))
        total_docs = len(all_files)

        # Count documents from the last week
        one_week_ago = datetime.now() - timedelta(days=7)
        for file_path in all_files:
            if datetime.fromtimestamp(file_path.stat().st_mtime) > one_week_ago:
                recent_docs += 1

    # Drafts are stored in localStorage, so we return 0 for now
    # The frontend will update this from localStorage

    return jsonify({
        "total": total_docs,
        "recent": recent_docs,
        "drafts": drafts,
        "templates": len(TEAMS[team_id]["templates"])
    })


@app.route("/api/documents/<team_id>")
def api_documents(team_id):
    """API endpoint for recent documents"""
    if team_id not in TEAMS:
        return jsonify({"error": "Team not found"}), 404

    output_dir = NUAA_CLI_PATH / "outputs" / team_id
    documents = []

    if output_dir.exists():
        # Get all markdown files
        all_files = sorted(
            output_dir.rglob("*.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        # Get limit from query params
        limit = int(request.args.get("limit", 10))

        for file_path in all_files[:limit]:
            rel_path = file_path.relative_to(output_dir)
            documents.append({
                "id": str(rel_path).replace("/", "_").replace(".md", ""),
                "name": file_path.stem.replace("-", " ").title(),
                "date": datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                "path": str(file_path),
                "size": file_path.stat().st_size
            })

    return jsonify({"documents": documents})


@app.route("/api/search")
def api_search():
    """Search across all documents"""
    query = request.args.get("q", "").lower()
    team_id = request.args.get("team_id")

    if not query:
        return jsonify({"results": []})

    results = []
    search_dirs = []

    if team_id and team_id in TEAMS:
        search_dirs.append(NUAA_CLI_PATH / "outputs" / team_id)
    else:
        # Search all team outputs
        for tid in TEAMS.keys():
            search_dirs.append(NUAA_CLI_PATH / "outputs" / tid)

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue

        for file_path in search_dir.rglob("*.md"):
            try:
                content = file_path.read_text()
                if query in content.lower() or query in file_path.name.lower():
                    # Extract context snippet
                    lines = content.split("\n")
                    context = ""
                    for i, line in enumerate(lines):
                        if query in line.lower():
                            start = max(0, i - 1)
                            end = min(len(lines), i + 2)
                            context = " ".join(lines[start:end])
                            break

                    results.append({
                        "title": file_path.stem.replace("-", " ").title(),
                        "path": str(file_path),
                        "team": str(file_path.parent.parent.name),
                        "date": datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d"),
                        "context": context[:200] + "..." if len(context) > 200 else context
                    })
            except Exception:
                continue

    # Limit results
    results = results[:50]

    return jsonify({"results": results, "query": query, "count": len(results)})


@app.route("/document/<team_id>/<path:doc_path>")
def view_document(team_id, doc_path):
    """View a specific document"""
    if team_id not in TEAMS:
        return "Team not found", 404

    file_path = NUAA_CLI_PATH / "outputs" / team_id / doc_path

    if not file_path.exists() or not file_path.suffix == ".md":
        return "Document not found", 404

    try:
        content = file_path.read_text()
        # Convert markdown to HTML (basic implementation)
        html_content = markdown_to_html(content)

        return render_template(
            "document_view.html",
            team_id=team_id,
            team=TEAMS[team_id],
            doc_name=file_path.stem.replace("-", " ").title(),
            content=html_content,
            raw_path=str(file_path)
        )
    except Exception as e:
        return f"Error loading document: {str(e)}", 500


@app.route("/export/pdf", methods=["POST"])
def export_pdf():
    """Export document as PDF"""
    try:
        data = request.json
        content = data.get("content", "")
        filename = data.get("filename", "document")

        # For now, create a simple text file
        # In production, you'd use a library like WeasyPrint or ReportLab
        output = io.BytesIO()
        output.write(f"NUAA Document Export\n{'=' * 50}\n\n{content}".encode("utf-8"))
        output.seek(0)

        response = make_response(send_file(
            output,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"{filename}.pdf"
        ))

        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/export/word", methods=["POST"])
def export_word():
    """Export document as Word"""
    try:
        data = request.json
        content = data.get("content", "")
        filename = data.get("filename", "document")

        # Create simple RTF format (readable by Word)
        rtf_content = r"{\rtf1\ansi\deff0 {\fonttbl {\f0 Arial;}}" + "\n"
        rtf_content += r"{\colortbl;\red0\green0\blue0;}" + "\n"
        rtf_content += r"\f0\fs24 " + content.replace("\n", r"\par ") + "\n}"

        output = io.BytesIO()
        output.write(rtf_content.encode("utf-8"))
        output.seek(0)

        response = make_response(send_file(
            output,
            mimetype="application/rtf",
            as_attachment=True,
            download_name=f"{filename}.rtf"
        ))

        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/email", methods=["POST"])
def send_email():
    """Send document via email"""
    try:
        data = request.json
        recipient = data.get("recipient", "")
        subject = data.get("subject", "NUAA Document")
        content = data.get("content", "")

        # In production, integrate with email service (SendGrid, AWS SES, etc.)
        # For now, return success with instructions

        return jsonify({
            "success": True,
            "message": f"Email functionality coming soon! Document prepared for: {recipient}",
            "instructions": "Please copy the content and email manually for now."
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def markdown_to_html(markdown_text):
    """Basic markdown to HTML conversion"""
    html = markdown_text

    # Headers
    html = html.replace("### ", "<h3>").replace("\n\n", "</h3>\n\n")
    html = html.replace("## ", "<h2>").replace("\n\n", "</h2>\n\n")
    html = html.replace("# ", "<h1>").replace("\n\n", "</h1>\n\n")

    # Bold
    import re
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)

    # Lists
    lines = html.split("\n")
    in_list = False
    new_lines = []
    for line in lines:
        if line.strip().startswith("- "):
            if not in_list:
                new_lines.append("<ul>")
                in_list = True
            new_lines.append(f"<li>{line.strip()[2:]}</li>")
        else:
            if in_list:
                new_lines.append("</ul>")
                in_list = False
            new_lines.append(line)

    if in_list:
        new_lines.append("</ul>")

    html = "\n".join(new_lines)

    # Paragraphs
    html = html.replace("\n\n", "</p><p>")
    html = f"<p>{html}</p>"

    return html


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
