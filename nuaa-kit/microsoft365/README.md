# Microsoft 365 Integration Guide

## Overview

This guide provides practical strategies for integrating NUAA-Kit documentation workflows with Microsoft 365 tools already in use at NUAA. While full template automation is planned for Q2 2026, you can start using these manual integration methods immediately.

---

## Quick Start: Immediate Integration (No Setup Required)

### Word Documents

**Export from Markdown**:

1. Open your NUAA-Kit markdown file (e.g., `program-design.md`, `proposal.md`)
2. Copy content to Word (formatting will transfer cleanly)
3. Apply NUAA branding template if available:
   - Logo placement (header/footer)
   - Color scheme (NUAA blue/green)
   - Font standards (Arial, Calibri, or NUAA-specified)
4. Save to SharePoint in appropriate program folder

**Templates Available in Word**:

- Proposal template (branded)
- Report template (branded)
- Program design template (formatted)

**Where to Store**:

- SharePoint: `NUAA Programs/[Program Name]/Documentation/`
- Version naming: `[program-name]-[document-type]-v[X.X].docx`

---

### Excel Spreadsheets

**Budget Calculator Export**:

1. Open `budget-calculator.md` template
2. Copy each budget category table to Excel
3. Apply formulas:
   - Subtotal column: `=C2*D2` (Quantity × Rate)
   - Category totals: `=SUM(E2:E10)` (adjust range)
   - Grand total: `=SUM(B2:B7)` (sum of category totals)
   - Percentages: `=B2/$B$8*100` (Category / Total × 100)
4. Format as currency and percentage
5. Save as `[program-name]-budget-v[X.X].xlsx`

**Impact Framework Dashboard**:

1. Export indicator data from `impact-framework.md` to Excel
2. Create simple dashboard with:
   - Indicator list (Name, Target, Actual, Achievement Rate)
   - Charts: Column chart for outputs, line chart for outcomes over time
   - Conditional formatting: Green (met target), Yellow (partial), Red (not met)
3. Update monthly or quarterly

**Evaluation Data Tracking**:

1. Create workbook with tabs:
   - `Participants` (demographic data)
   - `Activities` (session logs, attendance)
   - `Outcomes` (survey results, pre/post measures)
   - `Dashboard` (summary charts and tables)
2. Link to `impact-framework.md` indicators
3. Use pivot tables for disaggregation by demographics

---

### SharePoint Organization

**Recommended Folder Structure**:

```
NUAA Programs/
├── [Program Name]/
│   ├── Documentation/
│   │   ├── program-design-v1.0.md (or .docx)
│   │   ├── logic-model-v1.0.md
│   │   ├── impact-framework-v1.0.md
│   │   ├── proposal-v1.0.docx
│   │   └── budget-v1.0.xlsx
│   ├── Evaluation/
│   │   ├── data-collection-[year].xlsx
│   │   ├── evaluation-report-midprogram.docx
│   │   └── evaluation-report-final.docx
│   ├── Operations/
│   │   ├── session-attendance-[year].xlsx
│   │   ├── meeting-notes/
│   │   └── partnership-agreements/
│   └── Archived/
│       └── [Previous versions]
```

**Version Control Best Practices**:

- Use SharePoint version history feature (File > Version History)
- Name files with version numbers (v1.0, v1.1, v2.0)
- Archive major versions before significant changes
- Add metadata: Program name, Document type, Date, Owner

---

### Teams Collaboration

**Program Channel Setup**:

1. Create dedicated Teams channel for each program (or use existing)
2. Pin key documents from SharePoint to Files tab
3. Use Channel conversations for:
   - Program updates
   - Refinement discussions (link to `/nuaa.refine` command outputs)
   - Feedback integration from consumer advisory groups
4. Schedule recurring meetings:
   - Monthly program review
   - Quarterly evaluation check-in

**Notification Workflow**:

- Post to channel when major documents updated (e.g., new proposal version)
- @mention stakeholders for review requests
- Use announcements for critical milestones (funding awarded, evaluation complete)

---

## Power Automate Workflows (Coming Q2 2026)

**Planned Automation Features**:

### Workflow 1: Auto-Save to SharePoint

**Trigger**: New or updated markdown file in NUAA-Kit folder  
**Action**: Convert to Word/PDF, save to SharePoint program folder  
**Benefit**: Automatic versioning and backup

### Workflow 2: Approval Process

**Trigger**: New proposal or report marked `status: final`  
**Action**: Send approval request to [Manager], notify on approval/rejection  
**Benefit**: Formalized review and sign-off

### Workflow 3: Reminder Notifications

**Trigger**: Scheduled (quarterly)  
**Action**: Send reminder to program coordinators to review/update documentation  
**Benefit**: Ensures documentation stays current

### Workflow 4: Budget Alert

**Trigger**: Budget variance >10% in Excel tracker  
**Action**: Alert program coordinator and finance team  
**Benefit**: Early warning of budget issues

**Status**: Design phase. Implementation requires Power Automate license and IT support. Timeline: Q2 2026.

---

## Word Template Specifications (Planned)

**Proposal Template** (`proposal-template.dotx`):

- NUAA branding (logo, colors, fonts)
- Pre-formatted sections matching `proposal.md` structure:
  - Executive Summary (1 page)
  - Program Overview
  - Methodology (with embedded logic model table)
  - Evaluation Plan (with indicator table)
  - Budget Summary (with category breakdown table)
  - Appendices
- Styles: Heading 1-3, Body text, Quote, Table
- Auto-generated Table of Contents
- Page numbering and headers/footers

**Report Template** (`report-template.dotx`):

- Similar branding and structure
- Sections matching `report.md` template
- Chart placeholders for data visualization
- Appendix structure for detailed tables

**Timeline**: Q2 2026 (requires graphic designer for branding consistency)

---

## Excel Dashboard Specifications (Planned)

**Budget Calculator Workbook** (`budget-calculator-template.xlsx`):

- Input sheet: All budget categories pre-formatted
- Calculations sheet: Automatic totals, percentages, variance analysis
- Sensitivity sheet: 80%/120% scenarios auto-calculated
- Charts: Budget allocation pie chart, category comparison bar chart
- Data validation: Dropdowns for categories, formulas protected

**Evaluation Dashboard** (`evaluation-dashboard-template.xlsx`):

- Indicator tracker: Process, Output, Outcome, Impact tabs
- Demographic disaggregation: Pivot tables by Aboriginal/TSI, gender, age, etc.
- Progress charts: Target vs. Actual visualizations
- Timeline: Gantt chart for evaluation milestones
- Export: Summary report auto-generated from data

**Impact Tracker** (`impact-tracker-template.xlsx`):

- Participant-level data entry (secure, privacy-compliant)
- Aggregate reporting (no individual data in reports)
- Outcome trends over time
- Equity analysis (disaggregated outcomes)
- Export to Word report format

**Timeline**: Q2 2026 (requires data analyst for formula design)

---

## Data Privacy & Security

**Principles**:

- All participant-level data must be stored securely with restricted access
- Aggregate/de-identified data only for reporting
- Informed consent for all data collection
- Regular backups (SharePoint provides automatic backups)
- Access controls: Program staff only, audited access logs

**SharePoint Security Settings**:

- Sensitivity labels: "NUAA Internal", "NUAA Confidential"
- Access permissions:
  - Program team: Full access
  - NUAA management: Read access
  - External partners: No access (share specific documents only)
- Encryption: Enable for folders containing participant data

**Excel Security**:

- Protect sensitive sheets (password-protected)
- Hide formulas to prevent accidental changes
- Use data validation to reduce errors
- Regular audit of who has access to files

---

## Training & Support

**Current Resources**:

- Microsoft 365 basics: [Microsoft Learn](https://learn.microsoft.com/en-us/training/)
- SharePoint: [NUAA IT support] (internal)
- Excel formulas: YouTube tutorials, Microsoft support

**NUAA-Specific Training** (Planned Q2 2026):

- 1-hour webinar: "Integrating NUAA-Kit with Microsoft 365"
- Step-by-step guides for common tasks
- Template walkthroughs (video demonstrations)
- Q&A sessions with program teams using integration

**Support Contacts**:

- NUAA IT Help Desk: [Contact details]
- Program Support: [Contact details]
- External consultant (if engaged): [Contact details]

---

## Troubleshooting

**Problem**: Markdown formatting lost when pasting to Word  
**Solution**: Use "Keep Source Formatting" paste option, or convert markdown to HTML first, then paste

**Problem**: Excel formulas breaking when copying budget tables  
**Solution**: Copy values only for static snapshots, or use linked workbooks for dynamic updates

**Problem**: SharePoint version history showing too many versions  
**Solution**: Enable major/minor versioning; only create major versions for significant changes

**Problem**: Teams channel cluttered with notifications  
**Solution**: Mute non-essential channels, use @mentions for important updates only

**Problem**: Difficulty finding documents in SharePoint  
**Solution**: Use metadata tagging (Program name, Document type, Date), implement folder structure consistently

---

## Roadmap & Timeline

| Quarter               | Features                                                               | Status      |
| --------------------- | ---------------------------------------------------------------------- | ----------- |
| **Q4 2025 (Current)** | Manual integration guidance (this document)                            | ✅ Complete |
| **Q1 2026**           | Word/Excel basic templates (unbranded)                                 | Planned     |
| **Q2 2026**           | Branded templates, Power Automate workflows (basic), training webinars | Planned     |
| **Q3 2026**           | Advanced dashboards, automated reporting, integration testing          | Planned     |
| **Q4 2026**           | Full rollout, staff training, continuous improvement                   | Planned     |

**Dependencies**:

- IT resources for Power Automate development
- Graphic designer for branded templates
- Budget for Microsoft 365 licenses (Power Automate Premium if advanced workflows needed)
- Staff capacity for training and change management

**Risk Mitigation**:

- Phased rollout: Start with manual methods (Q4 2025), automate incrementally
- Pilot with 1-2 programs before full rollout
- Regular feedback loops with program teams
- Fallback: Manual methods always available if automation fails

---

## Feedback & Iteration

**Share Your Needs**:

- What Microsoft 365 features would be most useful for your program?
- What manual tasks are most time-consuming that automation could address?
- What barriers are you experiencing with current integration methods?

**Contact**: [NUAA Program Support Team] or [Internal feedback channel]

**Version History**:

- v1.0 (2025-11-10): Initial guidance document with manual integration methods
- v2.0 (Planned 2026-Q2): Update with automated workflows and templates

---

**Status**: Phase 1 (Manual Integration) implemented. Phase 2 (Templates & Automation) planned for Q2 2026.
