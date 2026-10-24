# Findings
- Baseline main 4942aed, origin https://github.com/scenariofour/warehouse-lab.git; no tracked edits.
- Untracked discovery reports, two scripts, and discovery evidence predate this work; preserve bytes.
- Original discovery uses explicit inferred customer half-size mapping and one encoded cell per modeled unit; repeated and zero-quantity source records retained.
- The five requested findings are interpretation limits or observed differences, not confirmed operational failures.
- Reviewed source schemas and production normalization, Data Card, Model Card, experiment credibility, scenario/proxy feasibility, discovery report/brief and reproducibility packet. No authoritative support for deletion, quantity correction or real service-failure classification.
- jsonschema is unavailable; the contract uses a documented validator for the exact JSON Schema subset in use, with explicit cross-field tests and no new dependency.
- Official Tableau documentation supports logical relationships to preserve table grains; overlap still requires explicit measure guards. Actual Tableau workbook rendering remains untested.
- Official Microsoft inventory on-hand/status/journal documentation and GS1 traceability guidance support proposed exception mechanisms, not universal thresholds or current warehouse findings. One direct GS1 overview open returned an internal web error; search and the standard page supplied the cited conceptual evidence. No external data were ingested.
