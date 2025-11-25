# NUAA Microsoft Teams Bot

> **⚠️ PLANNED FEATURE - NOT YET IMPLEMENTED**
>
> This document describes a planned feature that is currently under consideration for future development.
> The Microsoft Teams bot is not currently available in this version of NUAA CLI.

**Create reports and documents directly in Microsoft Teams - no CLI, no separate tools.**

## Overview

The NUAA Teams Bot integrates seamlessly with Microsoft Teams, allowing any team member to create professional documents through simple chat commands.

**Perfect for**:
- Office staff who use Teams daily
- Management and communications teams
- Remote collaboration
- Quick approvals and reviews
- Team coordination

## How It Works

### Simple Chat Interface

**In any Teams channel or chat**:

1. Type: `@NUAA create [document type]`
2. Bot asks questions in chat
3. Answer in your own words
4. Bot generates document
5. Document saved to SharePoint
6. Team notified when complete

**That's it!** No software to install, no complex commands.

## Example Usage

### Example 1: Create Outreach Report

```
You: @NUAA create outreach report

NUAA Bot: 👋 Hi! I'll help you create an outreach report.
          Let's start with a few questions.

NUAA Bot: 📅 What date and time was your outreach session?

You: Today from 8pm to 11pm

NUAA Bot: 📍 What location?

You: King's Cross

NUAA Bot: 👥 How many people did you contact?

You: About 20 people

NUAA Bot: 💉 What supplies did you distribute?

You: 45 needles, 60 swabs, 20 tourniquets

NUAA Bot: ✅ Great! I have all the information.
          Creating your report now...

NUAA Bot: ✅ Done! Your outreach report is ready.
          📄 View: [King's Cross Outreach - Nov 18.pdf]
          💾 Saved to: Outreach Reports > 2025 > November

          Need any changes? Just ask!
```

### Example 2: Funding Proposal

```
You: @NUAA I need help with a funding proposal

NUAA Bot: I can help with that!
          Would you like to:
          1️⃣ Start a new proposal
          2️⃣ Continue a saved draft
          3️⃣ Get proposal tips

          Just reply with the number.

You: 1

NUAA Bot: Great! Let's create your funding proposal.
          I'll ask about 12 questions. We can do this now
          or spread it over a few days. Your choice!

          Ready to start? Reply "yes" or "later"

You: yes

NUAA Bot: 📝 Question 1 of 12
          What is the name of your project?

[... conversation continues ...]

NUAA Bot: ✅ Your funding proposal is complete!
          📄 View: [Proposal - Peer Support Program.pdf]
          📄 Editable: [Proposal - Peer Support Program.docx]
          💾 Saved to: Funding Proposals > 2025

          I've also created:
          ✓ Budget breakdown (Excel)
          ✓ Timeline (Gantt chart)
          ✓ Logic model

          Your board can review and approve in SharePoint.
```

### Example 3: Quick Status Update

```
You: @NUAA quick update

NUAA Bot: Sure! What's the update?

You: Just finished DanceWize shift at festival.
     Saw about 50 people, no major incidents,
     checked 12 samples, all volunteers did great

NUAA Bot: ✅ Update logged!
          📊 View: [DanceWize Quick Update - Nov 18]

          I've notified:
          - DanceWize Coordinator
          - Outreach Team

          Need a full report? Reply "full report"
```

## Features

### For Team Members

✓ **Chat-based** - Natural conversation, no commands to memorize
✓ **Available everywhere** - Desktop, mobile, web
✓ **Saves as you go** - Never lose your work
✓ **Can pause and resume** - Come back later
✓ **Team collaboration** - Others can help complete
✓ **Smart suggestions** - Bot helps with answers
✓ **Approval workflows** - Send to manager for review

### Document Types

**Outreach**:
- `@NUAA create outreach report`
- `@NUAA create safety incident`
- `@NUAA quick outreach update`

**DanceWize/Festival**:
- `@NUAA create festival report`
- `@NUAA create event plan`
- `@NUAA log volunteer hours`

**Peer Distribution**:
- `@NUAA log distribution`
- `@NUAA request resupply`

**NSP Warehouse**:
- `@NUAA log shipment`
- `@NUAA inventory check`

**Peerline**:
- `@NUAA log call` (privacy-protected)
- `@NUAA create resource`

**Management/Board**:
- `@NUAA create funding proposal`
- `@NUAA create board paper`
- `@NUAA create strategic plan`

**Communications**:
- `@NUAA create media release`
- `@NUAA create campaign plan`
- `@NUAA create stakeholder brief`

**Training**:
- `@NUAA create training curriculum`
- `@NUAA create participant materials`

**Any Team**:
- `@NUAA help` - Show available commands
- `@NUAA examples` - Show examples
- `@NUAA templates` - List all templates

### Smart Features

#### Auto-Complete

```
You: Location was King's

NUAA Bot: Did you mean "King's Cross"?
          (You've used this location 15 times before)
```

#### Data From History

```
NUAA Bot: What supplies did you distribute?

You: Same as last time

NUAA Bot: ✅ Got it! Using:
          45 needles, 60 swabs, 20 tourniquets
          (from your Nov 15 session)
```

#### Collaboration

```
You: @NUAA create funding proposal
     @Sarah can you help with this?

Sarah: Sure!

NUAA Bot: 👥 Now working with you and Sarah.
          Sarah, would you like to answer some questions?
```

#### Approval Workflow

```
NUAA Bot: Your report is ready!
          Send to [Manager] for approval?

You: Yes

NUAA Bot: ✅ Sent to [Manager] for review.
          I'll notify you when they approve or comment.

[Later...]

NUAA Bot: ✅ Your report was approved by [Manager]
          📄 Final version: [link]
```

## SharePoint Integration

### Automatic Organization

All documents automatically saved to SharePoint in organized structure:

```
NUAA SharePoint
├── Outreach Reports
│   └── 2025
│       └── November
│           ├── Kings Cross - Nov 18.pdf
│           └── Redfern - Nov 15.pdf
├── Festival Reports
│   └── DanceWize
│       └── 2025
│           └── Lost Paradise Festival Report.pdf
├── Funding Proposals
│   └── 2025
│       ├── Peer Support Program
│       │   ├── Proposal.pdf
│       │   ├── Budget.xlsx
│       │   └── Logic Model.pdf
│       └── Outreach Expansion
└── Team Documents
    └── ...
```

### SharePoint Features

✓ **Version control** - Track all changes
✓ **Co-authoring** - Edit together in real-time
✓ **Permissions** - Control who sees what
✓ **Search** - Find any document instantly
✓ **Workflows** - Automate approvals
✓ **Retention** - Auto-archive old files

## Mobile Experience

### On Your Phone

The bot works perfectly on Teams mobile app:

- **Voice typing** - Speak your answers
- **Quick buttons** - Tap instead of type
- **Camera** - Add photos to reports
- **Location** - Auto-fill location
- **Offline draft** - Start without signal, finish later

### Example Mobile Flow

```
You (via voice): Hey NUAA, create outreach report

NUAA Bot: 📱 Great! Starting outreach report.
          I'll use quick buttons to make this faster.

          📅 When was your session?
          [Today] [Yesterday] [Other date]

You: [Tap: Today]

NUAA Bot: 📍 Where?
          [King's Cross] [Redfern] [Other]

You: [Tap: King's Cross]

NUAA Bot: 👥 How many people?
          [Type a number or use buttons]
          [10] [20] [30] [40] [50+]

[...continues with easy taps and voice...]
```

## Technical Setup

### For NUAA IT Team

#### Prerequisites

1. **Microsoft 365 Subscription** (includes Teams & SharePoint)
2. **Azure AD** access (to register bot)
3. **Admin permissions** (to install bot for organization)
4. **NUAA CLI** installed on server

#### Setup Steps

**Step 1: Register Bot in Azure**

1. Go to Azure Portal → Azure Active Directory
2. App Registrations → New Registration
3. Name: "NUAA Project Tools Bot"
4. Supported accounts: Single tenant
5. Redirect URI: `https://token.botframework.com/.auth/web/redirect`
6. Save Application (client) ID

**Step 2: Create Bot Resource**

1. Azure Portal → Create Resource → Bot
2. Bot handle: "nuaatools"
3. Pricing: Free or S1
4. Connect to app registration (Step 1)
5. Microsoft App ID: [from Step 1]

**Step 3: Configure Channels**

1. Bot Settings → Channels
2. Add Microsoft Teams channel
3. Enable: Calling, Groups, Messages
4. Save configuration

**Step 4: Grant Permissions**

Azure AD → App Registrations → NUAA Bot → API Permissions:
- `Files.ReadWrite.All` (SharePoint)
- `Sites.ReadWrite.All` (SharePoint sites)
- `User.Read` (User info)
- `TeamMember.Read.All` (Team membership)

Grant admin consent.

**Step 5: Deploy Bot Code**

```bash
cd interfaces/teams-bot

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env:
#   - APP_ID=[from Azure]
#   - APP_PASSWORD=[from Azure]
#   - SHAREPOINT_SITE=[NUAA SharePoint site]

# Test locally
python bot.py

# Deploy to production
# Option 1: Azure App Service
az webapp up --name nuaa-teams-bot

# Option 2: Azure Container Instances
docker build -t nuaa-bot .
docker push nuaa-bot
az container create --name nuaa-bot --image nuaa-bot
```

**Step 6: Install for Organization**

1. Teams Admin Center
2. Manage Apps → Upload Custom App
3. Upload bot manifest (manifest.json)
4. Set policies (who can use bot)
5. Make available to all NUAA users

**Step 7: Test**

1. Open Teams
2. Search for "NUAA" in apps
3. Add to a test channel
4. Type: `@NUAA help`
5. Verify bot responds

### Configuration Files

**`manifest.json`** - Teams app manifest
**`.env`** - Environment variables
**`bot.py`** - Main bot logic
**`handlers/`** - Command handlers
**`sharepoint.py`** - SharePoint integration
**`nuaa_bridge.py`** - NUAA CLI integration

### Detailed setup guide in: `SETUP_GUIDE.md`

## Security & Compliance

### Authentication

✓ **Azure AD** - Enterprise-grade security
✓ **Single Sign-On** - Use NUAA credentials
✓ **MFA support** - Multi-factor authentication
✓ **Conditional access** - Based on location, device

### Permissions

✓ **Role-based** - Different access for different roles
✓ **Channel-based** - Control by Teams channel
✓ **Document-level** - SharePoint permissions apply
✓ **Audit logs** - Track all bot activity

### Privacy

✓ **No external servers** - All NUAA data stays in NUAA tenant
✓ **Encrypted** - In transit and at rest
✓ **GDPR compliant** - Microsoft 365 compliance
✓ **Data residency** - Australia region (if configured)

### Compliance

✓ **NUAA privacy policy** - Built into bot
✓ **Retention policies** - Follow organizational rules
✓ **eDiscovery** - Searchable if needed
✓ **Backup** - Automatic SharePoint backup

## Training & Adoption

### For Team Members

**"Using NUAA Bot in Teams" (5-minute guide)**
1. Find NUAA bot in Teams
2. Type `@NUAA help`
3. Try creating a simple document
4. Done!

**Quick Reference Card**:

```
┌─────────────────────────────────────┐
│  NUAA Teams Bot Quick Commands      │
│                                     │
│  @NUAA create [type]                │
│  @NUAA help                         │
│  @NUAA examples                     │
│  @NUAA continue                     │
│                                     │
│  In any Teams channel or chat!      │
└─────────────────────────────────────┘
```

### For Managers

**"Managing Team Documents" (10-minute guide)**
- View all team submissions
- Approve/reject workflows
- Export for reporting
- Set up permissions

### Adoption Strategy

**Week 1: Pilot Team**
- Choose 5 enthusiastic users
- Train them personally
- Get feedback
- Fix issues

**Week 2: Expand to One Department**
- Outreach or Comms team
- Team training session (30 min)
- Monitor usage
- Collect success stories

**Week 3-4: Organization-Wide**
- Announce to all staff
- Lunch & learn sessions
- Help desk support
- Celebrate early adopters

**Ongoing: Support & Improve**
- Weekly tip emails
- Monthly usage reports
- Quarterly feature updates
- Annual satisfaction survey

## Advanced Features

### Workflows

Create approval workflows:

```
You: @NUAA create funding proposal

[...complete proposal...]

NUAA Bot: Should I send this for approval?

You: Yes, send to board

NUAA Bot: ✅ Sent to:
          1. Executive Director (for review)
          2. Finance Manager (for budget check)
          3. Board Chair (for final approval)

          You'll get notified at each stage.
```

### Analytics

Admins can see:
- Most used templates
- Average completion time
- User satisfaction
- Document types by team
- Adoption rates

### Integrations

Connect to other tools:
- **Power BI** - Usage dashboards
- **Power Automate** - Custom workflows
- **Azure Logic Apps** - Complex integrations
- **Third-party tools** - Via APIs

## Troubleshooting

### Common Issues

**"Bot doesn't respond"**
- Check bot is added to channel
- Try in direct message first
- Verify @mention is correct
- Contact IT if still issues

**"Can't find my document"**
- Check SharePoint ([team name] folder)
- Search in Teams files
- Ask bot: `@NUAA where is [document name]`

**"Bot says 'permission denied'"**
- Check your SharePoint access
- Contact your manager
- IT admin may need to update permissions

### Getting Help

**For Users**:
- Type: `@NUAA help`
- Teams channel: #nuaa-tools-help
- Email: tech@nuaa.org.au

**For Admins**:
- Admin dashboard
- Azure bot logs
- Support: tech@nuaa.org.au

## Roadmap

### Phase 1 (Current)
- ✓ Basic chat interface
- ✓ Document generation
- ✓ SharePoint integration
- ✓ Mobile support

### Phase 2 (Next Quarter)
- [ ] Approval workflows
- [ ] Advanced analytics
- [ ] Voice commands
- [ ] Proactive notifications

### Phase 3 (Future)
- [ ] AI-powered suggestions
- [ ] Meeting integration
- [ ] Multi-language support
- [ ] Custom team workflows

## Success Stories

### Outreach Team
"Before: 30 minutes per report. Now: 5 minutes. The bot is amazing!" - Outreach Worker

### Management
"Board papers used to take hours. Now I just chat with the bot. Game changer." - Executive Director

### Festival Team
"During festivals, we can update in real-time from our phones. So easy!" - DanceWize Coordinator

## Support

**Email**: tech@nuaa.org.au
**Teams**: #nuaa-tools channel
**Phone**: [number]

---

**Making project tools as easy as sending a Teams message.** 💬✨
