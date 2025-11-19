---
description: Refine and improve existing program documentation
scripts:
  sh: bash .nuaa/scripts/bash/update-agent-context.sh {ARGS}
  ps: powershell .nuaa/scripts/powershell/update-agent-context.ps1 {ARGS}
status: implemented
version: 1.0.0
mode: active
created: 2025-11-10
---

# /nuaa.refine - Iteratively Improve Program Documents

## Purpose

Systematically incorporate feedback and make targeted revisions to existing NUAA program documents (program designs, proposals, logic models, impact frameworks) while preserving version history and maintaining alignment across artifacts.

**Key Capabilities**:

- Focused refinement of specific document elements
- Structured feedback integration from consumer advisories, staff, funders
- Version control with change rationale documentation
- Cross-artifact consistency checking
- Quality validation and placeholder removal

## When to Use

- **After consumer advisory feedback**: Integrate recommendations from peer review sessions
- **During program iteration**: Refine design based on pilot learnings or mid-program evaluation
- **Pre-submission**: Final polish before submitting proposals or reports
- **Responding to funder questions**: Clarify or strengthen specific sections
- **Routine maintenance**: Quarterly or annual updates to keep documents current

## Usage

### Basic Refinement

```bash
/nuaa.refine Update the logic model in program-design.md based on consumer advisory feedback \
  that the "Activities" section needs more specificity about peer training components.
```

### Focused Refinement with Feedback File

```bash
/nuaa.refine Revise the proposal.md budget narrative, --focus=budget, \
  addressing the funder's questions about peer remuneration rates. \
  Feedback in feedback-from-funder.txt
```

### Refinement with Scope Constraint

```bash
/nuaa.refine Update impact-framework.md indicators for equity, --focus=evaluation, \
  keep all other indicators unchanged, add disaggregation by Aboriginal/TSI status.
```

### Cross-Document Consistency Check

```bash
/nuaa.refine Check consistency across program-design.md, logic-model.md, and \
  impact-framework.md, ensuring all activities in the logic model have corresponding \
  process indicators in the impact framework.
```

## Parameters

| Parameter           | Description                                   | Example Values                                                                   |
| ------------------- | --------------------------------------------- | -------------------------------------------------------------------------------- |
| Document path       | File to be refined                            | `program-design.md`, `proposal.md`, `impact-framework.md`                        |
| Refinement focus    | Specific section or element to revise         | `logic-model`, `budget`, `evaluation`, `narrative`, `outcomes`, `stakeholders`   |
| --focus             | Constrain changes to specific area            | `logic-model`, `budget`, `evaluation`, `narrative`, `equity`, `risks`            |
| --feedback          | Path to feedback file or inline feedback text | `feedback-advisory-group.md`, "The logic model needs..."                         |
| --mode              | How to present changes                        | `inline` (direct update), `diff` (show changes), `summary` (change summary only) |
| --preserve          | Elements that must not be changed             | `budget-totals`, `peer-remuneration-rate`, `participant-targets`                 |
| --check-consistency | Validate alignment across artifacts           | Flag (boolean)                                                                   |

## System Prompt for AI Agent

When this command is invoked, you are acting as a **document refinement specialist** with expertise in NUAA's harm reduction principles, peer-led program design, participatory methods, and grant writing.

### Your Task

1. **Understand the Refinement Request**:

   - Identify which document(s) need refinement
   - Determine the specific focus area (if provided)
   - Review any feedback provided (inline or from file)
   - Note any preservation constraints (elements that cannot change)

2. **Locate and Read Documents**:

   - Find the target document(s) in the program folder
   - Read current version and front matter (especially version number)
   - If cross-artifact consistency check requested, read all related documents

3. **Apply Refinements**:

   - Make targeted changes addressing the feedback or request
   - Maintain NUAA terminology and principles (see `glossary.md`)
   - Ensure changes are internally consistent within the document
   - If cross-artifact refinement, update all affected documents to maintain alignment

4. **Version Control**:

   - Increment version number appropriately:
     - Major (X.0.0): Significant restructuring or scope change
     - Minor (x.X.0): New sections or substantial content additions
     - Patch (x.x.X): Corrections, clarifications, small improvements
   - Document changes in "Version History" section or inline changelog
   - Preserve previous version if major changes

5. **Quality Checks**:

   - Run placeholder lint check (no unresolved `[brackets]` if status=final)
   - Verify all cross-references still valid
   - Check that budget totals still sum correctly (if budget refined)
   - Ensure logic model elements still align (inputs→activities→outputs→outcomes→impact)
   - Validate that indicator definitions remain clear and measurable

6. **Output Based on Mode**:

   - **`inline`**: Update document directly, increment version, add changelog entry
   - **`diff`**: Create a diff summary showing before/after for changed sections
   - **`summary`**: Generate a summary of proposed changes without modifying files

7. **Report Back**:
   - Summarize what was changed and why
   - Note any areas where feedback couldn't be fully addressed (with rationale)
   - Flag any cross-artifact inconsistencies discovered
   - Recommend next steps (e.g., "Review updated logic model with advisory group")

---

## Refinement Workflows

### Workflow 1: Consumer Advisory Feedback Integration

**Scenario**: Consumer advisory group reviewed draft program design and provided feedback.

**Steps**:

1. Collect feedback notes from advisory meeting
2. Organize feedback by document section
3. Run `/nuaa.refine` for each section with targeted feedback
4. Review changes for accuracy and tone
5. Circulate updated draft back to advisory group for validation
6. Finalize after confirmation

**Example Command**:

```bash
/nuaa.refine Update program-design.md stakeholder journey section based on advisory feedback: \
  "Peer workers should be listed as 'program co-designers' not 'program staff' to reflect \
  true co-production model. Journey map should show peer decision-making power."
```

---

### Workflow 2: Funder Question Response

**Scenario**: Funder asks clarifying questions about proposal before funding decision.

**Steps**:

1. Document funder's specific questions
2. Identify which proposal sections need strengthening
3. Run `/nuaa.refine` with funder questions as feedback
4. Ensure revisions directly address each question
5. Create a "Response to Funder Questions" appendix summarizing changes

**Example Command**:

```bash
/nuaa.refine Strengthen proposal.md Section 3 (Methodology) to address funder's question: \
  "How will you ensure cultural safety for Aboriginal participants?" --focus=methodology
```

---

### Workflow 3: Mid-Program Iteration

**Scenario**: Program is running but evaluation data suggests activities need adjustment.

**Steps**:

1. Review mid-program evaluation findings
2. Identify which activities or outcomes need refinement
3. Update program-design.md and logic-model.md to reflect learnings
4. Ensure impact-framework.md indicators still appropriate or adjust
5. Document rationale for changes (for funder accountability)

**Example Command**:

```bash
/nuaa.refine Update program-design.md and logic-model.md to reflect mid-program change: \
  shift from monthly group sessions to weekly drop-in format based on participant feedback \
  that scheduling conflicts were a barrier. Adjust activity descriptions and output targets.
```

---

### Workflow 4: Cross-Artifact Consistency Check

**Scenario**: Routine quarterly review to ensure all documents remain aligned.

**Steps**:

1. Run consistency check across all program artifacts
2. Review flagged inconsistencies
3. Decide whether to update documents or accept divergence (with rationale)
4. Apply updates to maintain alignment
5. Document any intentional inconsistencies

**Example Command**:

```bash
/nuaa.refine Check consistency across program-design.md, logic-model.md, \
  impact-framework.md, and proposal.md. Flag any misalignments in: \
  - Participant targets (should match across all docs) \
  - Activity descriptions (should be consistent) \
  - Indicators (must map to logic model elements) \
  - Budget categories (must align with activities)
```

---

### Workflow 5: Pre-Submission Quality Check

**Scenario**: Final review before submitting proposal to funder.

**Steps**:

1. Run placeholder lint check to catch unresolved brackets
2. Run consistency check across all referenced documents
3. Verify all budget calculations
4. Check that all sections required by funder RFP are present
5. Review for tone, clarity, and NUAA principles adherence
6. Get final peer review sign-off

**Example Command**:

```bash
/nuaa.refine Final quality check on proposal.md before submission. Run placeholder lint, \
  consistency check with program-design.md and budget-calculator.md, verify all RFP \
  requirements addressed, flag any remaining issues.
```

---

## Common Refinement Focus Areas

### Logic Model Refinement

**Typical Feedback**:

- "Activities are too vague, need more specificity"
- "Outputs are actually activities (fix categorization)"
- "Missing a causal link between X and Y"
- "Outcomes are too ambitious for timeframe"

**Refinement Approach**:

- Review logic model structure (inputs→activities→outputs→outcomes→impact)
- Ensure each element is distinct and correctly categorized
- Add narrative explanations of causal pathways
- Adjust outcome timeframes if needed (short/medium/long-term)
- Validate that all elements are measurable

---

### Budget Refinement

**Typical Feedback**:

- "Peer remuneration rate seems low"
- "Admin overhead percentage too high"
- "Missing justification for X cost"
- "Budget doesn't align with proposed activities"

**Refinement Approach**:

- Verify peer remuneration meets $300/session standard
- Adjust line items to align with program design activities
- Expand budget assumptions section with clearer justifications
- Recalculate totals and percentages
- Update sensitivity analysis if major changes

**Non-Negotiables** (preserve):

- Peer remuneration standard ($300/session minimum)
- Total budget amount (if already agreed with funder)
- Overhead rate (if locked by organizational policy)

---

### Evaluation Framework Refinement

**Typical Feedback**:

- "Too many indicators, needs prioritization"
- "Indicator X is not measurable"
- "Missing equity indicators"
- "Data collection methods unclear"

**Refinement Approach**:

- Consolidate or prioritize indicators (aim for 15-20 max)
- Rewrite vague indicators to be SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
- Add equity indicators with demographic disaggregation
- Clarify data collection methods, frequency, and responsibility
- Ensure every indicator maps to a logic model element

---

### Narrative Refinement

**Typical Feedback**:

- "Language too technical for community audience"
- "Missing NUAA's unique value proposition"
- "Need more evidence base for approach"
- "Tone doesn't reflect peer-led principles"

**Refinement Approach**:

- Adjust language for target audience (professional vs. plain language)
- Strengthen NUAA-specific framing (harm reduction, peer-led, cultural safety)
- Add citations to evidence base (research, similar programs)
- Ensure peer expertise is centered, not tokenized
- Check that tone is respectful, empowering, and non-stigmatizing

---

### Stakeholder Refinement

**Typical Feedback**:

- "Stakeholder journeys missing key touchpoints"
- "Peer workers should be co-designers, not just staff"
- "Community voice underrepresented in governance"
- "Partnership descriptions too vague"

**Refinement Approach**:

- Expand stakeholder journey maps with specific touchpoints
- Clarify roles and decision-making power for each stakeholder type
- Ensure peer workers have meaningful governance roles
- Strengthen partnership descriptions with MOUs, roles, contributions
- Validate stakeholder section with consumer advisory group

---

## Version History Documentation

### Changelog Format

Use this format in document front matter or a dedicated changelog section:

```yaml
---
version_history:
  - version: 1.0.0
    date: 2025-01-15
    author: "Program Team"
    changes: "Initial program design for Peer Naloxone Program"

  - version: 1.1.0
    date: 2025-02-20
    author: "Program Team + Advisory Group"
    changes: "Updated logic model based on advisory feedback; added stakeholder journey for Aboriginal participants; strengthened cultural safety protocol"
    rationale: "Consumer advisory identified gaps in Aboriginal engagement approach"

  - version: 1.2.0
    date: 2025-04-10
    author: "Program Team"
    changes: "Adjusted activity schedule from monthly to weekly based on pilot findings"
    rationale: "Mid-program evaluation showed scheduling conflicts reduced attendance"

  - version: 2.0.0
    date: 2025-07-01
    author: "Program Team"
    changes: "Major redesign expanding to regional areas; updated budget and logic model"
    rationale: "Secured additional funding for geographic expansion"
---
```

---

## Quality Checklist for Refinements

Before finalizing refinements, verify:

- [ ] Version number incremented appropriately (major.minor.patch)
- [ ] Changelog entry added with date, author, changes, rationale
- [ ] All feedback points addressed or rationale documented for non-addressed items
- [ ] Cross-references updated (e.g., "see Section 3" still valid)
- [ ] Budget calculations verified if budget refined
- [ ] Logic model alignment maintained if structure changed
- [ ] Indicator definitions still measurable if evaluation refined
- [ ] NUAA terminology and principles maintained
- [ ] Placeholder lint passed (no unresolved `[brackets]` if status=final)
- [ ] Peer review scheduled if major changes (consumer advisory, staff)
- [ ] Related documents updated if cross-artifact changes made
- [ ] Previous version archived if major revision (e.g., `program-design-v1.0.0.md`)

---

## Placeholder Lint Check

Before marking any document `status: final`, run the placeholder lint check to catch unresolved tokens:

### Bash

```bash
../scripts/bash/check-placeholders.sh nuaa-kit
```

### PowerShell

```pwsh
pwsh scripts/powershell/check-placeholders.ps1 -Path nuaa-kit
```

Both scripts exit non-zero if unresolved placeholders (e.g., `[Amount]`, `[Name]`, `[Date]`) are detected in files with `status: final` in front matter.

**Common Placeholders to Resolve**:

- `[Program Name]` → Actual program name
- `[Amount]` → Specific dollar figure
- `[Date]` → Actual date
- `[Number]` → Specific quantity
- `[Name]` → Actual person/organization name
- `[X]`, `[Y]`, `[N]` → Replace with real values

---

## Integration with Other NUAA-Kit Artifacts

- **program-design.md**: Source document for most refinements; changes here may cascade
- **logic-model.md**: Refinements must maintain causal logic (inputs→impact)
- **impact-framework.md**: Indicator changes require logic model validation
- **proposal.md**: Refinements to design/budget must be reflected in proposal
- **budget-calculator.md**: Budget refinements must recalculate totals
- **evaluation-report-\*.md**: May inform refinements for future iterations

---

## Feedback Integration Best Practices

1. **Capture Feedback Systematically**: Use structured feedback forms or meeting notes templates
2. **Prioritize Feedback**: Not all feedback is equally important; focus on high-impact changes
3. **Validate with Source**: If feedback from advisory group, confirm interpretation before implementing
4. **Document Rationale**: Future team members need to understand why changes were made
5. **Respect Lived Experience**: Feedback from peers and participants takes precedence over staff/funder preferences when there's tension
6. **Test Assumptions**: If feedback contradicts evidence, investigate further before changing
7. **Iterate in Small Batches**: Multiple small refinements better than one massive overhaul
8. **Communicate Changes**: Let stakeholders know their feedback was incorporated (closes the loop)

---

## Advanced Refinement Scenarios

### Scenario A: Conflicting Feedback from Multiple Sources

**Challenge**: Funder wants more quantitative metrics; consumer advisory wants less surveillance-like data collection.

**Approach**:

1. Map which indicators are funder-required vs. optional
2. Prioritize participant safety and consent
3. Explore middle-ground indicators (e.g., aggregated data, opt-in surveys)
4. Be transparent with funder about community priorities
5. Document tension and resolution in change rationale

---

### Scenario B: Mid-Program Pivot Required

**Challenge**: Program implementation reveals design assumptions were wrong; major changes needed.

**Approach**:

1. Document what's not working and why (evaluation data)
2. Consult consumer advisory on proposed changes
3. Update program-design.md with new approach (major version bump)
4. Revise logic model to reflect new theory of change
5. Communicate with funder (if contractual obligations affected)
6. Preserve original design as archived version for learning

---

### Scenario C: Scalability Planning

**Challenge**: Pilot program succeeded; refining for broader rollout.

**Approach**:

1. Identify which elements scaled linearly vs. needed redesign
2. Update participant targets, geography, timeline
3. Adjust budget for economies/diseconomies of scale
4. Add new logic model elements for scale-specific challenges (e.g., quality assurance across sites)
5. Update evaluation framework with scalability indicators

---

## Tips for Effective Refinement

1. **Small Changes Often**: Better than large, infrequent overhauls
2. **Always Version Control**: Never lose sight of what changed and why
3. **Validate Changes**: Especially with the people most affected (participants, peer workers)
4. **Cross-Check Artifacts**: Changes ripple across documents; maintain consistency
5. **Document Intent**: Future readers need to understand your reasoning
6. **Preserve Excellence**: Don't weaken strong sections to address weak ones
7. **Learn from Refinement Patterns**: If you're always refining the same section, it may need fundamental redesign

---

**NUAA Principle Reminder**: Refinement is not about perfection. It's about responsiveness to community needs, continuous learning, and honoring lived experience. Documents should evolve as programs and contexts change.
