---
status: implemented
version: 1.0.0
purpose: "Budget calculator template for NUAA program design and proposals"
created: 2025-11-10
---

# Budget Calculator Template

## Overview

This template helps you build comprehensive, transparent program budgets aligned with NUAA principles of fair remuneration, cultural safety, and harm reduction. Use it during program design (`/nuaa.design`) or proposal development (`/nuaa.propose`).

**Key Features**:

- Pre-populated NUAA remuneration standards ($300/session baseline)
- Standard cost categories for peer-led harm reduction programs
- Automatic calculations and percentage breakdowns
- Sensitivity scenarios (reduced/expanded funding)
- Export-ready formatting for Excel and Word proposals

## Usage Instructions

### 1. Fill in Program Details

Copy this template and fill in the Program Information section below with your specific program details.

### 2. Complete Budget Tables

Work through each category table, adjusting quantities and rates based on your program design. All subtotals calculate automatically when exported to Excel.

### 3. Review Assumptions

Document all rate assumptions in the "Budget Assumptions" section. Funders appreciate transparency about how you calculated costs.

### 4. Run Sensitivity Scenarios

Complete at least one sensitivity analysis (e.g., "What if funding is reduced by 20%?") to show program flexibility and risk management.

### 5. Export

- **For Word proposals**: Copy tables directly
- **For Excel**: Use the provided formulas
- **For internal planning**: Keep as Markdown in program design folder

---

## Program Information

| Field                         | Value                             |
| ----------------------------- | --------------------------------- |
| **Program Name**              | [Program Name]                    |
| **Duration**                  | [Months/Years]                    |
| **Target Participants**       | [Number] people who [description] |
| **Geographic Area**           | [Location]                        |
| **Total Sessions/Activities** | [Number]                          |
| **Budget Period**             | [Start Date] to [End Date]        |
| **Prepared By**               | [Name/Role]                       |
| **Date**                      | [Date]                            |
| **Version**                   | [1.0]                             |

---

## Budget Summary

| Category                         | Amount            | % of Total |
| -------------------------------- | ----------------- | ---------- |
| **1. Personnel Costs**           | $[calculated]     | [%]        |
| **2. Peer Remuneration**         | $[calculated]     | [%]        |
| **3. Operations**                | $[calculated]     | [%]        |
| **4. Participant Support**       | $[calculated]     | [%]        |
| **5. Evaluation & Data**         | $[calculated]     | [%]        |
| **6. Administration & Overhead** | $[calculated]     | [%]        |
| **TOTAL PROGRAM BUDGET**         | **$[calculated]** | **100%**   |

---

## 1. Personnel Costs

Direct staff costs for program coordination, project management, and professional roles.

| Line Item              | Role/Description                              | Unit    | Quantity                          | Rate/Unit         | Subtotal      |
| ---------------------- | --------------------------------------------- | ------- | --------------------------------- | ----------------- | ------------- |
| Program Coordinator    | FTE allocation for overall program management | Month   | [e.g., 0.6 FTE × 12 months = 7.2] | $[monthly rate]   | $[Qty × Rate] |
| Project Officer        | Program delivery, stakeholder liaison         | Month   | [e.g., 0.4 FTE × 12]              | $[monthly rate]   | $[Qty × Rate] |
| Clinical Supervision   | For peer workers (mandatory)                  | Session | [e.g., monthly × 12]              | $[hourly × hours] | $[Qty × Rate] |
| Evaluation Specialist  | Data analysis, report writing                 | Day     | [e.g., 10 days]                   | $[day rate]       | $[Qty × Rate] |
| **PERSONNEL SUBTOTAL** |                                               |         |                                   |                   | **$[sum]**    |

**Excel Formula for Subtotal**: `=SUM(E2:E5)` (adjust row numbers as needed)

---

## 2. Peer Remuneration

Fair payment for people with lived experience contributing expertise and labor.

| Line Item                           | Description                            | Unit       | Quantity                       | Rate/Unit | Subtotal      |
| ----------------------------------- | -------------------------------------- | ---------- | ------------------------------ | --------- | ------------- |
| Peer Workers - Session Facilitation | Delivery of program sessions           | Session    | [e.g., 24 sessions]            | $300      | $[Qty × 300]  |
| Peer Workers - Co-Design            | Program design workshops               | Workshop   | [e.g., 4 workshops]            | $300      | $[Qty × 300]  |
| Consumer Advisory Group             | Quarterly advisory meetings            | Meeting    | [e.g., 4 meetings × 6 members] | $300      | $[Qty × 300]  |
| Peer Researchers                    | Data collection, interviews            | Day        | [e.g., 5 days]                 | $300      | $[Qty × 300]  |
| Storytelling/Advocacy               | Lived experience representation        | Event      | [e.g., 3 events]               | $300      | $[Qty × 300]  |
| Travel Time (if >1 hour)            | Compensation for travel to/from venues | Occurrence | [number]                       | $[rate]   | $[Qty × Rate] |
| **PEER REMUNERATION SUBTOTAL**      |                                        |            |                                |           | **$[sum]**    |

**NUAA Standard**: $300 per structured session/meeting (adjust for local award rates and funding constraints)
**Excel Formula**: `=SUM(E2:E7)`

---

## 3. Operations

Venue, materials, equipment, and program delivery costs.

| Line Item               | Description                         | Unit    | Quantity            | Rate/Unit                 | Subtotal      |
| ----------------------- | ----------------------------------- | ------- | ------------------- | ------------------------- | ------------- |
| Venue Hire              | Accessible, culturally safe space   | Session | [e.g., 24 sessions] | $[hourly × hours]         | $[Qty × Rate] |
| Catering                | Food and refreshments for sessions  | Session | [e.g., 24 sessions] | $[per person × attendees] | $[Qty × Rate] |
| Program Materials       | Harm reduction resources, handouts  | Batch   | [e.g., 4 batches]   | $[cost]                   | $[Qty × Rate] |
| Naloxone Kits           | Overdose prevention                 | Kit     | [number]            | $[cost/kit]               | $[Qty × Rate] |
| Equipment               | Laptops, projector, flipcharts      | Item    | [list items]        | $[cost]                   | $[total]      |
| Communications          | Phone credit, internet for outreach | Month   | [months]            | $[monthly]                | $[Qty × Rate] |
| **OPERATIONS SUBTOTAL** |                                     |         |                     |                           | **$[sum]**    |

**Excel Formula**: `=SUM(E2:E7)`

---

## 4. Participant Support

Direct support reducing barriers to participation.

| Line Item                        | Description                                          | Unit           | Quantity                | Rate/Unit      | Subtotal      |
| -------------------------------- | ---------------------------------------------------- | -------------- | ----------------------- | -------------- | ------------- |
| Transport Vouchers               | Public transport to/from sessions                    | Person-Session | [e.g., 300 attendances] | $[per trip]    | $[Qty × Rate] |
| Childcare                        | On-site or voucher for childcare costs               | Session        | [sessions]              | $[per session] | $[Qty × Rate] |
| Participation Incentives         | Gift cards for survey completion                     | Person         | [number]                | $[amount]      | $[Qty × Rate] |
| Accessibility Support            | Interpreters, auslan, materials in alternate formats | Service        | [as needed]             | $[cost]        | $[total]      |
| **PARTICIPANT SUPPORT SUBTOTAL** |                                                      |                |                         |                | **$[sum]**    |

**Excel Formula**: `=SUM(E2:E5)`

---

## 5. Evaluation & Data

Tools, systems, and expertise for impact measurement and reporting.

| Line Item               | Description                           | Unit        | Quantity    | Rate/Unit  | Subtotal      |
| ----------------------- | ------------------------------------- | ----------- | ----------- | ---------- | ------------- |
| Survey Tools            | SurveyMonkey, Qualtrics license       | Month       | [months]    | $[monthly] | $[Qty × Rate] |
| Data Management System  | Database, CRM for tracking            | Year        | [years]     | $[annual]  | $[Qty × Rate] |
| Ethics Approval         | University HREC application if needed | Application | [1]         | $[cost]    | $[total]      |
| Report Design           | Professional layout for final report  | Report      | [e.g., 1-2] | $[cost]    | $[Qty × Rate] |
| Data Security/Privacy   | Encrypted storage, compliance         | Year        | [years]     | $[annual]  | $[Qty × Rate] |
| **EVALUATION SUBTOTAL** |                                       |             |             |            | **$[sum]**    |

**Excel Formula**: `=SUM(E2:E6)`

---

## 6. Administration & Overhead

Organizational infrastructure supporting the program.

| Line Item                   | Description                                             | Unit    | Quantity    | Rate/Unit      | Subtotal      |
| --------------------------- | ------------------------------------------------------- | ------- | ----------- | -------------- | ------------- |
| Organizational Overhead     | Finance, HR, governance, facilities (% of direct costs) | Percent | [%]         | $[base amount] | $[% × base]   |
| Insurance                   | Public liability, professional indemnity                | Year    | [years]     | $[annual]      | $[Qty × Rate] |
| Accounting/Audit            | Financial reporting, compliance                         | Year    | [years]     | $[annual]      | $[Qty × Rate] |
| Legal                       | Contracts, agreements, risk review                      | Service | [as needed] | $[cost]        | $[total]      |
| **ADMINISTRATION SUBTOTAL** |                                                         |         |             |                | **$[sum]**    |

**Excel Formula**: `=SUM(E2:E5)`
**Overhead Formula**: `=(sum of categories 1-5) * [percentage]/100`

---

## Budget Assumptions

Document all assumptions for transparency and funder confidence.

### Remuneration Rates

- **Peer workers**: $300/session (NUAA standard, in line with [relevant award/agreement])
- **Staff salaries**: Based on [award/classification], including [X]% superannuation
- **Travel time**: Compensated for journeys exceeding [threshold]

### Program Parameters

- **Session duration**: [hours] per session
- **Participant numbers**: [number] per session, [total] unique participants over program duration
- **Attendance rate**: Assumed [%] attendance rate ([justify based on similar programs])

### Operational Costs

- **Venue**: Based on quotes from [venue names], accessible and culturally appropriate
- **Catering**: $[amount] per person per session, includes dietary diversity
- **Materials**: Bulk purchase discounts applied where possible

### Contingency

- [X]% contingency built into [which categories] to manage unforeseen costs or scope adjustments

### Exchange Rates / Indexation

- If multi-year program: Assumed [X]% annual indexation for salaries and operational costs
- Rates current as of [date]

---

## Sensitivity Analysis

### Scenario 1: Reduced Funding (80% of requested budget)

**Adjustments**:

- Reduce program coordinator FTE from [X] to [Y] (e.g., 0.6 to 0.4)
- Decrease session count from [X] to [Y] sessions
- Maintain peer remuneration rate ($300/session - non-negotiable)
- Reduce participant support budget by [X]%
- Scale back evaluation to essential indicators only

| Category            | Original Budget | Reduced Budget (80%) | Notes                           |
| ------------------- | --------------- | -------------------- | ------------------------------- |
| Personnel           | $[amount]       | $[80% amount]        | Reduced FTE                     |
| Peer Remuneration   | $[amount]       | $[adjusted]          | Fewer sessions, rate maintained |
| Operations          | $[amount]       | $[80% amount]        | Smaller scale                   |
| Participant Support | $[amount]       | $[80% amount]        | Prioritize transport            |
| Evaluation          | $[amount]       | $[80% amount]        | Core indicators only            |
| Administration      | $[amount]       | $[80% amount]        | Proportional reduction          |
| **TOTAL**           | **$[original]** | **$[80% original]**  |                                 |

**Impact on Outcomes**: [Describe which outcomes may be reduced or delayed]

---

### Scenario 2: Expanded Funding (120% of requested budget)

**Enhancements**:

- Increase session frequency or add additional cohort
- Extend geographic reach to [additional area]
- Add [specific enhancement, e.g., advanced training for peer workers]
- Strengthen evaluation with [additional methods/tools]

| Category            | Original Budget | Expanded Budget (120%) | Notes                        |
| ------------------- | --------------- | ---------------------- | ---------------------------- |
| Personnel           | $[amount]       | $[120% amount]         | Additional project support   |
| Peer Remuneration   | $[amount]       | $[increased]           | More sessions or wider reach |
| Operations          | $[amount]       | $[120% amount]         | Additional venues/materials  |
| Participant Support | $[amount]       | $[120% amount]         | Enhanced support services    |
| Evaluation          | $[amount]       | $[120% amount]         | Longitudinal follow-up       |
| Administration      | $[amount]       | $[120% amount]         | Proportional increase        |
| **TOTAL**           | **$[original]** | **$[120% original]**   |                              |

**Impact on Outcomes**: [Describe enhanced outcomes or accelerated timeline]

---

## Export Guidance

### For Excel Spreadsheet

1. Copy this entire document to Excel
2. Apply formulas to "Subtotal" columns:
   - Cell E2 in each table: `=C2*D2`
   - Drag formula down for all rows
   - Bottom of each table: `=SUM(E2:E[last row])`
3. Budget Summary "Amount" cells link to table subtotals:
   - `='1. Personnel'!E[last row]`
   - Repeat for each category
4. "% of Total" column: `=B2/$B$7*100` (adjust for your summary row)
5. Format currency columns as currency ($)

### For Word Proposals

1. Copy tables directly from Markdown or Excel
2. Ensure consistent formatting (Arial 11pt or similar)
3. Include "Budget Assumptions" as a separate section
4. Reference sensitivity analysis in narrative: "See Appendix B: Budget Sensitivity"

### For SharePoint / Internal Planning

1. Save this file as `[program-name]-budget-[version].md` in program folder
2. Link from main `program-design.md`
3. Update VERSION in front matter with each revision
4. Track changes in Version History section below

---

## Version History

| Version | Date   | Author | Changes                                      |
| ------- | ------ | ------ | -------------------------------------------- |
| 1.0     | [Date] | [Name] | Initial budget for [program]                 |
| 1.1     | [Date] | [Name] | Adjusted [specific change] based on [reason] |
| 2.0     | [Date] | [Name] | Major revision for [reason]                  |

---

## Quality Checklist

Before finalizing your budget, check:

- [ ] All line items aligned with program design logic model
- [ ] Peer remuneration rate meets or exceeds $300/session standard
- [ ] Total budget realistic for proposed scope and timeline
- [ ] Assumptions documented and justified
- [ ] Overhead/admin percentage appropriate for organizational context (typically 10-20%)
- [ ] Sensitivity analysis addresses funder's likely questions
- [ ] All calculations verified (recommend double-check in Excel)
- [ ] Budget summary percentages add to 100%
- [ ] Costs compared to similar programs (reasonable range?)
- [ ] Culturally safe elements budgeted (e.g., interpreters, accessible venues)
- [ ] Evaluation budget sufficient for proposed impact framework
- [ ] Version number and date updated

---

## Integration with Other NUAA-Kit Artifacts

- **program-design.md**: Budget must align with program activities in logic model
- **proposal.md**: Budget summary table embeds into Section 5 (Budget)
- **impact-framework.md**: Evaluation costs must support indicator data collection
- **logic-model.md**: Inputs section lists financial resources (this budget)

---

## Tips for Funder Confidence

1. **Transparency**: Show your work. Funders trust budgets that explain assumptions clearly.
2. **Alignment**: Every budget line should trace back to the program design.
3. **Realism**: Avoid both overestimation (looks like padding) and underestimation (raises viability concerns).
4. **Peer Equity**: Never compromise peer remuneration to fit a budget. Adjust scope instead.
5. **Flexibility**: Sensitivity analysis demonstrates you've thought through risks.
6. **Evidence**: Reference similar programs, market rates, quotes from vendors.

---

**NUAA Principle Reminder**: Fair remuneration for peer expertise is non-negotiable. If budget constraints threaten peer payment standards, reduce program scope or decline the funding opportunity.
