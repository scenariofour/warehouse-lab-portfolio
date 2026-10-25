# Authoring capability evidence

Historical authoring check: **2026-10-24**. The observations below describe that signed-out web-authoring attempt, not the current publication state.

Update **2026-10-25**: the owner manually authored the dashboard in Tableau Desktop and published it. The signed-out viewer exposes CT01–CT07, the Line + Shape chart and `pIssue`. [Publication evidence and current QA](PUBLISHED.md) distinguish the verified viewer from web-authoring capabilities that remain untested. The local one-sheet draft is not the final published workbook.

## Actual UI observation

In the available in-app browser, opened Tableau Public Discover, opened **Create**, then selected **Web Authoring**. The browser redirected to Tableau's identity sign-in page with Email/Password fields. The session was signed out. Investigation stopped at that authentication boundary; no credentials were entered and no CSV, workbook or publication was created. Only the sanitized route/title is recorded here; OAuth state, nonce and authentication URLs are intentionally excluded.

| Capability | Actual Public web test in this session | Construction route / fallback |
|---|---|---|
| Reach Public Create → Web Authoring | **Observed**; redirected to sign-in | Sign in independently when authoring |
| Upload generated CSV, confirm field types | **Unverified**, editor inaccessible | Free Desktop Public: Text file connection; validate types before plotting |
| XY Line mark with discrete Path and edge Detail | **Unverified in Public UI**; Desktop technique documented | Desktop native Cartesian axes with ordered points; no spatial geometry required |
| Dual-axis Line + Shape, fixed synchronized/reversed Y | **Unverified in Public UI** | Desktop native dual axis; single worksheet avoids cross-sheet overlay dependency |
| String parameter control and calculated focus filter | Public included in official parameter documentation; **UI unverified** | Manual pIssue control is the core, actions optional |
| Create issue-click parameter action in web | **Unverified**; generic Cloud/Server web guidance is not evidence of Public parity | Free Desktop parameter action, then test published rendering; retain manual selector |
| Floating sizes, exact padding and transparent label overlay | **Unverified in Public UI** | Desktop fixed layout; tiled chart/panel alternative; optional label overlay omitted from core |
| Native tooltip behavior and parameter action on published Public view | **Unverified**; no workbook authored | Explicit save/reopen/publish acceptance checks in AUTHORING.md |
| Phone-specific layout | **Unverified** | Construct/test in Desktop; a fixed desktop dashboard may scroll on mobile |

The full native **Desktop** route is documented as an implementation recipe, not as a workbook completion claim. In particular, exact custom font rendering, label placement, hover parity, action dialogs and transparent layering still require authoring tests. No blanket claim that Public web authoring supports or forbids these operations is justified by this signed-out session.

## Primary documentation reviewed

- [Tableau Public FAQ](https://help.tableau.com/current/public/desktop/en-us/public_faq.htm): explicitly identifies free web authoring and free Desktop Public Edition as creation routes. Published workbooks are public. Supports the no-paid-feature path, not a test of these particular files.
- [Create Parameters](https://help.tableau.com/current/pro/desktop/en-us/parameters_create.htm): explicitly lists Tableau Public, documents string/list parameters and controls. The pIssue + Boolean focus filter follows this native model. UI execution is still pending.
- [Marks properties](https://help.tableau.com/current/pro/desktop/en-us/viewparts_marks_markproperties.htm): describes Line/Path mark properties. [Ordered origin/destination example](https://help.tableau.com/current/pro/desktop/en-us/maps_howto_origin_destination.htm) documents grouped, ordered path points and is scoped to Desktop. Our geometry uses ordinary XY axes, not geographic maps; no geographic interpretation is imported from that example.
- [Dashboard size and layout](https://help.tableau.com/current/pro/desktop/en-us/dashboards_organize_floatingandtiled.htm): fixed sizes, containers and floating/tiled construction. Applicability lists Cloud/Desktop/Server, so this is not proof of exact Public web controls. It points to Desktop for device-specific layouts.
- [Desktop/web editing comparison](https://help.tableau.com/current/pro/desktop/en-us/server_desktop_web_edit_differences.htm): useful general context, scoped to Cloud/Desktop/Server. Do not assume a listed server/web capability was observed in Tableau Public.
- [Parameter actions](https://help.tableau.com/current/pro/desktop/en-us/actions_parameters.htm): basis for the optional native action recipe; confirm the actual authoring menu and published result in the target environment.

## Historical reconstruction route

In a signed-in authoring session, import only the new public-safe scaffold into a **new, unpublished workbook**. First test Line/Path/Detail, then add the Shape axis, then pIssue. Record whether each action and layout menu exists and whether it survives save/reopen. If a control is absent, use the documented Desktop path or the manual parameter/tiled layout fallback. This paragraph records the original prototype task boundary. The subsequent publication is recorded separately; archive work does not modify the published dashboard.
