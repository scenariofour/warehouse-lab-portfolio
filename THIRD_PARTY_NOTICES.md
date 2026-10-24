# Data attribution and third-party notices

## Research dataset and adaptations

Creator: Rodrigo Furlan de Assis. Title: *Order Picking Dataset from a Warehouse of a Footwear Manufacturing Company*. Mendeley Data, version 1, published December 24, 2024. DOI: [10.17632/pf2w725pw3.1](https://doi.org/10.17632/pf2w725pw3.1). [Original publication](https://data.mendeley.com/datasets/pf2w725pw3/1). License: [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) ([legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en)).

The 21 files in `data/raw/` are byte-identical to the publisher manifest. The manifest preserves publisher metadata and attribution. The publication describes anonymization and randomization; Warehouse Lab does not identify the underlying company, customers or operators, or attempt reidentification. Coded source identifiers are research identifiers, not a private WMS connection.

Warehouse Lab adaptations include CSV parsing, whitespace and numeric normalization, inferred half-size mappings, wave/order grouping, source-row lineage, derived geometry and routing, issue/metric aggregation, alternative interpretation calculations, and stable domain-separated pseudonyms in advanced Tableau CSVs. One carton per storage cell, spatial scaling and robot parameters are modeling assumptions. See the [data audit](docs/data-audit.md), [advanced dictionary](docs/data-quality/advanced/DATA_DICTIONARY.md) and [source hashes](data/manifest.json).

CC BY 4.0 permits sharing and adaptation, including commercially, subject to attribution. Retain the creator and supplied notices, link the source and license, indicate changes and earlier modifications, and do not imply endorsement or impose additional legal/technical restrictions on licensed material. The license supplies no warranties and does not waive privacy, publicity, moral or unrelated third-party rights. No separate third-party restriction was identified in the reviewed dataset notices. The original CAD file is preserved from the public publisher release; Warehouse Lab does not claim to have decoded or surveyed it.

## Application dependencies and fonts

- Three.js: MIT, copyright its authors. Installed license: `node_modules/three/LICENSE`.
- Lucide: ISC for code; portions of icon designs retain the MIT Feather attribution. Complete installed notice: `node_modules/lucide/LICENSE`.
- DM Sans and Manrope: SIL Open Font License 1.1. Bundled copies: [DM Sans notice](public/fonts/dmsans-OFL.txt), [Manrope notice](public/fonts/manrope-OFL.txt). Fonts are unmodified; Vite may give bundled assets hashed filenames.
- Vite, TypeScript, Playwright and other build/test packages retain the licenses supplied by their respective packages. Versions are pinned by `package-lock.json`; they are installed through npm, not vendored into source.

The production artifact includes dependency notices as `THIRD_PARTY_NOTICES.txt`, alongside font licenses. The 3D warehouse preview is a screenshot of this application's actual render. Tableau workbooks are linked to their interactive originals; no remote preview image is redistributed. Tableau trademarks and service assets belong to their respective owners. No `.twb`/`.twbx` is distributed here.

No new license has been assigned to the owner's original application code or documentation by this release.
