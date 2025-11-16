# NUAA-Kit Workflow Diagram

**Purpose**: Visual guide to understanding how NUAA-Kit commands connect throughout the program lifecycle.

---

## Complete Program Lifecycle

```mermaid
graph TD
    Start[Program Idea] --> Design[/nuaa.design]
    Design --> DesignDoc[program-design.md]

    DesignDoc --> ConsumerReview{Consumer<br/>Advisory<br/>Review?}
    ConsumerReview -->|Feedback| Refine1[/nuaa.refine]
    Refine1 --> DesignDoc
    ConsumerReview -->|Approved| MeasureBranch{Need<br/>Funding?}

    MeasureBranch -->|Yes| Propose[/nuaa.propose]
    MeasureBranch -->|No| Measure[/nuaa.measure]

    Propose --> ProposalDoc[proposal.md]
    ProposalDoc --> FunderReview{Funder<br/>Review?}
    FunderReview -->|Revisions Needed| Refine2[/nuaa.refine]
    Refine2 --> ProposalDoc
    FunderReview -->|Funded| Measure

    Measure --> ImpactDoc[impact-framework.md]
    ImpactDoc --> Implementation[Program Implementation]

    Implementation --> DataCollection[Data Collection]
    DataCollection --> Report[/nuaa.report]
    Report --> EvalReport[evaluation-report.md]

    EvalReport --> Review{Outcomes<br/>Achieved?}
    Review -->|No - Adapt| Adapt[/nuaa.adapt]
    Review -->|Yes - Continue| Continue[Continue Program]
    Review -->|Mixed - Diagnose| Diagnose[/nuaa.diagnose]

    Adapt --> DesignDoc
    Diagnose --> Troubleshoot[/nuaa.troubleshoot]
    Troubleshoot --> Implementation

    Continue --> NextCycle[Next Funding Cycle]
    NextCycle --> Propose

    style Start fill:#e1f5e1
    style DesignDoc fill:#fff3cd
    style ProposalDoc fill:#fff3cd
    style ImpactDoc fill:#fff3cd
    style EvalReport fill:#fff3cd
    style Implementation fill:#cfe2ff
    style Continue fill:#d1e7dd
```

---

## Quick Reference: Command Flow

### Phase 1: Design

```
Program Idea
    ↓
/nuaa.design
    ↓
program-design.md
    ↓
Consumer Advisory Review
    ↓
[Iterate with /nuaa.refine if needed]
```

**Outputs**:

- program-design.md
- logic-model.md
- stakeholder journey maps

**Decision Point**: Need funding? → Yes: Go to Phase 2a | No: Go to Phase 2b

---

### Phase 2a: Funding Path

```
program-design.md
    ↓
/nuaa.propose
    ↓
proposal.md
    ↓
Submit to Funder
    ↓
[Revise with /nuaa.refine if needed]
    ↓
Funded → Go to Phase 2b
```

**Outputs**:

- proposal.md
- budget-calculator.xlsx
- supporting documents

---

### Phase 2b: Measurement Planning

```
program-design.md
    ↓
/nuaa.measure
    ↓
impact-framework.md
    ↓
Set up data collection tools
```

**Outputs**:

- impact-framework.md
- data collection instruments
- evaluation timeline

---

### Phase 3: Implementation

```
impact-framework.md
    ↓
Implement Program
    ↓
Collect Data Continuously
    ↓
[Use /nuaa.diagnose if issues arise]
    ↓
[Use /nuaa.adapt to modify approach]
```

**Outputs**:

- Activity logs
- Participant data
- Process documentation

---

### Phase 4: Reporting & Learning

```
Collected Data
    ↓
/nuaa.report
    ↓
evaluation-report.md
    ↓
Share with stakeholders
    ↓
Decision: Continue, Adapt, or End?
```

**Outputs**:

- evaluation-report.md
- data dashboards
- learnings documentation

**Decision Point**: Outcomes achieved?

- Yes → Continue program, prepare next funding cycle
- No → Use /nuaa.adapt to redesign
- Mixed → Use /nuaa.diagnose to understand why

---

## Workflow Patterns

### Pattern 1: New Greenfield Program

**Scenario**: Designing a brand new program from scratch

```
1. /nuaa.design       (4-6 hours)
2. Consumer review    (1 week)
3. /nuaa.refine       (2-3 hours if needed)
4. /nuaa.propose      (3-4 hours)
5. Submit proposal    (varies)
6. /nuaa.measure      (2-3 hours)
7. Implement          (program duration)
8. /nuaa.report       (quarterly/final)
```

**Total Planning Time**: 10-15 hours
**Key Success Factor**: Consumer advisory involvement early

---

### Pattern 2: Documenting Existing Program

**Scenario**: An established program lacks documentation

```
1. /nuaa.document     (NEW - to be implemented)
2. Staff interviews   (gather current state)
3. /nuaa.design       (formalize into design doc)
4. /nuaa.measure      (add evaluation if missing)
5. Continue program   (with documentation)
```

**Total Time**: 8-12 hours
**Key Success Factor**: Accurate current state assessment

---

### Pattern 3: Iterating on Existing Program

**Scenario**: Program running but needs improvements

```
1. /nuaa.diagnose     (identify issues)
2. /nuaa.adapt        (redesign problem areas)
3. /nuaa.refine       (update program-design.md)
4. Re-implement       (with changes)
5. /nuaa.measure      (update indicators)
6. /nuaa.report       (compare before/after)
```

**Total Time**: 6-10 hours
**Key Success Factor**: Clear problem identification

---

### Pattern 4: Quick Proposal from Existing Design

**Scenario**: Program designed, new funder opportunity arises

```
1. Open program-design.md  (existing)
2. /nuaa.propose           (customize for funder)
3. Submit proposal         (quickly)
```

**Total Time**: 3-4 hours
**Key Success Factor**: Comprehensive original design

---

## Command Dependency Map

Shows which commands require which artifacts as inputs:

```
/nuaa.design
  ├── Inputs: Program idea, target population, duration
  └── Outputs: program-design.md, logic-model.md

/nuaa.propose
  ├── Inputs: program-design.md (required)
  └── Outputs: proposal.md, budget-calculator.xlsx

/nuaa.measure
  ├── Inputs: program-design.md (required), logic-model.md
  └── Outputs: impact-framework.md, data collection tools

/nuaa.report
  ├── Inputs: impact-framework.md (required), collected data
  └── Outputs: evaluation-report.md, dashboards

/nuaa.refine
  ├── Inputs: Any existing document + feedback
  └── Outputs: Updated version of that document

/nuaa.diagnose (planned)
  ├── Inputs: program-design.md, evaluation data, staff feedback
  └── Outputs: problem analysis, recommendations

/nuaa.adapt (planned)
  ├── Inputs: problem analysis, program-design.md
  └── Outputs: Updated program-design.md with changes

/nuaa.document (planned)
  ├── Inputs: Existing program information, staff interviews
  └── Outputs: program-design.md for existing program
```

---

## Decision Trees

### "Where Should I Start?" Decision Tree

```
Do you have a program idea?
├── Yes → Is it new or existing?
│   ├── New → Start with /nuaa.design
│   └── Existing → Start with /nuaa.document (or /nuaa.design if manual)
└── No → Review NUAA strategic plan, community needs, then start with /nuaa.design
```

### "Do I Need a Proposal?" Decision Tree

```
Is the program funded?
├── Yes → Skip to /nuaa.measure
├── No → Do you have a design?
│   ├── Yes → Use /nuaa.propose
│   └── No → Start with /nuaa.design, then /nuaa.propose
└── Partially → Use /nuaa.propose for additional funding
```

### "My Program Isn't Working" Decision Tree

```
Are outcomes being achieved?
├── No → Use /nuaa.diagnose
│   └── Then use /nuaa.adapt to redesign
├── Partially → Use /nuaa.diagnose
│   └── Then use /nuaa.troubleshoot for specific issues
└── Yes, but not as expected → Use /nuaa.refine to adjust targets
```

---

## Integration with Microsoft 365 (Future)

```
NUAA-Kit Commands → Microsoft 365 Tools
├── /nuaa.design → Word (branded template)
├── /nuaa.propose → Word + Excel (budget)
├── /nuaa.measure → Excel (data tracking)
├── /nuaa.report → Word + Excel (dashboards)
└── All docs → SharePoint (version control)
                   ↓
            Power Automate (workflows)
                   ↓
            Teams (collaboration)
```

**Planned Automations**:

- Auto-save to SharePoint on document generation
- Email notifications when review needed
- Calendar events for evaluation milestones
- Dashboard updates when data entered

---

## Multi-Agent Workflow (Recommended)

Different AI agents excel at different tasks:

```
/nuaa.design
├── Best: Claude Code (long-form, contextual)
└── Alternative: GitHub Copilot Chat

/nuaa.propose
├── Best: Claude Code (persuasive writing)
└── Alternative: Gemini (research synthesis)

/nuaa.measure
├── Best: GitHub Copilot (Excel formulas, data structure)
└── Alternative: Claude Code

/nuaa.report
├── Best: GitHub Copilot (data analysis, charts)
└── Alternative: Claude Code (narrative synthesis)

Excel Work
├── Best: GitHub Copilot (formulas, VBA)
└── Alternative: Claude Code

Word Formatting
├── Best: GitHub Copilot (styles, layout)
└── Alternative: Claude Code
```

**Consistency Tip**: Use the same agent for a full workflow (design → propose → measure) to maintain context and voice consistency.

---

## Timeline Estimates

### Minimal Viable Program (MVP)

- Design: 4 hours
- Proposal: 3 hours
- Measurement: 2 hours
- **Total**: 9 hours (1-2 business days)

### Comprehensive Program

- Design + Consumer Review: 8 hours + 1 week
- Proposal + Funder Customization: 6 hours
- Measurement + Tool Setup: 5 hours
- **Total**: 19 hours + 1 week (3 business days + review time)

### Existing Program Documentation

- Document/Design: 6 hours
- Measurement Framework: 3 hours
- **Total**: 9 hours (1-2 business days)

---

## Common Pitfalls & Solutions

### Pitfall 1: Skipping Consumer Advisory Review

**Problem**: Design doesn't reflect community needs
**Solution**: Always include consumer review step before finalizing design
**Workflow**: `/nuaa.design` → Consumer Advisory → `/nuaa.refine` → Finalize

### Pitfall 2: Writing Proposals Before Design

**Problem**: Proposals lack depth, logic models weak
**Solution**: Always complete `/nuaa.design` first
**Workflow**: `/nuaa.design` → program-design.md → `/nuaa.propose`

### Pitfall 3: No Evaluation Planning

**Problem**: Can't measure impact, funder reporting difficult
**Solution**: Use `/nuaa.measure` before implementation
**Workflow**: `/nuaa.design` → `/nuaa.measure` → Implement

### Pitfall 4: Forgetting to Update Documentation

**Problem**: Design becomes outdated, doesn't reflect reality
**Solution**: Use `/nuaa.adapt` when making program changes
**Workflow**: Program Change → `/nuaa.adapt` → Update program-design.md

### Pitfall 5: Not Diagnosing Issues Early

**Problem**: Program continues failing, resources wasted
**Solution**: Use `/nuaa.diagnose` at first sign of trouble
**Workflow**: Issues Arise → `/nuaa.diagnose` → `/nuaa.adapt` → Retry

---

## Next Steps

1. **Bookmark this page**: Reference when starting new programs
2. **Print workflow diagram**: Post in office for quick reference
3. **Share with team**: Ensure everyone understands the flow
4. **Customize if needed**: Adapt patterns to NUAA's specific context
5. **Provide feedback**: Help us improve the workflow based on your experience

---

## Related Documentation

- [README.md](../README.md) - Overview of NUAA-Kit
- [QUICKSTART.md](../QUICKSTART.md) - Week-by-week onboarding guide
- [STATUS.md](../STATUS.md) - Implementation status of commands
- [commands/design.md](../commands/design.md) - Detailed `/nuaa.design` guide
- [commands/propose.md](../commands/propose.md) - Detailed `/nuaa.propose` guide
- [commands/measure.md](../commands/measure.md) - Detailed `/nuaa.measure` guide

---

**Questions?** Contact NUAA program team or refer to the QUICKSTART guide.

---

_This workflow diagram is based on best practices from spec-driven development and adapted for NUAA's peer-led, harm reduction approach._
