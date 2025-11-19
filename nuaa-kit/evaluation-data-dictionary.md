---
status: draft
version: 0.1.0
audience: internal
purpose: Reference mapping of NUAA evaluation indicators to data collection spec
---

# Evaluation Data Dictionary (Draft)

This dictionary standardizes indicator variable names, types, allowed values, collection frequency, and sources. Use it when configuring surveys, spreadsheets, dashboards, and analysis scripts.

## Conventions

- Variable names: snake_case, lowercase
- Boolean: use 0/1 (integer) unless a scale is required
- Dates: ISO-8601 (YYYY-MM-DD)
- Timestamps: ISO-8601 with timezone when needed
- Categorical fields: lowercase tokens (document enumerations below)

## Core Reference Tables

### Program Metadata

| Variable       | Type   | Allowed / Format            | Description                   | Source            | Frequency        |
| -------------- | ------ | --------------------------- | ----------------------------- | ----------------- | ---------------- |
| program_id     | string | `[a-z0-9_-]+`               | Unique program key            | Registry / manual | Once             |
| program_name   | string | free text                   | Human-readable program title  | Registry          | Once             |
| cohort_id      | string | `[a-z0-9_-]+`               | Cohort or batch identifier    | Admin log         | Per cohort       |
| participant_id | string | pseudonymous                | Unique pseudonymous ID (hash) | Intake system     | Once             |
| consent_status | enum   | granted, withdrawn, pending | Current consent state         | Consent form      | Update on change |
| consent_date   | date   | YYYY-MM-DD                  | Date consent granted          | Consent form      | Once             |

### Process & Implementation

| Variable                   | Type         | Allowed / Format                                   | Description                                   | Source           | Frequency   |
| -------------------------- | ------------ | -------------------------------------------------- | --------------------------------------------- | ---------------- | ----------- |
| session_id                 | string       | `[a-z0-9_-]+`                                      | Unique session identifier                     | Session log      | Per session |
| session_date               | date         |                                                    | Date held                                     | Session log      | Per session |
| session_type               | enum         | workshop, support_group, training, outreach, other | Session format                                | Session log      | Per session |
| facilitator_role           | enum         | peer_worker, staff, partner, mixed                 | Leading role composition                      | Session log      | Per session |
| attendance_count           | integer      | >=0                                                | Total attendees (unique)                      | Sign-in sheet    | Per session |
| attendance_participant_ids | string(list) | comma-separated                                    | Participant IDs present                       | Sign-in sheet    | Per session |
| fidelity_percent           | integer      | 0–100                                              | % of planned activity elements delivered      | Staff checklist  | Per session |
| retention_flag             | boolean(int) | 0/1                                                | Participant retained at milestone (e.g., end) | Derived          | Milestones  |
| referral_made_count        | integer      | >=0                                                | Referrals initiated                           | Referral log     | Weekly      |
| referral_completed_count   | integer      | >=0                                                | Referrals resulting in successful connection  | Follow-up log    | Weekly      |
| partnerships_active        | integer      | >=0                                                | Active partner orgs this period               | Partner register | Monthly     |
| budget_spent_amount        | decimal      | >=0                                                | Cumulative spend local currency               | Finance export   | Monthly     |
| budget_variance_percent    | decimal      | +/-                                                | (Actual - Planned)/Planned \* 100             | Finance export   | Monthly     |

### Output Indicators

| Variable                    | Type    | Allowed / Format | Description                           | Source           | Frequency     |
| --------------------------- | ------- | ---------------- | ------------------------------------- | ---------------- | ------------- |
| sessions_delivered          | integer | >=0              | Count of sessions delivered in period | Aggregation      | Weekly/Report |
| participants_engaged_unique | integer | >=0              | Unique participants engaged to date   | Aggregation      | Weekly        |
| peer_hours                  | decimal | >=0              | Peer worker hours logged              | Timesheets       | Monthly       |
| resources_distributed       | integer | >=0              | Physical / digital resource count     | Distribution log | Weekly        |
| referrals_made              | integer | >=0              | Total referrals initiated             | Referral log     | Weekly        |
| referrals_completed         | integer | >=0              | Successful referral completions       | Follow-up        | Weekly        |

### Short-Term Outcomes (0–3 months)

| Variable                | Type         | Allowed / Format | Description                             | Source          | Frequency |
| ----------------------- | ------------ | ---------------- | --------------------------------------- | --------------- | --------- |
| knowledge_score_pre     | integer      | 0–100            | Baseline composite score                | Survey (pre)    | Baseline  |
| knowledge_score_post    | integer      | 0–100            | Post composite score                    | Survey (post)   | End       |
| knowledge_gain_percent  | decimal      |                  | ((post-pre)/pre)\*100                   | Derived         | End       |
| confidence_score_pre    | integer      | 1–5              | Self-rated confidence baseline          | Survey          | Baseline  |
| confidence_score_post   | integer      | 1–5              | Self-rated confidence post              | Survey          | End       |
| confidence_delta        | integer      | -4..4            | Change in confidence                    | Derived         | End       |
| awareness_services_flag | boolean(int) | 0/1              | Aware of key services post              | Survey          | End       |
| stigma_self_score_pre   | integer      | scale-specific   | Internalized stigma baseline            | Validated scale | Baseline  |
| stigma_self_score_post  | integer      | scale-specific   | Internalized stigma post                | Validated scale | End       |
| connection_peer_count   | integer      | >=0              | # peer connections participant can name | Survey          | End       |
| satisfaction_rating     | integer      | 1–5              | Overall satisfaction                    | Exit survey     | End       |

### Medium-Term Outcomes (3–12 months)

| Variable                     | Type         | Allowed / Format | Description                         | Source          | Frequency      |
| ---------------------------- | ------------ | ---------------- | ----------------------------------- | --------------- | -------------- |
| wellbeing_k10_score          | integer      | 10–50            | K10 distress score                  | Survey          | Baseline/3m/6m |
| wellbeing_k10_delta_3m       | integer      |                  | Change baseline→3m                  | Derived         | 3m             |
| service_access_regular       | boolean(int) | 0/1              | Accessing target services regularly | Survey          | 3m/6m          |
| behavior_change_adopted      | boolean(int) | 0/1              | Adopted target behavior/practice    | Survey          | 3m/6m          |
| peer_support_engaged         | boolean(int) | 0/1              | Giving/receiving peer support       | Survey          | 3m/6m          |
| empowerment_score            | integer      | scale-specific   | Empowerment metric                  | Validated scale | Baseline/6m    |
| participation_other_programs | boolean(int) | 0/1              | Joined other NUAA activities        | Admin           | 6m             |

### Long-Term Outcomes (12+ months)

| Variable               | Type         | Allowed / Format | Description                         | Source       | Frequency    |
| ---------------------- | ------------ | ---------------- | ----------------------------------- | ------------ | ------------ |
| health_self_rating     | integer      | 1–5              | Self-rated overall health           | Survey       | Baseline/12m |
| harm_indicator_value   | decimal      | program-specific | Quant value (e.g., risky incidents) | Survey / log | Baseline/12m |
| social_inclusion_score | integer      | scale-specific   | Inclusion metric                    | Scale        | Baseline/12m |
| leadership_role_flag   | boolean(int) | 0/1              | Took peer/advocacy role             | Tracking     | 12m          |
| sustained_change_flag  | boolean(int) | 0/1              | Maintained positive change since 6m | Follow-up    | 12m          |

### Impact (Community/System)

| Variable                     | Type    | Allowed / Format | Description                          | Source           | Frequency    |
| ---------------------------- | ------- | ---------------- | ------------------------------------ | ---------------- | ------------ |
| community_stigma_index       | decimal | standardized     | Community stigma index               | Community survey | Baseline/End |
| service_responsiveness_count | integer | >=0              | Services reporting improved practice | Partner survey   | End          |
| policy_citations_count       | integer | >=0              | Policy docs citing program/evidence  | Doc analysis     | Ongoing      |
| sector_presentations_count   | integer | >=0              | Presentations/public outputs         | Tracking log     | End          |
| continuation_funding_amount  | decimal | >=0              | Funding secured for continuation     | Finance          | End          |

### Equity & Participation

| Variable                  | Type         | Allowed / Format                | Description                      | Source      | Frequency  |
| ------------------------- | ------------ | ------------------------------- | -------------------------------- | ----------- | ---------- |
| subgroup_id               | string       | e.g., aboriginal, lgbtiq, rural | Participant subgroup label       | Self-report | Intake     |
| subgroup_outcome_gap_flag | boolean(int) | 0/1                             | Outcome gap vs overall threshold | Analysis    | Post-cycle |
| remuneration_total_amount | decimal      | >=0                             | Total remuneration paid to peers | Finance     | Quarterly  |
| peer_researcher_hours     | decimal      | >=0                             | Peer researcher labor hours      | Timesheets  | Monthly    |

### Qualitative Artifacts (Indexed)

| Variable                   | Type         | Allowed / Format           | Description                      | Source       | Frequency |
| -------------------------- | ------------ | -------------------------- | -------------------------------- | ------------ | --------- |
| story_id                   | string       | `[a-z0-9_-]+`              | Unique narrative/case identifier | Qual DB      | Per story |
| story_type                 | enum         | msc, case_study, interview | Narrative classification         | Qual DB      | Per story |
| story_theme_primary        | string       | controlled vocab           | Primary coded theme              | Qual coding  | Per story |
| quote_count                | integer      | >=0                        | Extracted quotes used            | Qual coding  | Per story |
| participant_validated_flag | boolean(int) | 0/1                        | Member checking done             | Qual process | Per story |

## Enumerations

| Enum             | Values                                             | Notes                           |
| ---------------- | -------------------------------------------------- | ------------------------------- |
| session_type     | workshop, support_group, training, outreach, other | Extend cautiously               |
| facilitator_role | peer_worker, staff, partner, mixed                 |                                 |
| consent_status   | granted, withdrawn, pending                        |                                 |
| story_type       | msc, case_study, interview                         | "msc" = Most Significant Change |

## Derived Field Formulas

| Field                   | Formula                                                                             | Notes                   |
| ----------------------- | ----------------------------------------------------------------------------------- | ----------------------- |
| knowledge_gain_percent  | (knowledge_score_post - knowledge_score_pre) / NULLIF(knowledge_score_pre,0) \* 100 | Guard divide by zero    |
| confidence_delta        | confidence_score_post - confidence_score_pre                                        |                         |
| wellbeing_k10_delta_3m  | wellbeing_k10_score(3m) - wellbeing_k10_score(baseline)                             | Negative is improvement |
| budget_variance_percent | (actual - planned)/planned \* 100                                                   | Sign shows direction    |

## Data Quality Rules

| Rule                                   | Severity | Action                |
| -------------------------------------- | -------- | --------------------- |
| knowledge_score_pre/post outside 0–100 | error    | Reject record         |
| Missing participant_id                 | error    | Reject row            |
| consent_status not in enum             | error    | Reject row            |
| session_date future > 30 days          | warn     | Flag for review       |
| wellbeing_k10_score outside 10–50      | warn     | Flag, allow with note |

## Privacy & Ethics Notes

- Pseudonymization: `participant_id` generated via salted hash, salt stored separately.
- Small subgroup suppression: if subgroup cell count <5, aggregate or suppress in reports.
- Data retention: raw identifiable intake forms retained per NUAA policy (not in analytics layer).

## Versioning

- Update `version` front matter when adding/removing indicators or changing definitions.
- Record changes in forthcoming `CHANGELOG.md` when created.

---

_End of draft dictionary — invite peer researcher review before marking status: final._
