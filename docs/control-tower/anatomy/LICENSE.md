# Attribution and reusable assets

The constellation's node layout, curves, diamond/circle/square vocabulary, editorial composition and static SVG were created for this redesign. No artwork, screenshots or dashboard assets were copied from the inspiration dashboards. The screenshots in `review/` are actual renders of this repository's HTML prototype.

## Original assets and documentation

The newly created `assets/constellation-overview.svg`, original visual composition, accompanying documentation and prototype screenshots may be reused under **Creative Commons Attribution 4.0 International** ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)). Attribute “Warehouse Lab / scenariofour — The Anatomy of a Decision” and indicate changes. This license covers these new materials only, not the whole repository or third-party datasets/fonts.

The SVG is a standalone, editable overview with title/description semantics. The live experience uses native SVG geometry from the same model. Do not use the static network image as a background under the live Tableau graph: it would draw every relationship twice.

## Code in this implementation

The new generator, HTML/CSS/JS prototype and constellation-specific tests are offered under the MIT License:

Copyright (c) 2026 Warehouse Lab contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Data and typography

Underlying warehouse data: Rodrigo Furlan de Assis, *Order Picking Dataset*, Mendeley Data v1, [DOI 10.17632/pf2w725pw3.1](https://doi.org/10.17632/pf2w725pw3.1), CC BY 4.0, as recorded in the existing public extract manifests. The new CSVs transform registered public evidence into presentation geometry, keeping source attribution and AI-proposed interpretation labels. They make no new operational observations.

The prototype references the repository's existing **DM Sans** font files and their [SIL Open Font License](../../../public/fonts/dmsans-OFL.txt). Georgia is a system font, not bundled here. No newly downloaded or proprietary fonts are redistributed. Tableau font rendering must be checked independently; the authoring guide supplies Arial/Georgia fallbacks.

## Design research continuity

The [previous M5 design brief](../CONTROL_TOWER_DESIGN_BRIEF.md) preserves the original inspiration study and its links: Mila Kholodii's *Amazon Sales Overview*, La'Princia Mance's *Supply Chain Performance & Vendor Operations*, Hue Vuong's *Hospital ER Operation*, and Karen Biltcliffe's *Northstar Logistics*. Those references informed readable framing, restrained color and analytical hierarchy. This redesign replaces the KPI/matrix composition with a new evidence constellation, using its own coordinates and curves. No supplier metrics, historical sparklines, financial results or operational performance claims were imported from the examples.
