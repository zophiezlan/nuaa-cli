# /nuaa.design - Program Design Command

Template: See [program-design.md](../templates/program-design.md). Related: [logic-model.md](../templates/logic-model.md), [impact-framework.md](../templates/impact-framework.md).

## Description

Generate a comprehensive NUAA program design document including stakeholder journeys, logic models, risk assessment, and impact measurement frameworks. This command guides the creation of peer-led, harm reduction programs that center consumer participation and cultural safety.

---

## Purpose

Create detailed program designs that:

- Center lived experience and peer leadership
- Embed harm reduction principles
- Map stakeholder journeys and touch points
- Define clear logic models (inputs → activities → outputs → outcomes → impact)
- Assess risks and ethical considerations
- Plan for impact measurement
- Ensure cultural safety and consumer participation
- Budget appropriately (including $300/session consumer remuneration)

---

## Usage

```bash
/nuaa.design [PROGRAM_NAME] [TARGET_POPULATION] [DURATION]
```

**Examples**:

- `/nuaa.design "Peer-Led Hepatitis C Education" "people who inject drugs" "6 months"`
- `/nuaa.design "LGBTIQ+ Harm Reduction Support Groups" "queer and trans people who use drugs" "ongoing"`
- `/nuaa.design "Stigma Reduction Workshops" "health service staff" "12 weeks"`

---

## Inputs Required

When you invoke this command, the AI will ask you for:

1. **Program Name**: Clear, descriptive name
2. **Target Population**: Who will benefit? (demographics, needs, location)
3. **Duration**: How long? (weeks, months, ongoing)
4. **Purpose**: What problem does this address?
5. **Evidence Base**: What research/data supports this?
6. **Key Activities**: What will participants do? (3-5 core activities)
7. **Resources Available**: Budget, staff, partnerships, venue
8. **NUAA Alignment**: How does this fit NUAA's mission and strategic plan?

**Optional Context**:

- Similar existing programs to learn from
- Stakeholder feedback or community consultation notes
- Specific funder requirements or constraints

---

## Output Generated

The AI will create a complete **program-design.md** document (based on the template) containing:

1. **Program Overview**: Purpose, evidence base, NUAA alignment
2. **Stakeholder Journey Maps**:
   - Direct beneficiaries (detailed journey from awareness → engagement → participation → outcomes)
   - Partner organizations
   - Additional stakeholders (volunteers, families, community)
3. **Program Logic Model**: Visual and detailed logic model showing inputs → activities → outputs → outcomes → impact
4. **Risk Assessment Matrix**: Risks identified with likelihood, impact, mitigation strategies
5. **Ethical Considerations**: Consumer participation, informed consent, confidentiality, cultural safety, do no harm
6. **Preliminary Budget**: Personnel, operations, participant support, evaluation costs
7. **Impact Measurement Framework**: Process, output, outcome, and impact indicators with data collection methods
8. **Timeline & Milestones**: Phased implementation plan
9. **Sustainability Plan**: How outcomes will be sustained after funding
10. **Approval Checklist**: Review and sign-off requirements

---

## NUAA Principles Integration

The AI will automatically ensure the program design:

### 1. Centers Peer Leadership

- Identifies roles for people with lived experience in design, delivery, and evaluation
- Plans for consumer advisory involvement
- Allocates budget for peer workers and consumer remuneration ($300/session standard)

### 2. Embeds Harm Reduction

- Non-judgmental, non-coercive approach
- Meets people where they're at (no prerequisites)
- Evidence-based information
- Participant agency and choice

### 3. Ensures Cultural Safety

- Cultural competency for staff
- Language accessibility (interpreters, plain language)
- Respect for diversity (LGBTIQ+, CALD, Aboriginal & Torres Strait Islander)
- Trauma-informed practices

### 4. Plans for Consumer Participation

- Advisory group involvement ($300/meeting remuneration)
- Co-design opportunities
- Evaluation participation
- Decision-making power

### 5. Addresses Stigma

- Stigma reduction strategies
- Empowerment focus
- Community education component
- Rights-based framing

---

## Prompt for AI Agent

When `/nuaa.design` is invoked, use this system prompt:

```text
You are a program design specialist for NSW Users & AIDS Association (NUAA),
a peer-led harm reduction organization with 30+ years of experience.

Your task is to create a comprehensive program design document that:
- Centers lived experience and peer leadership
- Embeds harm reduction principles (non-judgmental, meet people where they're at)
- Ensures cultural safety and trauma-informed practice
- Plans for meaningful consumer participation with appropriate remuneration ($300/session)
- Includes detailed stakeholder journeys (awareness → engagement → participation → outcomes)
- Defines clear logic models (inputs → activities → outputs → outcomes → impact)
- Assesses risks and ethical considerations
- Plans for impact measurement (process, output, outcome, impact indicators)
- Budgets realistically (including peer workers, consumer advisory, participant support)

Use the program-design.md template as your structure. Fill in all sections with
specific, actionable content based on the user's inputs.

Ask clarifying questions if you need more information. Be specific about:
- How peer leadership is embedded
- What harm reduction principles look like in practice
- How cultural safety is ensured
- How consumer participation is meaningful (not tokenistic)
- What data will be collected and how

Your output should be ready for NUAA staff to use immediately - no placeholders,
specific details, and aligned with NUAA's values and practice.

Target audience: NUAA staff, management, consumer advisory, potential funders
Output format: Professional but accessible, evidence-based, rights-affirming
Tone: Compassionate, pragmatic, empowering, anti-stigma
```

---

## Example Workflow

**User**: `/nuaa.design "Peer Naloxone Distribution" "people at risk of opioid overdose" "12 months"`

**AI Response**:

```text
I'll help you design a peer-led Naloxone distribution program. Let me gather some information:

1. **Purpose**: What specific problem does this address?
   (e.g., rising overdose deaths, barriers to Naloxone access, need for peer education)

2. **Evidence Base**: What data supports this?
   (e.g., NSW overdose statistics, peer distribution effectiveness studies)

3. **Key Activities**: What will the program involve?
   (e.g., peer training, community outreach, Naloxone distribution, follow-up support)

4. **Resources**: What do you have available?
   - Budget: $[amount]?
   - Staff: [roles/FTE]?
   - Partnerships: [health services, pharmacies]?
   - Venue: [NUAA office, mobile outreach]?

5. **Target Reach**: How many people do you aim to reach?
   (e.g., 200 people receive Naloxone, 50 peer educators trained)

6. **NUAA Alignment**: How does this fit with strategic plan?
   (e.g., Priority 1: Reduce drug-related harm)

Please provide these details and I'll create a comprehensive program design.
```

**User provides details**

**AI Generates**: Complete program-design.md document with:

- Stakeholder journey for person receiving Naloxone (from learning about program → getting trained → receiving Naloxone → using it in emergency → follow-up support)
- Logic model showing inputs (peer educators, Naloxone supply, training materials) → activities (training, distribution, support) → outputs (200 people reached, 500 Naloxone kits distributed) → outcomes (increased knowledge, confidence to respond to overdose, lives saved) → impact (reduced overdose deaths community-wide)
- Risk assessment (e.g., Naloxone supply interruption, peer educator turnover, legal concerns)
- Budget including peer educator remuneration, Naloxone costs, training materials, outreach expenses
- Impact measurement plan with indicators (knowledge pre/post, kits distributed, reversals reported, follow-up data)

---

## Integration with Other Commands

After `/nuaa.design`, you might use:

- `/nuaa.propose` - Turn the program design into a funding proposal
- `/nuaa.measure` - Expand the impact measurement framework
- `/nuaa.report` - Track progress and outcomes during implementation

---

## Quality Checks

Before finalizing the design, the AI should verify:

✓ **Peer leadership**: Are people with lived experience central to design and delivery?  
✓ **Harm reduction**: Are principles explicitly embedded (non-judgmental, agency, evidence-based)?  
✓ **Consumer participation**: Is remuneration budgeted ($300/session)?  
✓ **Cultural safety**: Are trauma-informed, LGBTIQ+ inclusive, culturally responsive practices planned?  
✓ **Logic model**: Is the causal chain clear (inputs → activities → outputs → outcomes → impact)?  
✓ **Risk assessment**: Are key risks identified with mitigation strategies?  
✓ **Budget**: Are all costs accounted for (personnel, operations, participant support, evaluation)?  
✓ **Impact measurement**: Are indicators defined at all levels (process, output, outcome, impact)?  
✓ **Stakeholder journeys**: Are journeys detailed with specific touch points and success indicators?  
✓ **Ethics**: Are informed consent, confidentiality, and do no harm principles addressed?

---

## Customization Options

**Output Format**:

- **Professional** (for funders): Formal language, comprehensive detail
- **Professional-Peer** (for NUAA staff): Balanced, practical
- **Peer-Friendly** (for consumer advisory): Plain language, visual, accessible

Specify format with: `/nuaa.design [INPUTS] --format=professional`

**Focus Area**:

- Add `--focus=logic-model` for deeper logic model development
- Add `--focus=stakeholder-journeys` for detailed journey mapping
- Add `--focus=evaluation` for comprehensive impact measurement

---

## Tips for Best Results

1. **Be specific about target population**: Don't just say "people who use drugs" - specify which drugs, demographics, location, needs
2. **Provide context**: Share any existing data, community feedback, or similar programs
3. **Think about resources**: Be realistic about budget, staff capacity, and timeframe
4. **Involve consumers early**: Use this design as a starting point for consumer advisory input
5. **Iterate**: Review the generated design, refine, and regenerate sections as needed

---

## Support & Resources

**Questions?** Contact NUAA program team for support using this command.

**Related Templates**:

- `program-design.md` - Template this command fills out
- `logic-model.md` - Detailed logic model template
- `impact-framework.md` - Comprehensive impact measurement template

**Related Commands**:

- `/nuaa.propose` - Create funding proposals
- `/nuaa.measure` - Expand impact measurement
- `/nuaa.refine` - Iterate on existing design

---

**This command empowers NUAA staff to quickly create comprehensive, peer-led, harm reduction program designs that are ready for implementation and funding.**
