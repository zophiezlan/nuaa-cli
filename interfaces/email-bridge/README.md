# NUAA Email Bridge

**Make NUAA tools accessible via email for users who only use email.**

## Overview

The Email Bridge allows NUAA team members to create reports and documents by simply sending an email. No software installation, no command line, no web browsers required.

**Perfect for**:
- Board members who only use email
- Remote workers with limited technology
- Older staff members comfortable with email only
- Quick submissions from anywhere
- Accessible technology for everyone

## How It Works

### Simple Version (Guided)

1. **Send email** to: `nuaa@nuaa.org.au`
2. **Subject**: The type of document you want (e.g., "Outreach Report")
3. **System replies** with questions
4. **You reply** with your answers
5. **System sends back** completed document

### Advanced Version (One Email)

1. **Send email** to: `nuaa@nuaa.org.au`
2. **Subject**: Document type
3. **Body**: Fill in the template (sent to you first time)
4. **Get back**: Professional formatted document

## Example Usage

### Example 1: Outreach Report

**Email 1 (You send)**:

```
To: nuaa@nuaa.org.au
Subject: Outreach Report

Hi, I need to submit my outreach report for today.
```

**Email 2 (System sends)**:

```
From: NUAA Tools <nuaa@nuaa.org.au>
Subject: Re: Outreach Report - Question 1 of 5

Hi! I'll help you create your outreach report.

Question 1: What date and time was your session?

Please reply with your answer.

Tips:
- Keep your answer simple
- You can skip questions by typing "skip"
- Type "help" if you need assistance
```

**Email 3 (You reply)**:

```
November 18, 2025, from 8pm to 11pm
```

*(System continues asking questions...)*

**Final Email (System sends)**:

```
From: NUAA Tools <nuaa@nuaa.org.au>
Subject: Your Outreach Report is Ready

Hi! Your outreach report has been created.

Attached:
- outreach-report-2025-11-18.pdf
- outreach-report-2025-11-18.docx

The report has been saved and shared with your coordinator.

Need to make changes? Just reply to this email.

Thank you for your work!
```

### Example 2: Quick Update (SMS-style)

**You send**:

```
To: nuaa@nuaa.org.au
Subject: Quick Outreach Update

Kings Cross outreach tonight
20 contacts, 45 needles distributed
All good, no incidents
Need resupply by Friday
```

**System replies**:

```
From: NUAA Tools <nuaa@nuaa.org.au>
Subject: Quick Update Received

Thanks! Your update has been logged.

Summary:
✓ Location: King's Cross
✓ Contacts: 20 people
✓ Needles: 45 distributed
✓ Status: All good
✓ Resupply: Requested for Friday

Your coordinator has been notified about the resupply request.

Need more details added? Reply to this email.
```

## Document Types Available

### Outreach Team
- **Subject**: Outreach Report
- **Subject**: Outreach Quick Update
- **Subject**: Safety Incident

### Peer Distributors
- **Subject**: Distribution Log
- **Subject**: Resupply Request

### DanceWize/Festival
- **Subject**: Festival Report
- **Subject**: Event Plan

### Peerline
- **Subject**: Call Log
- **Subject**: Resource Request

### NSP Warehouse
- **Subject**: Shipment Log
- **Subject**: Inventory Update

### Board/Management
- **Subject**: Funding Proposal
- **Subject**: Board Paper
- **Subject**: Strategic Plan

### All Teams
- **Subject**: General Report
- **Subject**: Help Me Choose

(Type "Help Me Choose" if you're not sure which template you need)

## Features

### For Users

✓ **No software to install** - Just your email
✓ **Works on any device** - Phone, tablet, computer
✓ **Works with any email service** - Gmail, Outlook, Yahoo, etc.
✓ **Guided questions** - Step by step
✓ **Forgiving** - Can skip questions, make mistakes
✓ **Save and resume** - Come back later
✓ **Get help anytime** - Type "help" in any email

### For Coordinators

✓ **All submissions logged** - Nothing gets lost
✓ **Automatic formatting** - Professional documents every time
✓ **Email notifications** - Know when reports come in
✓ **Easy to manage** - Web dashboard shows all submissions
✓ **Searchable** - Find any past report
✓ **Export options** - PDF, Word, Excel

## Technical Implementation

### Architecture

```
┌─────────────┐
│   User      │
│   Email     │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Email Server   │
│  (IMAP/SMTP)    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Email Bridge   │
│  Python Script  │
│  - Parse email  │
│  - Run NUAA CLI │
│  - Format reply │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  NUAA CLI Core  │
│  Generate docs  │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Send Reply     │
│  with Document  │
└─────────────────┘
```

### Components

1. **Email Listener** (`email_listener.py`)
   - Monitors NUAA inbox via IMAP
   - Parses incoming emails
   - Extracts subject, body, sender

2. **Conversation Manager** (`conversation.py`)
   - Tracks multi-email conversations
   - Remembers context
   - Manages state

3. **Template Matcher** (`matcher.py`)
   - Matches subject to template
   - Suggests alternatives if unclear
   - Handles typos/variations

4. **Question Engine** (`questions.py`)
   - Extracts questions from templates
   - Sends one at a time
   - Validates answers

5. **Document Generator** (`generator.py`)
   - Calls NUAA CLI
   - Generates documents
   - Formats for email

6. **Email Sender** (`sender.py`)
   - Sends formatted replies
   - Attaches documents
   - Handles errors gracefully

### Requirements

```python
# requirements.txt
imaplib3
smtplib
email
python-dotenv
nuaa-cli
```

### Configuration

```bash
# .env file
EMAIL_HOST=imap.gmail.com
EMAIL_PORT=993
EMAIL_USER=nuaa@nuaa.org.au
EMAIL_PASSWORD=[app-specific-password]
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

### Setup Instructions

#### For NUAA IT Team

1. **Create dedicated email account**:
   - Email: `nuaa@nuaa.org.au` (or `nuaa-tools@nuaa.org.au`)
   - Enable IMAP access
   - Create app-specific password

2. **Install the bridge**:

   ```bash
   cd interfaces/email-bridge
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with email credentials
   ```

3. **Test the connection**:

   ```bash
   python test_connection.py
   ```

4. **Run the bridge**:

   ```bash
   python email_bridge.py
   ```

5. **Set up as service** (runs automatically):

   ```bash
   # Linux/Mac
   sudo cp nuaa-email-bridge.service /etc/systemd/system/
   sudo systemctl enable nuaa-email-bridge
   sudo systemctl start nuaa-email-bridge

   # Windows
   # Use Task Scheduler or NSSM
   ```

6. **Monitor logs**:

   ```bash
   tail -f logs/email-bridge.log
   ```

#### For Microsoft 365

If NUAA uses Microsoft 365:

1. **Use Microsoft Graph API** (recommended)
2. **Create app registration** in Azure AD
3. **Grant permissions**: Mail.Read, Mail.Send
4. **Use OAuth2** instead of passwords

See `microsoft365/EMAIL_BRIDGE_M365.md` for detailed setup.

## Security & Privacy

### Email Security

✓ **Encrypted connection** (TLS/SSL)
✓ **No passwords stored** (use OAuth or app passwords)
✓ **Automatic timeout** (sessions expire)
✓ **No sensitive data in subject lines**
✓ **Audit log** of all emails

### Privacy Protection

✓ **No names in logs** (only email addresses)
✓ **Documents encrypted** at rest
✓ **Automatic deletion** of old emails (configurable)
✓ **GDPR compliant**
✓ **Follows NUAA privacy policies**

### Anti-Spam

✓ **Sender verification** (only known NUAA emails)
✓ **Rate limiting** (prevents abuse)
✓ **Malware scanning** (attachments)
✓ **Suspicious activity alerts**

## Advanced Features

### Auto-Fill from Previous Submissions

The system remembers your previous answers:

```
Question: What's your location?

Your last answer was: "King's Cross"
Press Enter to use this, or type a new location:
```

### Smart Parsing

The system understands natural language:

**You write**: "20 people, gave out 45 needles and 30 swabs"

**System extracts**:
- People contacted: 20
- Needles distributed: 45
- Swabs distributed: 30

### Attachments

**Send photos** with your email:
- Photos of session
- Receipts
- Supporting documents

**System automatically**:
- Includes in report
- Compresses if needed
- Stores securely

### Mobile Email Apps

Works perfectly with:
- Gmail app
- Outlook app
- Apple Mail
- Any email app!

**Voice-to-email**:
- Use phone's voice typing
- System handles imperfect transcription
- Will ask for clarification if unclear

## Training Materials

### For End Users

**"Submitting Reports via Email" Guide** (1 page)
- Send email to nuaa@nuaa.org.au
- Put document type in subject
- Follow the questions
- Get your document back!

**Video Tutorial** (3 minutes)
- Watch someone send an email report
- See the questions and answers
- See the final document

**Quick Reference Card** (business card size)

```
┌─────────────────────────────────┐
│  NUAA Email Reports             │
│                                 │
│  To: nuaa@nuaa.org.au          │
│                                 │
│  Subject Examples:              │
│  - Outreach Report              │
│  - Distribution Log             │
│  - Festival Report              │
│  - Help Me Choose               │
│                                 │
│  Questions? Reply "help"        │
└─────────────────────────────────┘
```

### For Coordinators

**"Managing Email Submissions" Guide** (5 pages)
- How to view submissions
- How to help users
- How to export data
- Troubleshooting

**Admin Dashboard**:
- See all submissions
- Search by date/team/person
- Export to Excel
- Generate reports

## Troubleshooting

### Common Issues

**Issue**: "I sent an email but got no response"
**Solution**:
1. Check spam folder
2. Verify email address (nuaa@nuaa.org.au)
3. Try again in 5 minutes
4. Contact tech support if still not working

**Issue**: "System doesn't understand my answer"
**Solution**:
- Try shorter, simpler answers
- Use numbers for quantities
- One fact per line
- Type "help" to get examples

**Issue**: "I made a mistake in my answer"
**Solution**:
- Reply "back" to go to previous question
- Or finish and ask for edits at the end
- Or reply to final email with corrections

### Getting Help

**For Users**:
- Reply "help" to any system email
- Email: tech@nuaa.org.au
- Call: [phone]

**For Coordinators**:
- Dashboard: https://tools.nuaa.org.au/admin
- Email: tech@nuaa.org.au
- Phone support: [phone]

## Roadmap

### Phase 1 (Current)
- ✓ Basic email parsing
- ✓ Question-answer flow
- ✓ Document generation
- ✓ PDF/Word attachments

### Phase 2 (Next Month)
- [ ] Smart answer parsing
- [ ] Auto-fill from history
- [ ] Photo attachments
- [ ] Multi-language support

### Phase 3 (Future)
- [ ] Voice message support
- [ ] SMS integration
- [ ] WhatsApp integration
- [ ] AI assistant for complex queries

## Success Metrics

### Usage
- Target: 50% of reports via email within 3 months
- Track: Number of submissions per day
- Goal: Make reporting easier for everyone

### Satisfaction
- Survey users monthly
- Target: 90% find it "easy" or "very easy"
- Collect feedback for improvements

### Quality
- Error rate < 5%
- Response time < 2 minutes
- Document accuracy 100%

## Support

**Email**: tech@nuaa.org.au
**Phone**: [number]
**Teams**: #nuaa-tools channel

---

**Making NUAA tools accessible to everyone, one email at a time.** 📧
