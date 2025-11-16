---
status: implemented
version: 1.0.0
mode: active
created: 2025-11-10
---

# /nuaa.document - Document Existing Programs (Brownfield)

## Purpose

Reverse-engineer comprehensive documentation for existing NUAA programs that are already running but lack formal program designs, logic models, or impact frameworks. This "brownfield" documentation process captures institutional knowledge, supports quality improvement, and enables evidence-based refinement.

**Key Capabilities**:

- Systematic documentation of existing programs
- Interview protocols for staff and participants
- Gap analysis (current state vs. best practice)
- Logic model reconstruction from existing activities
- Retrospective impact framework development
- Integration with ongoing NUAA-Kit workflows

## When to Use

- **Undocumented programs**: Programs running for years without formal documentation
- **Transition planning**: New staff taking over existing programs
- **Quality improvement**: Establishing baseline for systematic enhancement
- **Funding applications**: Need documentation to apply for continued/expanded funding
- **Evaluation setup**: Implementing evaluation for the first time
- **Compliance**: Funders or accreditors require formal program documentation

## Usage

### Basic Usage

```bash
/nuaa.document Peer Needle and Syringe Program running since 2020, \
  serving approximately 150 people who use drugs in Western Sydney.
```

### With Historical Data

```bash
/nuaa.document Stigma Reduction Workshops --running-since=2018-06 \
  --current-participants=80 --budget-amount=45000 --staff-count=3
```

### Comprehensive Documentation

```bash
/nuaa.document Existing Hepatitis C Testing & Treatment Support Program, \
  operating since 2019, currently serving 200 participants annually, \
  annual budget $75,000, 2 FTE staff + 4 peer workers, \
  --focus=evaluation --participatory=high
```

## Parameters

| Parameter              | Description                             | Example Values                                                            |
| ---------------------- | --------------------------------------- | ------------------------------------------------------------------------- |
| Program name           | Name of the existing program            | "Peer NSP Program", "Stigma Workshops"                                    |
| Running since          | Approximate start date                  | "2020", "2018-06", "5 years ago"                                          |
| --running-since        | Formal start date parameter             | "2020-01", "2018-06-15"                                                   |
| --current-participants | Number of active participants           | 150, 200, "50-100"                                                        |
| --budget-amount        | Current annual budget                   | 50000, 75000                                                              |
| --staff-count          | Number of staff (FTE or headcount)      | "2 FTE", "3 staff + 4 peers"                                              |
| --focus                | Prioritize specific documentation area  | `evaluation`, `logic-model`, `impact`, `all`                              |
| --participatory        | Degree of staff/participant involvement | `light`, `standard`, `high`                                               |
| --urgency              | Timeline for documentation              | `quick` (1-2 weeks), `standard` (4-6 weeks), `comprehensive` (8-12 weeks) |

## System Prompt for AI Agent

When this command is invoked, you are acting as a **program archaeology and knowledge capture specialist** with expertise in NUAA's harm reduction programs, participatory documentation methods, and organizational learning.

### Your Task

1. **Gather Existing Information**:

   - Review any available materials (reports, meeting notes, emails, budgets)
   - Identify key stakeholders (staff, peer workers, participants, partners)
   - Map program history and major milestones
   - Document current operations and activities

2. **Conduct Structured Interviews**:

   - Use interview protocols (see below) with staff, peer workers, participants
   - Capture implicit knowledge and "tribal wisdom"
   - Document decision rationale and historical context
   - Record challenges, adaptations, and learnings

3. **Reconstruct Program Logic**:

   - Identify actual inputs (resources, people, partnerships)
   - Map current activities (what's actually happening)
   - Document outputs (immediate results, numbers served)
   - Infer outcomes (changes observed in participants/community)
   - Hypothesize impact (broader systemic changes)
   - Create logic model from reconstructed elements

4. **Develop Impact Framework**:

   - Identify indicators already being tracked (formal or informal)
   - Add missing indicators for comprehensive evaluation
   - Define data collection methods going forward
   - Establish baseline measures where possible

5. **Gap Analysis**:

   - Compare current documentation to NUAA-Kit best practices
   - Identify what's working well (preserve and formalize)
   - Flag areas needing improvement
   - Prioritize gaps by importance and feasibility

6. **Generate Documentation**:

   - Create `existing-program-analysis.md` (diagnostic summary)
   - Generate `program-design.md` reflecting actual current state
   - Build `logic-model.md` based on observed operations
   - Develop `impact-framework.md` for ongoing evaluation
   - Produce recommendations for refinement

7. **Quality Validation**:
   - Review draft documentation with program staff
   - Validate with peer workers and participants (if high participatory)
   - Iterate based on feedback
   - Finalize with version history noting "Baseline documentation"

---

## Documentation Workflow

### Phase 1: Discovery (Week 1-2)

**Activities**:

1. Collect all available program materials
2. Interview program coordinator/manager (2-3 hours)
3. Interview peer workers (1-2 hours each)
4. Observe program activities if feasible (1-2 sessions)
5. Review financial records and participant data

**Outputs**:

- Discovery notes document
- Stakeholder list
- Timeline of program history
- Inventory of existing documentation

---

### Phase 2: Knowledge Capture (Week 2-4)

**Activities**:

1. Conduct staff interviews using structured protocol
2. Facilitate peer worker focus group (if participatory=standard/high)
3. Conduct participant interviews or surveys (if participatory=high)
4. Review partnership agreements and MOUs
5. Analyze historical data (attendance, outcomes, incidents)

**Outputs**:

- Interview transcripts/summaries
- Program activity inventory
- Resource mapping
- Outcomes stories and evidence

---

### Phase 3: Documentation (Week 4-6)

**Activities**:

1. Draft `existing-program-analysis.md` (gap analysis)
2. Create `program-design.md` (current state)
3. Build `logic-model.md` (reconstructed theory of change)
4. Develop `impact-framework.md` (evaluation going forward)
5. Generate recommendations for improvement

**Outputs**:

- Complete documentation suite
- Gap analysis report
- Recommendations document

---

### Phase 4: Validation & Refinement (Week 6-8)

**Activities**:

1. Review draft documentation with program staff
2. Validate with consumer advisory group (if available)
3. Incorporate feedback and refine
4. Finalize documentation with version 1.0.0
5. Plan next steps (immediate improvements, evaluation implementation)

**Outputs**:

- Validated documentation (v1.0.0)
- Action plan for addressing gaps
- Evaluation implementation timeline

---

## Interview Protocols

### Staff Interview Protocol (Program Coordinator/Manager)

**Duration**: 2-3 hours
**Format**: Semi-structured interview, can be split into 2 sessions

#### Section 1: Program History & Context (30 min)

1. When and why was this program started?
2. What problem or need was it designed to address?
3. How has the program evolved since it began?
4. What were the major milestones or turning points?
5. What funding sources have supported the program over time?

#### Section 2: Current Operations (45 min)

6. Describe a typical program cycle (weekly, monthly, annually).
7. What activities do you currently deliver? (List all)
8. Who are your current participants? (Demographics, numbers, catchment area)
9. How do participants find out about and access the program?
10. Who delivers the program? (Staff, peer workers, volunteers, partners)
11. What resources are required? (Budget, materials, space, equipment)
12. What partnerships are essential to operations?

#### Section 3: Outcomes & Impact (30 min)

13. What changes have you observed in participants?
14. What data do you collect about program activities and outcomes?
15. What success stories or examples stand out?
16. Have there been any unintended positive or negative consequences?
17. What feedback have you received from participants, funders, partners?

#### Section 4: Challenges & Adaptations (30 min)

18. What challenges or barriers has the program faced?
19. How have you adapted in response to challenges?
20. What aspects of the program work really well?
21. What aspects need improvement?
22. If you could redesign from scratch, what would you change?

#### Section 5: Future Directions (15 min)

23. Where should this program go in the next 1-3 years?
24. What resources or support are needed for improvement?
25. What documentation would be most useful for managing/improving the program?

---

### Peer Worker Interview Protocol

**Duration**: 1-2 hours
**Format**: Individual or small group (2-3 peer workers)

#### Section 1: Your Role (15 min)

1. How long have you been involved with this program?
2. What do you do as a peer worker in this program?
3. What training or support have you received?
4. How are you remunerated? (Rate, frequency, consistency)

#### Section 2: Program Activities (30 min)

5. Walk me through what happens in a typical session or outreach activity.
6. What do participants value most about the program?
7. What makes this program different from other services?
8. How do you know when the program is working well?

#### Section 3: Participant Perspectives (20 min)

9. Who are the participants? (Your perspective)
10. What challenges do participants face in accessing or engaging with the program?
11. What outcomes or changes do you see in participants?
12. Are there participants or communities we're not reaching? Why?

#### Section 4: Improvements & Recommendations (20 min)

13. What's working really well that we should keep?
14. What could be improved?
15. What would make your role as a peer worker easier or more effective?
16. What would make the program more effective for participants?

#### Section 5: Peer Expertise (10 min)

17. How does your lived experience inform the program design and delivery?
18. Do you feel your expertise is valued and integrated? (Honest feedback)
19. What advice would you give to someone documenting this program?

---

### Participant Interview/Survey Protocol (Optional - High Participatory)

**Duration**: 30-45 minutes
**Format**: Individual interview or anonymous survey
**Ethics**: Informed consent, confidentiality, remuneration ($50-$100 suggested)

#### Section 1: Engagement (10 min)

1. How did you first hear about this program?
2. How long have you been participating?
3. How often do you engage with the program?
4. What made you decide to participate?

#### Section 2: Experience (15 min)

5. What activities or services do you access through the program?
6. What do you value most about the program?
7. What aspects work well for you?
8. What aspects could be improved?
9. Have you faced any barriers to accessing or participating?

#### Section 3: Outcomes (15 min)

10. What, if anything, has changed for you since participating? (Knowledge, skills, confidence, health, connections, etc.)
11. Can you share a specific example of how the program has helped you?
12. Has the program influenced your access to other services or supports?
13. Would you recommend this program to others? Why or why not?

#### Section 4: Future Directions (5 min)

14. What would make the program even better?
15. Is there anything else you think we should know about the program?

---

## Existing Program Analysis Template

This template is generated by the AI agent after discovery and knowledge capture phases.

### Front Matter

```yaml
---
status: final
version: 1.0.0
program: [Program Name]
analysis_date: [Date]
running_since: [Start Date]
current_participants: [Number]
annual_budget: [Amount]
analyst: [Name/Role]
methodology: [Interviews, document review, observation]
---
```

### Section 1: Executive Summary

**Purpose**: 1-page overview of findings

- Program overview (what, who, when, where, why)
- Current operational status (active, thriving, struggling)
- Key strengths to preserve
- Critical gaps to address
- Top 3 recommendations

---

### Section 2: Program Background

#### Historical Context

- When and why program was established
- Original goals and design (if known)
- Major milestones and turning points
- Funding history
- Leadership transitions

#### Current Context

- Organizational placement (within NUAA or partner)
- Relationship to NUAA strategic priorities
- Regulatory/compliance environment
- Community need and demand

---

### Section 3: Current State Documentation

#### Inputs (Resources)

| Type         | Description     | Quantity/Amount    |
| ------------ | --------------- | ------------------ |
| Funding      | [Sources]       | $[Amount/year]     |
| Staff        | [Roles]         | [FTE]              |
| Peer Workers | [Roles]         | [Number/hours]     |
| Facilities   | [Description]   | [Details]          |
| Materials    | [Types]         | [Inventory/budget] |
| Partnerships | [Organizations] | [Contribution]     |

#### Activities (What We Do)

| Activity     | Frequency        | Duration   | Participants | Peer-Led? |
| ------------ | ---------------- | ---------- | ------------ | --------- |
| [Activity 1] | [Weekly/monthly] | [Hours]    | [Number]     | [Yes/No]  |
| [Activity 2] | [Frequency]      | [Duration] | [Number]     | [Yes/No]  |

**Narrative**: Describe typical program cycle and delivery model.

#### Outputs (Immediate Results)

| Output                | Target (if known) | Actual | Measurement Method |
| --------------------- | ----------------- | ------ | ------------------ |
| Sessions delivered    | [N]               | [N]    | Attendance records |
| Participants engaged  | [N]               | [N]    | Intake forms       |
| Materials distributed | [N]               | [N]    | Inventory logs     |

#### Outcomes (Changes Observed)

| Outcome                      | Evidence      | Source                             |
| ---------------------------- | ------------- | ---------------------------------- |
| [Knowledge/awareness change] | [Description] | [Staff observations, testimonials] |
| [Skill/behavior change]      | [Description] | [Pre/post surveys, stories]        |
| [Access to services]         | [Description] | [Referral data, interviews]        |
| [Community connection]       | [Description] | [Feedback, observations]           |

**Note**: Outcomes are often informally observed rather than systematically measured in undocumented programs.

#### Impact (Long-term/Systemic Change)

| Impact Indicator    | Observed Trend | Program Contribution |
| ------------------- | -------------- | -------------------- |
| [Population health] | [If known]     | [Likely/possible]    |
| [System change]     | [If known]     | [Likely/possible]    |
| [Stigma reduction]  | [If known]     | [Likely/possible]    |

**Note**: Impact attribution difficult without longitudinal data; document anecdotal evidence and hypotheses.

---

### Section 4: Reconstructed Logic Model

**Inputs** → **Activities** → **Outputs** → **Outcomes (Short/Medium/Long)** → **Impact**

[Insert Mermaid diagram or table representation]

**Causal Assumptions**:

- _If_ we provide [inputs] and deliver [activities]...
- _Then_ we expect [outputs]...
- _Leading to_ [short-term outcomes] within 3-6 months...
- _Which contribute to_ [medium-term outcomes] within 6-12 months...
- _And ultimately_ [long-term outcomes] within 1-3 years...
- _Contributing to_ [broader impact] at population/system level.

**Validation Status**:

- ⚠️ Logic model reconstructed from current practice; not validated against original design intent (no original documentation available)
- ✅ Validated with program staff and peer workers [Date]

---

### Section 5: Gap Analysis

#### Documentation Gaps

| Artifact               | Current Status                           | Gap Severity | Priority |
| ---------------------- | ---------------------------------------- | ------------ | -------- |
| Program Design         | Missing                                  | High         | 1        |
| Logic Model            | Missing                                  | High         | 1        |
| Impact Framework       | Missing                                  | High         | 1        |
| Budget Documentation   | Partial (line items exist, no narrative) | Medium       | 2        |
| Partnership Agreements | Informal only                            | Medium       | 3        |
| Evaluation Plan        | None                                     | High         | 1        |

#### Operational Gaps

| Area                | Gap Description                               | Impact                                      | Recommendation                   |
| ------------------- | --------------------------------------------- | ------------------------------------------- | -------------------------------- |
| Evaluation          | No systematic data collection                 | Can't demonstrate outcomes to funders       | Implement basic impact framework |
| Remuneration        | Peer payment inconsistent ($200-$350/session) | Equity concerns, peer dissatisfaction       | Standardize at $300/session      |
| Cultural Safety     | No formal protocol                            | Risk of harm, reduced Aboriginal engagement | Develop cultural safety protocol |
| Participant Journey | No formal intake/exit                         | Lost follow-up data, reduced retention      | Implement journey mapping        |

#### Alignment Gaps (NUAA Principles)

| Principle         | Current Alignment                            | Gap                                            | Recommendation                       |
| ----------------- | -------------------------------------------- | ---------------------------------------------- | ------------------------------------ |
| Peer-led          | Moderate (peer delivery, staff-led design)   | Peers not involved in program design decisions | Establish peer advisory group        |
| Harm Reduction    | Strong (non-judgmental, pragmatic)           | None                                           | Maintain current approach            |
| Cultural Safety   | Weak (generic approach)                      | Insufficient Aboriginal/LGBTIQ+ responsiveness | Strengthen cultural protocols        |
| Transparency      | Weak (informal processes)                    | Decision-making not documented                 | Document decision rationale          |
| Fair Remuneration | Moderate (payments made, inconsistent rates) | Rate variation and payment delays              | Standardize and systematize payments |

---

### Section 6: Strengths to Preserve

#### What's Working Well

1. **[Strength 1]**: [Evidence/example]
2. **[Strength 2]**: [Evidence/example]
3. **[Strength 3]**: [Evidence/example]

#### Critical Success Factors

- [Factor 1]: Do not change this element; it's core to program success
- [Factor 2]: Protect this in any refinement
- [Factor 3]: Replicate this in similar programs

#### Institutional Knowledge

- [Key insight or practice known by staff but not documented]
- [Adaptation or workaround that resolved a recurring challenge]
- [Community relationship or trust built over time]

---

### Section 7: Recommendations

#### Immediate (Next 1-3 months)

1. **[Recommendation 1]**: [Specific action, rationale, resource needs]
2. **[Recommendation 2]**: [Action, rationale, resources]
3. **[Recommendation 3]**: [Action, rationale, resources]

#### Short-term (3-6 months)

1. **[Recommendation]**: [Description]
2. **[Recommendation]**: [Description]

#### Medium-term (6-12 months)

1. **[Recommendation]**: [Description]
2. **[Recommendation]**: [Description]

#### Long-term (12+ months)

1. **[Recommendation]**: [Description]

---

### Section 8: Implementation Roadmap

| Phase                 | Timeframe | Actions                                                | Owner  | Status      |
| --------------------- | --------- | ------------------------------------------------------ | ------ | ----------- |
| Documentation         | [Dates]   | Finalize program design, logic model, impact framework | [Name] | In Progress |
| Evaluation Setup      | [Dates]   | Implement basic data collection, train staff           | [Name] | Not Started |
| Refinement            | [Dates]   | Address priority gaps, strengthen cultural safety      | [Name] | Not Started |
| Expansion (if funded) | [Dates]   | Scale to [new area/population]                         | [Name] | Planned     |

---

### Section 9: Data Collection Going Forward

**Starting from [Date]**, implement these data collection practices:

| Indicator           | Data Source | Frequency        | Responsible | Storage  |
| ------------------- | ----------- | ---------------- | ----------- | -------- |
| [Process indicator] | [Method]    | [Weekly/monthly] | [Role]      | [System] |
| [Output indicator]  | [Method]    | [Frequency]      | [Role]      | [System] |
| [Outcome indicator] | [Method]    | [Frequency]      | [Role]      | [System] |

**Baseline Measures**: Establish baseline for key indicators now (even if retrospective data unavailable) to enable future evaluation.

---

### Appendices

**Appendix A**: Interview summaries (anonymized)
**Appendix B**: Document inventory
**Appendix C**: Historical timeline
**Appendix D**: Stakeholder map
**Appendix E**: Financial summary (if available)
**Appendix F**: Participant testimonials (with consent)

---

## Quality Checklist

Before finalizing brownfield documentation, verify:

- [ ] All available program materials reviewed
- [ ] Key stakeholders interviewed (staff, peer workers, participants if high participatory)
- [ ] Reconstructed logic model reflects actual operations (not idealized)
- [ ] Gap analysis honest and specific (not generic or judgmental)
- [ ] Strengths explicitly documented (not just deficit focus)
- [ ] Recommendations are specific, prioritized, and resourced
- [ ] NUAA principles used as evaluation criteria
- [ ] Documentation validated with program staff
- [ ] Peer worker review completed (if standard/high participatory)
- [ ] Baseline measures identified for future evaluation
- [ ] Implementation roadmap has assigned owners and dates
- [ ] Version history notes "Baseline documentation from brownfield analysis"

---

## Integration with NUAA-Kit Workflows

### After Brownfield Documentation

1. **Use `/nuaa.refine`** to improve documented program based on gap analysis
2. **Use `/nuaa.measure`** to expand impact framework with additional indicators
3. **Use `/nuaa.report`** to create evaluation reports using new data collection
4. **Use `/nuaa.propose`** to apply for expanded/continued funding with solid documentation

### Ongoing Maintenance

- Quarterly: Review program-design.md for accuracy, update as program evolves
- Annually: Conduct mini-gap analysis, update recommendations
- After major changes: Use `/nuaa.refine` with change documentation

---

## Tips for Effective Brownfield Documentation

1. **Avoid Judgment**: This is archaeology, not audit. Focus on understanding, not blame.
2. **Honor Institutional Knowledge**: Staff and peer workers hold critical insights not in any document.
3. **Expect Messy Reality**: Programs evolve organically; reconstructed logic may not be perfectly linear.
4. **Preserve What Works**: Document strengths explicitly; don't assume "best practice" is always better.
5. **Be Realistic About Baselines**: You can't retroactively create data that wasn't collected.
6. **Start Data Collection Now**: Even if no baseline, start measuring going forward.
7. **Engage Peers Meaningfully**: Peer workers often see dynamics staff miss.
8. **Validate Early and Often**: Draft documentation should be reviewed iteratively, not as final product.

---

**NUAA Principle Reminder**: Brownfield documentation is an act of respect for the work already done and the knowledge already created. It's about making implicit knowledge explicit, not imposing external standards that ignore context and history.
