# NUAA-Kit Evolution Guide

**How to Keep Program Designs Fresh as Programs Evolve**

---

## The Challenge

Programs change over time:

- Scope expands or contracts
- Target populations shift
- Budgets get adjusted
- New evidence emerges
- Staff learn from experience
- Community needs evolve

**Without a strategy**, program designs become outdated, creating a gap between documentation and reality. This guide provides systematic approaches to evolving your program designs while maintaining quality and alignment.

---

## Core Principles

### 1. Specifications Should Be "Living Documents"

✅ Update regularly (not just once at creation)
✅ Reflect current reality (not just original plan)
✅ Guide ongoing implementation (not just historical record)

### 2. Not Everything Changes

Some elements should remain stable:

- Core NUAA principles (peer-led, harm reduction)
- Consumer remuneration standards ($300/session)
- Ethical guidelines (informed consent, confidentiality)

Other elements should evolve:

- Specific activities based on learnings
- Target numbers based on capacity
- Budget allocations based on actuals
- Evaluation indicators based on feasibility

### 3. Version Control Matters

Track what changed, when, and why:

- Version numbers (v1.0, v1.1, v2.0)
- Change logs (what changed in each version)
- Rationale (why changes were made)

---

## Preservation Strategy

### Protected Files (Never Auto-Regenerate)

These files contain project-specific customizations:

✅ **Keep and manually maintain**:

- `nuaa-kit/config.yml` (if you customize settings)
- Program-specific `program-design.md` files (after initial creation)
- Consumer advisory feedback documents
- Stakeholder interview notes
- Custom evaluation instruments

**Rationale**: These reflect NUAA's specific decisions and context

### Updatable Files (Safe to Regenerate)

These files can be replaced when NUAA-Kit updates:

✅ **Safe to update**:

- `nuaa-kit/templates/` (core templates)
- `nuaa-kit/commands/` (command documentation)
- `nuaa-kit/docs/` (methodology guides)
- NUAA-Kit README and QUICKSTART

**Rationale**: These are methodology, not project data

### Hybrid Files (Merge Carefully)

These files might have both NUAA-Kit content and project customizations:

⚠️ **Review before updating**:

- `accessibility-guidelines.md` (if you added NUAA-specific guidance)
- `evaluation-data-dictionary.md` (if you added custom indicators)
- `glossary.md` (if you added NUAA-specific terms)

**Rationale**: Mix of methodology and project data

---

## Update Frequency Recommendations

### Quarterly Reviews (Every 3 Months)

**Purpose**: Light-touch review of program designs

**Process**:

1. Review program-design.md for accuracy
2. Update any changed numbers (participants reached, budget spent)
3. Note any activity modifications
4. Document learnings in a "Change Log" section

**Who**: Program coordinator + consumer advisory member
**Time**: 1-2 hours per program
**Trigger**: End of quarter, prepare funder report

**Example Changes**:

- Participant numbers adjusted (planned 40, reaching 35)
- Meeting frequency changed (monthly → bi-monthly based on feedback)
- Budget reallocated (more catering, less printing)

---

### Annual Reviews (Once per Year)

**Purpose**: Comprehensive re-evaluation of program design

**Process**:

1. Use `/nuaa.diagnose` to assess outcomes achieved
2. Gather consumer advisory feedback
3. Review evaluation data
4. Use `/nuaa.adapt` to redesign problem areas
5. Generate updated program-design.md (new major version)

**Who**: Program team + consumer advisory + management
**Time**: 4-6 hours per program
**Trigger**: End of funding year, strategic planning

**Example Changes**:

- Stakeholder journeys revised based on participant feedback
- Logic model updated (added intermediate outcomes discovered)
- Risk assessment updated (new risks emerged, old ones mitigated)
- Evaluation framework refined (some indicators dropped, new ones added)

---

### Event-Triggered Reviews (As Needed)

**Purpose**: Respond to significant changes

**Triggers**:

- Major scope change (funder adds/cuts budget significantly)
- Target population shift (program expands to new community)
- Partnership changes (key partner leaves or joins)
- Critical incident (safety issue, ethical concern)
- Poor outcomes (evaluation shows not achieving goals)

**Process**:

1. Use `/nuaa.diagnose` to understand issue
2. Use `/nuaa.adapt` to redesign affected areas
3. Update program-design.md immediately
4. Communicate changes to all stakeholders

**Who**: Program coordinator + relevant stakeholders
**Time**: 2-4 hours (urgent response)
**Trigger**: As event occurs

---

## Version Control Best Practices

### Versioning Scheme

Use semantic versioning: `MAJOR.MINOR.PATCH`

**Examples**:

- `v1.0` - Initial program design (approved and funded)
- `v1.1` - Minor update (participant numbers adjusted, no redesign)
- `v1.2` - Minor update (activity schedule changed)
- `v2.0` - Major update (redesigned logic model, new activities)

**When to increment**:

- **MAJOR** (v1 → v2): Significant redesign, different approach, new theory of change
- **MINOR** (v1.0 → v1.1): Adjustments but same basic design, activity tweaks
- **PATCH** (v1.1.0 → v1.1.1): Typo fixes, clarifications, formatting

---

### Adding Version History to Documents

Add this section to your `program-design.md`:

```markdown
## Version History

| Version | Date       | Author          | Changes                                          | Rationale                                        |
| ------- | ---------- | --------------- | ------------------------------------------------ | ------------------------------------------------ |
| v1.0    | 2025-01-15 | Jane Smith      | Initial design                                   | Program approved by consumer advisory            |
| v1.1    | 2025-04-20 | Jane Smith      | Participant target: 40 → 35                      | Capacity constraint identified                   |
| v1.2    | 2025-07-10 | Jane Smith      | Meeting frequency: monthly → bi-monthly          | Participant feedback preference                  |
| v2.0    | 2026-01-15 | Jane Smith + CA | Major redesign of activities based on evaluation | Evaluation showed activities not engaging enough |

## Change Log (v2.0)

### What Changed

- Activities redesigned from didactic workshops to peer-led discussion circles
- Added one-on-one follow-up component
- Logic model updated with intermediate outcome: "Increased peer support connections"
- Risk assessment added: "Peer facilitator burnout"

### Why Changed

- Evaluation data showed low engagement with lecture-style sessions (avg. 3/10 rating)
- Participant feedback: "Want more discussion, less talking at us"
- Consumer advisory recommendation: "Peer circles work better than workshops"

### Impact of Change

- Expect higher engagement (target 7/10 rating)
- Budget reallocated from venue hire (big rooms) to catering (small groups)
- Staff time reallocated from presentation prep to facilitator support
```

---

## Workflow: Quarterly Update

**Time Required**: 1-2 hours

**Steps**:

### 1. Review Current Program Design (15 min)

- Open `program-design.md`
- Skim all sections
- Note anything that feels outdated

### 2. Check Against Reality (30 min)

Compare design to what's actually happening:

- ✅ Participant numbers: Planned vs. Actual
- ✅ Activities: Described vs. Delivered
- ✅ Budget: Allocated vs. Spent
- ✅ Timeline: Planned vs. Actual

### 3. Gather Feedback (15 min)

Quick check-in:

- Consumer advisory: "How's it going? Anything to change?"
- Participants: Review recent feedback forms
- Staff: "What's working? What's not?"

### 4. Update Document (30 min)

Make minor edits:

- Update numbers (participants, sessions delivered, budget spent)
- Tweak activities if delivery changed
- Note any learnings in Change Log

### 5. Increment Version (5 min)

- Update version number (e.g., v1.0 → v1.1)
- Add row to Version History table
- Document changes in Change Log

### 6. Share Update (10 min)

- Email consumer advisory with changes
- Share in team meeting
- Post updated version to SharePoint

---

## Workflow: Annual Review

**Time Required**: 4-6 hours

**Steps**:

### 1. Gather Data (1 hour)

Collect evidence:

- Evaluation data (outputs, outcomes achieved)
- Participant feedback (surveys, interviews)
- Staff observations (what worked, what didn't)
- Consumer advisory input (meeting notes)
- Funder feedback (if available)

### 2. Diagnose (1 hour)

Use `/nuaa.diagnose`:

```bash
/nuaa.diagnose "Peer Naloxone Distribution" \
    --outcomes="200 reached (target 200), 80% knowledge increase (target 60%), \
                15 reported reversals (no target but positive)" \
    --issues="Peer educator turnover high (3 of 5 left), \
              hard-to-reach populations not accessing (only 10% Aboriginal participants)"
```

**AI will help identify**:

- What's working well (keep doing)
- What's not working (stop or change)
- What's missing (add)
- Root causes of issues

### 3. Adapt Program Design (2 hours)

Use `/nuaa.adapt`:

```bash
/nuaa.adapt "Peer Naloxone Distribution" \
    --changes="Add peer educator support program, partner with Aboriginal-led orgs, \
               increase remuneration for peer educators" \
    --rationale="Address turnover and reach issues"
```

**AI will help**:

- Redesign problem areas
- Update logic model
- Revise stakeholder journeys
- Adjust evaluation indicators

### 4. Consumer Advisory Review (1 week wait time)

- Share draft updated design
- Present at consumer advisory meeting
- Gather feedback
- Revise as needed

### 5. Finalize and Version (30 min)

- Increment to next major version (v1.x → v2.0)
- Add comprehensive Change Log
- Update Version History table
- Mark document as `status: approved` in front matter

### 6. Communicate Broadly (30 min)

- Email all stakeholders with summary of changes
- Update SharePoint with new version
- Schedule staff training if major changes
- Brief funders if significant redesign

---

## Workflow: Event-Triggered Update

**Time Required**: 2-4 hours (urgent)

**Scenarios**:

### Scenario 1: Budget Cut

**Event**: Funder cuts budget from $50K to $35K mid-program

**Response**:

1. **Immediate** (1 hour):

   - Use `/nuaa.adapt` to redesign with reduced budget
   - Identify what to cut (least essential activities)
   - Consult consumer advisory urgently

2. **Within 1 week**:
   - Update program-design.md (new MAJOR version)
   - Communicate changes to all stakeholders
   - Adjust evaluation indicators (lower targets)

**Version**: v2.0 (major change to scope)

---

### Scenario 2: Safety Incident

**Event**: Participant discloses serious trauma during workshop

**Response**:

1. **Immediate** (same day):

   - Follow NUAA incident response protocol
   - Debrief with staff and consumer advisory
   - Pause program if needed for safety

2. **Within 2 days**:

   - Use `/nuaa.adapt` to add trauma-informed protocols
   - Update program-design.md Risk Assessment section
   - Add staff training requirement
   - Revise Ethical Considerations section

3. **Within 1 week**:
   - Share updated design with all staff
   - Implement new protocols
   - Update consumer advisory

**Version**: v1.1 or v2.0 depending on severity

---

### Scenario 3: Population Shift

**Event**: Program originally for PWID, now many meth users joining

**Response**:

1. **Within 1 month**:

   - Use `/nuaa.diagnose` to understand new population needs
   - Use `/nuaa.adapt` to modify activities for broader audience
   - Update target population description
   - Revise stakeholder journeys for meth users specifically
   - Adjust evaluation to include meth-specific outcomes

2. **Consumer advisory**:
   - Get input from people who use meth
   - Ensure content appropriate and relevant

**Version**: v2.0 (major change to target population)

---

## Migration Strategies

### Strategy 1: Gradual Evolution

**Best for**: Programs with minor ongoing tweaks

**Approach**:

- Update document directly (inline edits)
- Increment MINOR versions frequently
- Maintain continuity over time

**Example**:

```
v1.0 → v1.1 → v1.2 → v1.3 → v1.4 → v1.5 (over 2 years)
All minor tweaks, never major redesign
```

---

### Strategy 2: Annual Refresh

**Best for**: Programs with stable design but annual planning cycles

**Approach**:

- Run annually at planning time
- Major redesign if needed based on evaluation
- Skip minor updates in between

**Example**:

```
v1.0 (Year 1) → v2.0 (Year 2) → v3.0 (Year 3)
Each year, comprehensive review and redesign
```

---

### Strategy 3: Cohort-Based Versions

**Best for**: Programs with distinct cohorts or phases

**Approach**:

- New major version for each cohort
- Learn from Cohort 1, improve for Cohort 2
- Document learnings explicitly

**Example**:

```
v1.0 (Cohort 1: Jan-Jun) → v2.0 (Cohort 2: Jul-Dec)
"Cohort 1 taught us X, so we changed Y for Cohort 2"
```

---

## Tools for Tracking Changes

### Option 1: Git (Recommended for Tech-Savvy Teams)

Use Git to track all changes:

```bash
# Initialize git in your program folder
cd program-design-folder
git init
git add program-design.md
git commit -m "v1.0 - Initial design approved by consumer advisory"

# Make changes
# Edit program-design.md
git add program-design.md
git commit -m "v1.1 - Update participant numbers: 40 → 35"

# View history
git log --oneline
```

**Benefits**:

- Full change history
- Can revert to any previous version
- Diff view shows exactly what changed

**Drawbacks**:

- Requires git knowledge
- Learning curve for non-technical staff

---

### Option 2: SharePoint Versioning

Use built-in SharePoint features:

1. Upload `program-design.md` to SharePoint
2. Enable "Require Check Out"
3. Enable "Version History"
4. Each edit creates automatic version
5. View history: Right-click file → "Version History"

**Benefits**:

- No new tools to learn
- Automatic versioning
- Integrated with NUAA's existing systems

**Drawbacks**:

- Less control than Git
- Harder to see detailed diffs

---

### Option 3: Manual Version Folders

Simple folder structure:

```
Program Name/
├── v1.0/
│   └── program-design.md
├── v1.1/
│   └── program-design.md
├── v2.0/
│   └── program-design.md
└── CURRENT → v2.0/ (symlink or copy)
```

**Benefits**:

- Very simple
- No tools needed
- Easy to understand

**Drawbacks**:

- Takes more disk space
- Manual management
- Can get messy

---

## Quality Checks for Updates

Before finalizing any update, verify:

✓ **Version number updated** correctly
✓ **Version History table** has new row
✓ **Change Log** explains what and why
✓ **All numbers accurate** (participants, budget, dates)
✓ **Logic model still makes sense** (inputs → activities → outcomes)
✓ **Risk assessment current** (new risks added, old ones removed if mitigated)
✓ **Evaluation indicators still measurable** (don't track what you can't measure)
✓ **Consumer advisory approved** changes (if significant)
✓ **Stakeholders notified** of changes
✓ **SharePoint updated** with latest version

---

## Common Mistakes & How to Avoid

### Mistake 1: Letting Designs Get Stale

**Problem**: Program design from 2 years ago, totally outdated
**Impact**: Documentation doesn't guide practice, just bureaucratic burden
**Solution**: Set calendar reminders for quarterly reviews

### Mistake 2: Changing Too Much, Too Often

**Problem**: Redesigning every month, no stability
**Impact**: Staff confused, participants don't know what to expect
**Solution**: Only make changes when evidence warrants, not on whim

### Mistake 3: Not Documenting Rationale

**Problem**: Version history says "Update activities" but not why
**Impact**: Can't learn from past, repeat mistakes
**Solution**: Always add "Why" to Change Log, not just "What"

### Mistake 4: No Consumer Input on Changes

**Problem**: Staff redesign program without consumer advisory input
**Impact**: Changes don't reflect community needs
**Solution**: Always involve consumer advisory in significant changes

### Mistake 5: Forgetting to Communicate Updates

**Problem**: Update document but don't tell anyone
**Impact**: Different stakeholders working from different versions
**Solution**: Share every update, even minor ones

---

## Success Metrics

How to know if your evolution strategy is working:

**Good Signs**:

- Program designs accurately reflect current practice
- Staff reference designs regularly (not just for funding)
- Consumer advisory feels heard (their input leads to changes)
- Evaluation data aligns with design (measuring what we said we'd do)
- New staff can onboard using design docs (docs actually useful)

**Bad Signs**:

- Nobody looks at designs after initial creation
- Staff say "The design is outdated" when asked
- Consumer advisory doesn't know there's a design document
- Evaluation reports don't mention the design
- Documents have placeholder text still (never finalized)

---

## Next Steps

1. **Choose your update frequency**: Quarterly? Annual? Event-driven?
2. **Set calendar reminders**: Don't rely on memory
3. **Train staff**: Everyone should know how to update designs
4. **Involve consumer advisory**: Make them part of review process
5. **Start small**: Pick one program, try quarterly update, refine process
6. **Scale up**: Apply learnings to all programs

---

## Related Documentation

- [workflow-diagram.md](workflow-diagram.md) - How commands connect
- [multi-agent-setup.md](multi-agent-setup.md) - Using different AI agents
- [../QUICKSTART.md](../QUICKSTART.md) - Initial setup guide
- [../commands/adapt.md](../commands/adapt.md) - Adapting program designs

---

**Remember**: The goal is not perfection, but continuous improvement. Programs evolve, and documentation should evolve with them.

---

*This evolution guide is inspired by best practices from the github/spec-kit community and adapted for NUAA's harm reduction context.*
