# EVALS — Feishu Formatting (Stage 6)

Run after editing the Feishu doc, verifying with `--detail full`. **Blocking** must all pass.
This stage is largely mechanical compliance — every blocking item is a hard gate.

## Layout compliance

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| L1 | Heading levels correct | ✅ | h1 = post titles; h2 only Title/素材/Body/评论设计; no other headings |
| L2 | 素材 block preserved | ✅ | If a 素材 block existed, it survives intact (structure + content) |
| L3 | Metadata deleted | ✅ | No Post Type / Flair / Link Permissibility remnants |
| L4 | 评论设计 starts correctly | ✅ | `<h2>评论设计</h2>` present; Standalone + Trees merged under it |
| L5 | Tree labels removed | ✅ | No `Tree N`, no `Comment Trees`, no leftover h3 |
| L6 | Standalone converted | ✅ | `Standalone N` → `**User N**` |
| L7 | Usernames normalized | ✅ | All `u/xxx` → `User N`; `User X replies to User Y` in `<b>` |
| L8 | OP replies deleted | ✅ | No OP reply comments remain; other users' threads intact |
| L9 | No blockquote in comments | ⬜ | No `>`-prefixed comment lines |
| L10 | Empty paragraphs cleaned (comments) | ⬜ | No `<p></p>`/`<p> </p>` inside 评论设计 |
| L11 | Separators kept | ⬜ | `---`/`<hr/>` between threads preserved; body blank-line `<p> </p>` kept |

## Brand highlight

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| H1 | All brand variants highlighted | ✅ | Every case variant wrapped in `<span background-color="light-yellow">`; verified via `--detail full` |
| H2 | No false highlight | ✅ | No non-brand lookalike word highlighted |
| H3 | Coverage all blocks | ⬜ | Brand highlighted in body, comments, titles wherever it appears |

## Comment nativeness (final)

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| N1 | AI-tell comments removed | ⬜ | No over-structured / formal / review-like / customer-service comments |
| N2 | Native voice intact | ⬜ | Slang, anecdotes, light typos present; no Chinglish |
| N3 | Body/title text unchanged | ✅ | Stage 6 did NOT rewrite body/title wording |
| N4 | Resources preserved | ✅ | `<img>`/`<source>`/`<whiteboard>` blocks untouched |

## Verification (mandatory)

Re-read the doc with `--detail full` and confirm: L2, L3, H1, L8, N4 specifically — these
are the high-cost failures (lost 素材, leftover metadata, missing brand spans, OP replies,
destroyed resources).

## Failure → action

- Any blocking fail → fix the specific block and re-verify; do not mark done.
- Write `format_report.md`: blocks changed, blocks preserved, brand variants highlighted,
  OP replies removed count, `--detail full` verification result. Log verdict in manifest.

## Reviewer prompt (optional subagent)

"Read this Feishu post doc (full detail). Are only h1=titles and h2=Title/素材/Body/评论设计
present? Is the 素材 block intact and the Metadata block gone? Are all usernames User-N with
`User X replies to User Y`, no Tree labels, no OP replies, no blockquotes? Are all brand-word
case variants highlighted with light-yellow spans and no lookalike falsely highlighted? List
every violation."
