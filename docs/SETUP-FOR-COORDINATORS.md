# NUAA Setup Guide for Coordinators

This guide helps coordinators and administrators set up NUAA for their teams with minimal technical barriers.

---

## 🎯 Your Goal

Get your team accessing NUAA WebUI in under 5 minutes, regardless of their technical skills.

---

## 📊 Quick Assessment

**Choose your setup method based on your team:**

| Your Team | Best Method | Time | Skill Level |
|-----------|-------------|------|-------------|
| All in one office | Local server on shared computer | 5 min | Easy |
| Remote/distributed | Cloud deployment | 30 min | Medium |
| Mobile-only workers | Cloud deployment + mobile setup | 30 min | Medium |
| Mixed (office + field) | Local + cloud | 45 min | Medium |

---

## 🚀 Method 1: Local Server (Shared Computer)

**Best for:** Teams working in the same office

### What You'll Need
- One computer that's always on (or on during work hours)
- Python installed (we'll check this)
- 5 minutes

### Step-by-Step

#### 1. Check Python Installation

**Windows:**
```cmd
python --version
```

**Mac/Linux:**
```bash
python3 --version
```

**What you want to see:** `Python 3.8` or higher

**If not installed:** See "Installing Python" section below

#### 2. Download NUAA Files

Option A: Download ZIP
- Go to: https://github.com/zophiezlan/nuaa-cli
- Click "Code" → "Download ZIP"
- Extract to a folder like `C:\NUAA` (Windows) or `~/NUAA` (Mac)

Option B: Use Git (if you know it)
```bash
git clone https://github.com/zophiezlan/nuaa-cli.git
cd nuaa-cli
```

#### 3. Run the Quick Setup

**Windows:**
1. Find the file `START-WEBUI.bat`
2. Double-click it
3. Windows might show a security warning - click "More info" → "Run anyway"
4. A window will open with server information
5. **DO NOT CLOSE THIS WINDOW** while team is using NUAA

**Mac/Linux:**
1. Find the file `START-WEBUI.sh`
2. Right-click → "Open With" → "Terminal"
3. A window will open with server information
4. **DO NOT CLOSE THIS WINDOW** while team is using NUAA

#### 4. Get Your Team's Access Link

The setup will show you two links:

```
On this computer:
  http://localhost:5000

From other devices on your network:
  http://192.168.1.XXX:5000
```

**The second link is what your team needs!**

#### 5. Share with Your Team

**Copy the network link** (the one with numbers like 192.168.1.XXX) and share it via:
- Email
- Slack/Teams message
- Text message
- Post it on a whiteboard

**Sample message to send:**
```
Hi team! 👋

NUAA WebUI is now available! Access it here:
http://192.168.1.100:5000

📱 Mobile users: Open in browser, then "Add to Home Screen"
💻 Desktop users: Bookmark this page
🔖 No installation needed!

Questions? Ask me!
```

#### 6. Help Team Members Add to Phone

**For iPhone/iPad users:**
1. Open link in Safari
2. Tap Share button
3. "Add to Home Screen"
4. Tap "Add"

**For Android users:**
1. Open link in Chrome
2. Tap three dots menu
3. "Add to Home screen"
4. Tap "Add"

---

## 🚀 Method 2: Cloud Deployment

**Best for:** Remote teams, mobile workers, 24/7 access

### Option A: Deploy to Render (Easiest)

**Cost:** Free tier available

1. Go to: https://render.com
2. Sign up (free)
3. Click "New +" → "Web Service"
4. Connect your GitHub account
5. Select the NUAA repository
6. Settings:
   - **Name:** nuaa-webui
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python interfaces/web-simple/app.py`
7. Click "Create Web Service"
8. Wait 5 minutes for deployment
9. You'll get a URL like: `https://nuaa-webui.onrender.com`
10. Share this URL with your team!

### Option B: Deploy to Heroku

**Cost:** Free tier available

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Login:
   ```bash
   heroku login
   ```
3. Create app:
   ```bash
   heroku create nuaa-webui
   ```
4. Deploy:
   ```bash
   git push heroku main
   ```
5. Open:
   ```bash
   heroku open
   ```

### Option C: Deploy with Docker (Advanced)

If your organization uses Docker:

```bash
docker-compose up -d
```

That's it! Access at `http://your-server:5000`

---

## 🔧 Installing Python (If Needed)

### Windows

1. Go to: https://www.python.org/downloads/
2. Click the big yellow "Download Python" button
3. Run the installer
4. **CRITICAL:** Check ☑️ "Add Python to PATH"
5. Click "Install Now"
6. Wait for completion
7. Restart your computer

### Mac

**Option 1: Official Installer**
1. Go to: https://www.python.org/downloads/
2. Download for macOS
3. Run the installer
4. Follow prompts

**Option 2: Homebrew** (if you have it)
```bash
brew install python3
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

## 📱 Mobile-Specific Setup Tips

### For Mobile-First Teams

1. **Use cloud deployment** - local servers don't work well for mobile
2. **Send QR code** - easier than typing URL
   - Use: https://www.qr-code-generator.com/
   - Generate QR for your NUAA URL
   - Print and post in office
3. **Create setup guide with screenshots**
   - Take screenshots of "Add to Home Screen" steps
   - Print as one-pager
   - Keep at desk for walkins

### Data Usage Optimization

If your team has limited data plans:

1. Edit `app.py` to enable aggressive caching
2. Host images locally (don't use CDN)
3. Enable service worker for offline
4. Initial load: ~2MB
5. Subsequent loads: ~50KB

---

## 🔒 Security Considerations

### Local Server

**Risks:**
- Anyone on your network can access
- No authentication by default

**Mitigations:**
- Only use on trusted networks
- Don't expose to internet without authentication
- Keep computer secure (password, encryption)

### Cloud Deployment

**Risks:**
- Public URL = anyone can access (if they know it)
- Data travels over internet

**Mitigations:**
- Add authentication (see "Adding Password Protection" below)
- Use HTTPS (most platforms do this automatically)
- Don't store sensitive client data

### Adding Password Protection (Optional)

Edit `app.py` to add basic auth:

```python
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

users = {
    "nuaa": generate_password_hash("your-password-here")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route("/")
@auth.login_required
def index():
    # ... rest of code
```

Then install:
```bash
pip install flask-httpauth
```

---

## 🎨 Customization Tips

### Change Team List

Edit `app.py` to add/remove teams:

```python
TEAMS = {
    "your-team": {
        "name": "Your Team Name",
        "icon": "🎯",  # Any emoji!
        "templates": ["template1.md", "template2.md"],
        "description": "What your team does",
    },
}
```

### Change Colors/Branding

Edit `templates/index.html` CSS:

```css
/* Change primary color */
#2c5aa0 → #YOUR-COLOR

/* Change header */
h1 {
    color: #YOUR-COLOR;
}
```

### Add Your Logo

1. Save logo as `static/logo.png`
2. Edit `templates/index.html`:
   ```html
   <header>
       <img src="/static/logo.png" alt="Logo" style="max-width: 200px;">
       <h1>NUAA Project Tools</h1>
   </header>
   ```

---

## 🐛 Troubleshooting

### Server Won't Start

**Error:** "Address already in use"
```bash
# Find what's using port 5000
# Windows:
netstat -ano | findstr :5000

# Mac/Linux:
lsof -i :5000

# Kill it or change NUAA port in app.py
```

**Error:** "Module not found"
```bash
pip install flask werkzeug
```

### Team Can't Access

**Check firewall:**
- Windows: Windows Firewall → Allow Python
- Mac: System Preferences → Security → Firewall → Allow

**Check network:**
- Make sure computers are on same network
- Try pinging the server computer
- Check if server computer has VPN that blocks local network

### Slow Performance

**Solutions:**
1. Use cloud deployment instead of old computer
2. Reduce number of templates loaded
3. Enable caching in Flask
4. Use production server (gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

---

## 📊 Usage Monitoring

### Check Who's Using It

Add analytics (optional):

```python
@app.before_request
def log_request():
    with open('access.log', 'a') as f:
        f.write(f"{datetime.now()} - {request.remote_addr} - {request.path}\n")
```

### Basic Stats

```bash
# Count daily users
cat access.log | grep $(date +%Y-%m-%d) | cut -d'-' -f2 | sort -u | wc -l

# Most popular team
cat access.log | grep "/team/" | cut -d'/' -f3 | sort | uniq -c | sort -rn
```

---

## 🔄 Keeping It Running

### Auto-Start on Boot (Windows)

1. Create shortcut to `START-WEBUI.bat`
2. Press `Win+R`, type `shell:startup`, press Enter
3. Move shortcut to this folder
4. Server will start when computer boots

### Auto-Start on Boot (Mac/Linux)

Create a launch agent or systemd service:

```bash
# systemd example
sudo nano /etc/systemd/system/nuaa.service
```

```ini
[Unit]
Description=NUAA WebUI
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/nuaa-cli
ExecStart=/usr/bin/python3 interfaces/web-simple/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable nuaa
sudo systemctl start nuaa
```

### Monitor for Crashes

Use a process manager:

```bash
pip install supervisor

# Create supervisor config
# Will restart server if it crashes
```

---

## 📞 Getting Help

### For You (Coordinator)

**Technical issues:**
- Email: tech@nuaa.org.au
- GitHub issues: https://github.com/zophiezlan/nuaa-cli/issues

**Training/support:**
- Schedule a walkthrough: tech@nuaa.org.au
- Video tutorials: [link]

### For Your Team

Give them:
1. The quick-start guide: `docs/QUICK-START-NON-TECHNICAL.md`
2. Your contact info
3. NUAA tech support: tech@nuaa.org.au

---

## ✅ Setup Checklist

Use this to ensure everything is working:

- [ ] Python installed and working
- [ ] NUAA files downloaded
- [ ] Server starts successfully
- [ ] You can access at http://localhost:5000
- [ ] Network link works from another device
- [ ] Team members can access the link
- [ ] Mobile "Add to Home Screen" tested
- [ ] Accessibility options work
- [ ] Forms can be filled and submitted
- [ ] Output files are created correctly
- [ ] Help contact info is correct
- [ ] Team link is bookmarked/documented
- [ ] Team is trained on basic usage
- [ ] Troubleshooting guide is available

---

## 🎉 You're Done!

Your team now has easy access to NUAA tools without any technical barriers.

**Remember to:**
- Keep the server computer on during work hours
- Share the link prominently
- Encourage team to bookmark it
- Be available for questions in the first week
- Collect feedback for improvements

**Questions?** Email tech@nuaa.org.au

---

**Last Updated:** 2025-11-19
**Version:** 1.0
**Feedback:** tech@nuaa.org.au
