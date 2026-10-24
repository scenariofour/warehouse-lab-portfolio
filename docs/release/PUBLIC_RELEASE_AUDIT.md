# Public-release audit

Reviewed October 23, 2026. **Original repository publication is blocked by historical identity metadata; the owner authorized a separate clean public repository, `scenariofour/warehouse-lab-portfolio`.** No visibility change, history rewrite, force-push or deletion has been performed. The clean snapshot uses fresh history and GitHub no-reply commit metadata. Original development history remains private.

## Repository and history scope

The authenticated GitHub account has ADMIN permission. Remote enumeration found `main` at `4942aedb7421fc8aeb5a87ed35f021654d12e708` and `codex/data-quality-foundation` at `9204da2bceec575c5d76d831e4b30cbb48f46bd0`, no tags, no pull-request refs, no issues, no releases, zero Actions runs and zero Actions artifacts. The 12 reachable commits contain 272 unique blobs and 103 trees. Both remote branches and all reachable versions were inspected, rather than only the current checkout. The separate release branch fast-forwarded the ten development commits without discarding the existing Tableau learning tree. Untracked Discovery scripts, reports and evidence in the owner's checkout are outside the release and remain untouched.

Git history contains a private academic email in commit author/committer records. Two committed regression logs contain a local username and absolute workspace path. These are **privacy blockers for publishing that history** under the owner's latest preference. This report deliberately does not repeat those values. Removing current files would not erase historical versions. No credential rotation is indicated by these identity findings.

## Secrets, configuration and artifacts

Gitleaks v8.30.1 scanned all 12 commits (approximately 76.10 MB) and returned three `generic-api-key` candidates. All three are the same SHA-256 digest recorded for `normalization_tokens.csv`, in design-review, validation and integrity-baseline JSON. Each equals the independently calculated file checksum; these are documented false positives, not service credentials. No candidates were suppressed before review.

A separate all-object scan checked commits/blobs for credential formats, private keys, email addresses, local paths and private-network URLs. No actual secret, connection string, `.env`, credential store or private service was found. Localhost URLs in Playwright, the former README and the publisher notebook are development/Colab examples. The notebook's metadata has generic Colab/kernel fields and four plot outputs; no account credential was found. Historical test traces and JSON evidence were reviewed as well as source code. Generated JSON/CSV tables contain public research data and derived metrics, not private WMS exports.

## Dataset and privacy review

The [publisher's version-1 page](https://data.mendeley.com/datasets/pf2w725pw3/1) identifies Rodrigo Furlan de Assis, publication December 24, 2024, DOI `10.17632/pf2w725pw3.1` and CC BY 4.0. It states anonymization and randomization were applied. All 21 raw files match the pinned publisher SHA-256 values. Schema/value checks found 588 coded customer IDs; customer operators (24 distinct) and picking operators (22 distinct) all use `Operator_<number>`. No customer/operator personal names, contact addresses or private credentials were found in those fields. Published order IDs, dates and geometry remain research records; no reidentification is attempted.

| Path | Review and disposition |
|---|---|
| `data/raw/` | CSV schemas/coded identifiers, notebook source/metadata/outputs, SVG links and PDF metadata reviewed. All originals retained. DWG is byte-identical to the publisher artifact; printable strings scanned, but compressed CAD entities were not decoded. No claim of exhaustive CAD semantic inspection. It adds no locally generated CAD metadata. |
| `public/data/` | Normalized geometry, demand and allocations traced to raw data. No credential/configuration data. These files intentionally ship in the static site. |
| `docs/evidence/` | Research/governance logs, snapshots and regression artifacts. Two historical logs expose local paths; public snapshot must use explicitly labeled redacted copies. Original evidence remains private. |
| `docs/data-quality/tableau/internal/` | Detailed source identifiers, metrics and research lineage derived from the same licensed public source. No secrets found. Retained for reproducibility; not included in website artifact or linked as public Tableau input. |
| `docs/data-quality/advanced/public/` | Fourteen allowlisted, typed CSVs with pseudonymized analytical identifiers. Existing independent verifier and manifest establish computational provenance; pseudonyms are not an assertion of irreversible anonymization. |
| `docs/control-tower/` | Educational design proposal, embedded research metrics and concept screenshots. Kept as historical design work, not represented as a shipped app feature. |
| `public/fonts/` | DM Sans/Manrope with supplied SIL OFL notices. |

PDF metadata identifies Matplotlib/Inkscape/Cairo, with no custom metadata, scripts, encryption or forms. Extracted PDF text is empty. SVG external URLs are standard XML/RDF/Creative Commons/Matplotlib/Inkscape namespaces; no script or onload handler was found. No separate third-party restriction was identified in source notices. The unread compressed structure of the publisher DWG is a disclosed technical limit, not a claim to have inspected its geometry. Raw files are redistributed under the publisher's explicit dataset license and are not silently treated as original project assets.

## Redistribution and attribution

[CC BY 4.0 legal code, sections 2–3](https://creativecommons.org/licenses/by/4.0/legalcode.en), permits reproduction and adaptations. Sharing requires creator/supplied notices, source/license links, modification notices, no implied endorsement and no added legal or effective technical restrictions on licensed material. Other privacy/publicity/third-party rights and lack of warranties still apply. [THIRD_PARTY_NOTICES](../../THIRD_PARTY_NOTICES.md) records title/creator/version/DOI/license and transformations. Font notices remain bundled; production builds copy complete Three.js/Lucide license notices. Original application code has no newly assigned reuse license.

## Tableau publication review

Signed-out browser inspection loaded Data Quality & Decision Intelligence, Dashboard 02, Dashboard 03 and the B04 tab/link. Dashboard 02's exact permalink was read from Share after selecting the published tab: `WarehouseLabOperationsDecisionStudio/Dashboard02NormalizationInterpretationLab2`. Published titles and observed worksheet roles are linked in the [showcase](../tableau/README.md). The preview URL from Tableau's own embed code returned HTTP 404; the broken image was removed. A workbook download was offered but no inspectable file was returned by the attempt; **no workbook or packaged data was committed**. Uploaded-extract identity and hidden formula/action QA remain unverified. No publication or workbook editing action was taken.

## Safest remediation and publication gate

1. Preserve this original private repository, all branches, commits and evidence. Do not publish it or force-push.
2. Export the reviewed release tree into a separate repository with fresh history. Do not copy `.git`, scratch outputs, untracked Discovery work or Actions logs. Use the owner's GitHub no-reply email in new commits.
3. In the public snapshot only, replace absolute local paths in the two logs with `<local-workspace>`. Add an explicit redaction notice and record old/new hashes. Preserve original private logs and historical manifests; explain that old identity checks attest to the private original and are not a fresh public-snapshot PASS.
4. Scan all snapshot files and new Git objects again, including metadata, for private identity strings and credentials. Verify no old commit is reachable. The existing remote must remain private.
5. The owner chooses a new public repository name, or explicitly authorizes renaming the original private repository to free its current name. New public-repository creation, Pages enablement and anonymous verification then complete the release. Renaming the private original requires updating its local origin and accounting for old links; it is not assumed.

The owner chose the separate public repository on October 23, 2026. The clean snapshot privacy and secret checks passed. Hosted verification is recorded separately after deployment. This is a release-safety assessment, not an approval of model validity, real-world stock quantities, policy ranking or human governance gates.

## Clean public snapshot gate — PASS

The owner explicitly authorized `scenariofour/warehouse-lab-portfolio` while keeping the development repository private. The new repository was initialized independently and is not a fork. No original `.git` objects, branches, Actions logs or untracked Discovery files were copied. Every reachable new commit/blob and all release source files were checked for the private academic email, local username and absolute macOS home prefix; none remained. New commits use GitHub no-reply metadata. Two redacted log copies are documented in [PRIVACY_REDACTIONS.json](PRIVACY_REDACTIONS.json); original private evidence and historical hash manifests were not rewritten. Python bytecode caches are excluded because they may contain local paths.

Gitleaks on the snapshot again found only the same three reviewed file-checksum false positives. The original application data and analytical exports are unchanged, and no Tableau workbook package was added. Publication is authorized after these checks; the original repository must remain private. The private development branch was integrated into private main through merge PR #1 (`f67ea1b037e296e1ad0db5ddf20de216ea682cd0`), preserving the ten development commits and release commits.

## Maintenance publication safeguard

A later GitHub-generated merge introduced personal author metadata. The affected repository was made private, preserved under `warehouse-lab-portfolio-private-archive` with the owner’s authorization, and replaced by a separately initialized clean repository at the same public name. The replacement includes the floor depth-precision fix and rendering regression; old commit objects and PR refs are absent. New commits must use explicit no-reply identities for both author and committer. The original `warehouse-lab` remains private.
