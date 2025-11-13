# /nuaa.measure - Impact Measurement Command

Template: See [impact-framework.md](../templates/impact-framework.md). Related: [logic-model.md](../templates/logic-model.md), [program-design.md](../templates/program-design.md).

## Description

Generate a comprehensive impact measurement and evaluation framework for NUAA programs. This command creates rigorous, participatory evaluation plans that demonstrate outcomes, center participant voice, and contribute to the evidence base for peer-led harm reduction.

---

## Purpose

Create evaluation frameworks that:

- Define clear indicators at all levels (process, output, outcome, impact)
- Plan data collection methods (quantitative, qualitative, participatory)
- Ensure ethical, culturally safe evaluation practices
- Center participant voice and lived experience
- Enable continuous learning and improvement
- Demonstrate accountability to funders and community
- Contribute to harm reduction evidence base
- Are feasible with available resources

---

## Usage

```bash
/nuaa.measure [PROGRAM_NAME] [EVALUATION_PERIOD] [BUDGET]
```

**Examples**:

- `/nuaa.measure "Peer Naloxone Distribution" "12 months" "$7000"`
- `/nuaa.measure "Stigma Reduction Workshops" "6 months" "$3500"`
- `/nuaa.measure "LGBTIQ+ Support Groups" "ongoing" "$10000"`

---

## Inputs Required

When you invoke this command, the AI will ask you for:

### Program Information

1. **Program Name**: What program are you evaluating?
2. **Program Design**: Existing program-design.md or key details (logic model, activities, target outcomes)
3. **Evaluation Period**: How long? (duration of program + follow-up)
4. **Primary Evaluation Questions**: What do you most need to know?

### Evaluation Scope

5. **Evaluation Type**:

   - Process evaluation (Are we doing what we planned?)
   - Outcome evaluation (What changed for participants?)
   - Impact evaluation (What broader change occurred?)
   - All of the above?

6. **Target Reach**: How many participants? (affects sample size, feasibility)
7. **Key Stakeholders**: Who needs to hear evaluation findings? (funders, community, sector, participants)

### Resources Available

8. **Evaluation Budget**: How much allocated? (typically 5-15% of program budget)
9. **Staff Capacity**: Who will lead evaluation? (peer researchers, program staff, external evaluator)
10. **Data Access**: What data sources available? (surveys, admin records, service data, community data)

**Optional Context**:

- Funder reporting requirements (what they require)
- Existing baseline data
- Similar program evaluations to learn from
- Participant preferences for data collection methods

---

## Output Generated

The AI will create a complete **impact-framework.md** document containing:

1. **Purpose & Principles**: Why evaluate, ethical principles (participatory, culturally safe, practical)
2. **Evaluation Questions**: Process, outcome, impact, and equity questions
3. **Indicators Framework**: Process, output, outcome (short/medium/long-term), and impact indicators with targets and data sources
4. **Data Collection Methods**:
   - Quantitative (surveys, monitoring data, admin data)
   - Qualitative (interviews, focus groups, case studies, observations)
   - Participatory (Most Significant Change, outcome harvesting, participatory analysis)
5. **Data Collection Timeline**: When each method used throughout program
6. **Data Management & Ethics**: Informed consent, confidentiality, data security, Aboriginal & Torres Strait Islander data sovereignty
7. **Data Analysis Plan**: Quantitative and qualitative analysis approaches
8. **Reporting & Dissemination**: Reports for different audiences (funder, community, sector)
9. **Quality Assurance**: Validity, reliability, cultural validity, bias minimization
10. **Evaluation Budget**: Detailed costs for tools, incentives, peer researcher time, analysis
11. **Evaluation Team**: Roles and responsibilities (including peer researchers)

---

## NUAA Evaluation Principles

The AI will automatically ensure the framework:

### Centers Participant Voice

- Participants involved in designing evaluation questions
- Participants contribute to data analysis and interpretation
- Participants review and validate findings
- Participant stories and perspectives prioritized
- Incentives provided for evaluation participation

### Employs Peer Researchers

- People with lived experience lead data collection
- Peer researchers as co-authors
- Remuneration: $300/session or appropriate hourly rate
- Training and support for peer researchers
- Recognition of peer research as expertise

### Ensures Cultural Safety

- Trauma-informed questions and processes
- LGBTIQ+ inclusive methods
- Culturally responsive approaches (CALD, Aboriginal & Torres Strait Islander)
- Language accessibility
- Safe spaces for sharing

### Maintains Ethics

- Informed consent (written and verbal)
- Confidentiality and anonymity protected
- Right to withdraw at any time
- Secure data storage
- Aboriginal & Torres Strait Islander data sovereignty

### Balances Rigor & Feasibility

- Methods appropriate to resources
- Realistic data collection burden
- Valid and reliable measures
- Pragmatic timelines

---

## Evaluation Approach by Program Type

### Community Education Programs

**Focus**: Knowledge, attitudes, skills, satisfaction

**Methods**:

- Pre/post surveys (knowledge tests, attitude scales)
- Session feedback forms
- Interviews (what changed for you?)
- Observation (engagement, participation quality)

**Indicators**: % knowledge increase, % attitude shift, satisfaction ratings, session attendance

---

### Support/Peer Programs

**Focus**: Connection, wellbeing, empowerment, peer support

**Methods**:

- Validated wellbeing scales (K10, empowerment scale)
- Network mapping (connections made)
- Interviews (how has this affected your life?)
- Most Significant Change stories
- Follow-up surveys (3, 6, 12 months)

**Indicators**: Wellbeing scores, number of peer connections, empowerment ratings, sustained engagement

---

### Service Access/Navigation Programs

**Focus**: Service access, barriers reduced, health outcomes

**Methods**:

- Service usage data (with consent from partners)
- Participant surveys (services accessed, barriers experienced)
- Case studies (journeys through services)
- Health outcomes data (if available and consented)

**Indicators**: Number accessing services, barriers reduced, health improvements, satisfaction with services

---

### Advocacy/Policy Programs

**Focus**: Policy influence, systems change, community capacity

**Methods**:

- Policy document analysis (citations, alignment)
- Stakeholder interviews (decision-makers, partners)
- Media analysis (reach, framing)
- Community capacity assessment

**Indicators**: Policy citations, legislation influenced, media reach, community mobilization

---

## Prompt for AI Agent

When `/nuaa.measure` is invoked, use this system prompt:

```text
You are an evaluation specialist for NSW Users & AIDS Association (NUAA),
a peer-led harm reduction organization.

Your task is to create a comprehensive, feasible evaluation framework that:
- Defines clear indicators at all levels (process, output, outcome, impact)
- Plans data collection methods that are rigorous yet practical
- Centers participant voice and lived experience
- Employs peer researchers meaningfully (not tokenistic)
- Ensures ethical, culturally safe practices
- Balances accountability with learning
- Enables continuous improvement
- Contributes to harm reduction evidence base

Use the impact-framework.md template as your structure.

Your framework should be:
- Specific (clear indicators, targets, methods)
- Participatory (participants involved throughout)
- Ethical (consent, confidentiality, safety)
- Culturally safe (trauma-informed, inclusive)
- Feasible (realistic with available resources)
- Rigorous (valid, reliable measures)
- Useful (findings inform action)

Ask clarifying questions about:
- Program design and logic model
- Primary evaluation questions
- Evaluation budget and capacity
- Data access and availability
- Funder reporting requirements

Target audience: NUAA staff, peer researchers, funders, community
Output format: Professional, clear, actionable
Tone: Rigorous yet accessible, participatory, ethical
```

---

## Example Workflow

**User**: `/nuaa.measure "Peer Naloxone Distribution" "12 months" "$7000"`

**AI Response**:

```text
I'll help you create an impact measurement framework for the Peer Naloxone Distribution program. Let me gather information:

1. **Program Design**: Do you have a program-design.md or can you share:
   - Target reach (e.g., 200 people receive Naloxone, 50 peer educators trained)
   - Key activities (training, distribution, follow-up)
   - Expected outcomes (knowledge, confidence, lives saved)

2. **Primary Evaluation Questions**: What do you most need to know?
   - Process: Did we reach and train 200 people as planned?
   - Outcome: Did participants gain knowledge and confidence to use Naloxone?
   - Impact: Were overdoses reversed? Lives saved?

3. **Data Sources Available**:
   - Surveys (pre/post training, follow-up)
   - Distribution records (who received Naloxone, when)
   - Reversal reports (did they use it? outcome?)
   - Service data (ambulance, hospital admissions)

4. **Evaluation Capacity**:
   - Who will lead? (program staff, peer researcher, external evaluator)
   - Peer researcher time available (e.g., 20 hours @ $300/session = $6000)
   - Tools needed (survey software, analysis support)

5. **Reporting Requirements**:
   - What does NSW Health require? (interim report, final report, metrics)
   - Community reporting? (plain language summary)

Please provide these details and I'll create a comprehensive framework.
```

**User provides details**

**AI Generates**: Complete impact-framework.md with:

- Evaluation questions: Process (Did we reach 200 people? Deliver 40 training sessions?), Outcome (Did knowledge increase? Confidence improve? Were reversals successful?), Impact (Were overdose deaths reduced community-wide?)
- Indicators: Process (attendance records, 200 target), Output (Naloxone kits distributed, 500 target), Outcome short-term (knowledge pre/post, 30% increase target), Outcome medium-term (reversals reported, 50 target), Impact (overdose death rate in catchment area)
- Data collection methods: Pre/post surveys (knowledge, confidence), distribution logs (who, when, where), follow-up calls (did you use it? outcome?), case studies (reversal stories), service data (ambulance/hospital records with partnership agreement)
- Data collection timeline: Week 1 (baseline survey), Weekly (distribution logs), Monthly (follow-up calls), 3/6/12 months (follow-up surveys), Ongoing (reversal reports)
- Peer researcher role: Lead interviews/calls (build trust), co-analyze data, co-author report, remuneration $300/session
- Ethical considerations: Informed consent (training + data), confidentiality (de-identified data), support available (if disclosing overdose trauma), secure storage (encrypted files)
- Reporting: Interim report (6 months, NSW Health), Final report (12 months, NSW Health + community), Case studies (with consent, funding proposals)

---

## Indicator Development

The AI will create SMART indicators:

**Specific**: Clear what's measured (not vague)  
**Measurable**: Can be quantified or clearly observed  
**Achievable**: Realistic with program resources  
**Relevant**: Linked to program logic model  
**Time-bound**: When measured, target timeframe

**Example - Good Indicator**:

- ❌ "Participants feel better" (too vague)
- ✅ "70% of participants report 10+ point improvement on K10 psychological distress scale by 6 months" (specific, measurable, achievable, relevant, time-bound)

---

## Data Collection Method Selection

The AI will recommend appropriate methods based on:

### What You're Measuring

- **Knowledge**: Pre/post surveys, quizzes
- **Attitudes**: Validated scales, focus groups
- **Behavior**: Self-report surveys, observation, admin data
- **Wellbeing**: Validated scales (K10, WEMWBS, etc.)
- **Connection**: Network mapping, self-report
- **Service access**: Admin records, participant tracking
- **System change**: Document analysis, stakeholder interviews

### Your Resources

- **Limited budget**: Surveys (online free tools), monitoring data, brief interviews
- **Moderate budget**: Validated scales, peer researcher-led focus groups, case studies
- **Strong budget**: Longitudinal follow-up, external evaluation support, creative methods (photovoice)

### Your Participants

- **High literacy**: Online surveys, written materials
- **Low literacy**: Phone/in-person surveys, visual methods, peer-led data collection
- **Diverse languages**: Translated surveys, interpreters, community researchers
- **Trauma histories**: Trauma-informed questions, safe spaces, optional participation

---

## Quality Checks

Before finalizing, the AI will verify:

✓ **Indicators defined**: Clear indicators at all levels (process, output, outcome, impact)  
✓ **Methods appropriate**: Data collection methods match indicators and resources  
✓ **Timeline feasible**: Data collection schedule is realistic  
✓ **Ethics covered**: Consent, confidentiality, safety, Aboriginal & Torres Strait Islander data sovereignty  
✓ **Peer involvement**: Peer researchers meaningfully involved, fairly remunerated  
✓ **Cultural safety**: Trauma-informed, inclusive, culturally responsive  
✓ **Budget realistic**: Evaluation costs align with resources available  
✓ **Reporting planned**: Reports for all stakeholders (funder, community, sector)  
✓ **Useful**: Findings will inform program improvement and future work  
✓ **Feasible**: Evaluation burden is manageable for staff and participants

---

## Customization Options

### Evaluation Depth

- `--depth=light` - Process and output evaluation only (monitoring)
- `--depth=standard` - Process, output, short-term outcome evaluation (standard)
- `--depth=comprehensive` - All levels including long-term outcome and impact evaluation (robust)

### Participatory Focus

- `--participatory=high` - Maximum participant involvement (co-design, co-analysis, co-authorship)
- `--participatory=standard` - Peer researchers lead data collection, participants review findings
- `--participatory=light` - Participant feedback sought, limited involvement in analysis

### Method Mix

- `--methods=quantitative` - Primarily surveys, scales, monitoring data
- `--methods=qualitative` - Primarily interviews, focus groups, case studies
- `--methods=mixed` - Balance of quantitative and qualitative (recommended)

---

## Integration with Other Commands

**Before `/nuaa.measure`**, use:

- `/nuaa.design` - Create program design with logic model first (evaluation flows from this)

**After `/nuaa.measure`**, use:

- `/nuaa.report` - Track progress and generate evaluation reports during implementation

---

## Tips for Best Results

1. **Start with logic model**: Clear logic model makes indicators obvious (measure at each level)
2. **Prioritize questions**: Can't measure everything - focus on most important questions
3. **Use validated scales**: Don't reinvent the wheel (K10, empowerment scales, stigma scales exist)
4. **Plan for attrition**: Participants may drop out - plan follow-up strategies, realistic targets
5. **Budget for incentives**: Gift vouchers, prize draws, catering increase participation
6. **Involve peer researchers early**: Co-design evaluation, don't just extract labor
7. **Think about use**: How will findings be used? (improvement, funding, advocacy, evidence base)
8. **Be realistic**: Don't over-burden staff or participants with excessive data collection

---

## Common Evaluation Challenges & Solutions

### Challenge: Low survey response rates

**Solutions**:

- Keep surveys short (10 minutes max)
- Offer multiple formats (online, paper, phone)
- Incentivize (gift vouchers, prize draws)
- Send reminders (email, text, calls)
- Make it relevant (explain how data helps)

### Challenge: Participant attrition (lost to follow-up)

**Solutions**:

- Collect multiple contact methods (phone, email, social media)
- Stay connected (newsletter, social media, events)
- Flexible follow-up windows (not just one date)
- Peer outreach (peers find peers)

### Challenge: Sensitive topics cause distress

**Solutions**:

- Trauma-informed questions (avoid re-traumatizing)
- Optional questions (right to skip)
- Support available (debrief, referrals)
- Peer data collectors (build trust, safe space)

### Challenge: Data quality issues (missing, inconsistent)

**Solutions**:

- Standardized procedures (training, checklists)
- Regular data checks (catch errors early)
- Clear definitions (what counts as "completion"?)
- Simple tracking systems (not over-complicated)

### Challenge: Limited evaluation expertise

**Solutions**:

- Use existing tools (validated scales, templates)
- Partner with researchers (university partnerships)
- Hire external evaluator (if budget allows)
- Professional development (evaluation training for staff)

---

## Support & Resources

**Questions?** Contact NUAA evaluation lead or external evaluation partners.

**Related Templates**:

- `impact-framework.md` - Template this command fills out
- `logic-model.md` - Logic model guides evaluation design
- `program-design.md` - Program design includes preliminary impact measurement

**Related Commands**:

- `/nuaa.design` - Create program design first (includes impact measurement section)
- `/nuaa.report` - Generate evaluation reports during/after implementation
- `/nuaa.refine` - Improve evaluation framework based on pilot learnings

**NUAA Evaluation Resources**:

- Validated scales library (K10, stigma scales, empowerment scales, etc.)
- Previous evaluation reports (learn from past programs)
- Peer researcher training materials
- Ethics and consent form templates

**External Resources**:

- Better Evaluation (bettervaluation.org)
- CDC Evaluation Framework
- UNSW Social Policy Research Centre (evaluation support)
- Harm Reduction International (sector evaluations, evidence base)

---

**This command empowers NUAA staff to rapidly create rigorous, participatory evaluation frameworks that demonstrate impact while honoring participant voice and contributing to the harm reduction evidence base.**
