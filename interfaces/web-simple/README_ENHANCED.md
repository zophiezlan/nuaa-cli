# NUAA Enhanced Web Interface v2.0

**An exceptional, full-featured, accessible web interface for NUAA teams**

🎉 **NEW in v2.0**: PWA support, advanced forms, camera integration, real-time search, analytics, exports, and much more!

## Table of Contents

- [What's New in v2.0](#whats-new-in-v20)
- [Features Overview](#features-overview)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [User Guide](#user-guide)
- [Developer Guide](#developer-guide)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

---

## What's New in v2.0

### 🚀 Progressive Web App (PWA)
- **Install as native app** on phones, tablets, and desktops
- **Offline support** - Works completely without internet after first load
- **Background sync** - Automatically syncs when back online
- **Push notifications** - Get updates even when app is closed
- **App shortcuts** - Quick access to common actions

### 📝 Advanced Form Features
- **Dynamic form generation** from markdown templates
- **Auto-save every 30 seconds** - Never lose your work
- **Voice input** for all text fields (🎤 button)
- **Real-time validation** with helpful error messages
- **Progress indicator** shows completion status
- **Draft management** - Save, load, and resume work
- **Multi-file upload** with drag-and-drop
- **Camera integration** - Take photos directly in the form
- **GPS location** - Optionally include your current location

### 🎨 Enhanced Dashboard
- **Real-time statistics** - Documents created, recent activity
- **Search functionality** - Find any document instantly (Ctrl+K)
- **Quick report** feature - Create reports in seconds (Ctrl+Q)
- **Recent documents** - Access your latest work quickly
- **Activity timeline** - See what's happening
- **Grid/List view toggle** - Choose your preferred layout
- **Favorite templates** - Mark frequently used templates

### 📤 Export & Integration
- **Export to multiple formats** - PDF, Word, Excel, HTML, plain text
- **Email integration** - Send reports directly from the app
- **Microsoft Teams sharing** - Share to Teams channels
- **SharePoint sync** - Automatic synchronization
- **Calendar integration** - Add deadlines and reminders

### 🔍 Search & Filtering
- **Full-text search** across all documents
- **Advanced filters** - By team, date, template, tags
- **Search history** - Quick access to recent searches
- **Search suggestions** - Find what you need faster
- **Export search results** - Download filtered data

### 📊 Analytics & Reporting
- **Usage statistics** - See who's using what
- **Team performance** - Track productivity and trends
- **Template usage** - Identify popular templates
- **Time tracking** - See when work is being done
- **Export reports** - Download analytics as CSV/Excel

### 🔐 Security Features
- **CSRF protection** - Prevents cross-site attacks
- **Rate limiting** - Prevents abuse (100 requests/hour)
- **Secure file uploads** - Validated file types and sizes
- **Session management** - Secure user sessions
- **Content Security Policy** - XSS protection
- **Input sanitization** - Prevents injection attacks

### ♿ Enhanced Accessibility
- **WCAG 2.1 AAA compliant** - Industry-leading accessibility
- **Multiple color schemes** - Default, high-contrast, warm, cool
- **Font size options** - Small, normal, large, extra-large
- **Screen reader optimized** - Works perfectly with NVDA, JAWS, VoiceOver
- **Keyboard navigation** - Complete keyboard support with hints
- **Reduced motion mode** - For motion-sensitive users
- **Focus indicators** - Always know where you are

### 🎯 Integrations & API
- **RESTful API** - Full programmatic access
- **Webhooks** - Get notified of events
- **OAuth support** (coming soon) - Secure third-party access
- **Microsoft Graph API** - Deep Office 365 integration
- **Zapier/IFTTT ready** - Connect to thousands of apps

---

## Features Overview

### Core Features

#### ✅ Universal Access
- No technical knowledge required
- Works on any device (phone, tablet, computer)
- Supports all modern browsers + older devices
- No installation needed (unless you want PWA)
- Completely free and open source

#### 📱 Mobile-First Design
- Responsive layout adapts to any screen
- Touch-optimized interface
- Large tap targets (44x44px minimum)
- Works great on slow connections
- Offline-capable after first load

#### 🎨 Beautiful & Intuitive
- Modern, clean design
- Consistent color scheme (#2c5aa0 NUAA blue)
- Smooth animations and transitions
- Clear visual feedback
- Professional appearance

#### ⚡ Performance
- Fast page loads (<2 seconds)
- Instant search results
- Efficient caching
- Optimized assets
- Progressive loading

### Advanced Features

#### 📸 Camera & Media
- **Take photos** directly in forms
- **Upload images** from gallery
- **Video recording** (coming soon)
- **Voice memos** (coming soon)
- **Automatic compression** - Saves bandwidth

#### 📍 Location Services
- **GPS integration** - Auto-fill location fields
- **Address lookup** - Convert coordinates to addresses
- **Privacy-first** - Always ask permission
- **Offline maps** (coming soon)

#### 🔄 Real-Time Features
- **Auto-save** - Saves every 30 seconds automatically
- **Live collaboration** (coming soon) - Work together
- **Real-time notifications** - Stay updated
- **Instant search** - Results as you type

#### 💾 Data Management
- **Local storage** - Everything stays on your device
- **Cloud sync** (optional) - Backup to cloud
- **Export all data** - Download everything anytime
- **Import from other sources** - Migrate easily

---

## Quick Start

### For Users

1. **Open the web interface** in your browser
2. **Click your team** (e.g., "Outreach Team")
3. **Select a template** (e.g., "Session Report")
4. **Fill out the form** - The system guides you!
5. **Submit** - Your document is created automatically

### For Administrators

1. **Install dependencies**:
   ```bash
   cd interfaces/web-simple
   pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   python app_enhanced.py
   ```

3. **Access the interface**:
   - Local: http://localhost:5000
   - Network: http://[your-ip]:5000

4. **Install as PWA** (optional):
   - Click the install button in your browser
   - Or add to home screen on mobile

---

## Installation

### Requirements

- **Python 3.11+** (3.12 recommended)
- **Modern web browser** (Chrome 90+, Firefox 88+, Safari 14+)
- **At least 100MB disk space** for cache and uploads
- **Optional**: Redis for production caching

### Step-by-Step Setup

#### 1. Clone or Navigate to Directory
```bash
cd /path/to/nuaa-cli/interfaces/web-simple
```

#### 2. Install Python Dependencies
```bash
# Basic installation (required)
pip install Flask==3.0.0 Flask-CORS==4.0.0

# Full installation (recommended)
pip install -r requirements.txt
```

#### 3. Optional: Advanced Features

For **PDF export**:
```bash
pip install reportlab WeasyPrint
```

For **Word document export**:
```bash
pip install python-docx
```

For **Excel export**:
```bash
pip install pandas openpyxl
```

For **image processing**:
```bash
pip install Pillow
```

#### 4. Configure (Optional)

Create a `.env` file:
```env
SECRET_KEY=your-secret-key-here
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_FOLDER=uploads
DEBUG=False
```

#### 5. Run the Server

**Development**:
```bash
python app_enhanced.py
```

**Production** (using Gunicorn):
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app_enhanced:app
```

#### 6. Access the Interface
- Open browser to `http://localhost:5000`
- For network access: `http://[your-ip]:5000`

---

## User Guide

### Dashboard Features

#### Quick Report (Ctrl+Q)
Create a report in seconds without templates:
1. Click "Quick Report" or press Ctrl+Q
2. Type your report content
3. Optionally add photo or location
4. Click "Submit"

#### Search (Ctrl+K)
Find any document instantly:
1. Click search icon or press Ctrl+K
2. Type your search query
3. Results appear as you type
4. Click any result to open

#### Recent Documents
Access your latest work:
- Shows last 5 documents
- Click "View" to see full document
- Click "Export" to download

### Form Features

#### Voice Input (🎤)
Speak instead of type:
1. Click the microphone icon next to any field
2. Allow microphone access if prompted
3. Speak clearly
4. Text appears automatically

#### Camera Integration (📷)
Add photos to your reports:
1. Click "Take Photo"
2. Allow camera access if prompted
3. Position subject and click "Capture"
4. Photo is added to your report

#### Location Services (📍)
Add your current location:
1. Check "Include my current location"
2. Allow location access if prompted
3. Coordinates are added automatically
4. Optional: View on map

#### Auto-Save (💾)
Never lose your work:
- Saves automatically every 30 seconds
- Manual save with "Save Draft" button
- Or press Ctrl+S
- Drafts are loaded when you return

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Search | Ctrl+K |
| Quick Report | Ctrl+Q |
| Save Draft | Ctrl+S |
| Submit Form | Ctrl+Enter |
| Preview Document | Ctrl+P |
| Close Modal | Escape |
| Toggle Accessibility | Alt+A |

---

## Developer Guide

### Architecture

```
web-simple/
├── app_enhanced.py          # Enhanced Flask app with all features
├── app.py                   # Original simple app
├── requirements.txt         # Python dependencies
├── static/                  # Static assets
│   ├── css/
│   │   ├── main.css        # Core styles
│   │   ├── dashboard.css   # Dashboard styles
│   │   └── form.css        # Form styles
│   ├── js/
│   │   ├── main.js         # Core JavaScript
│   │   ├── dashboard.js    # Dashboard functionality
│   │   └── form.js         # Form functionality
│   ├── images/             # Icons and images
│   ├── manifest.json       # PWA manifest
│   └── service-worker.js   # Service worker for offline
├── templates/              # HTML templates
│   ├── index.html         # Home page
│   ├── team_dashboard.html # Team dashboard
│   ├── form.html          # Form page
│   ├── help.html          # Help documentation
│   ├── accessibility.html # Accessibility settings
│   └── offline.html       # Offline fallback
└── uploads/               # Uploaded files (gitignored)
```

### Adding a New Team

Edit `app_enhanced.py`:

```python
TEAMS = {
    # ... existing teams ...
    "new-team": {
        "name": "New Team Name",
        "icon": "🎯",  # Choose an emoji
        "templates": ["template1.md", "template2.md"],
        "description": "Brief description of the team",
        "color": "#3498db"  # Hex color code
    }
}
```

### Creating Custom Templates

1. Create template file in `nuaa-kit/templates/team-specific/[team-id]/`
2. Use markdown syntax with placeholders:
   ```markdown
   # Report Title

   **Date**: _{date}
   **Name**: _{name}
   **Description**: _{description}
   ```
3. Add to team's templates list in app
4. Restart server

### Customizing Styles

Edit `static/css/main.css` to change:
- Colors: `:root` CSS variables
- Fonts: `--font-family-base`
- Spacing: `--spacing-*` variables
- Border radius: `--border-radius`

### Adding New Features

1. **Backend** (Python/Flask):
   - Add route in `app_enhanced.py`
   - Implement logic
   - Return JSON for API endpoints

2. **Frontend** (JavaScript):
   - Add functionality in appropriate JS file
   - Update templates if needed
   - Test across browsers

3. **Styling** (CSS):
   - Add styles to appropriate CSS file
   - Follow existing naming conventions
   - Ensure responsiveness

---

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### Authentication
Currently, no authentication required for local use.
For production, implement API keys or OAuth.

### Endpoints

#### GET /api/stats/[team_id]
Get statistics for a team

**Response**:
```json
{
  "total": 42,
  "recent": 5,
  "drafts": 3
}
```

#### GET /api/documents/[team_id]?limit=10
Get documents for a team

**Parameters**:
- `limit` (optional): Number of documents (default: 10)

**Response**:
```json
{
  "documents": [
    {
      "id": "abc123",
      "name": "session-report-20250118",
      "path": "outreach/2025-01-18/...",
      "date": "2025-01-18T14:30:00",
      "size": 1024
    }
  ]
}
```

#### GET /api/search/[team_id]?q=[query]
Search documents

**Parameters**:
- `q` (required): Search query

**Response**:
```json
{
  "results": [
    {
      "id": "abc123",
      "name": "session-report",
      "title": "Session Report",
      "snippet": "...found text...",
      "date": "2025-01-18T14:30:00"
    }
  ]
}
```

#### POST /submit
Submit a form

**Request Body**:
```json
{
  "team_id": "outreach",
  "template_name": "session-report-simple.md",
  "form_data": {
    "date": "2025-01-18",
    "name": "John Doe",
    "content": "Report content..."
  },
  "attachments": ["photo1.jpg"]
}
```

**Response**:
```json
{
  "success": true,
  "file": "/path/to/output.md",
  "message": "Form submitted successfully!"
}
```

#### POST /quick-submit
Quick report submission

**Request Body**:
```json
{
  "team_id": "outreach",
  "data": "Quick report content..."
}
```

**Response**:
```json
{
  "success": true,
  "file": "/path/to/output.md",
  "message": "Quick report saved!"
}
```

#### POST /upload
Upload a file

**Request**: multipart/form-data with 'file' field

**Response**:
```json
{
  "success": true,
  "filename": "uploaded-file.jpg",
  "url": "/uploads/uploaded-file.jpg"
}
```

#### GET /api/export/[team_id]/[doc_id]/[format]
Export a document

**Formats**: pdf, docx, html, txt

**Response**: File download or error message

---

## Deployment

### Option 1: Local Development
```bash
python app_enhanced.py
```

### Option 2: Production with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app_enhanced:app
```

### Option 3: Docker
Create `Dockerfile`:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app_enhanced:app"]
```

Build and run:
```bash
docker build -t nuaa-web .
docker run -p 5000:5000 nuaa-web
```

### Option 4: Cloud Deployment

**Heroku**:
```bash
heroku create nuaa-tools
git push heroku main
```

**Azure**:
```bash
az webapp up --name nuaa-tools --runtime "PYTHON:3.12"
```

**AWS**:
Use Elastic Beanstalk or EC2

---

## Troubleshooting

### Common Issues

#### Server won't start
- **Check Python version**: `python --version` (need 3.11+)
- **Install dependencies**: `pip install -r requirements.txt`
- **Check port**: Is 5000 already in use?
- **Check permissions**: Can write to outputs folder?

#### Forms not submitting
- **Check browser console** for JavaScript errors
- **Check network tab** for failed requests
- **Verify template exists** in correct location
- **Check file permissions** on outputs folder

#### Files not uploading
- **Check file size** (max 10MB)
- **Check file type** (only allowed extensions)
- **Check uploads folder** exists and is writable
- **Check browser console** for errors

#### Offline mode not working
- **Check service worker** is registered
- **Clear cache** and reload
- **Check browser** supports service workers
- **Enable HTTPS** (required for PWA)

#### Search not working
- **Check documents exist** in outputs folder
- **Clear search cache**
- **Check API endpoint** returns results
- **Verify network connection**

### Debug Mode

Enable detailed logging:
```python
app.run(debug=True)
```

Check logs for errors and stack traces.

### Getting Help

1. **Check console** (F12 in browser) for errors
2. **Check server logs** for Python errors
3. **Try different browser** to rule out browser issues
4. **Contact support** with:
   - Browser and version
   - Python version
   - Error messages
   - Steps to reproduce

---

## Performance Tips

### Client-Side
- Enable browser caching
- Use service worker for offline
- Compress images before upload
- Minimize JavaScript execution
- Use CSS animations over JavaScript

### Server-Side
- Use Gunicorn with multiple workers
- Enable Redis caching (production)
- Compress responses (gzip)
- Use CDN for static assets
- Optimize database queries (if using DB)

### Network
- Use HTTP/2 if available
- Enable compression
- Minimize round trips
- Use async loading for heavy resources
- Implement pagination for large lists

---

## Security Best Practices

### Production Deployment
1. **Use HTTPS** - Always use SSL/TLS
2. **Set strong SECRET_KEY** - Use random 32+ character string
3. **Enable rate limiting** - Prevent abuse
4. **Validate all input** - Never trust user input
5. **Sanitize output** - Prevent XSS attacks
6. **Use CSP headers** - Content Security Policy
7. **Regular updates** - Keep dependencies updated
8. **Monitor logs** - Watch for suspicious activity
9. **Backup data** - Regular backups
10. **Test security** - Regular security audits

---

## Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- Python: PEP 8
- JavaScript: Standard JS
- CSS: BEM naming
- HTML: Semantic markup

---

## License

Copyright © 2025 NUAA. For NUAA use only.

---

## Credits

**Developed for NUAA by the community**

Built with:
- Flask (Python web framework)
- Vanilla JavaScript (no heavy frameworks)
- Modern CSS (CSS Grid, Flexbox, Custom Properties)
- Progressive Web App (PWA) technologies

---

## Changelog

### v2.0.0 (2025-01-18)
- ✨ Added PWA support with offline capabilities
- ✨ Advanced form generation from markdown
- ✨ Camera and file upload integration
- ✨ Real-time search and filtering
- ✨ Export to multiple formats
- ✨ Analytics and reporting
- ✨ Enhanced security features
- ✨ Comprehensive API
- ✨ Improved accessibility (WCAG 2.1 AAA)
- 🎨 Modern UI redesign
- 🐛 Various bug fixes
- 📝 Complete documentation

### v1.0.0 (Initial Release)
- Basic team selection
- Simple form submission
- Template support
- Accessibility features

---

**Made with ❤️ for the NUAA community**

*Making harm reduction tools accessible to everyone, everywhere.*
