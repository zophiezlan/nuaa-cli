# Quick Start Guide

This guide will help you get started with the NUAA Project toolkit.

> NEW: All automation scripts now provide both Bash (`.sh`) and PowerShell (`.ps1`) variants. The `nuaa` CLI auto-selects based on OS unless you pass `--script sh|ps`.

## The 4-Step Process

### 1. Install NUAA CLI

Initialize your project depending on the coding agent you're using:

```bash
uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init <PROJECT_NAME>
```

Pick script type explicitly (optional):

```bash
uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init <PROJECT_NAME> --script ps  # Force PowerShell
uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init <PROJECT_NAME> --script sh  # Force POSIX shell
```

> **Note**: The legacy `specify` command is still supported for backwards compatibility.

### 2. Design Your Program

Use the `/nuaa.design` command to create a comprehensive program design. Focus on outcomes, activities, and stakeholder needs.

```bash
/nuaa.design Create a peer-led workshop series on stigma reduction in healthcare settings, targeting both people who use drugs and healthcare providers
```

### 3. Create a Funding Proposal

Use the `/nuaa.propose` command to generate a professional funding proposal based on your program design.

```bash
/nuaa.propose Generate a funding proposal for the stigma reduction workshop series, targeting NSW Health funding opportunities
```

### 4. Define Impact Measurement

Use `/nuaa.measure` to create evaluation frameworks with clear indicators and data collection methods.

```bash
/nuaa.measure Define impact measurement framework for the stigma reduction program, including process, output, and outcome indicators
```

## Detailed Example: Stigma Reduction Program

Here's a complete example of designing a NUAA program:

### Step 1: Create Program Design with `/nuaa.design`

```text
Design a peer-led workshop series addressing stigma reduction in healthcare settings. The program should:
- Target both people who use drugs and healthcare providers
- Include 4 x 2-hour workshops over 4 weeks
- Use lived experience facilitators (2 per session)
- Cover topics: understanding stigma, communication strategies, trauma-informed care, building partnerships
- Include pre/post evaluation surveys
- Provide certificates of completion
- Follow harm reduction and peer-led principles
```

### Step 2: Refine the Design

After the initial design is created, add specific details:

```text
For the peer facilitators, ensure we budget for:
- 4 hours preparation time per workshop ($300/session)
- 2 hours delivery per workshop ($300/session)
- 2 hours debrief and documentation ($300/session)
Add catering budget for each session and ensure venues are accessible
```

### Step 3: Generate Funding Proposal with `/nuaa.propose`

Be specific about the funding context:

```text
Create a funding proposal for the NSW Health Prevention and Harm Reduction Grant. Focus on:
- Budget of $50,000-$75,000
- 12-month timeline
- Partnership with local health district
- Clear outcome measures aligned with NSW Health priorities
- Include NUAA's track record in similar programs
```

### Step 4: Define Impact Framework with `/nuaa.measure`

Create measurable outcomes:

```text
Define evaluation framework including:
- Process indicators: number of workshops delivered, attendance rates, facilitator feedback
- Output indicators: participants completing program, certificates issued
- Outcome indicators: changes in attitudes (pre/post surveys), reported behavior changes
- Impact indicators: reduction in discriminatory incidents (6-month follow-up)
Include data collection templates and analysis methods
```

## Key Principles for NUAA Programs

- **Peer-led approach** - Lived experience at the center
- **Harm reduction philosophy** - Non-judgmental, evidence-based
- **Fair remuneration** - $300/session standard for peer workers
- **Cultural safety** - Respectful of diverse communities
- **Clear outcomes** - Measurable impact aligned with funder priorities
- **NUAA principles** - Built into every template and output

## Next Steps

- Read the complete methodology for in-depth guidance
- Check out more examples in the repository
- Explore the source code on GitHub
