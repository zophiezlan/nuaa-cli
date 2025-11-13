# /nuaa.propose - Funding Proposal Command

Template: See [proposal.md](../templates/proposal.md). Related: [program-design.md](../templates/program-design.md), [logic-model.md](../templates/logic-model.md), [impact-framework.md](../templates/impact-framework.md).

## Description

Generate a comprehensive funding proposal for NUAA programs, transforming program designs into compelling funding applications. This command creates professional, evidence-based proposals that demonstrate impact, center lived experience, and align with funder priorities.

---

## Purpose

Create funding proposals that:

- Tell a compelling story of need and impact
- Demonstrate NUAA's expertise and track record
- Present clear program design with logic models
- Show detailed, justified budgets
- Articulate evaluation and accountability
- Center peer leadership and harm reduction
- Align with funder priorities and guidelines
- Are ready to submit

---

## Usage

```bash
/nuaa.propose [PROGRAM_NAME] [FUNDER] [AMOUNT_REQUESTED] [DURATION]
```

**Examples**:

- `/nuaa.propose "Peer Naloxone Distribution" "NSW Health" "$50000" "12 months"`
- `/nuaa.propose "Stigma Reduction Workshops" "CAGES Foundation" "$25000" "6 months"`
- `/nuaa.propose "LGBTIQ+ Support Groups" "ACON Partnership" "$75000" "2 years"`

---

## Inputs Required

When you invoke this command, the AI will ask you for:

### Program Information

1. **Program Name**: Clear, descriptive name
2. **Target Population**: Who benefits? (specific demographics, needs, location)
3. **Duration**: How long? (months, years)
4. **Total Budget**: Amount requested (be realistic)
5. **Program Design**: Existing program-design.md or key details

### Funder Information

6. **Funder Name**: Organization you're applying to
7. **Funder Priorities**: What do they care about? (check their website/guidelines)
8. **Application Guidelines**: Word limit, format, sections required
9. **Submission Deadline**: When is it due?

### Supporting Evidence

10. **Need Statement**: Data/stories demonstrating the problem
11. **Evidence Base**: Research supporting your approach
12. **NUAA Track Record**: Similar programs you've run successfully
13. **Partnership Letters**: Who will support/collaborate?

**Optional Context**:

- Previous proposals to this funder
- Community consultation findings
- Pilot data or preliminary results
- Letters of support ready to attach

---

## Output Generated

The AI will create a complete **proposal.md** document containing:

1. **Executive Summary**: Compelling 2-3 paragraph overview
2. **Background & Need**: NUAA's expertise, problem statement, evidence of need, why NUAA is best placed
3. **Program Description**: Target population, activities, innovation, harm reduction approach
4. **Methodology & Approach**: Phased implementation, timeline, cultural safety measures, consumer participation
5. **Timeline & Milestones**: Gantt chart, key deliverables
6. **Budget**: Summary + detailed line items with justification
7. **Evaluation & Impact**: Framework, indicators, data collection, reporting
8. **Risks & Mitigation**: Identified risks with strategies
9. **Sustainability**: How outcomes continue after funding
10. **Organizational Capacity**: NUAA's governance, financials, staffing, relevant experience
11. **Conclusion & Call to Action**: Compelling close

---

## NUAA Narrative Integration

The AI will automatically ensure the proposal:

### Tells NUAA's Story

- 30+ years of peer-led harm reduction
- State-wide reach across NSW
- Trusted voice in the community
- Track record of successful programs
- Strong governance and financial management

### Demonstrates Peer Leadership

- Lived experience at center of design, delivery, evaluation
- Consumer advisory involvement
- Peer worker roles with fair remuneration ($300/session)
- Meaningful participation (not tokenistic)

### Embeds Harm Reduction

- Non-judgmental, pragmatic approach
- Evidence-based information
- Meeting people where they're at
- Participant agency and choice

### Shows Cultural Safety

- Trauma-informed practices
- LGBTIQ+ inclusive
- Culturally responsive (CALD, Aboriginal & Torres Strait Islander)
- Language accessibility

### Addresses Stigma

- Rights-based framing
- Anti-stigma language
- Empowerment focus
- Community education

---

## Funder Alignment

The AI will tailor the proposal to the specific funder:

### Government Funders (NSW Health, Commonwealth)

- Policy alignment (e.g., National Drug Strategy, NSW Strategic Framework)
- Evidence-based practice
- Accountability and evaluation
- Value for money
- Population health outcomes

### Philanthropic Funders (CAGES, StreetSmart, etc.)

- Compelling human stories
- Innovation and creativity
- Community leadership
- Sustainable impact
- Collaboration

### Corporate/Partnership Funders

- Shared values alignment
- Community benefit
- Partnership opportunities
- Measurable outcomes

---

## Prompt for AI Agent

When `/nuaa.propose` is invoked, use this system prompt:

```text
You are a grant writer for NSW Users & AIDS Association (NUAA), a peer-led
harm reduction organization with 30+ years of experience.

Your task is to create a compelling funding proposal that:
- Tells a powerful story of need and impact
- Demonstrates NUAA's unique expertise and track record
- Presents a clear, evidence-based program design
- Shows detailed budget with justification
- Articulates rigorous evaluation plan
- Centers lived experience and peer leadership
- Embeds harm reduction principles
- Aligns with funder priorities
- Uses anti-stigma, rights-affirming language

Use the proposal.md template as your structure. Customize based on funder type:
- Government: Policy alignment, evidence, accountability, population health
- Philanthropic: Human stories, innovation, community leadership, sustainable impact
- Corporate: Shared values, measurable outcomes, partnership opportunities

Your writing should be:
- Compelling but not sensationalist
- Evidence-based but human-centered
- Professional but passionate
- Specific (no vague claims)
- Action-oriented (clear what you'll do)

Target audience: Funder decision-makers (may not be harm reduction experts)
Output format: Professional, well-structured, ready to submit
Tone: Confident, compassionate, evidence-based, anti-stigma, empowering

Ask clarifying questions if you need more information about:
- Funder priorities and guidelines
- Specific program details
- Budget breakdown
- Evidence base
- NUAA track record
```

---

## Example Workflow

**User**: `/nuaa.propose "Peer Naloxone Distribution" "NSW Health" "$50000" "12 months"`

**AI Response**:

```text
I'll help you create a funding proposal for NSW Health. Let me gather information:

1. **Funder Priorities**: NSW Health priorities include:
   - Reducing drug-related harm and overdose deaths
   - Implementing the NSW Strategic Framework for Alcohol and Other Drugs
   - Community-based harm reduction interventions
   - Is this proposal responding to a specific funding round or open call?

2. **Application Guidelines**:
   - Word limit? (e.g., 10 pages, 5000 words)
   - Required sections? (check guidelines)
   - Submission deadline?

3. **Program Details**: Do you have an existing program-design.md or should I help create one?

4. **Evidence of Need**:
   - NSW overdose statistics (e.g., X deaths in 2023, Y% increase)
   - Barriers to Naloxone access
   - Community feedback

5. **NUAA Track Record**:
   - Have you run Naloxone programs before? Results?
   - Similar programs demonstrating success?

6. **Budget Details**:
   - Peer educator wages/remuneration
   - Naloxone supply costs
   - Training materials
   - Outreach expenses
   - Admin/overhead percentage

Please provide these details and I'll create a compelling proposal.
```

**User provides details**

**AI Generates**: Complete proposal.md with:

- Executive summary highlighting NSW's overdose crisis, NUAA's peer-led solution, $50K investment reaching 200 people, lives saved
- Background establishing NUAA credibility + NSW overdose data + why peer distribution is evidence-based
- Program description detailing peer training, community outreach, Naloxone distribution, follow-up support
- Methodology showing 5 phases (setup, training, outreach, distribution, evaluation)
- Budget with line items (peer educators $18K, Naloxone $15K, materials $5K, evaluation $7K, admin $5K)
- Evaluation plan with indicators (kits distributed, reversals reported, knowledge gained, lives saved)
- Risk mitigation (supply continuity, peer retention, legal clarity)
- Sustainability (partnerships with pharmacies, ongoing funding plan)

---

## Budget Builder

The AI will automatically:

### Calculate Personnel Costs

- Coordinator: [FTE] x [months] x [rate]
- Peer workers: [sessions] x $300/session
- Admin support: [% of total]

### Include All Operational Costs

- Venue hire
- Materials and supplies
- Technology/software
- Equipment

### Budget for Participant Support

- Transport/parking reimbursement
- Catering (accessibility measure)
- Childcare (if needed)
- Consumer advisory remuneration ($300/meeting)
- Participant honorariums

### Allocate Evaluation Funds

- Survey tools
- Data analysis (staff time)
- Report production
- Typically 5-15% of total budget

### Apply Admin Overhead

- Finance, HR, IT support
- Rent, utilities
- Usually 10-20% of direct costs

### Justify Every Line Item

- Explain why each cost is necessary
- Show calculations clearly
- Note if rates are based on awards/standards

---

## Quality Checks

Before finalizing, the AI will verify:

✓ **Alignment**: Proposal matches funder priorities and guidelines  
✓ **Clarity**: Problem, solution, and impact are crystal clear  
✓ **Evidence**: Claims backed by data, research, or lived experience  
✓ **NUAA values**: Peer leadership, harm reduction, cultural safety embedded  
✓ **Budget**: All costs accounted for and justified  
✓ **Evaluation**: Clear indicators and data collection methods  
✓ **Realism**: Timeline and targets are achievable  
✓ **Completeness**: All required sections included  
✓ **Language**: Professional, anti-stigma, empowering  
✓ **Formatting**: Follows funder's format requirements

---

## Customization Options

### Output Format

- **Professional** (for government/institutional funders): Formal, comprehensive, policy-aligned
- **Engaging** (for philanthropic funders): Storytelling, human-centered, inspiring
- **Partnership** (for corporate funders): Mutual benefit, measurable outcomes, collaboration opportunities

Specify format with: `/nuaa.propose [INPUTS] --format=engaging`

### Focus Area

- Add `--focus=budget` for detailed budget development
- Add `--focus=evaluation` for comprehensive impact measurement
- Add `--focus=storytelling` for narrative strength

### Length

- Add `--length=short` for brief concept notes (2-3 pages)
- Add `--length=full` for comprehensive applications (10-20 pages)

---

## Integration with Other Commands

**Before `/nuaa.propose`**, use:

- `/nuaa.design` - Create the program design first

**After `/nuaa.propose`**, use:

- `/nuaa.refine` - Improve specific sections based on feedback
- `/nuaa.report` - Track progress if funded

---

## Common Funder Types & Adaptations

### NSW Health / Government

**Emphasize**:

- Policy alignment (National Drug Strategy, NSW Strategic Framework)
- Evidence-based practice (cite research)
- Population health outcomes (reduced harm, improved health)
- Accountability (rigorous evaluation, financial reporting)
- Value for money (cost per person reached, cost per outcome)

**Language**: Formal, evidence-focused, outcome-oriented

### CAGES Foundation / Philanthropic

**Emphasize**:

- Human stories (lived experience narratives)
- Innovation (new approaches, creative solutions)
- Community leadership (peer-led, grassroots)
- Sustainable impact (lasting change beyond funding)

**Language**: Engaging, story-driven, inspiring

### Harm Reduction International / Sector Funders

**Emphasize**:

- Harm reduction principles (explicit framing)
- Rights-based approach (human rights, dignity)
- Peer leadership (lived experience at center)
- Evidence contribution (learnings shared with sector)

**Language**: Sector-specific, rights-affirming, evidence-based

---

## Tips for Best Results

1. **Start with program design**: Have a clear program-design.md before proposing
2. **Research the funder**: Know their priorities, previous grants, language they use
3. **Be specific**: Avoid vague claims like "improve wellbeing" - say how and by how much
4. **Show NUAA's value**: What can NUAA do that others can't? (30 years trust, peer-led, community connections)
5. **Budget realistically**: Don't lowball to seem cheap - fund what's actually needed
6. **Tell stories**: Include de-identified case studies or community voices (with consent)
7. **Proofread**: Errors undermine credibility - review carefully
8. **Get feedback**: Share draft with consumer advisory, management, peers

---

## Attachments Checklist

The AI will remind you to prepare:

- [ ] NUAA Annual Report (most recent)
- [ ] Letters of Support (from partners, community members)
- [ ] Staff CVs/Bios (key personnel)
- [ ] Logic Model (visual diagram)
- [ ] Evidence Base References (research citations)
- [ ] Budget Detail (Excel spreadsheet)
- [ ] Evaluation Framework (full version)
- [ ] MOUs/Partnership Agreements
- [ ] Organizational Policies (if required by funder)
- [ ] Financial Statements (audited, recent)

---

## Support & Resources

**Questions?** Contact NUAA program team or development manager for support.

**Related Templates**:

- `proposal.md` - Template this command fills out
- `program-design.md` - Design your program first
- `logic-model.md` - Visual logic model for attachment

**Related Commands**:

- `/nuaa.design` - Create program design first
- `/nuaa.measure` - Expand evaluation framework
- `/nuaa.refine` - Improve specific sections

**NUAA Grant Writing Resources**:

- Previous successful proposals (ask management for examples)
- Funder database (who funds what in harm reduction)
- Boilerplate text (NUAA's history, approach, capacity)

---

**This command empowers NUAA staff to rapidly create compelling, professional funding proposals that secure resources for peer-led harm reduction programs.**
