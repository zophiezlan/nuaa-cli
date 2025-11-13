# NUAA-Kit Multi-Agent Setup Guide

**Using Multiple AI Agents in One Project**

---

## The Reality: Teams Use Different Tools

Not everyone on your team uses the same AI coding assistant. Some prefer Claude Code for long-form writing, others love GitHub Copilot for Excel work, and maybe someone uses Gemini for research. **That's okay!** NUAA-Kit is designed to work with multiple agents.

This guide helps you:

1. Choose the right agent for each task
2. Maintain consistency across agents
3. Share context effectively
4. Avoid common multi-agent pitfalls

---

## Supported AI Agents

NUAA-Kit commands work with these AI agents:

| Agent                   | Strengths                                                     | Best For                                      | How to Use                     |
| ----------------------- | ------------------------------------------------------------- | --------------------------------------------- | ------------------------------ |
| **Claude Code**         | Long-form writing, contextual understanding, empathy          | `/nuaa.design`, `/nuaa.propose`               | Chat interface, slash commands |
| **GitHub Copilot Chat** | Code completion, Excel formulas, data structures              | `/nuaa.measure` (Excel work), Word formatting | VS Code, Chat mode             |
| **Gemini CLI**          | Research synthesis, evidence gathering, multi-source analysis | Background research, evidence base            | Terminal commands              |
| **Qwen Code**           | Multilingual support, accessibility, inclusive language       | Peer-friendly outputs, plain language         | Chat interface                 |
| **Windsurf**            | Workflow automation, UI design, iterative refinement          | Visual workflows, Microsoft 365 integration   | IDE-based                      |
| **Cursor**              | Code editing, refactoring, technical documentation            | Technical specs, API documentation            | IDE-based                      |

---

## Agent Comparison Matrix

### By Task Type

| Task                     | Best Agent     | Alternative            | Avoid                     |
| ------------------------ | -------------- | ---------------------- | ------------------------- |
| Write program design     | Claude Code    | Gemini                 | -                         |
| Write funding proposal   | Claude Code    | Qwen (if multilingual) | -                         |
| Create logic model       | Claude Code    | Copilot                | -                         |
| Build Excel dashboards   | GitHub Copilot | Windsurf               | Claude (not its strength) |
| Write Excel formulas     | GitHub Copilot | Claude                 | -                         |
| Format Word documents    | GitHub Copilot | Windsurf               | -                         |
| Gather evidence/research | Gemini         | Claude                 | -                         |
| Write in plain language  | Qwen           | Claude                 | -                         |
| Create visual workflows  | Windsurf       | Copilot                | -                         |
| Debug issues             | Cursor         | Copilot                | -                         |

### By Output Format

| Output Format                  | Best Agent     | Why                                  |
| ------------------------------ | -------------- | ------------------------------------ |
| Markdown (program designs)     | Claude Code    | Excellent long-form, structured text |
| Word (.docx) with formatting   | GitHub Copilot | Native Office integration            |
| Excel (.xlsx) with formulas    | GitHub Copilot | Native Office integration            |
| PowerPoint (.pptx)             | Windsurf       | Visual design strengths              |
| Plain language (peer-friendly) | Qwen           | Accessibility focus                  |
| Technical documentation        | Cursor         | Code/tech documentation strengths    |

### By Workflow Phase

| Phase               | Recommended Agent | Alternative |
| ------------------- | ----------------- | ----------- |
| 1. Design Program   | Claude Code       | -           |
| 2. Gather Evidence  | Gemini            | Claude      |
| 3. Write Proposal   | Claude Code       | Qwen        |
| 4. Create Budget    | GitHub Copilot    | Windsurf    |
| 5. Build Data Tools | GitHub Copilot    | Cursor      |
| 6. Implement        | GitHub Copilot    | Claude      |
| 7. Analyze Data     | GitHub Copilot    | Gemini      |
| 8. Write Report     | Claude Code       | Qwen        |

---

## Setup Strategies

### Strategy 1: Primary + Secondary (Recommended for Small Teams)

**Best for**: 2-5 person teams, simple programs

**Approach**:

- Choose **one primary agent** for consistency (e.g., Claude Code)
- Use **one secondary agent** for specialized tasks (e.g., Copilot for Excel)
- Everyone uses the same two agents

**Example**:

```
Primary: Claude Code
  - /nuaa.design
  - /nuaa.propose
  - /nuaa.report

Secondary: GitHub Copilot
  - Excel dashboards
  - Word formatting
  - Data analysis
```

**Benefits**:

- Simple to manage
- Consistent output style
- Easy context sharing

**Drawbacks**:

- May not leverage best agent for every task

---

### Strategy 2: Task-Based Selection (Best for Medium Teams)

**Best for**: 5-10 person teams, multiple programs

**Approach**:

- Match **agent to task type**, not person
- Create agent recommendation guide (see matrix above)
- Everyone uses best agent for their task

**Example**:

```
Program Manager (Jane):
  - Claude Code for /nuaa.design
  - Claude Code for /nuaa.propose

Evaluation Coordinator (John):
  - GitHub Copilot for Excel dashboards
  - Claude Code for /nuaa.report

Research Officer (Maria):
  - Gemini for evidence gathering
  - Claude Code for synthesis
```

**Benefits**:

- Leverages each agent's strengths
- Higher quality outputs
- Team flexibility

**Drawbacks**:

- More complex to manage
- Potential inconsistency

---

### Strategy 3: Role-Based Agents (For Large Teams)

**Best for**: 10+ person teams, organizational adoption

**Approach**:

- Assign agents by **organizational role**
- Standardize within each role
- Cross-role collaboration strategies

**Example**:

```
Program Design Team:
  - Primary: Claude Code
  - Secondary: Gemini (research)

Development/Fundraising Team:
  - Primary: Claude Code
  - Secondary: Qwen (multilingual)

Evaluation Team:
  - Primary: GitHub Copilot
  - Secondary: Gemini (analysis)

Community Engagement:
  - Primary: Qwen (accessibility)
  - Secondary: Claude Code
```

**Benefits**:

- Clear team standards
- Expertise development
- Role-appropriate tools

**Drawbacks**:

- Requires coordination
- Training overhead

---

## Context Sharing Between Agents

Different agents don't automatically share context. Here's how to share key information:

### Method 1: Context Files

Create a `project-context.md` file with essential information:

```markdown
# Project Context: Peer Naloxone Distribution Program

## Key Details

- **Program Name**: Peer Naloxone Distribution
- **Target**: 200 people at risk of opioid overdose
- **Duration**: 12 months (Jan 2025 - Dec 2025)
- **Budget**: $50,000
- **Key Staff**: Jane (coordinator), John (peer educator), Maria (evaluator)

## NUAA Principles

- Peer-led approach (John is person with lived experience)
- Consumer remuneration: $300/session standard
- Harm reduction: Non-judgmental, meet people where they're at
- Cultural safety: LGBTIQ+ inclusive, trauma-informed

## Key Decisions Made

- Decision to use peer circles, not lectures (Consumer Advisory, March 2025)
- Decision to increase follow-up support (Evaluation data, June 2025)

## Files to Reference

- program-design.md (v2.0 current)
- proposal.md (NSW Health funded, Jan 2025)
- impact-framework.md (current evaluation plan)
```

**Usage**:

- Share this file at start of every AI session
- Update when key decisions made
- All agents read same context

---

### Method 2: Consistent Naming

Use the same naming conventions across all agents:

**File naming**:

```
✅ peer-naloxone-program-design-v2.0.md
✅ peer-naloxone-proposal-nsw-health-2025.md
✅ peer-naloxone-evaluation-data-q2-2025.xlsx

❌ program1.md
❌ proposal_final_v3_really_final.md
❌ data.xlsx
```

**Benefit**: Any agent can find and reference the right files

---

### Method 3: Explicit Cross-References

When using one agent after another, explicitly reference previous outputs:

**Example** (using Copilot after Claude):

```
I'm working on an Excel dashboard for the "Peer Naloxone Distribution" program.
Here's the program design created with Claude Code:

[Paste key sections from program-design.md]

Please create an Excel dashboard with these indicators:
[List indicators from impact-framework.md]
```

**Benefit**: Agent has full context even if it didn't create original design

---

### Method 4: SharePoint as Single Source of Truth

Store all documents in SharePoint:

- Agents reference SharePoint links
- Version history tracked automatically
- Everyone accesses latest version
- No duplicate/conflicting files

**Example SharePoint structure**:

```
NUAA Programs/
├── Peer Naloxone Distribution/
│   ├── Design/
│   │   ├── program-design-v2.0.md
│   │   └── logic-model-v2.0.md
│   ├── Funding/
│   │   └── proposal-nsw-health-2025.md
│   ├── Evaluation/
│   │   ├── impact-framework-v1.0.md
│   │   └── evaluation-data-q2-2025.xlsx
│   └── Reports/
│       └── quarterly-report-q2-2025.md
```

---

## Maintaining Consistency Across Agents

### 1. Standard Prompts

Create reusable prompts that work with any agent:

**Template**:

```
I'm working on a NUAA program: "[PROGRAM_NAME]"

NUAA Principles to embed:
- Peer-led approach (center lived experience)
- Harm reduction (non-judgmental, evidence-based)
- Consumer remuneration ($300/session standard)
- Cultural safety (trauma-informed, LGBTIQ+ inclusive)

Task: [SPECIFIC TASK]

Context: [PROJECT CONTEXT]

Please ensure the output:
- Uses NUAA language and values
- Is specific and actionable (no placeholders)
- Is ready for immediate use
```

**Usage**: Copy-paste this template, fill in brackets, use with any agent

---

### 2. Style Guidelines

Define NUAA's communication style:

**Professional (for funders)**:

- Formal language
- Evidence-based
- Technical detail
- Policy-ready

**Professional-Peer (internal)**:

- Clear, direct language
- Balance detail and accessibility
- Practical focus

**Peer-Friendly (community)**:

- Plain language
- Visual emphasis
- Accessible, inclusive

**Agent instruction**:

```
Use "Professional-Peer" style:
- Clear, direct language (not overly formal)
- Avoid jargon unless essential
- Explain technical terms
- Practical, actionable guidance
```

---

### 3. Quality Checklist

Use the same quality checks regardless of agent:

✓ **NUAA principles embedded** (peer-led, harm reduction)  
✓ **Consumer remuneration** included ($300/session)  
✓ **No placeholders** (all [brackets] filled in)  
✓ **Specific numbers** (not "some people" but "40 people")  
✓ **Evidence-based** (references research/data)  
✓ **Cultural safety** addressed (LGBTIQ+, trauma-informed)  
✓ **Stakeholder-appropriate** language (funder, peer, etc.)

---

## Common Multi-Agent Pitfalls

### Pitfall 1: Inconsistent Voice

**Problem**: Claude writes compassionately, Copilot writes technically, outputs sound disjointed

**Solution**:

- Use Standard Prompts (above) with every agent
- Define style guidelines explicitly
- Have one person edit for consistency across agents

**Example**:

```
❌ Claude writes: "Participants journey from isolation to connection..."
   Copilot writes: "User engagement metrics: mean=7.2, SD=1.4"
   (Sounds like two different programs!)

✅ Both agents told: "Use Professional-Peer style, balance empathy and evidence"
   Claude: "Participants rate connection at 7.2/10 (up from 4.5 baseline)"
   Copilot: "Connection scores improved significantly: 4.5 → 7.2 (p<0.01)"
   (Consistent but appropriate to each agent's strength)
```

---

### Pitfall 2: Context Loss

**Problem**: Copilot doesn't know what Claude designed, creates Excel dashboard that doesn't match program design

**Solution**:

- Use Context Files (project-context.md)
- Explicitly cross-reference previous outputs
- Store everything in SharePoint

---

### Pitfall 3: Duplicate Work

**Problem**: Two people use different agents to do the same task, waste time

**Solution**:

- Clear role assignments (who does what)
- Communication (check before starting)
- SharePoint version control (see who's working on what)

---

### Pitfall 4: Agent Limitations Ignored

**Problem**: Using Claude for Excel formulas, frustrating experience

**Solution**:

- Use Agent Comparison Matrix (above)
- Match agent to task type
- Accept that switching agents is okay

---

### Pitfall 5: No Standard Naming

**Problem**: Files named inconsistently, can't find right version

**Solution**:

- Adopt naming convention (see Method 2 above)
- Train everyone on standard
- Review periodically

---

## Team Setup Checklist

When setting up multi-agent workflow for your team:

### 1. Choose Strategy

- [ ] Decide: Primary+Secondary, Task-Based, or Role-Based?
- [ ] Document decision and communicate to team

### 2. Create Context File

- [ ] Create `project-context.md` with key details
- [ ] Store in SharePoint
- [ ] Train team to reference it

### 3. Define Style Guidelines

- [ ] Document NUAA's 3 communication styles
- [ ] Create examples of each
- [ ] Share with team

### 4. Set Up SharePoint

- [ ] Create folder structure
- [ ] Enable version control
- [ ] Set permissions

### 5. Train Team

- [ ] Agent comparison matrix workshop
- [ ] Context sharing practice
- [ ] Quality checklist review

### 6. Test with One Program

- [ ] Pilot with one program
- [ ] Refine based on learnings
- [ ] Scale to other programs

---

## Example Workflows

### Workflow 1: Design with Claude, Budget with Copilot

**Step 1: Design (Claude Code)**

```
User in Claude:
/nuaa.design "Peer Naloxone Distribution" "people at risk of overdose" "12 months"

Claude creates: program-design.md with preliminary budget
```

**Step 2: Budget Detail (GitHub Copilot)**

```
User in Copilot Chat:
I have a NUAA program design (attached: program-design.md).

Create detailed budget in Excel with:
- Personnel costs (peer educator $35/hour x 15 hours/week x 52 weeks)
- Consumer remuneration ($300/session x 24 sessions)
- Materials (naloxone kits, training materials)
- Operations (venue, catering, transport)
- Evaluation (10% of budget)

Format with tables, formulas, charts.

Copilot creates: budget-calculator.xlsx with all formulas
```

**Result**: Design in Markdown (Claude's strength), budget in Excel (Copilot's strength)

---

### Workflow 2: Research with Gemini, Write with Claude

**Step 1: Research (Gemini CLI)**

```
User in terminal:
gemini "Find evidence on peer naloxone distribution effectiveness. \
        Focus on NSW context, peer-led models, overdose prevention outcomes. \
        Summarize key studies with statistics."

Gemini creates: research-summary.md with evidence
```

**Step 2: Synthesize (Claude Code)**

```
User in Claude:
I'm writing a proposal for peer naloxone distribution.
Here's the research evidence (attached: research-summary.md).

Synthesize this into a compelling "Evidence Base" section for the proposal.
Use NUAA's values (harm reduction, peer-led, lived experience).
Include specific statistics but tell the story compellingly.

Claude creates: evidence-section.md (ready to insert in proposal)
```

**Result**: Research from Gemini (its strength), compelling narrative from Claude (its strength)

---

### Workflow 3: Complete Program Lifecycle with Multiple Agents

**1. Design (Claude Code)**

```
/nuaa.design → program-design.md
```

**2. Evidence Gathering (Gemini CLI)**

```
gemini "Research [topic]" → research-summary.md
```

**3. Proposal Writing (Claude Code)**

```
/nuaa.propose → proposal.md (incorporating research)
```

**4. Budget Building (GitHub Copilot)**

```
Create Excel budget → budget-calculator.xlsx
```

**5. Word Formatting (GitHub Copilot)**

```
Format proposal in Word with NUAA branding → proposal.docx
```

**6. Evaluation Setup (GitHub Copilot)**

```
Create Excel dashboard for data tracking → evaluation-dashboard.xlsx
```

**7. Data Analysis (GitHub Copilot)**

```
Analyze evaluation data, generate charts → analysis-results.xlsx
```

**8. Report Writing (Claude Code)**

```
/nuaa.report → evaluation-report.md
```

**Total agents used**: 3 (Claude, Gemini, Copilot)  
**Each agent used for its strengths**

---

## Troubleshooting

### Issue: Agent Doesn't Understand NUAA Context

**Symptom**: Generic nonprofit language, doesn't sound like NUAA

**Solution**:

1. Share `project-context.md` at start of session
2. Use Standard Prompt template with NUAA principles
3. Give examples of NUAA voice (paste previous program designs)
4. Explicitly request: "Use NUAA's language and values (peer-led, harm reduction)"

---

### Issue: Excel Dashboard Doesn't Match Program Design

**Symptom**: Indicators in Excel differ from impact-framework.md

**Solution**:

1. Open both documents side-by-side
2. Copy indicator list from impact-framework.md
3. Paste into Copilot prompt: "Use exactly these indicators:"
4. Review generated dashboard against framework before finalizing

---

### Issue: Outputs Have Different Formatting

**Symptom**: Some documents use Title Case, others use Sentence case, etc.

**Solution**:

1. Create NUAA style guide (formatting standards)
2. Include in Standard Prompt template
3. One person does final formatting pass
4. Use Word/SharePoint styles for consistency

---

### Issue: Too Many Agents, Team Confused

**Symptom**: People don't know which agent to use

**Solution**:

1. Simplify to Primary + Secondary strategy
2. Clear decision tree: "Use Claude unless doing Excel/Word, then Copilot"
3. Training session on agent selection

---

## Success Stories

### Example 1: Efficiency Boost

**Team**: 3 staff (program coordinator, evaluator, development officer)  
**Agents**: Claude Code (primary), GitHub Copilot (secondary)  
**Result**:

- Design time reduced from 40 hours → 8 hours (Claude)
- Budget building from 6 hours → 2 hours (Copilot)
- Evaluation dashboard from 10 hours → 3 hours (Copilot)
- Total time saved: 43 hours per program

---

### Example 2: Quality Improvement

**Team**: Consumer advisory involved in all design  
**Agents**: Claude for design, Qwen for peer-friendly versions  
**Result**:

- Consumer advisory rated designs 8/10 (up from 6/10)
- Plain language versions more accessible
- Multilingual outputs for CALD communities
- Greater community engagement

---

## Next Steps

1. **Review Agent Comparison Matrix**: Understand strengths of each agent
2. **Choose Strategy**: Primary+Secondary, Task-Based, or Role-Based
3. **Create Context File**: Start with project-context.md for current program
4. **Train Team**: Workshop on agent selection and context sharing
5. **Pilot with One Program**: Test approach, refine, scale

---

## Related Documentation

- [workflow-diagram.md](workflow-diagram.md) - How commands connect
- [evolution-guide.md](evolution-guide.md) - Maintaining specs over time
- [../QUICKSTART.md](../QUICKSTART.md) - Initial setup guide

---

**Remember**: The best agent is the one that produces the best output for the specific task. Don't force one agent for everything. Use the right tool for the job!

---

_This multi-agent guide is inspired by community feedback from the github/spec-kit repository and adapted for NUAA's multi-stakeholder context._
