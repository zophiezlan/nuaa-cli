# /nuaa.engage - Stakeholder Engagement Plan Command

**Purpose**: Create a comprehensive stakeholder engagement plan for a NUAA program

**Template**: See [stakeholder-engagement-plan.md](../templates/stakeholder-engagement-plan.md)

---

## Overview

The `/nuaa.engage` command generates a detailed stakeholder engagement plan that identifies all stakeholders, analyzes their interests and influence, and defines strategies for meaningful engagement throughout the program lifecycle.

This is essential for:
- Building and maintaining strong relationships with key stakeholders
- Ensuring all voices are heard (especially community voices)
- Managing expectations and preventing conflicts
- Creating sustainable partnerships
- Demonstrating NUAA's commitment to authentic engagement

---

## Command Syntax

```bash
nuaa engage <program-name> <target-population> <duration> [options]
```

### Required Arguments

1. **program-name**: Name of the program (used to create feature folder)
2. **target-population**: Description of who the program serves
3. **duration**: Planning period for engagement (e.g., "12 months", "2 years")

### Optional Arguments

- `--feature <slug>`: Override feature folder slug
- `--force`: Overwrite existing file if present

---

## Examples

### Basic Usage

```bash
nuaa engage "Peer Naloxone Program" "People who inject drugs in Western Sydney" "18 months"
```

**Creates**: `nuaa/001-peer-naloxone-program/stakeholder-engagement-plan.md`

---

### With Custom Feature Slug

```bash
nuaa engage "Stigma Reduction Campaign" "People who use drugs and service providers" "12 months" --feature "002-stigma-campaign"
```

**Creates**: `nuaa/002-stigma-campaign/stakeholder-engagement-plan.md`

---

## What Gets Created

The command generates a comprehensive stakeholder engagement plan including:

### 1. Stakeholder Mapping
- Internal stakeholders (Board, staff, peer workers)
- External stakeholders - primary (participants, consumer advisory)
- External stakeholders - partners (service providers, funders, research institutions)
- External stakeholders - influencers (government, sector peers, media)
- External stakeholders - observers (general community)

### 2. Stakeholder Analysis
- Interest and influence assessment
- Priority ranking (P1, P2, P3)
- Engagement strategy for each group

### 3. Engagement Activities
- Pre-program engagement timeline
- During program engagement schedule
- Post-program follow-up activities

### 4. Communication Channels
- Primary and backup channels for each stakeholder group
- Frequency and format specifications
- Accessibility considerations

### 5. Key Messages
- Tailored messages for different stakeholder groups
- Tone and language guidance
- Stigma-free communication principles

### 6. Managing Challenges
- Stakeholder resistance strategies
- Competing interests management
- Over-engagement boundaries

### 7. Success Indicators
- Engagement metrics and targets
- Feedback mechanisms
- Continuous improvement processes

### 8. Cultural Safety
- Aboriginal & Torres Strait Islander engagement protocols
- LGBTIQ+ inclusive practices
- CALD community considerations
- Accessibility measures

---

## Integration with Other Commands

The stakeholder engagement plan works alongside:

- **`/nuaa.design`**: Identifies stakeholders in program design, detailed in engagement plan
- **`/nuaa.partner`**: Partnership agreements implement engagement strategies
- **`/nuaa.propose`**: Demonstrates stakeholder buy-in to funders
- **`/nuaa.event`**: Events as engagement activities
- **`/nuaa.risk`**: Stakeholder risks identified and mitigated

---

## Best Practices

### 1. Start Early
Create the stakeholder engagement plan during program design, not as an afterthought.

### 2. Be Comprehensive
Don't just list stakeholders - analyze their interests, influence, and how to engage them meaningfully.

### 3. Prioritize Community Voice
Ensure people who use drugs (primary community) have genuine decision-making power, not just consultation.

### 4. Plan for Diversity
Consider how to reach and engage Aboriginal & Torres Strait Islander people, LGBTIQ+ people, CALD communities.

### 5. Resource Appropriately
Budget for stakeholder engagement activities (meetings, catering, consumer remuneration, accessibility support).

### 6. Review Regularly
Stakeholder dynamics change - review and update the plan quarterly.

### 7. Track Engagement
Monitor engagement metrics to ensure you're reaching targets and adjust strategies as needed.

---

## NUAA-Specific Considerations

### Nothing About Us Without Us
- People who use drugs lead and guide all engagement
- Authentic participation, not tokenism
- Decision-making power, not just consultation

### Consumer Remuneration
- $300/session standard rate for peer workers and advisory group members
- Value lived experience as expertise
- Budget for consumer participation in all engagement activities

### Harm Reduction Principles
- Non-judgmental engagement
- Meeting people where they're at
- Reducing barriers to participation
- Trauma-informed approaches

### Cultural Safety
- Respect for Aboriginal & Torres Strait Islander peoples and protocols
- LGBTIQ+ inclusive language and practices
- Culturally appropriate engagement methods
- Accessibility as standard, not exception

---

## Output Format

The generated file includes:
- YAML frontmatter (metadata)
- Markdown content with:
  - Stakeholder mapping sections
  - Analysis matrices and tables
  - Engagement timelines
  - Communication protocols
  - Resource requirements

---

## Typical Workflow

1. **Create program design** (`/nuaa.design`)
2. **Create stakeholder engagement plan** (`/nuaa.engage`) ← You are here
3. **Identify specific partnerships**
4. **Create partnership agreements** (`/nuaa.partner`) for key collaborations
5. **Develop communication plan** (manual or with communication-plan.md template)
6. **Implement engagement activities**
7. **Monitor and adapt** based on stakeholder feedback

---

## Customization

After generation:

1. **Review and customize stakeholder groups**: Add/remove stakeholders specific to your program
2. **Set priorities**: Determine which stakeholders are P1 (critical) vs P2 (important) vs P3 (useful)
3. **Define engagement methods**: Choose methods that work for your context
4. **Set realistic timelines**: Adjust engagement frequency based on capacity
5. **Budget appropriately**: Ensure resources for meaningful engagement
6. **Get input**: Have consumer advisory and key partners review the plan

---

## Related Resources

- **Template**: [stakeholder-engagement-plan.md](../templates/stakeholder-engagement-plan.md)
- **Related Commands**:
  - [/nuaa.design](design.md) - Program design
  - [/nuaa.partner](partner.md) - Partnership agreements
  - [communication-plan.md](../templates/communication-plan.md) - Communications strategy
  - [community-engagement-strategy.md](../templates/community-engagement-strategy.md) - Community engagement

---

## Support

For questions about stakeholder engagement:
- Review the full template for detailed guidance
- Consult with NUAA management or experienced staff
- Engage consumer advisory for community perspective
- Draw on NUAA's 30+ years of stakeholder engagement experience

---

**Effective stakeholder engagement is the foundation of program success. This command ensures all voices are heard and valued.**
