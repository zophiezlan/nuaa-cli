# Universal Access Plan for NUAA Teams

## Vision

**Every NUAA team member can contribute to project design, proposals, and impact measurement—regardless of technical skill level.**

## Team Access Profiles

### 1. Email-Only Users

**Who**: Board members, community partners, some peer distributors
**Comfort Level**: Email only
**Solution**: Email-to-NUAA bridge

#### How It Works

1. Send email to `nuaa@nuaa.org.au` with subject line indicating task
2. Email contains simple prompts or form fields
3. System processes request and sends back formatted results
4. No software installation required

**Example Email Workflow**:

```
To: nuaa@nuaa.org.au
Subject: Create Outreach Event Plan

Event Name: King's Cross Outreach
Date: March 15, 2025
Location: King's Cross, Sydney
Expected Participants: 50 people
Services: Harm reduction info, NSP, BBV testing
```

**Response**: Receives complete event plan document via email attachment

### 2. Mobile-Only Users

**Who**: Outreach workers, festival teams, peer distributors, field staff
**Comfort Level**: Smartphones, apps
**Solution**: Mobile web interface + SMS

#### Mobile Web (Progressive Web App)

- Works on any smartphone browser
- No app store download needed
- Works offline for field use
- Large buttons, simple navigation
- Voice input option

#### SMS Interface

- Text short codes to create reports
- Useful for quick field updates
- Example: Text "NSP 50 needles 10 people Kings Cross" → Auto-generates distribution report

### 3. Microsoft Teams Users

**Who**: Office staff, management, comms, advocacy
**Comfort Level**: Teams, email, Office 365
**Solution**: NUAA Teams Bot

#### Teams Bot Features

- Type `/nuaa design outreach program` in any Teams channel
- Bot guides through questions in chat
- Generates documents directly to SharePoint
- Notifies team when complete
- No CLI knowledge needed

### 4. SharePoint/Forms Users

**Who**: Training, org services, workforce development
**Comfort Level**: Web forms, SharePoint
**Solution**: SharePoint-embedded forms

#### SharePoint Integration

- Pre-built forms for each template type
- Fill out form → Auto-generates document
- Saves to team SharePoint library
- Version control built-in
- Can collaborate on same form

### 5. Basic Computer Users

**Who**: Peerline, some advocacy staff, warehouse/shipping
**Comfort Level**: Web browsers, basic desktop
**Solution**: Simple web interface

#### Web Dashboard Features

- Click-based navigation (no typing commands)
- Visual progress bars
- "Wizard" mode: one question at a time
- Template library with examples
- Auto-save (never lose work)
- Print-friendly outputs

### 6. Advanced Users

**Who**: Some comms staff, IT-savvy team members
**Comfort Level**: CLI, automation
**Solution**: Current CLI + API

#### Existing Features

- Full CLI access
- GitHub integration
- Slash commands for AI assistants
- Python scripting
- API for custom integrations

## Team-Specific Workflows

### Outreach Team

**Primary Needs**: Quick field reports, event planning, safety protocols
**Best Interface**: Mobile web + SMS
**Templates**:

- Outreach session report
- Safety incident documentation
- Engagement statistics
- Service delivery summary

**Example SMS Workflow**:

```
Text: "Outreach KingsX 20 contacts 45 needles"
Receives: "Report saved. View at: [link]"
```

### Festival/DanceWize Team

**Primary Needs**: Event planning, drug checking reports, volunteer coordination
**Best Interface**: Mobile web + Teams
**Templates**:

- Festival preparation plan
- Drug checking session report
- Volunteer roster and briefing
- Incident reporting

**Teams Workflow**:

```
In Teams: @NUAA create festival plan
Bot asks: Festival name? Date? Location? Services?
Team answers in chat
Bot generates: Complete festival plan in SharePoint
```

### NSP Warehouse/Shipping

**Primary Needs**: Inventory tracking, distribution reports, supplier coordination
**Best Interface**: Web forms + Email
**Templates**:

- Distribution report
- Inventory reconciliation
- Supplier order
- Delivery schedule

**Web Form Workflow**:

1. Open "NSP Distribution Report" form
2. Fill in: Date, recipient, items, quantities
3. Click "Generate Report"
4. PDF auto-emails to coordinator

### Peer Distributors

**Primary Needs**: Simple distribution tracking, contact reporting
**Best Interface**: SMS + Mobile web
**Templates**:

- Distribution log (simplified)
- Contact summary
- Re-supply request

**SMS Workflow**:

```
Text: "Distributed 30 needles 5 people Redfern"
Receives: "Logged. Need re-supply? Reply YES/NO"
```

### Comms/Advocacy

**Primary Needs**: Campaign planning, media releases, impact reports
**Best Interface**: Teams + Web + CLI
**Templates**:

- Campaign strategy
- Media release
- Impact statement
- Stakeholder briefing

**Teams Workflow**:

```
@NUAA create campaign strategy
Topic: Pill testing legislation
Target: NSW Parliament
Timeline: 3 months
→ Generates comprehensive campaign plan
```

### Training Team

**Primary Needs**: Curriculum development, participant materials, evaluation
**Best Interface**: SharePoint forms + Web
**Templates**:

- Training curriculum
- Participant handbook
- Evaluation framework
- Facilitator guide

**SharePoint Workflow**:

1. Navigate to "Training Tools" library
2. Click "New Curriculum"
3. Fill out structured form
4. Auto-generates full curriculum document
5. Saves to SharePoint with version history

### Peerline

**Primary Needs**: Call logging, resource creation, peer support materials
**Best Interface**: Web dashboard
**Templates**:

- Call summary template
- Resource guide
- Peer support protocol
- Referral pathway

**Web Dashboard**:

- Large "Create Call Summary" button
- Simple form: Caller needs, information provided, referrals
- One-click save
- Searchable call history

### Board/Management

**Primary Needs**: Strategic planning, funding proposals, impact reporting
**Best Interface**: Email + SharePoint
**Templates**:

- Strategic plan
- Funding proposal
- Impact report
- Board paper

**Email Workflow**:

```
Email: nuaa@nuaa.org.au
Subject: Create Funding Proposal
Body: (Fill simple questionnaire)
→ Receives: Professional funding proposal as Word doc
```

### BBV Testing/Prevention

**Primary Needs**: Testing protocols, education materials, referral pathways
**Best Interface**: Mobile web + Web forms
**Templates**:

- Testing session plan
- Client education handout
- Referral protocol
- Session statistics

### Workforce Development

**Primary Needs**: Position descriptions, onboarding materials, career pathways
**Best Interface**: SharePoint + Web
**Templates**:

- Position description
- Onboarding checklist
- Professional development plan
- Career pathway mapping

## Implementation Priority

### Phase 1: Immediate (Week 1-2)

1. ✅ Enhanced CLI accessibility (already complete)
2. 🔄 Team-specific template library
3. 🔄 Simplified web interface (local hosting)
4. 🔄 Comprehensive user guides for each team

### Phase 2: Near-Term (Week 3-4)

1. Microsoft Teams bot
2. SharePoint integration
3. Mobile-responsive web interface
4. Email-to-NUAA bridge

### Phase 3: Medium-Term (Month 2-3)

1. SMS interface for field workers
2. Progressive Web App (offline support)
3. Voice input for accessibility
4. Multi-language interfaces (6 languages already supported in CLI)

### Phase 4: Long-Term (Month 4-6)

1. Power Automate connectors
2. Mobile native apps
3. API for third-party integrations
4. Advanced analytics dashboard

## Technical Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interfaces                       │
├──────────┬──────────┬──────────┬──────────┬─────────────┤
│  Email   │  SMS     │  Teams   │SharePoint│  Web App    │
│  Bridge  │Interface │   Bot    │  Forms   │  (Mobile)   │
└────┬─────┴────┬─────┴────┬─────┴────┬─────┴──────┬──────┘
     │          │          │          │            │
     └──────────┴──────────┴──────────┴────────────┘
                         │
                    ┌────▼────┐
                    │   API   │
                    │ Gateway │
                    └────┬────┘
                         │
                ┌────────▼─────────┐
                │   NUAA CLI Core  │
                │  (Current Code)  │
                └────────┬─────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼─────┐    ┌────▼─────┐    ┌────▼─────┐
   │Templates │    │ AI Agent │    │  Output  │
   │ Library  │    │  System  │    │Generator │
   └──────────┘    └──────────┘    └──────────┘
```

## Accessibility Standards

All interfaces must meet:

### Technical Standards

- ✅ WCAG 2.1 AAA compliance
- ✅ Screen reader compatible
- ✅ Keyboard navigation only (no mouse required)
- ✅ High contrast mode
- ✅ Dyslexia-friendly fonts and spacing
- ✅ Mobile responsive (works on all screen sizes)

### Cultural Standards

- ✅ Person-first, non-stigmatizing language
- ✅ Harm reduction philosophy
- ✅ Aboriginal and Torres Strait Islander protocols
- ✅ LGBTIQ+ inclusive
- ✅ Trauma-informed design
- ✅ Multi-language support (6 languages)

### Usability Standards

- ✅ Grade 8-10 reading level
- ✅ No jargon without explanation
- ✅ Clear error messages with recovery steps
- ✅ Progress indicators
- ✅ Auto-save functionality
- ✅ Works offline where possible

## Training and Support

### For Each Team Type

1. **15-minute Quick Start Guide** (role-specific)
2. **Video Tutorial** (< 5 minutes, accessible)
3. **One-page Cheat Sheet** (printable, large text)
4. **Peer Supporter** (designated team member)
5. **Help Desk** (email/phone support)

### Training Materials Include

- Screenshots with annotations
- Step-by-step workflows
- Common scenarios for that team
- Troubleshooting guide
- Contact for help

## Success Metrics

### Adoption Targets

- **90%** of team members able to use at least one interface
- **100%** of teams have access through their preferred method
- **<5 minutes** average time to complete simple tasks
- **<15 minutes** average time to complete complex tasks
- **Zero** technical barriers to participation

### Satisfaction Targets

- Interface is "easy to use" (8+ /10)
- Feels "culturally safe" (9+ /10)
- Would "recommend to colleagues" (90%+)
- Reduces "administrative burden" (80%+)

## Support Contacts

### For Technical Issues

- Email: tech@nuaa.org.au
- Phone: [number]
- Teams: #nuaa-help channel

### For Content Questions

- Email: projects@nuaa.org.au
- Peer Support: [designated contact]

## Next Steps

1. **Gather Team Feedback**: Survey each team about their preferences
2. **Pilot Testing**: Start with 2-3 enthusiastic teams
3. **Iterate**: Refine based on real-world usage
4. **Roll Out Gradually**: One team type at a time
5. **Continuous Improvement**: Monthly check-ins with users

---

**Last Updated**: 2025-11-18
**Version**: 1.0
**Owner**: NUAA Project Team
**Review Date**: 2026-02-18 (3 months)
