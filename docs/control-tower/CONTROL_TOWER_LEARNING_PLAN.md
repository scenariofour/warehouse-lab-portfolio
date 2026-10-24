# Learn Tableau by building M5

Proposed learning sequence after design approval. Prior knowledge and worksheet recipes are already indexed in the [existing learning notebook](../data-quality/advanced/tableau-workbook/LEARNING_INDEX.md); do not create a second B/C tutorial set.

| Build component | Tableau concept to learn | Explain or demonstrate before moving on |
|---|---|---|
| KPI cards T01–T04 | Aggregate calculations, MIN versus SUM, COUNTD, metric-key filters, null formatting | Reproduce all three fractions; explain why records, units and references cannot share a total. Select two metrics and show the guard suppressing the share |
| Dependency map T05 + lineage T09 | Logical relationships, one-to-many grain, discrete headers, Text Marks, aggregate role labels, tooltip detail | Find 35 role records in 33 cells; show the two A+C cells without dropping a role or doubling an affected count |
| Decision exposure T06 | Categorical bars, COUNTD, manual aliases and sort order | Explain why 5/4/2/2/1 partition questions but cannot quantify operational risk |
| Selected evidence T07/T08 | Workbook parameters versus filters, calculated keep/highlight fields across sources, ATTR and empty states | Select each of 14 issues, identify its smallest request and switch to an unmeasured physical metric without displaying zero |
| Sensitivity T10 | Measure Names/Values, one-mark grain, fixed versus changing denominators | Explain why 12,985 / 215,460 is a different assumption from 13,003 / 228,195, not an improvement or time trend |
| Priorities and controls T11/T12 | Custom sort, local versus global filters, categorical state labels | Keep the curated queue honest: editorial ordering, no risk score. Explain why PASS_DESCRIPTIVE does not mean protocol approved |
| Investigation navigation | Action direction, Selected Fields mapping, clearing policy; manual fallback when menus are unavailable | Open the existing investigation, state that its scope resets independently, and demonstrate a manual route when custom actions are absent |
| Final composition and review | Tiled containers, padding, fixed sizing, dashboard scope, keyboard/tooltips, saved state | Run the three brief journeys, verify global KPIs survive selections, and record what was actually tested in Public |

Keep a small learning log when authoring: `component | question | attempted setting | observed behavior | reason/fix | screenshot | remaining uncertainty`. Write first-person learning takeaways only after doing the work. Repository validation and HTML clicks do not count as Tableau skills already demonstrated.

Suggested sessions: metrics and grains; relationships and dependencies; selection and decision explanation; composition and QA. Session length is a personal planning choice, not an estimated completion commitment. Stop on unexplained totals or unavailable editor capabilities and return to the [feasibility plan](CONTROL_TOWER_TABLEAU_PLAN.md).
