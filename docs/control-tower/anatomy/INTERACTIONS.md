# Interaction contract

The unit of investigation is **one registered issue**. Default: DQ-EXP-001. Clear state: `__ALL__`, labeled “All registered associations.” The selected issue is a view state, not an approval or data correction.

| Trigger | HTML behavior | Native Tableau core / optional enhancement |
|---|---|---|
| Choose issue in selector | Persist selection; show all context; emphasize exactly its incident source curves and its one category curve | Required string `pIssue` parameter selects the matching precomputed focus slice |
| Click circular issue / Enter / Space | Same result as selector; `aria-pressed` updates | Optional Desktop-authored parameter action; manual parameter selector always remains available |
| View all | All 47 curves and 30 nodes active; panel explains how to investigate | Set pIssue to `__ALL__`; no dependency on action-clearing behavior |
| Hover/focus source | Temporary tooltip with full filename and registered issue-association count; highlight only that source's real incident curves | Core: native mark tooltip. Incident-curve hover parity is **not claimed**; no custom extension needed |
| Hover/focus issue | Full registered issue title and ID; incident curves emphasized temporarily | Core: native mark tooltip; persistent selection still uses parameter |
| Hover/focus category | Category and number of registered issue assignments; AI-proposed label | Core: native tooltip, with the same interpretation disclaimer |
| Pointer exit / blur / Escape | Remove temporary hover emphasis; selected issue stays unchanged | Core tooltip dismissal does not change pIssue |
| Expand evidence trail | Exact sources and role sets, preserving both roles on multi-role pairs | Optional separate role-grain table filtered by pIssue, no physical geometry join |
| Expand uncertainty / metrics | Existing residual uncertainty; individual metrics with their original units and denominators | Context text sheet + optional separate metric-key sheet; never aggregate across keys |

Selection algorithm: pick edges with `issue_id=selected_issue`; collect their endpoint node IDs. All other nodes and edges stay visible at a subdued, constant style. Source neighbors' *other* issues do not become selected. A selected decision category does not expand to all issues in that category. This prevents the visual from implying extra evidence relationships. At the default selection, exactly five evidence edges, one decision edge, five sources, one issue and one category are active.

Every issue's decision, alternatives and next evidence request are copied from the existing public decision extract. AFFECTED, CONTRIBUTING_POPULATION and DEFINITION_EVIDENCE appear as distinct textual roles in the trail. The line hue distinguishes evidence associations from proposed decision-category associations; line hue does **not** encode lineage role, confidence or severity. Both multi-role pairs use one curve each and retain two lineage rows in the bridge.

Context panel persistence is deliberate: hover never changes the investigation narrative. Source/category marks do not navigate to other apps or run data-changing actions. No URL action, publication, approval transition or simulator action occurs.

HTML accessibility: all nodes receive keyboard focus and full text labels, issue nodes support Enter/Space, native issue selector supplies an alternative to spatial navigation, skip link reaches the investigation, focus/selection rings are visible, and the panel has a polite live region. No continuous animation; brief styling transitions honor reduced-motion preferences. On mobile the chart pans internally while the selector and panel remain usable at full page width.

Tableau acceptance checks (publication now exists; see [dated verification and remaining QA](PUBLISHED.md)):

1. DQ-EXP-001: five evidence curves + one amber category curve; source filenames match the public lineage extract.
2. DQ-DUP-CUSTOMER and DQ-DUP-PICKING: one evidence curve each, **two** original roles each in the role table.
3. DQ-STOCK-001: preserve DEFINITION_EVIDENCE where registered; no blank count converted to an affected zero.
4. All 14 selector options reproduce their exact sources, category, decision narrative and next request.
5. `__ALL__`: 33 source–issue curves + 14 category curves, 30 nodes; no 35-curve misinterpretation.
6. Save/reopen and test the published view separately, including keyboard and tooltips. HTML browser tests do not certify Tableau behavior.
