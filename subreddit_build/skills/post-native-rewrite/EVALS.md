# EVALS — Post Native Rewrite (Stage 6a) — the core de-AI / native system

Run by a SEPARATE evaluator worker (EVAL_WORKER_CONTRACT.md), per post, on
`06_optimized/native_posts.md`. The evaluator also reads the Stage 5 `handoff_packet.json` to
verify viral intent survived. **Blocking** must pass.
Threshold: all blocking pass AND de-AI total ≥ 85/100 (higher bar than other stages).

Three sub-systems here: (VP) viral-intent preserved, (A) de-AI/native Title+Body,
(B) comment-section nativeness. (Brand-safety, facts, images, subreddits, Feishu are scored in
6b/6c/6d, not here.)

---

## VP. Viral intent preserved (BLOCKING — vs Stage 5 handoff_packet.json)

The de-AI rewrite must not flatten the post into something safe but forgettable.

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| VP1 | Core hook kept | ✅ | The final title/body still carries `viral_intent.core_hook` (the counter-intuitive/tension angle), not a generic restatement |
| VP2 | Emotional trigger kept | ✅ | `viral_intent.emotional_trigger` is still felt; the feeling that drives upvote/share wasn't neutralized |
| VP3 | must_preserve details kept | ✅ | Every item in `viral_intent.must_preserve[]` (concrete scene, contrast, "not a tool pitch") is present |
| VP4 | Comment engine kept | ✅ | `viral_intent.comment_engine` survives — the post still invites the intended reply/debate |
| VP5 | Title pattern respected | ⬜ | Main or an alternate title follows `title_pattern_to_preserve` from heat evidence |

A post that passes A/B (reads native) but fails any VP1–VP4 is an overall FAIL: it was
de-AI'd at the cost of its breakout potential. Send back to a fresh rewrite worker.

---

## A. De-AI / Native — Title + Body

### A-Title

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| AT1 | Reads like a user, not an ad | ✅ | Sounds like a real poster venting/asking, not marketing copy |
| AT2 | No hype words | ✅ | No "revolutionary / game changer / finally solved / best / 完美 / 终结" |
| AT3 | One core pain | ⬜ | Title carries one real pain, not stuffed with multiple claims |
| AT4 | Allows mild frustration/confusion | ⬜ | A little 吐槽/困惑/求建议 tone is fine and preferred |
| AT5 | ≥3 alternate titles (备用标题) | ✅ | At least 3 备用标题 present; each passes AT1+AT2; varied angle, not restatements |

### A-Body (de-AI heuristics — each "AI tell" found = fail until removed)

| # | Criterion | Blocking | Pass / fail signal |
|---|-----------|:---:|----------------|
| AB1 | First-person lived narrative | ✅ | Tells a personal story; NOT a product requirements doc / feature list |
| AB2 | Not a checklist / 三段论 | ✅ | FAIL if it follows "痛点→分析→产品→CTA" or "First/Second/In conclusion" |
| AB3 | One closing question | ✅ | Ends on ONE core question; FAIL if 3-4 questions stacked at the end |
| AB4 | Keeps doubt / hedge | ✅ | Has at least one uncertainty ("maybe I'm overthinking", "not treating it as proven") |
| AB5 | No feature dump | ✅ | FAIL if it lists "A, B, C and D" of the product, or "solves X via Y technology" |
| AB6 | Allowed messiness | ⬜ | Slight repetition / colloquialism / informal flow present (real users aren't essays) |
| AB7 | No em-dash-heavy formal transitions | ⬜ | Not over-using written-style "—" transitions; no overly formal vocab (utilize/consequently) |
| AB8 | Concrete specifics over generic | ⬜ | Real details ("ate three weekends") beat vague claims |
| AB9 | No Chinglish | ✅ | Reads as native English; nothing translated-from-Chinese (conventions.md §4b) |
| AB10 | Native slang & spoken syntax | ⬜ | Slang ≤3/paragraph, natural; short/inverted/elliptical sentences; not forced |
| AB11 | Controlled typo rate 1-3% | ⬜ | Error-word rate 1-3%, native-style mistakes, none in data/technical lines, not clustered |

---

## B. Comment-section nativeness

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| B1 | 8-12 comments | ⬜ | Not a full script; roughly 8-12 |
| B2 | Mixed emotions | ✅ | Has 共鸣 + 怀疑 + 个人经验 + 替代方案 + 等评测/提醒风险; not all praising |
| B3 | No comment fully sells brand | ✅ | No single comment explains the brand's selling points end-to-end |
| B4 | Brand ≤1-2 mentions total | ✅ | Across the whole comment section |
| B5 | No off-topic rabbit holes | ⬜ | No threads drifting to lights/keyboards/desk-mats etc.; ≤1 short ambient aside |
| B6 | Native voice | ⬜ | Natural slang ≤3/comment, native-style typos rate 1-3%, no Chinglish, no client-reply tone (conventions.md §4b) |
| B7 | Real disagreement exists | ⬜ | Comments diverge/argue; not all agreeing with OP |
| B8 | No Chinglish | ✅ | No comment reads as translated-from-Chinese |

---

## Failure → action

- Any VP/A/B blocking fail → rewrite that post and re-score (fresh evaluator worker); do NOT hand off to 6b.
- VP1–VP4 fail → restore the lost hook/trigger/detail/comment-engine from the Stage 5
  `handoff_packet.json` while keeping the native voice; native-but-flattened is not acceptable.
- AT5 fail → add/rewrite 备用标题 until ≥3, each passing A-Title rules with varied angles.
- AB9/B8 (Chinglish) fail → rewrite the offending lines into native English.
- Score < 85 even with blocking passing → keep de-AI'ing the weakest A/B items (slang ≤3/para,
  typo rate 1-3%, spoken syntax — conventions.md §4b).
- Record per-post VP/A/B scores in `run_manifest.md`.

## Reviewer prompt (MANDATORY evaluator worker — run this BLIND; EVAL_WORKER_CONTRACT.md)

Under isolated-worker execution this reviewer runs as a separate evaluator worker; it is NOT
optional. If the runtime has no subagents, emulate with a fresh evaluation session given only
the artifact, this EVALS.md, OUTPUT_SCHEMA.json, the minimal fact index, and the Stage 5
handoff_packet.json. Do NOT tell it the product is the client's.

"You are a long-time Reddit user with a strong nose for marketing. Read this post and its
comments. (1) Does it read like a real person or like an ad / AI? Point to specific AI tells:
checklist structure, feature dumps, stacked closing questions, no doubt, formal vocab.
(2) Do the comments feel like different real people disagreeing, or a script that all serves
the product? (3) Any Chinglish or forced slang? (4) Given this 'intended hook / emotional
trigger / must-keep details / comment engine' [from the handoff packet], did the post KEEP
them, or did it get flattened into something safe but boring? List every tell and every lost
hook. Would this get called out as an ad in a subreddit — and would it actually get upvotes?"

