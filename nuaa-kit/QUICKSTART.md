# NUAA Quick Start Guide

**Welcome!** This guide will help you start using NUAA to design programs, write proposals, and measure impact - all within your first week.

> **Note**: This guide assumes you've already run `uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init .` in your project directory. If you haven't done that yet, see the [README](https://github.com/zophiezlan/nuaa-cli/blob/main/README.md) for installation instructions.

---

## What is NUAA?

NUAA is a **project management toolkit** that helps you:

1. **Design programs** with logic models, stakeholder journeys, and risk assessments
2. **Write funding proposals** that tell compelling stories and secure resources
3. **Measure impact** with rigorous, participatory evaluation frameworks

It's based on "Spec-Driven Development" from software engineering, adapted for non-profit program management and infused with NUAA's peer-led, harm reduction values.

---

## Who Should Use This?

- **Program staff** - Design and implement peer-led programs
- **Development/fundraising staff** - Write funding proposals
- **Evaluation staff** - Create impact measurement frameworks
- **Management** - Oversee program planning and reporting
- **Consumer advisory members** - Co-design programs and evaluation

---

## What You Have After Init

After running `nuaa init .` in your project, you now have:

```
your-project/
├── .nuaa/
│   ├── memory/          # Project constitution, context
│   ├── scripts/         # Workflow scripts (bash/PowerShell)
│   └── templates/       # All 19 document templates
├── .claude/commands/    # (if you chose Claude)
├── .github/agents/      # (if you chose Copilot)
├── .gemini/commands/    # (if you chose Gemini)
└── [your existing files]
```

**Key locations**:

- **Templates**: `.nuaa/templates/` - All document templates
- **Commands**: In your AI agent's folder (`.claude/commands/`, etc.)
- **Scripts**: `.nuaa/scripts/` - Automation scripts for workflows

---

## Quick Start: Your First Week

### Week 1, Day 1: Orientation (30 minutes)

**1. Choose Your Interface**

You have two ways to use NUAA:

**Option A: WebUI (Recommended for most users)**

```bash
python .nuaa/scripts/start_webui.py
# Then open http://localhost:5000 in your browser
```

**Option B: AI Assistant Commands**
If you're using Claude Code, GitHub Copilot, or another AI assistant, use slash commands like `/nuaa.design`

**2. Understand the Core Commands**

- **Program Design**: `/nuaa.design` or WebUI → "Program Design"
- **Funding**: `/nuaa.propose` or WebUI → "Funding Proposal"
- **Evaluation**: `/nuaa.measure` or WebUI → "Impact Framework"
- **Planning**: `/nuaa.engage`, `/nuaa.partner`, `/nuaa.risk`
- **Events & Training**: `/nuaa.event`, `/nuaa.train`

**3. Explore Your Templates**

Your project now has **19 comprehensive templates** in `.nuaa/templates/`:

**Core templates**:

- `program-design.md` - Program design structure
- `proposal.md` - Funding proposal format
- `logic-model.md` - Logic model template
- `impact-framework.md` - Evaluation framework

**Planning & management templates**:

- `stakeholder-engagement-plan.md` - Stakeholder mapping and engagement
- `partnership-agreement.md` - MOUs and formal agreements
- `risk-register.md` - Risk identification and mitigation
- `communication-plan.md` - Communications strategy
- `event-plan.md` - Event and workshop planning
- `training-curriculum.md` - Training design

See `.nuaa/templates/README.md` for the complete catalog of all 19 templates.

**4. Try Your First Command**

Depending on your interface choice:

**If using WebUI**:

1. Start the WebUI: `python .nuaa/scripts/start_webui.py`
2. Open browser to `http://localhost:5000`
3. Click "Program Design" and fill in the form
4. See your generated program design!

**If using AI Assistant**:

1. Open your AI assistant (Claude, Copilot, etc.)
2. Type: `/nuaa.design Create a peer-led hepatitis C education program`
3. Answer the assistant's questions
4. Review the generated document

**Action**: By end of Day 1, you should understand what NUAA does and how it can help your work.

---

### Week 1, Day 2-3: Design Your First Program (2-4 hours)

**Scenario**: You want to design a peer-led Hepatitis C education program.

**Step 1: Gather Your Inputs**

Before using `/nuaa.design`, collect:

- **Program idea**: What are you trying to do?
  - Example: "Peer-Led Hepatitis C Education for people who inject drugs"
- **Target population**: Who benefits?
  - Example: "People who inject drugs in Western Sydney, particularly those unaware of treatment options"
- **Duration**: How long?
  - Example: "6 months (2 cohorts of 12 weeks each)"
- **Purpose**: What problem does this address?
  - Example: "Low awareness of Hep C treatment despite high prevalence in PWID community"
- **Evidence**: What supports this?
  - Example: "NSW Health data shows 50%+ PWID have Hep C, but only 20% have accessed treatment"
- **Key activities**: What will you do?
  - Example: "Peer-led workshops (6 sessions), one-on-one support, referrals to treatment services"
- **Resources**: What do you have?
  - Example: "$30K budget, 1 peer educator (0.6 FTE), partnership with Western Sydney LHD"

**Step 2: Use NUAA to Create the Design**

**Option A: Using WebUI**

1. Start WebUI: `python .nuaa/scripts/start_webui.py`
2. Click "Program Design"
3. Fill in the form with your inputs from Step 1
4. Click "Generate" and review the output

**Option B: Using AI Assistant**
In your AI chat interface, type:

```
/nuaa.design "Peer-Led Hepatitis C Education" "people who inject drugs in Western Sydney" "6 months"
```

The AI will ask you clarifying questions. Answer based on your inputs from Step 1.

**Step 3: Review and Refine**

The AI will generate a complete `program-design.md` document. Review it:

- ✅ Are the stakeholder journeys realistic?
- ✅ Does the logic model make sense (inputs → activities → outputs → outcomes → impact)?
- ✅ Are risks identified with mitigation strategies?
- ✅ Is consumer participation meaningful (not tokenistic)?
- ✅ Is the budget realistic and justified?

Refine sections as needed by asking the AI to revise specific parts.

**Step 4: Share for Feedback**

Share the draft with:

- Consumer advisory (get peer input)
- Management (check feasibility)
- Potential partners (confirm collaboration)

**Action**: By end of Day 3, you should have a draft program design ready for feedback.

---

### Week 1, Day 4: Write Your First Proposal (2-3 hours)

**Scenario**: You want to turn your Hep C education program design into a funding proposal for NSW Health.

**Step 1: Gather Your Inputs**

Before using `/nuaa.propose`, collect:

- **Program design**: Your completed program-design.md from Day 2-3
- **Funder**: Who are you applying to?
  - Example: "NSW Health - Hepatitis C Grants Round 2025"
- **Amount**: How much are you requesting?
  - Example: "$30,000"
- **Duration**: How long?
  - Example: "6 months"
- **Funder priorities**: What do they care about?
  - Example: "Reducing Hep C transmission, increasing treatment uptake, reaching priority populations"
- **Application guidelines**: What do they require?
  - Example: "10-page proposal, specific budget template, 3 x letters of support"

**Step 2: Use NUAA to Create the Proposal**

**Option A: Using WebUI**

1. Start WebUI: `python .nuaa/scripts/start_webui.py`
2. Click "Funding Proposal"
3. Select your program design as the basis
4. Fill in funder details
5. Click "Generate" and review the output

**Option B: Using AI Assistant**
In your AI chat interface, type:

```
/nuaa.propose "Peer-Led Hepatitis C Education" "NSW Health" "$30000" "6 months"
```

The AI will ask clarifying questions about the funder and your program. Provide details.

**Step 3: Customize for Funder**

The AI will generate a proposal. Customize it by:

- **Aligning language**: Use the funder's terminology (e.g., if they say "consumers," use that instead of "clients")
- **Highlighting alignment**: Show how your program fits their priorities
- **Adding required sections**: Include any specific sections they require
- **Formatting**: Match their format (page limits, section headings, budget template)

**Step 4: Gather Attachments**

Prepare attachments (listed at end of proposal):

- NUAA Annual Report
- Letters of Support (from partners)
- Staff CVs/Bios
- Logic Model (visual)
- Budget Detail (Excel)

**Step 5: Proofread and Submit**

- Get someone else to proofread (fresh eyes catch errors)
- Check all requirements met (use funder's checklist)
- Submit before deadline!

**Action**: By end of Day 4, you should have a draft proposal ready for final review and submission.

---

### Week 1, Day 5: Create Your First Impact Measurement Framework (2-3 hours)

**Scenario**: You want to create an evaluation framework for your Hep C education program.

**Step 1: Gather Your Inputs**

Before using `/nuaa.measure`, collect:

- **Program design**: Your program-design.md (includes logic model)
- **Evaluation period**: How long will you evaluate?
  - Example: "6 months program + 3-month follow-up = 9 months total"
- **Evaluation budget**: How much allocated?
  - Example: "$3,000 (10% of program budget)"
- **Primary questions**: What do you need to know?
  - Process: Did we reach 40 people as planned?
  - Outcome: Did knowledge and confidence increase?
  - Impact: Did more people access treatment?

**Step 2: Use NUAA to Create the Framework**

**Option A: Using WebUI**

1. Start WebUI: `python .nuaa/scripts/start_webui.py`
2. Click "Impact Framework"
3. Select your program design
4. Enter evaluation period and budget
5. Click "Generate" and review the indicators

**Option B: Using AI Assistant**
In your AI chat interface, type:

```
/nuaa.measure "Peer-Led Hepatitis C Education" "9 months" "$3000"
```

The AI will ask clarifying questions about your program and evaluation priorities.

**Step 3: Review Indicators and Methods**

The AI will generate an impact framework with indicators and methods. Review:

- ✅ Are indicators clear and measurable?
- ✅ Are methods feasible (not too burdensome)?
- ✅ Is participant voice centered (peer researchers, participatory methods)?
- ✅ Are ethics covered (consent, confidentiality, safety)?
- ✅ Is timeline realistic?

**Step 4: Plan for Implementation**

Prepare for evaluation:

- Set up survey tools (e.g., Google Forms, SurveyMonkey)
- Recruit peer researcher (if not already hired)
- Create consent forms (use NUAA templates)
- Train staff on data collection procedures

**Action**: By end of Day 5, you should have an evaluation framework ready to implement.

---

## Common Use Cases

### Use Case 1: You Have a Program Idea and Need to Design It

**Path**: `/nuaa.design` → share with consumer advisory → refine → approve

**Time**: 4-6 hours

**Output**: Complete program design document ready for implementation or proposal writing

---

### Use Case 2: You Have a Program Design and Need Funding

**Path**: `/nuaa.design` (if not done) → `/nuaa.propose` → customize for funder → gather attachments → submit

**Time**: 6-8 hours (design + proposal)

**Output**: Funding proposal ready to submit

---

### Use Case 3: You Have a Funded Program and Need to Evaluate It

**Path**: `/nuaa.design` (if not done) → `/nuaa.measure` → set up data collection → implement

**Time**: 4-6 hours (framework) + ongoing implementation

**Output**: Impact measurement framework and data collection tools

---

### Use Case 4: You Need to Report on a Program

**Path**: Use your impact framework from `/nuaa.measure` → collect data → analyze → report

**Time**: Varies (depends on data collection and analysis)

**Output**: Evaluation report for funders, community, and stakeholders

---

### Use Case 5: You're Planning a Major Event or Training

**Path**: `/nuaa.event` or `/nuaa.train` → review checklist → implement → evaluate

**Time**: 2-3 hours (planning document)

**Output**: Complete event plan or training curriculum with logistics, accessibility, and participant support

**Example**: Planning a Peer Forum launch event with 75 attendees:

```
/nuaa.event "Peer Forum Launch 2025" "Forum" "75 people"
```

This generates a comprehensive plan covering:

- Event program and schedule
- Logistics (venue, catering, equipment)
- Accessibility and participant support
- Risk management
- Budget and resources

---

### Use Case 6: You're Building Partnerships or Managing Risks

**Path**: `/nuaa.engage`, `/nuaa.partner`, or `/nuaa.risk` → customize → implement → review

**Time**: 2-4 hours (planning document)

**Output**: Stakeholder engagement plan, partnership agreement (MOU), or risk register

**Example**: Creating a partnership with a Local Health District:

```
/nuaa.partner "Harm Reduction Outreach" "Western Sydney LHD" "2 years"
```

This generates an MOU template covering:

- Roles and responsibilities
- Governance and decision-making
- Information sharing protocols
- Financial arrangements
- Dispute resolution

---

## Tips for Success

### 1. Start Simple

Don't try to design the most complex program ever on your first try. Start with:

- A program you know well
- A small-scale pilot
- An existing program you want to document

### 2. Involve Consumer Advisory Early

Don't design programs in isolation. Get peer input:

- Share draft designs with consumer advisory
- Ask: "Does this make sense? Would you participate? What's missing?"
- Incorporate feedback before finalizing

### 3. Use Real Examples

When using commands, provide specific details (not vague):

- ❌ "Some people"
- ✅ "40 people who inject drugs in Western Sydney, aged 18-50, accessing NUAA's NSP"

### 4. Budget Realistically

Don't lowball to seem cheap:

- Include consumer remuneration ($300/session standard)
- Include participant support (transport, catering)
- Include evaluation costs (5-15% of budget)
- Include admin overhead (10-20%)

### 5. Iterate

First draft won't be perfect. Refine by:

- Asking AI to revise specific sections
- Getting feedback from colleagues/peers
- Testing with a small pilot first

### 6. Save and Version

- Save your designs and proposals in shared folders
- Use version numbers (v1.0, v1.1, v2.0)
- Track changes (especially for co-authored documents)

### 7. Learn from Past Work

- Look at previous NUAA program designs and proposals
- See what worked (funded, successful outcomes)
- Adapt templates based on learnings

---

## Microsoft 365 Integration (Coming Soon)

The NUAA Kit will integrate with Microsoft 365 tools NUAA already uses:

**Word Templates**:

- Branded NUAA templates for proposals and reports
- Co-authoring (multiple people editing simultaneously)
- Comments and track changes for review

**Excel Dashboards**:

- Budget calculators (auto-calculate totals, percentages)
- Evaluation tracking (enter data, auto-generate graphs)
- Grant pipeline (track applications, deadlines, outcomes)

**SharePoint**:

- Document library (all designs and proposals in one place)
- Version history (see previous versions, restore if needed)
- Permissions (control who can view/edit)

**Teams**:

- Program channels (one channel per program)
- File sharing (designs, proposals, reports)
- Collaborative discussion

**Power Automate**:

- Automated workflows (e.g., when proposal approved, create program folder)
- Reminders (evaluation deadlines, funder check-ins)

**Watch this space** - these integrations will be rolled out in coming weeks!

---

## Troubleshooting

### Problem: AI asks too many questions

**Solution**: Provide more context upfront. Instead of just program name, include:

```
/nuaa.design "Peer-Led Hep C Education" "people who inject drugs in Western Sydney" "6 months" --context="Budget $30K, partnership with Western Sydney LHD, targeting 40 participants, peer-led workshops + one-on-one support"
```

### Problem: Generated document has placeholders like [Amount]

**Solution**: The AI needs more specific information. Re-run command with details:

- Budget amounts
- Specific targets (numbers)
- Actual dates/timeframes

### Problem: Generated content doesn't sound like NUAA

**Solution**: Add NUAA's voice by:

- Reviewing and editing (change language to NUAA's style)
- Providing examples of past NUAA documents
- Asking AI to revise with specific NUAA principles highlighted

### Problem: Too overwhelming - where do I start?

**Solution**: Start with ONE program you know well. Don't try to redesign everything at once:

1. Pick your most familiar program
2. Use `/nuaa.design` to document it
3. Learn the process
4. Apply to other programs

---

## Getting Help

### Internal Support

- **Program team**: Ask colleagues who've used NUAA Kit before
- **Management**: For strategic alignment and approval
- **Consumer advisory**: For peer input on designs

### External Support

- **AI agent communities**: GitHub Copilot, Claude, Gemini forums have active users
- **Harm reduction sector**: Network with other harm reduction orgs doing similar work
- **Evaluation partners**: UNSW, other research partners can support evaluation design

---

## Next Steps After Week 1

Once you're comfortable with the basics:

### Week 2-3: Implement Your First Program

- Use your program design to guide implementation
- Track activities and outputs
- Collect evaluation data as planned

### Week 4+: Iterate and Improve

- Review what worked and what didn't
- Update program design based on learnings
- Share learnings with team and consumer advisory
- Apply insights to next program

### Build Your Library

- Create a library of NUAA program designs
- Develop boilerplate text for proposals (NUAA's history, approach, capacity)
- Document case studies and success stories
- Build up evidence base

---

## Success Stories (To Be Added)

As NUAA staff use the kit, we'll add success stories here:

- Programs designed and funded
- Time saved (from X days to Y hours)
- Improved quality (clearer designs, stronger proposals)
- Greater impact (better evaluation, stronger evidence)

**Your success story could be next!**

---

## Feedback and Improvement

The NUAA Kit is a living toolkit. We want your feedback:

**What's working?**

- What saves you time?
- What improves your work quality?
- What features are most useful?

**What needs improvement?**

- What's confusing or unclear?
- What features are missing?
- What would make this more useful?

**How to provide feedback**:

- Email [program team email]
- Discuss at team meetings
- Share at consumer advisory meetings

---

## Conclusion

The NUAA Kit is designed to make your work **faster, easier, and better**:

- **Faster**: Generate comprehensive designs and proposals in hours, not days
- **Easier**: Templates and commands guide you through the process
- **Better**: Consistent quality, NUAA principles embedded, evidence-based

**You've got this!** By the end of Week 1, you'll have designed a program, written a proposal, and created an impact measurement framework. That's powerful.

**Welcome to the NUAA Kit community. Let's design some amazing peer-led, harm reduction programs together!**

---

**Questions? Get stuck? Ask for help - we're all learning together.**
