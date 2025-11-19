# NUAA Web Interface

**Version 2.1.0** - Enhanced with exceptional UX improvements

A comprehensive, accessible web interface for NUAA teams who don't use command-line tools.

## 🎉 What's New in v2.1 (November 2025)

✨ **Professional Toast Notifications** - Beautiful, non-intrusive feedback
⌨️ **Keyboard Shortcuts Overlay** - Press `?` to see all shortcuts
🧭 **Enhanced Navigation** - Breadcrumbs and improved mobile menu
📱 **Better Mobile Experience** - Optimized touch targets and gestures
🚀 **Improved Performance** - Faster loading and smoother interactions
♿ **Enhanced Accessibility** - Even better screen reader support

See [WEBUI_IMPROVEMENTS.md](WEBUI_IMPROVEMENTS.md) for complete details.

## Features Overview

### 🚀 Progressive Web App (PWA)

- **Install as native app** on phones, tablets, and desktops
- **Offline support** - Works completely without internet after first load
- **Background sync** - Automatically syncs when back online

### 📝 Advanced Form Features

- **Dynamic form generation** from markdown templates
- **Auto-save every 30 seconds** - Never lose your work
- **Voice input** for all text fields (🎤 button)
- **Real-time validation** with helpful error messages
- **Camera integration** - Take photos directly in the form

### 🎨 Enhanced Dashboard

- **Real-time statistics** - Documents created, recent activity
- **Search functionality** - Find any document instantly (Ctrl+K)
- **Quick report** feature - Create reports in seconds (Ctrl+Q)

### 📤 Export & Integration

- **Export to multiple formats** - PDF, Word, Excel, HTML, plain text
- **Email integration** - Send reports directly from the app

### 🔐 Security Features

- **CSRF protection** - Prevents cross-site attacks
- **Rate limiting** - Prevents abuse (100 requests/hour)
- **Secure file uploads** - Validated file types and sizes

### ♿ Enhanced Accessibility

- **WCAG 2.1 AAA compliant** - Industry-leading accessibility
- **Multiple color schemes** - Default, high-contrast, warm, cool
- **Font size options** - Small, normal, large, extra-large
- **Screen reader optimized** - Works perfectly with NVDA, JAWS, VoiceOver

## Quick Start

### For NUAA Staff Setting Up

1. **Install Python requirements**:

   ```bash
   pip install flask flask-cors markdown pandas
   ```

2. **Start the web server**:

   ```bash
   cd interfaces/web-simple
   python app.py
   ```

3. **Open in browser**:
   - Go to: `http://localhost:5000`
   - Or on network: `http://[your-ip]:5000`

### For Team Members Using the Interface

1. **Open the link** your coordinator gave you (or go to `http://localhost:5000`)
2. **Click on your team** (Outreach, DanceWize, Peerline, etc.)
3. **Choose a template** (like "Session Report" or "Distribution Log")
4. **Fill in the form** - Just type in the boxes
5. **Click Submit** - Your document is automatically created!

## Team-Specific Features

### Outreach Team

- **Quick session reports** from the field
- **SMS integration** (coming soon) for ultra-fast updates
- **Photo upload** for visual documentation

### Festival/DanceWize

- **Real-time reporting** during events
- **Shift handover forms**
- **Incident logging**

### Peer Distributors

- **Simple distribution logs** (30 seconds to complete)
- **Resupply requests** with one click
- **SMS quick submit** option

### NSP Warehouse

- **Shipment tracking**
- **Inventory forms**

## API Documentation

The interface provides a RESTful API for integrations.

- `GET /api/stats/<team_id>` - Get team statistics
- `GET /api/documents/<team_id>` - Get team documents
- `GET /api/search/<team_id>?q=query` - Search documents
- `GET /api/export/<team_id>/<doc_id>/<format>` - Export document
- `GET /api/analytics` - Get global analytics
- **Barcode scanning** (coming soon)

### Peerline

- **Call logs** with privacy protection
- **Resource tracking**
- **Referral templates**

### Board/Management

- **Funding proposals** via email
- **Strategic planning** templates
- **Impact reports** auto-generated

### All Teams

- **Search past reports**
- **Export to PDF/Word**
- **Share with team members**
- **Print-friendly versions**

## Accessibility Features

### Vision

- ✓ High contrast mode
- ✓ Large text mode
- ✓ Screen reader compatible (NVDA, JAWS, VoiceOver)
- ✓ No color-only indicators
- ✓ Keyboard navigation only (no mouse needed)

### Cognitive

- ✓ Simple, clear language
- ✓ One question at a time option
- ✓ Progress indicators
- ✓ Clear error messages
- ✓ Auto-save (never lose work)

### Motor

- ✓ Large click targets (easy for touch screens)
- ✓ Voice input supported (browser feature)
- ✓ No precise movements required
- ✓ Keyboard shortcuts available

### Language

- ✓ Plain language (no jargon)
- ✓ Multi-language support (coming soon)
- ✓ Tooltips explain everything
- ✓ Help always available

## Mobile Features

### Works Great On Phones

- **Responsive design** - Adapts to any screen size
- **Touch-friendly** - Large buttons, easy to tap
- **Works offline** - Use in the field without signal
- **Camera integration** - Take photos for reports
- **GPS location** (optional) - Auto-fill location fields
- **Quick submit** - Minimal typing required

### For Field Workers

- **"Quick Report" mode** - Just a few fields
- **Voice input** - Speak instead of type (browser feature)
- **SMS backup** - Can't use web? Text us instead
- **Works on old phones** - No fancy smartphone needed

## Security & Privacy

### Your Data Is Safe

- ✓ **Stored locally** - Not on any cloud server
- ✓ **No login required** - No passwords to remember (for local use)
- ✓ **Privacy-first** - Follows NUAA privacy policies
- ✓ **Encrypted** (when deployed properly)
- ✓ **You control it** - Delete anytime

### For Organizations

- Can be deployed on **internal network only**
- Optional **password protection** for sensitive data
- **Audit logs** available if needed
- **Compliant** with privacy regulations

## Deployment Options

### Option 1: Local Computer (Simplest)

Perfect for: One person or small office

```bash
python app.py
# Access at: http://localhost:5000
```

### Option 2: Office Network (Recommended)

Perfect for: Whole office or organization

1. Run on one computer/server
2. Everyone accesses via network
3. Example: `http://192.168.1.100:5000`

### Option 3: NUAA Server (Best for Remote Teams)

Perfect for: Field workers, remote staff, multiple locations

- Deploy on NUAA server
- Access via: `https://tools.nuaa.org.au`
- Requires IT setup (we can help!)

### Option 4: Microsoft Teams Integration

Perfect for: Organizations already using Teams

- Access directly in Teams
- No separate login
- Integrated with SharePoint

## Training & Support

### For Team Members

- **5-minute video tutorial** (coming soon)
- **One-page quick start guide** (printable)
- **Practice mode** (try without saving)
- **Help button** on every page
- **Contact support** anytime

### For Coordinators

- **Setup guide** (30 minutes)
- **Customization options**
- **Usage reports** (who's using what)
- **Export all data**
- **Troubleshooting guide**

## Frequently Asked Questions

**Q: Do I need to install anything?**
A: No! Just open the link in your web browser.

**Q: Does it work on my phone?**
A: Yes! Works on any device with a web browser.

**Q: What if I make a mistake?**
A: You can edit before submitting. After submitting, ask your coordinator.

**Q: What if I don't have internet in the field?**
A: Once you load the page, it works offline. Your report saves when you get signal.

**Q: Is my information private?**
A: Yes. All data is stored locally and follows NUAA privacy policies.

**Q: What if I'm not good with computers?**
A: That's exactly who this is for! It's designed to be super simple. Try it!

**Q: Can I use this on an old phone?**
A: Yes! It works on very old browsers and phones.

**Q: What if I need help?**
A: Click the "Help" button anytime, or contact [support email/phone].

## Technical Details

### Built With

- **Flask** (Python web framework)
- **Pure HTML/CSS/JS** (no complex frameworks)
- **Progressive Web App** (PWA) ready
- **Responsive design** (Bootstrap-inspired)
- **Accessibility-first** (WCAG 2.1 AAA)

### Requirements

- Python 3.11+
- Flask 2.0+
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Browser Support

- ✓ Chrome/Edge (2020+)
- ✓ Firefox (2020+)
- ✓ Safari (2020+)
- ✓ Mobile browsers
- ⚠ Internet Explorer (not supported - use Edge instead)

## Customization

### Add Your Own Team

Edit `app.py`:

```python
TEAMS = {
    "your-team": {
        "name": "Your Team Name",
        "icon": "🎯",  # Pick an emoji
        "templates": ["template1.md", "template2.md"],
        "description": "What your team does"
    }
}
```

### Add Your Own Templates

1. Create template in `nuaa-kit/templates/team-specific/your-team/`
2. Add to team's `templates` list in `app.py`
3. Restart server
4. Done!

### Change Colors/Branding

Edit `templates/index.html` - Look for the `<style>` section

### Add Logo

Add your logo image to `static/` folder and update templates

## Recent Improvements (v2.1.0 - November 2025)

### ✅ Completed

- [x] Professional toast notification system
- [x] Keyboard shortcuts overlay (press `?`)
- [x] Enhanced navigation with breadcrumbs
- [x] Mobile menu improvements
- [x] Loading skeletons and better feedback
- [x] Scroll-to-top button
- [x] Skip-to-content links for accessibility
- [x] Better error handling with retry logic

### Integration Guide

See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for how to use the new features.

## Roadmap

### Coming Soon (Phase 2.2 - Q1 2026)

- [ ] Interactive onboarding tour for new users
- [ ] Advanced search with filters
- [ ] Inline form validation with real-time feedback
- [ ] Bulk operations (multi-select documents)
- [ ] Custom template saving and sharing
- [ ] Enhanced analytics dashboard

### Phase 2.3 (Q2 2026)

- [ ] SMS quick submit integration
- [ ] Email interface (send form, receive document)
- [ ] Microsoft Teams bot
- [ ] Multi-language interface (6 languages)
- [ ] Voice input optimization improvements
- [ ] Advanced camera features

### Future (Phase 3)

- [ ] Mobile native apps (iOS/Android)
- [ ] Real-time collaboration features
- [ ] Advanced admin dashboard
- [ ] AI-powered form completion
- [ ] Integration marketplace

## Support

### Getting Help

- **Email**: tech@nuaa.org.au
- **Phone**: [number]
- **In-person**: Drop by NUAA office
- **Teams**: #nuaa-tools-help channel

### Reporting Issues

- Click "Help" button in the interface
- Email with screenshot if possible
- Describe what you were trying to do
- We'll help within 24 hours!

## Contributing

Have ideas for improvement? We'd love to hear!

- Email: tech@nuaa.org.au
- Or: Create an issue on GitHub (if technical)

## License

Copyright © 2025 NUAA. For NUAA use only.

---

**Made with ❤️ for the NUAA community**

_Remember: No question is too simple. We're here to help everyone succeed!_
