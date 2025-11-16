# NUAA-Kit Update Guide

**How to Keep NUAA-Kit Templates and Commands Up-To-Date**

---

## Why Update NUAA-Kit?

NUAA-Kit evolves over time with:

- 🐛 **Bug fixes** - Correcting errors in templates
- ✨ **New features** - Additional commands or templates
- 📚 **Improved documentation** - Clearer guidance
- 🔄 **Best practices** - Learnings from usage
- 🛡️ **Security updates** - Vulnerability patches

**Regular updates ensure** you benefit from these improvements without starting from scratch.

---

## Update Philosophy

### What Gets Updated

✅ **Safe to update** (NUAA-Kit methodology):

- `nuaa-kit/templates/` - Core templates
- `nuaa-kit/commands/` - Command documentation
- `nuaa-kit/docs/` - Methodology guides
- `nuaa-kit/README.md` - Overview
- `nuaa-kit/QUICKSTART.md` - Training guide

### What Stays Protected

🔒 **Never auto-update** (your project data):

- Your specific `program-design.md` files
- Your `proposal.md` files
- Your `evaluation-data.xlsx` files
- Custom configurations
- Consumer advisory notes
- Stakeholder feedback

### What Needs Care

⚠️ **Review before updating** (mixed content):

- `accessibility-guidelines.md` (if customized)
- `evaluation-data-dictionary.md` (if added indicators)
- `glossary.md` (if added NUAA-specific terms)

---

## When to Update

### Quarterly Check (Recommended)

**Frequency**: Every 3 months
**Time**: 30 minutes
**Purpose**: See if new features available

**Process**:

1. Check NUAA-Kit repository for updates
2. Review changelog for relevant changes
3. Decide if update needed
4. Plan update for next maintenance window

---

### Annual Update (Minimum)

**Frequency**: Once per year
**Time**: 2-3 hours
**Purpose**: Major version updates, new features

**Process**:

1. Review all changes since last update
2. Test in development environment
3. Update production
4. Train staff on new features

---

### As-Needed Updates

**Triggers**:

- 🐛 Critical bug discovered
- 🔒 Security vulnerability announced
- ✨ Feature you need is added
- 📚 Documentation improvement you need

**Process**: Update immediately when triggered

---

## How to Check for Updates

### Method 1: Check GitHub Repository (Manual)

1. Visit the NUAA-Kit/nuaa-cli repository
2. Check `nuaa-kit/CHANGELOG.md`
3. Compare current version to installed version

**Example**:

```markdown
# NUAA-Kit CHANGELOG

## [v2.1.0] - 2025-11-15

### Added

- New /nuaa.document command for existing programs
- Multi-agent setup guide

### Fixed

- Template placeholder validation

## [v2.0.0] - 2025-09-01

### Added

- /nuaa.refine command
- Evolution guide documentation

(etc.)
```

---

### Method 2: Email Notifications (Recommended)

**Setup**:

1. Go to GitHub repository
2. Click "Watch" → "Custom" → "Releases"
3. Enter your email
4. Receive notifications when updates released

---

### Method 3: Internal Schedule (Organizational)

**Setup**:

1. Add calendar reminder: "Check NUAA-Kit updates" (quarterly)
2. Assign to one person (e.g., IT lead)
3. That person reviews and recommends updates

---

## Update Process (Step-by-Step)

### Step 1: Backup Current Installation (15 min)

Before updating, backup your current NUAA-Kit:

**Option A: Manual Backup**

```bash
# Create backup folder
cd /path/to/your/projects
cp -r nuaa-kit nuaa-kit-backup-2025-11-10

# Verify backup
ls nuaa-kit-backup-2025-11-10
```

**Option B: Git Commit (if using version control)**

```bash
cd /path/to/your/projects
git add nuaa-kit
git commit -m "Backup before NUAA-Kit update to v2.1.0"
git tag backup-before-v2.1.0
```

**Why backup**: If update causes issues, you can revert

---

### Step 2: Review Changelog (15 min)

Read the changelog carefully:

**Questions to ask**:

- ✓ What's new? (features, commands, templates)
- ✓ What's fixed? (bugs, errors)
- ✓ What's changed? (breaking changes, deprecations)
- ✓ Do I need this update? (relevant to NUAA's work)

**Example assessment**:

```
v2.1.0 Changelog:
✅ New /nuaa.document command - YES! We need to document existing programs
✅ Multi-agent guide - YES! We use Claude and Copilot
⚠️ Updated program-design template - CAREFUL! We customized this
❌ Codex agent support - NO, we don't use Codex
```

**Decision**: Update, but review program-design template carefully

---

### Step 3: Download Updated Files (10 min)

**Option A: Manual Download**

1. Go to GitHub repository releases page
2. Download latest release ZIP
3. Extract to temporary folder
4. Review files before copying

**Option B: Git Pull (if using version control)**

```bash
cd /path/to/nuaa-kit
git pull origin main
```

**Option C: Selective Download**
Download only specific files you need (e.g., new documentation)

---

### Step 4: Merge Updates Carefully (30-60 min)

**Process**:

#### For New Files (Easy)

Simply copy new files to your installation:

```bash
# Example: New multi-agent guide
cp nuaa-kit-v2.1.0/docs/multi-agent-setup.md your-project/nuaa-kit/docs/
```

#### For Updated Core Templates (Easy)

Replace methodology files (safe to overwrite):

```bash
# Example: Updated command documentation
cp nuaa-kit-v2.1.0/commands/*.md your-project/nuaa-kit/commands/
```

#### For Customized Files (Careful!)

Compare your version to new version, merge manually:

**Example - program-design template updated**:

1. Open your customized `templates/program-design.md`
2. Open new `templates/program-design.md` from update
3. Compare side-by-side
4. Identify what's new in update
5. Decide: Accept new version OR Keep customization OR Merge both

**Merge tools**:

- Visual Studio Code: Built-in diff/merge
- Git: `git diff` and `git merge`
- Manual: Side-by-side windows, copy changes over

---

### Step 5: Test Updates (30 min)

Before using updated NUAA-Kit in production:

**Test checklist**:

- [ ] Open a sample command file - renders correctly?
- [ ] Try generating a test document - works as expected?
- [ ] Check all links in documentation - no broken links?
- [ ] Review new features - understand how to use?
- [ ] Test with your AI agent - commands recognized?

**Example test**:

```
1. Open commands/design.md
2. Verify it loads without errors
3. Try /nuaa.design with test program
4. Verify output format matches expectations
5. Check template placeholders work correctly
```

**If tests fail**:

- Review what went wrong
- Check if you missed a step
- Consult update notes for breaking changes
- If stuck, revert to backup

---

### Step 6: Train Staff on Changes (1-2 hours)

If update includes new features or significant changes:

**Training needed**:

- New commands: How to use them
- Changed templates: What's different
- New workflows: Updated processes

**Training format**:

- Team meeting demo (30 min)
- Hands-on workshop (1 hour)
- Written guide (update docs)
- Q&A session (30 min)

**Example**:

```
v2.1.0 Update Training:

1. New /nuaa.document Command (30 min)
   - What it does: Document existing programs
   - How to use it: Demo with real program
   - Practice: Each person tries with one program

2. Multi-Agent Guide (15 min)
   - Overview of guide
   - When to use different agents
   - Context sharing tips

3. Q&A (15 min)
   - Answer questions
   - Troubleshoot issues
```

---

### Step 7: Document Update (10 min)

Record that you updated:

**Create update log**:

```markdown
# NUAA-Kit Update Log

## Update 2025-11-10

**From**: v2.0.0
**To**: v2.1.0

**Changes Applied**:

- ✅ Added /nuaa.document command
- ✅ Added multi-agent setup guide
- ✅ Updated evolution guide
- ⚠️ Kept customized program-design template (merged manually)

**Testing Results**:

- All commands work
- Documentation links valid
- AI agents recognize new commands

**Staff Trained**: 2025-11-15 (all program staff)

**Notes**:

- program-design template customization preserved
- Next update scheduled: 2026-02-10 (3 months)
```

---

## Handling Breaking Changes

**Breaking change** = Update that requires changing your existing work

**Examples**:

- Template structure completely redesigned
- Command syntax changed
- File naming convention changed

**When announced**:

1. **Read migration guide** (included in update notes)
2. **Plan migration** (may take longer than normal update)
3. **Test thoroughly** before production
4. **Consider delaying** if not urgent

**Example - Template redesign**:

```
Old program-design template had 8 sections
New program-design template has 12 sections (added 4, kept 8)

Migration:
1. Generate new template with /nuaa.design
2. Copy content from old template to new template
3. Fill in new sections
4. Review and validate
5. Update all existing programs (over time, not all at once)
```

---

## Rollback Plan

If update causes problems, revert to previous version:

### Rollback from Manual Backup

```bash
# Remove problematic update
rm -rf /path/to/your/projects/nuaa-kit

# Restore backup
cp -r /path/to/your/projects/nuaa-kit-backup-2025-11-10 /path/to/your/projects/nuaa-kit

# Verify restoration
ls /path/to/your/projects/nuaa-kit
```

### Rollback with Git

```bash
cd /path/to/your/projects
git checkout backup-before-v2.1.0
# OR
git revert <commit-hash-of-update>
```

**After rollback**:

- Document what went wrong
- Report issue to NUAA-Kit maintainers
- Wait for fix before re-attempting update

---

## Update Checklist

Use this checklist for every update:

### Pre-Update

- [ ] Backup current installation
- [ ] Review changelog
- [ ] Identify customized files
- [ ] Schedule update window (low-impact time)
- [ ] Notify team of upcoming update

### During Update

- [ ] Download updated files
- [ ] Merge updates carefully (review customizations)
- [ ] Test all commands
- [ ] Verify documentation links
- [ ] Check AI agent compatibility

### Post-Update

- [ ] Document update in log
- [ ] Train staff on changes
- [ ] Monitor for issues (first week)
- [ ] Schedule next update check (3 months)

---

## Common Update Scenarios

### Scenario 1: Minor Bug Fix

**Example**: Template has typo, fixed in v2.0.1

**Process**:

1. Quick review of change (5 min)
2. Download fixed template
3. Replace old template
4. Test with one document
5. Done!

**Time**: 15 minutes
**Risk**: Very low

---

### Scenario 2: New Command Added

**Example**: /nuaa.document command added in v2.1.0

**Process**:

1. Review command documentation (15 min)
2. Download new command file
3. Copy to installation
4. Test with sample program
5. Train staff (1 hour)
6. Roll out to team

**Time**: 2 hours
**Risk**: Low (new feature, doesn't affect existing)

---

### Scenario 3: Template Updated

**Example**: program-design template expanded in v3.0.0

**Process**:

1. Review template changes (30 min)
2. Compare to customized version
3. Merge changes carefully (1 hour)
4. Test with existing program designs
5. Decide migration strategy (all at once OR gradual)
6. Train staff (2 hours)

**Time**: 4-5 hours
**Risk**: Medium (may affect existing work)

---

### Scenario 4: Major Version Upgrade

**Example**: NUAA-Kit v3.0.0 with significant changes

**Process**:

1. Read full migration guide (1 hour)
2. Test in isolated environment (2 hours)
3. Plan phased rollout (1 week per phase)
4. Backup everything
5. Migrate gradually (1-2 programs at a time)
6. Comprehensive staff training (4 hours)
7. Monitor closely (1 month)

**Time**: 10-15 hours + 1 month monitoring
**Risk**: High (significant changes)

**Recommendation**: Wait for v3.0.1 (first patch) before upgrading

---

## Best Practices

### 1. Don't Skip Versions

❌ **Wrong**: Update from v1.0 directly to v3.0
✅ **Right**: Update v1.0 → v2.0 → v3.0 (in order)

**Reason**: Migration guides assume sequential updates

---

### 2. Test Before Production

❌ **Wrong**: Update production installation immediately
✅ **Right**: Test in development environment first

**Setup dev environment**:

```bash
# Create test folder
mkdir nuaa-kit-test
cp -r nuaa-kit nuaa-kit-test

# Test update in nuaa-kit-test first
# If successful, then update production nuaa-kit
```

---

### 3. Read Release Notes Carefully

❌ **Wrong**: Download latest version, install blindly
✅ **Right**: Read changelog, understand what's changing

**Especially look for**:

- Breaking changes
- Deprecations
- Migration required

---

### 4. Keep Update Log

❌ **Wrong**: Update whenever, no record
✅ **Right**: Document all updates with dates, versions, notes

**Benefit**: Know your update history, troubleshoot issues

---

### 5. Schedule Regular Checks

❌ **Wrong**: Wait until something breaks
✅ **Right**: Quarterly check for updates

**Add to calendar**: "NUAA-Kit update check" (every 3 months)

---

## Troubleshooting

### Issue: Update Broke Something

**Symptom**: Command doesn't work after update

**Solution**:

1. Check changelog for breaking changes
2. Review what changed in that command
3. Update your usage to match new syntax
4. If still broken, rollback and report issue

---

### Issue: Lost Customizations

**Symptom**: My custom template sections disappeared

**Solution**:

1. Restore from backup
2. Identify what was customized
3. Merge carefully (compare old vs new)
4. Document customizations for future updates

**Prevention**: Always backup before updating!

---

### Issue: AI Agent Doesn't Recognize New Command

**Symptom**: `/nuaa.document` doesn't work in agent

**Solution**:

1. Restart AI agent (reload commands)
2. Clear cache if applicable
3. Verify command file in correct location
4. Check agent supports command format

---

## Support & Resources

### Getting Help

If you encounter issues:

1. **Check documentation**: Review update guide and changelog
2. **Search issues**: Look for similar problems on GitHub
3. **Ask community**: Post question in discussions
4. **Contact maintainers**: Email for complex issues

### Useful Links

- NUAA-Kit Repository: [GitHub link]
- Changelog: `nuaa-kit/CHANGELOG.md`
- Issue Tracker: [GitHub Issues]
- Discussions: [GitHub Discussions]

---

## Future: Automated Updates (Planned)

**Vision**: Simple command to update NUAA-Kit

**Proposed**:

```bash
nuaa-kit update
# Checks for updates
# Shows changelog
# Offers to backup
# Updates safely
# Tests automatically
# Reports success
```

**Status**: Planned for future release
**Meanwhile**: Use this manual guide

---

## Summary

**Key Takeaways**:

1. ✅ Update regularly (quarterly recommended)
2. 🔒 Always backup before updating
3. 📚 Read changelog carefully
4. ⚠️ Protect your customizations
5. 🧪 Test before production
6. 📝 Document all updates
7. 👥 Train staff on changes

**Remember**: Updates bring improvements, but should never risk your existing work. When in doubt, backup and test first!

---

## Related Documentation

- [evolution-guide.md](evolution-guide.md) - Maintaining program specs over time
- [workflow-diagram.md](workflow-diagram.md) - How commands connect
- [multi-agent-setup.md](multi-agent-setup.md) - Using multiple AI agents
- [../CHANGELOG.md](../CHANGELOG.md) - History of changes

---

_This update guide is inspired by best practices from the github/spec-kit community and adapted for NUAA's organizational context._
