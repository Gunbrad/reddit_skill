# Stage 6 — Feishu Formatting Report

Doc: https://my.feishu.cn/docx/GLVVdGqSUoHbk1xAw1ccx3Egnyh (revision 10)
Verified via `docs +fetch --detail full`.

## What changed
- Brand highlight: wrapped the one literal in-body brand mention `Enter's CLI` (post 9) in
  `<span background-color="light-yellow">Enter</span>` via `str_replace` (PowerShell). Verified the
  span is present in full-detail fetch (rendered rgba light-yellow).

## What was already compliant at authoring time (Stage 5 wrote to the standard)
- L1 Heading levels: exactly 10 `<h1>` (one per post), and `<h2>` only ∈ {Title, Body, 评论设计}.
  Verified counts: h1=10; h2 = 10×Title / 10×Body / 10×评论设计.
- L3 Metadata: no Post Type / Flair / Link Permissibility blocks (count 0).
- L4 评论设计: every post has `<h2>评论设计</h2>`; standalone + threads merged under it.
- L5 Tree labels: no `Tree N` / `Comment Trees` / `<h3>` (count 0).
- L7 Usernames: all comments use `User N` and `User X replies to User Y`; no `u/xxx` (count 0).
- L8 OP replies: no OP-reply comments present (the 2 "OP" substring hits are inside "OPA/Gatekeeper", a K8s tool — not labels).
- L11 Separators: `<hr/>` thread separators preserved between comment groups.

## What was preserved
- N3 Body/Title text unchanged by stage 6 (only the brand word got a span).
- N4 Resources: doc has no `<img>`/`<source>`/`<whiteboard>`/素材 blocks (all 10 are text posts, no images by design), so nothing to lose.

## Notes / residual (non-blocking)
- The doc `<title>` block "Enter Pro - 帖子 - 2026-06-27" can't carry an inline span (title block limitation); brand in the title is therefore not highlighted. All in-body brand mentions are.
- Comments deliberately keep brand indirect ("one platform whose backend is native PostgreSQL", "a thin publish CLI"), so there are very few literal brand tokens to highlight — by design for nativeness, consistent with red-line "vary narrative role / no feature dump".
- "Standalone:" lines aggregate short one-liner comments rather than numbered `Standalone N`; no `Standalone N` pattern exists, so L6 has nothing to convert.

## EVALS verdict
All blocking criteria (L1, L3, L4, L5, L7, L8, H1, H2, N3, N4) PASS. Stage 6 complete.
