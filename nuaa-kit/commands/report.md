---
description: Generate program progress reports and outcome documentation
scripts:
  sh: bash .nuaa/scripts/bash/create-new-feature.sh report {ARGS}
  ps: powershell .nuaa/scripts/powershell/create-new-feature.ps1 report {ARGS}
status: implemented
version: 1.0.0
mode: active
created: 2025-11-10
---

# /nuaa.report - Generate Evaluation Reports

## Purpose

Generate comprehensive evaluation reports that synthesize data from your impact framework, present findings in audience-appropriate formats, and support evidence-based program refinement and advocacy.

**Key Capabilities**:

- Multi-audience report formats (funder, community, internal)
- Data-driven insights from impact framework indicators
- Visual presentations of outcomes and impact
- Plain-language summaries for accessibility
- Integration with program design and logic model

## When to Use

- **Mid-program reviews**: Progress reporting, course correction
- **Final evaluation**: Comprehensive outcome and impact assessment
- **Funder reporting**: Acquittal and accountability documents
- **Community sharing**: Accessible summaries for participants and stakeholders
- **Internal learning**: Team reflection and program refinement

## Usage

### Basic Usage

```bash
/nuaa.report Generate a final evaluation report for the Peer Naloxone Distribution Program, \
  covering January to December 2025, for a funder audience.
```

### With Specific Options

```bash
/nuaa.report Create a mid-program progress report for the Stigma Reduction Workshops, \
  reporting period Q1-Q2 2025, --format=internal --focus=outcomes
```

### Multiple Audience Formats

```bash
/nuaa.report Generate both a funder report and a community-friendly summary for the \
  Peer Support Network program, final evaluation, 12-month period.
```

## Parameters

| Parameter        | Description                             | Example Values                                               |
| ---------------- | --------------------------------------- | ------------------------------------------------------------ |
| Program name     | Name of the program being evaluated     | "Peer NSP Program", "Hepatitis C Testing Initiative"         |
| Reporting period | Timeframe covered by the report         | "Q1 2025", "January-June 2025", "12-month final evaluation"  |
| Report type      | Stage of evaluation                     | "progress", "mid-program", "final", "quarterly"              |
| --format         | Target audience format                  | `funder`, `community`, `internal`, `all`                     |
| --focus          | Emphasize specific logic model elements | `outcomes`, `impact`, `process`, `equity`                    |
| --data-source    | Path to data files (optional)           | `data/survey-results.csv`, `sharepoint/evaluation-data.xlsx` |

## System Prompt for AI Agent

When this command is invoked, you are acting as an **evaluation synthesis expert** with deep knowledge of NUAA's harm reduction principles, peer-led program evaluation, and community-engaged reporting.

### Your Task

1. **Locate Core Documents**:

   - Find the program's `program-design.md`, `logic-model.md`, and `impact-framework.md`
   - Identify all indicators defined in the impact framework
   - Review the original program goals and intended outcomes

2. **Structure the Report**:

   - Use the template below as a starting point
   - Adapt sections based on report type (progress vs. final) and audience
   - Ensure alignment between reported findings and original logic model

3. **Synthesize Data**:

   - If data files are provided (CSV, Excel), analyze quantitative findings
   - Integrate qualitative data (quotes, stories, themes) where available
   - Calculate indicator achievement rates against targets
   - Identify equity patterns across demographic groups

4. **Format for Audience**:

   - **Funder**: Formal language, accountability focus, detailed methodology, budget alignment
   - **Community**: Plain language, visual emphasis, participant voices, accessibility (WCAG 2.1)
   - **Internal**: Candid assessment, lessons learned, recommendations for refinement

5. **Quality Checks**:

   - Every finding must link back to a specific indicator in the impact framework
   - Use NUAA terminology (see `glossary.md`)
   - Maintain cultural safety and ethical representation of participant data
   - Include both successes and challenges (honest, non-defensive)
   - Recommendations must be specific and actionable

6. **Output**:
   - Create a new file: `[program-folder]/evaluation-report-[period]-[audience].md`
   - Include front matter with metadata
   - If `--format=all`, generate separate files for each audience
   - Optionally create a Word export version (M365 integration)

---

## Report Template Structure

### Front Matter

```yaml
---
status: final
version: 1.0.0
program: [Program Name]
reporting_period: [Start Date] to [End Date]
report_type: [progress|mid-program|final]
audience: [funder|community|internal]
prepared_by: [Name/Organization]
date: [Report Date]
---
```

### Section 1: Executive Summary (All Audiences)

**Purpose**: 1-page high-level overview
**Length**: 300-500 words
**Key Elements**:

- Program overview (what, who, when, where)
- Key achievements (quantitative highlights)
- Main outcomes observed
- Impact snapshot (if final report)
- Top 3 recommendations (if internal/funder)

**Example**:

> The Peer Naloxone Distribution Program engaged 127 people who use drugs across Western Sydney over 12 months (January-December 2025), distributing 1,450 naloxone kits through peer-led outreach. Program participants reported 89 overdose reversals using distributed naloxone, with 100% of respondents indicating increased confidence in overdose response. The program exceeded its target of reaching 100 participants and achieved strong equity outcomes, with 45% of participants identifying as Aboriginal or Torres Strait Islander...

---

### Section 2: Program Overview & Context

**For All Audiences**:

- Brief program description
- Target population and setting
- Timeline and key milestones
- Alignment with NUAA strategic goals and harm reduction principles

**Funder-specific additions**:

- Grant reference number and funding amount
- Deliverables checklist (contracted vs. actual)
- Budget variance summary (refer to detailed budget section)

**Community-specific framing**:

- Why this program mattered (plain language problem statement)
- Who was involved (peer workers, participants, partners)
- Visual timeline or infographic of program phases

---

### Section 3: Evaluation Approach

**Purpose**: Describe methodology and data sources

**For Funder/Internal**:

- Evaluation framework (participatory evaluation, peer-led data collection)
- Data collection methods (surveys, interviews, administrative data)
- Sample sizes and response rates
- Limitations and constraints (honest assessment)
- Ethical considerations (consent, privacy, cultural safety)

**For Community**:

- How we listened to participants
- Different ways people shared their experiences
- Keeping information safe and private

---

### Section 4: Findings by Logic Model Element

#### 4a. Process Indicators (Activities Implemented)

**Structure**:

| Indicator | Target | Actual | Achievement Rate | Notes |
|-----------|--------|--------|------------------|-------|
| Number of sessions delivered | [target] | [actual] | [%] | [context] |
| Peer workers trained | [target] | [actual] | [%] | [context] |
| Partnerships established | [target] | [actual] | [%] | [context] |

**Narrative**:

- What activities were delivered as planned?
- What adaptations were made and why?
- Fidelity assessment: How closely did implementation match design?

#### 4b. Output Indicators (Direct Results)

| Indicator                  | Target   | Actual   | Achievement Rate | Notes     |
| -------------------------- | -------- | -------- | ---------------- | --------- |
| Participants engaged       | [target] | [actual] | [%]              | [context] |
| Kits/materials distributed | [target] | [actual] | [%]              | [context] |
| Touchpoints/contacts made  | [target] | [actual] | [%]              | [context] |

**Narrative**:

- Reach and engagement summary
- Demographic breakdown (equity lens)
- Patterns over time (e.g., monthly trends)

#### 4c. Outcome Indicators (Changes Observed)

| Indicator            | Baseline | Endline | Change | Significance | Notes     |
| -------------------- | -------- | ------- | ------ | ------------ | --------- |
| Knowledge/awareness  | [%]      | [%]     | [Δ%]   | [direction]  | [context] |
| Skills/self-efficacy | [score]  | [score] | [Δ]    | [direction]  | [context] |
| Behavior change      | [%]      | [%]     | [Δ%]   | [direction]  | [context] |
| Service access       | [%]      | [%]     | [Δ%]   | [direction]  | [context] |

**Narrative**:

- Short-term and medium-term outcomes achieved
- Participant voices (quotes, stories - with consent)
- Unexpected outcomes (positive and negative)
- Outcome sustainability (if longitudinal data available)

#### 4d. Impact Indicators (Long-Term Change)

**Note**: Impact often requires longer timeframes than single program cycles. Report observed trends and contribution (not attribution).

| Indicator               | Observed Trend | Program Contribution      | Notes     |
| ----------------------- | -------------- | ------------------------- | --------- |
| Population-level health | [description]  | [how program contributed] | [context] |
| System/policy change    | [description]  | [how program contributed] | [context] |
| Sector capacity         | [description]  | [how program contributed] | [context] |

**Narrative**:

- Broader changes observed during program period
- How this program contributed (among multiple factors)
- Evidence of sustained change or ripple effects

---

### Section 5: Equity Analysis

**Purpose**: Assess whether program access, experience, and outcomes were equitable across demographic and priority groups.

**Disaggregated Data Tables**:

| Demographic Group | % of Total Participants | Outcome Indicator 1 | Outcome Indicator 2 |
|-------------------|-------------------------|---------------------|---------------------|
| Aboriginal/TSI | [%] | [score/rate] | [score/rate] |
| Non-Indigenous | [%] | [score/rate] | [score/rate] |
| Gender diverse | [%] | [score/rate] | [score/rate] |
| CALD | [%] | [score/rate] | [score/rate] |

**Narrative**:

- Which groups were most/least represented?
- Were outcomes equitable across groups?
- Barriers to access identified
- Adaptations made to improve equity
- Recommendations for future equity improvements

---

### Section 6: Budget vs. Actual (Funder Reports)

| Category            | Budgeted     | Actual       | Variance | % Variance | Explanation           |
| ------------------- | ------------ | ------------ | -------- | ---------- | --------------------- |
| Personnel           | $[amount]    | $[amount]    | $[Δ]     | [%]        | [reason for variance] |
| Peer Remuneration   | $[amount]    | $[amount]    | $[Δ]     | [%]        | [reason]              |
| Operations          | $[amount]    | $[amount]    | $[Δ]     | [%]        | [reason]              |
| Participant Support | $[amount]    | $[amount]    | $[Δ]     | [%]        | [reason]              |
| Evaluation          | $[amount]    | $[amount]    | $[Δ]     | [%]        | [reason]              |
| Administration      | $[amount]    | $[amount]    | $[Δ]     | [%]        | [reason]              |
| **TOTAL**           | **$[total]** | **$[total]** | **$[Δ]** | **[%]**    |                       |

**Narrative**:

- Overall budget management assessment
- Explanation of significant variances (>10%)
- Cost-effectiveness observations
- Financial sustainability considerations

---

### Section 7: Lessons Learned & Recommendations

**For Internal/Funder Audiences**:

#### What Worked Well

- [Strength 1 with specific example]
- [Strength 2 with specific example]
- [Strength 3 with specific example]

#### Challenges Encountered

- [Challenge 1 and how it was addressed]
- [Challenge 2 and how it was addressed]
- [Challenge 3 and remaining concerns]

#### Recommendations

**Immediate (Next 3 months)**:

1. [Specific, actionable recommendation]
2. [Specific, actionable recommendation]

**Short-term (Next 6-12 months)**:

1. [Recommendation]
2. [Recommendation]

**Long-term (Beyond 12 months)**:

1. [Recommendation]
2. [Recommendation]

---

### Section 8: Participant Voices (All Audiences)

**Purpose**: Center lived experience and humanize data

**Community Format**:

- Photo stories (with consent, de-identified)
- Direct quotes highlighting impact
- "Before and after" narratives

**Funder Format**:

- Selected testimonials with brief context
- Thematic summary of qualitative feedback

**Ethical Considerations**:

- All quotes anonymized unless explicit consent for attribution
- Avoid voyeuristic or stigmatizing portrayals
- Balance vulnerability with dignity and agency
- Community members review before publication (if feasible)

**Examples**:

> "Before this program, I didn't know how to use naloxone. Now I carry it everywhere and I've already saved two people's lives." – Program participant

> "The peer workers got it. They didn't judge, they just showed me what to do. That made all the difference." – Participant, age 34

---

### Section 9: Next Steps & Sustainability (Final Reports)

**For Funder Reports**:

- Program continuation plans (secured/sought funding)
- Transition or exit strategy if program is concluding
- Knowledge transfer (what was learned that others can use)
- Advocacy asks (policy/system changes recommended)

**For Internal Reports**:

- Immediate action items for program refinement
- Staff development needs identified
- Partnership cultivation priorities
- Resource requirements for next phase

---

### Appendices

**Appendix A**: Full data tables (detailed disaggregation)
**Appendix B**: Survey instruments used
**Appendix C**: Interview protocols
**Appendix D**: Logic model (reference)
**Appendix E**: Indicator definitions (from impact framework)
**Appendix F**: Consent forms and ethical approvals
**Appendix G**: References and evidence base

---

## Quality Checklist

Before finalizing your evaluation report, verify:

- [ ] All indicators from impact framework are addressed
- [ ] Data sources are clearly documented
- [ ] Findings link back to program logic model
- [ ] Equity analysis included and disaggregated
- [ ] Participant voices are present and ethically represented
- [ ] Language is appropriate for target audience
- [ ] Honest assessment of both successes and challenges
- [ ] Recommendations are specific, actionable, and resourced
- [ ] Budget accountability (for funder reports)
- [ ] No unresolved placeholders (e.g., [Amount], [Name])
- [ ] Accessibility standards met (if community format)
- [ ] Peer review by program staff or advisory group
- [ ] Version number and metadata updated

---

## Export Guidance

### For Word (Funder/Community Formats)

1. Copy Markdown report to Word
2. Apply NUAA branding/logo (if available)
3. Format tables consistently
4. Insert charts/graphs if data supports visualization
5. Add page numbers, header/footer with program name
6. Convert to PDF for final distribution

### For SharePoint (Internal Sharing)

1. Save report as `[program-name]-evaluation-report-[period]-[audience].md`
2. Upload to program folder
3. Link from main program-design.md
4. Update program STATUS with report completion date

### For Community Dissemination

1. Create accessible formats (large print, audio summary, Easy Read)
2. Consider infographic summary (one-page visual)
3. Share via appropriate channels (email, social media, newsletter)
4. Host community debrief session to discuss findings

---

## Integration with Other NUAA-Kit Artifacts

- **program-design.md**: Report evaluates whether program was delivered as designed
- **logic-model.md**: Report structure follows logic model elements
- **impact-framework.md**: Report addresses every indicator defined
- **proposal.md**: Final report fulfills evaluation commitments made in proposal

---

## Tips for Effective Reporting

1. **Tell the Story**: Data is important, but narrative brings it to life
2. **Be Honest**: Acknowledge challenges; funders and communities appreciate transparency
3. **Center Participants**: Lived experience voices must be prominent and respectful
4. **Show Impact**: Move beyond outputs (what you did) to outcomes (what changed)
5. **Visualize**: Charts, infographics, photos (with consent) increase engagement
6. **Be Actionable**: Don't just report findings—recommend what to do with them
7. **Compare to Plan**: Show accountability by referencing original program design
8. **Celebrate Success**: Harm reduction work is hard; recognize achievements

---

**NUAA Principle Reminder**: Evaluation is not surveillance. It's a tool for learning, improvement, advocacy, and accountability to participants and communities. Reports should empower, not stigmatize.
