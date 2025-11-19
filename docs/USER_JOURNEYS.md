# NUAA Staff User Experience Journeys

## Overview
This document outlines user personas and experience journeys for various NUAA staff members, with a focus on accessibility and ease of use for people with minimal technical skills.

---

## User Personas

### 1. Sarah - Peer Support Worker (Non-Technical)
**Background:**
- 35 years old, lived experience, passionate about harm reduction
- Uses smartphone daily but never used a computer terminal/CLI
- Comfortable with WhatsApp, Facebook, email
- No experience with: coding, GitHub, VSCode, command line, technical documentation

**Tech Comfort Level:** 2/10
**Primary Device:** Smartphone (Android)
**Internet:** Often spotty mobile data
**Key Needs:**
- Quick access to resources to share with clients
- Simple way to log interactions (privacy-safe)
- No installation headaches
- Visual, intuitive interface

**Frustrations:**
- "I don't know what a terminal is and I don't want to learn"
- "I need this working in 2 minutes, not 2 hours"
- "If it needs more than one copy-paste, I'm out"

---

### 2. Marcus - Outreach Coordinator (Low-Tech)
**Background:**
- 42 years old, works in the field distributing supplies
- Uses basic office software (Word, email)
- Comfortable following step-by-step visual guides
- Has access to a Windows laptop but rarely uses advanced features

**Tech Comfort Level:** 4/10
**Primary Device:** Windows laptop, smartphone for field work
**Internet:** Office WiFi (reliable) + mobile (spotty in field)
**Key Needs:**
- Track supply distribution
- Generate simple reports
- Access harm reduction materials offline
- Sync data when back online

**Frustrations:**
- "Setup instructions assume I know what Python is"
- "I can follow steps if they're clear, but one error message and I'm lost"
- "I need offline access - the field has no WiFi"

---

### 3. Dr. Aisha - Clinical Director (Medium-Tech)
**Background:**
- 48 years old, MD with public health background
- Comfortable with electronic medical records, Office 365, Zoom
- Can install software but not comfortable troubleshooting
- Needs HIPAA/privacy compliance

**Tech Comfort Level:** 6/10
**Primary Device:** MacBook Pro, iPad
**Internet:** Reliable office connection
**Key Needs:**
- Quick access to evidence-based protocols
- Generate reports for stakeholders
- Coordinate team workflows
- Ensure client data privacy

**Frustrations:**
- "I don't have time to debug why something won't install"
- "Security is non-negotiable but I'm not a sysadmin"
- "I need this to 'just work' so I can focus on clinical care"

---

### 4. James - Data & Programs Manager (Tech-Comfortable)
**Background:**
- 29 years old, social work degree + self-taught data skills
- Uses Excel/Google Sheets heavily, basic SQL
- Comfortable installing software and following docs
- Interested in automation but not a developer

**Tech Comfort Level:** 7/10
**Primary Device:** Windows desktop, Linux familiarity
**Internet:** Reliable
**Key Needs:**
- Aggregate data across programs
- Customize workflows for different teams
- Integrate with existing systems
- Some CLI comfort but prefers GUI

**Frustrations:**
- "I can use CLI if needed but my team can't"
- "I need to set this up once, then my team uses a web interface"
- "Documentation is either too basic or too technical"

---

### 5. Lily - Community Health Worker (Mobile-First)
**Background:**
- 26 years old, bilingual (English/Spanish)
- Phone is primary computing device
- Limited laptop access (shared community center computer)
- Excellent with mobile apps, social media

**Tech Comfort Level:** 5/10 (mobile), 2/10 (desktop)
**Primary Device:** iPhone
**Internet:** Mobile data (limited)
**Key Needs:**
- Mobile-optimized interface
- Works offline (syncs later)
- Multilingual support
- Data-efficient (limited plan)

**Frustrations:**
- "Everything is designed for people with laptops"
- "Why do I need to install something when I just want to use it?"
- "My data plan can't handle huge downloads"

---

## User Journey Maps

### Journey 1: Sarah Gets Started (CRITICAL PATH - Non-Technical)

#### Current State (BROKEN FOR SARAH)
1. ❌ Sarah finds GitHub repo → **CONFUSED** (What is GitHub?)
2. ❌ Sees "pip install" or "uvx" → **OVERWHELMED** (What are these?)
3. ❌ Tries to install Python → **ERROR MESSAGES** (Installation fails)
4. ❌ Gives up → **FRUSTRATED** (Goes back to paper forms)

**Time to value:** NEVER
**Success rate:** 0%

#### Ideal State (GOAL)
1. ✅ Sarah receives link via text/email: `https://nuaa.app/start`
2. ✅ Clicks link → Opens in browser
3. ✅ Sees: "Welcome! Click START to begin" (big button)
4. ✅ Clicks START → WebUI loads instantly
5. ✅ Prompted to bookmark for easy access
6. ✅ Can immediately access resources, forms, help

**Time to value:** 30 seconds
**Success rate:** 95%
**No installation required**

---

### Journey 2: Marcus Sets Up Team Access

#### Current State (FRUSTRATING FOR MARCUS)
1. ⚠️ Marcus reads 600+ line README → **OVERWHELMED**
2. ⚠️ Tries `uvx nuaa init` → **STUCK** (Python not installed correctly)
3. ⚠️ Spends 2 hours troubleshooting → **FRUSTRATED**
4. ⚠️ Eventually gets CLI working → **EXHAUSTED**
5. ⚠️ Needs to start WebUI → **CONFUSED** (How? Where?)
6. ❌ Team members need access → **STUCK** (How to share?)

**Time to value:** 2-4 hours (if successful)
**Success rate:** 30%

#### Ideal State (GOAL)
1. ✅ Marcus downloads `NUAA-Setup.exe` (Windows)
2. ✅ Double-clicks installer → Wizard opens
3. ✅ Wizard: "Welcome! This will take 60 seconds"
   - Visual progress bar
   - Auto-detects Python or installs it
   - Creates desktop shortcut
4. ✅ Wizard finishes: "Setup complete! Click START WEBUI"
5. ✅ WebUI opens in browser at `localhost:5000`
6. ✅ Wizard shows team access link: `http://[his-ip]:5000`
7. ✅ Marcus shares link → Team accesses instantly

**Time to value:** 2 minutes
**Success rate:** 90%
**One double-click + automatic setup**

---

### Journey 3: Dr. Aisha Needs Quick Access During Crisis

#### Current State (BROKEN)
1. ⚠️ Crisis situation - needs naloxone protocol NOW
2. ❌ NUAA CLI not installed → Must follow setup
3. ❌ Setup takes time she doesn't have
4. ❌ Resorts to old PDFs or Google

**Time to value:** Too slow (during crisis)

#### Ideal State (GOAL)
1. ✅ Crisis situation - needs protocol NOW
2. ✅ Opens bookmark: `https://nuaa.app` or local server
3. ✅ Types "naloxone" in search → Instant results
4. ✅ Protocol loads offline (PWA cached)
5. ✅ Can access immediately, no login required

**Time to value:** 5 seconds
**Works offline**

---

### Journey 4: James Sets Up for Entire Organization

#### Current State (PARTIALLY WORKS)
1. ✅ James can use CLI → `uvx nuaa init project`
2. ⚠️ Configures templates → Manual editing
3. ⚠️ Starts WebUI → Needs to run command
4. ❌ Team needs access → Must teach them CLI (FAILS)
5. ⚠️ Sets up on server → Requires sysadmin knowledge

**Time to value:** 1-2 days
**Success rate:** 60% (works for James, not team)

#### Ideal State (GOAL)
1. ✅ James runs installer or Docker: `docker-compose up`
2. ✅ Web-based admin panel opens automatically
3. ✅ Admin panel:
   - Configure teams
   - Set permissions
   - Customize templates
   - Generate team access links
4. ✅ Shares links with team → They access WebUI instantly
5. ✅ Optional: James can still use CLI for advanced features

**Time to value:** 30 minutes (complete org setup)
**Success rate:** 90%

---

### Journey 5: Lily Uses Mobile in the Field

#### Current State (BROKEN)
1. ❌ NUAA requires desktop setup → Lily has no laptop access
2. ❌ WebUI exists but requires someone else to host it
3. ❌ Lily dependent on coordinator to keep server running

**Time to value:** Never (dependent on others)

#### Ideal State (GOAL)
1. ✅ Lily receives link: `https://nuaa.app/mobile`
2. ✅ Mobile-optimized PWA loads
3. ✅ Prompts: "Add to Home Screen" → Installs like app
4. ✅ Works offline (service worker caches resources)
5. ✅ Logs interactions offline → Syncs when online
6. ✅ Fully functional without desktop setup

**Time to value:** 1 minute
**Success rate:** 95%
**No desktop needed**

---

## Critical Requirements for Success

### For Non-Technical Users (Sarah, Marcus, Lily)

#### MUST HAVE
1. **Zero-install web access**
   - Public hosted version: `https://nuaa.app`
   - No GitHub account needed
   - No terminal/CLI required
   - Works in any browser

2. **One-click local setup (if hosting locally)**
   - `NUAA-Setup.exe` (Windows)
   - `NUAA-Setup.dmg` (Mac)
   - `NUAA-Setup.AppImage` (Linux)
   - Double-click → WebUI running in 60 seconds

3. **Visual setup wizard**
   - Progress indicators
   - Plain language (no jargon)
   - Error messages that explain what to do
   - Success confirmation with next steps

4. **Mobile PWA**
   - Add to home screen
   - Offline functionality
   - Touch-optimized UI
   - Data-efficient

#### NICE TO HAVE
- QR code for instant mobile access
- SMS-based access for feature phones
- Voice interface for accessibility
- Setup validation ("Test your setup" button)

---

### For Medium-Tech Users (Dr. Aisha, James)

#### MUST HAVE
1. **Reliable automated setup**
   - Dependency auto-detection/installation
   - Clear error messages with solutions
   - Rollback on failure
   - Validation checks

2. **Web-based administration**
   - Team management
   - Configuration GUI
   - Usage analytics
   - Backup/export tools

3. **Security by default**
   - HTTPS auto-configured
   - Privacy settings visible
   - Audit logs
   - Data encryption options

#### NICE TO HAVE
- CLI for power users (James)
- API for integrations
- Custom branding options
- Advanced reporting tools

---

## Implementation Priority

### Phase 1: Critical (Week 1-2)
**Target:** Sarah, Marcus, Lily can use NUAA without technical help

1. **Hosted WebUI** (highest priority)
   - Deploy to `nuaa.app` or similar
   - Public access (no auth required for public resources)
   - Mobile PWA functionality
   - Offline support

2. **One-click installers**
   - Windows `.exe` with wizard
   - Mac `.dmg` with wizard
   - Auto-starts WebUI on completion

3. **Quick-start page**
   - `GET-STARTED.md` with screenshots
   - "No technical skills needed" guide
   - 3-step setup maximum

### Phase 2: Important (Week 3-4)
**Target:** Dr. Aisha, James can deploy for teams

1. **Docker one-liner**
   - `docker run -p 5000:5000 nuaa/webui`
   - Auto-opens browser
   - Includes all dependencies

2. **Admin web panel**
   - Team configuration
   - Template customization
   - User management

3. **Improved documentation**
   - Separate docs for different user types
   - Video tutorials
   - Interactive setup guide

### Phase 3: Enhanced (Week 5+)
**Target:** All users have excellent experience

1. **Advanced features**
   - SMS interface
   - Email automation
   - Mobile app (iOS/Android)
   - Voice interface

2. **Enterprise features**
   - SSO integration
   - Advanced analytics
   - Custom workflows
   - API access

---

## Success Metrics

### For Sarah (Non-Technical)
- ✅ Can access NUAA WebUI in under 1 minute
- ✅ No installation required
- ✅ Can complete tasks without help
- ✅ Reports feeling confident using system

### For Marcus (Low-Tech)
- ✅ Can set up local WebUI in under 5 minutes
- ✅ Can share access with team
- ✅ Team members can access without Marcus's help
- ✅ Works offline in field

### For Dr. Aisha (Medium-Tech)
- ✅ Setup completes without errors
- ✅ Privacy/security requirements met
- ✅ Can generate reports without technical help
- ✅ Feels confident in data safety

### For James (Tech-Comfortable)
- ✅ Can deploy for entire organization in under 1 hour
- ✅ Can customize for team needs
- ✅ Team members (all skill levels) can access easily
- ✅ Has advanced options available when needed

### For Lily (Mobile-First)
- ✅ Can access fully functional system from phone
- ✅ Works offline
- ✅ Data-efficient (under 5MB for initial load)
- ✅ Add to home screen for app-like experience

---

## Key Insights

### What Makes Setup "Crazy Accessible"

1. **Multiple entry points** - Web, installer, Docker, CLI
2. **Zero to running in 60 seconds** - For most common path
3. **No prerequisites** - Installers handle everything
4. **Visual feedback** - Progress bars, success messages
5. **Plain language** - No jargon, clear instructions
6. **Mobile-first** - Works on phones, not just desktops
7. **Offline-capable** - Not dependent on connectivity
8. **Forgiving** - Errors have clear solutions

### What Kills Adoption

1. ❌ "Install Python first" - Lost 80% of users
2. ❌ "Open terminal" - Lost 70% of users
3. ❌ "Clone this repo" - Lost 90% of users
4. ❌ "Edit config file" - Lost 60% of users
5. ❌ "Requires desktop" - Lost mobile-only users
6. ❌ "Must be online" - Lost field workers
7. ❌ Technical error messages - Lost everyone when errors occur

### The "One-Click" Rule

**If Sarah can't get it working in under 2 minutes with zero technical knowledge, it's too complicated.**

Every decision should be evaluated against this standard.

---

## Next Steps

1. Implement hosted WebUI deployment
2. Create Windows/Mac installers with wizards
3. Enhance PWA for mobile users
4. Create separate documentation for each user type
5. User testing with real NUAA staff
6. Iterate based on feedback

---

**Last Updated:** 2025-11-19
**Owner:** NUAA Development Team
**Status:** Implementation In Progress
