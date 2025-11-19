---
description: Create partnership agreements and collaboration frameworks
scripts:
  sh: bash .nuaa/scripts/bash/create-new-feature.sh partner {ARGS}
  ps: powershell .nuaa/scripts/powershell/create-new-feature.ps1 partner {ARGS}
---

# /nuaa.partner - Partnership Agreement Command

**Purpose**: Generate formal partnership agreements (MOUs) for collaborations

**Template**: See [partnership-agreement.md](../templates/partnership-agreement.md)

## Command Syntax

```bash
nuaa partner <program-name> <partner-org> <duration> [options]
```

## Examples

```bash
nuaa partner "Harm Reduction Program" "Local Health District" "2 years"
nuaa partner "Peer Training" "Community Health NSW" "12 months" --feature "003-peer-training-mou"
```

## What Gets Created

Comprehensive MOU template including:
- Purpose and scope of partnership
- Roles and responsibilities (both organizations)
- Governance and decision-making protocols
- Information sharing and confidentiality agreements
- Financial arrangements and budget
- Evaluation and reporting requirements
- Risk management
- Dispute resolution process
- Termination provisions
- Signatory sections

## Use Cases

- Formalizing referral partnerships with service providers
- Research collaborations with universities
- Funding relationships beyond standard contracts
- Multi-organization program delivery
- Shared resource agreements

## Best Practices

1. **Co-create**: Develop the MOU together with your partner
2. **Be specific**: Clear roles prevent misunderstandings later
3. **Include lived experience**: Ensure peer participation requirements are explicit
4. **Set review dates**: Quarterly reviews keep partnerships healthy
5. **Plain language**: Avoid legal jargon where possible
6. **Get sign-off**: Senior management from both organizations

**See template for detailed guidance on partnership agreements.**
