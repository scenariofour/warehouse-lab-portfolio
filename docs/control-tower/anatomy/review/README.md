# Review evidence

## Preserved HTML prototype evidence · October 24, 2026

These are actual local HTML browser screenshots, not generated mockups or Tableau captures:

- `desktop-1600.png`: 1600×1000, default DQ-EXP-001.
- `desktop-1440.png`: 1440×900, same selection.
- `desktop-reconciliation.png`: 1600×1000, DQ-RECON-001.
- `narrow.png`: 390×844 after selecting DQ-LAYOUT-001 and scrolling to the selector. The graph pans inside its own frame above the panel.

Automated review commands (repository root):

```sh
python3 -B -m unittest tests/test_constellation.py
npx playwright test -c tests/constellation-browser/playwright.config.ts
python3 -B -m unittest discover -s tests -p 'test_dq_*.py'
python3 -B -m unittest discover -s tests -p 'test_data_pipeline.py'
npm test
npm run build
```

The browser suite regenerates these screenshots with reduced motion enabled so captures show settled selection styles. It checks every registered issue's selected edges/endpoints and exact context, both dual-role pairs through the data contract, actual role display, hover restoration, Enter/Space selection, reset, no JavaScript errors, desktop focal-panel area ≥55%, narrow-page overflow, and direct offline file opening. The area measure is the constellation **panel**, including its embedded legend; it is not a claim that colored pixels fill 55% of the screen.

The Python suite checks the independent geometry midpoint/endpoints, counts, role-preserving pair coverage, source immutability, reproducibility, public CSV guards and checked-in export freshness. See [validation.json](validation.json) for measured local results. At that historical prototype review, authentication prevented testing a real Tableau authoring canvas; no workbook had yet been authored by that task. A manually authored Tableau dashboard was subsequently published. Detailed evidence is in [CAPABILITIES.md](../CAPABILITIES.md).

Manual visual review: inspect both desktop captures for separation of source/question/category marks, readable selected paths, contextual dimming, full next-evidence text, and restrained nonanimated emphasis. Review the reconciliation state as a different neighborhood. The earlier mockup and all analytical sources remain versioned intact.

## Published Tableau evidence · October 25, 2026

- [tableau-public-default.png](tableau-public-default.png): actual signed-out published dashboard, `pIssue=DQ-EXP-001`.
- [tableau-public-reconciliation.png](tableau-public-reconciliation.png): same live view, `pIssue=DQ-RECON-001`.
- [published-validation.json](published-validation.json): dated observations, comparisons and capture hashes. Original [validation.json](validation.json) is preserved as the prototype-era record.

Captures are browser screenshots of Tableau's visualization iframe, including its toolbar, with no retouching or mockup generation. See [PUBLISHED.md](../PUBLISHED.md) for the exact URL, method, confirmed behavior and remaining QA. Parameter-value changes and issue-click Parameter Actions are separate checks.
