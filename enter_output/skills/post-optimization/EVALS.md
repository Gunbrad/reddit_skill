# EVALS — Post Optimization (Stage 5) — the core de-AI / native system

This is the deepest eval system in the pipeline. Run it per post. **Blocking** must pass.
Threshold: all blocking pass AND de-AI total ≥ 85/100 (higher bar than other stages).

The five sub-systems: (A) de-AI/native Title+Body, (B) comment-section nativeness,
(C) brand exposure safety, (D) fact accuracy, (E) images + subreddits.

---

## A. De-AI / Native — Title + Body

### A-Title

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| AT1 | Reads like a user, not an ad | ✅ | Sounds like a real poster venting/asking, not marketing copy |
| AT2 | No hype words | ✅ | No "revolutionary / game changer / finally solved / best / 完美 / 终结" |
| AT3 | One core pain | ⬜ | Title carries one real pain, not stuffed with multiple claims |
| AT4 | Allows mild frustration/confusion | ⬜ | A little 吐槽/困惑/求建议 tone is fine and preferred |

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

---

## B. Comment-section nativeness

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| B1 | 8-12 comments | ⬜ | Not a full script; roughly 8-12 |
| B2 | Mixed emotions | ✅ | Has 共鸣 + 怀疑 + 个人经验 + 替代方案 + 等评测/提醒风险; not all praising |
| B3 | No comment fully sells brand | ✅ | No single comment explains the brand's selling points end-to-end |
| B4 | Brand ≤1-2 mentions total | ✅ | Across the whole comment section |
| B5 | No off-topic rabbit holes | ⬜ | No threads drifting to lights/keyboards/desk-mats etc.; ≤1 short ambient aside |
| B6 | Native voice | ⬜ | Natural slang (tbh/lol/fr/rip), light typos (≤3%), no Chinglish, no client-reply tone |
| B7 | Real disagreement exists | ⬜ | Comments diverge/argue; not all agreeing with OP |

---

## C. Brand exposure safety

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| C1 | Brand as "stumbled-on option" | ✅ | "saw X mentioned while searching" framing, not "this product solves my problem" |
| C2 | ≤1-2 capabilities per mention | ✅ | No multi-feature pitch in body |
| C3 | Disclosure intent present | ⬜ | Relationship disclosed where recommending/comparing |
| C4 | No competitor attack | ⬜ | Comparisons = "different tools, different stages" |

---

## D. Fact accuracy (vs product_brief.md)

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| D1 | No unverified feature as fact | ✅ | Nothing the brief marks "不可说"/unverified is stated as fact |
| D2 | Claims match capability tree | ✅ | Every product claim traces to a verified capability |
| D3 | No fabricated data | ✅ | No invented revenue/benchmark/review/screenshot |
| D4 | Boundaries respected | ⬜ | Doesn't imply capabilities outside the product boundary |

---

## E. Images + subreddits

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| E1 | Image scenario matches body | ✅ | No conflict (e.g., pristine new-product hero when body is about an old/struggling setup) |
| E2 | Not an ad image | ✅ | No hero/studio/poster shot, no logo, no text overlay, no fake futuristic UI |
| E3 | Prompt + rationale saved locally | ✅ | images/prompts.md records prompt, which post, and why scenario was changed; png saved (or marked pending) |
| E4 | ≥3 subreddits, correct format | ✅ | `r/xxx or r/xxx or r/xxx`, ordered fit→audience→reach |
| E5 | Subreddits viable | ⬜ | Each >10k, allows advice/experience, low brand-filter risk |

---

## Failure → action

- Any A/B/C/D blocking fail → rewrite that post and re-score; do NOT write to Feishu.
- Score < 85 even with blocking passing → keep de-AI'ing the weakest A/B items.
- E1/E2 fail → rewrite the image scenario before generating.
- Record per-post sub-system scores in `run_manifest.md`.

## Reviewer prompt (optional subagent — run this BLIND, without telling it the product is the client's)

"You are a long-time Reddit user with a strong nose for marketing. Read this post and its
comments. (1) Does it read like a real person or like an ad / AI? Point to specific AI tells:
checklist structure, feature dumps, stacked closing questions, no doubt, formal vocab.
(2) Is the brand mentioned like an accidental find or like a pitch? How many times?
(3) Do the comments feel like different real people disagreeing, or a script that all serves
the product? (4) Does the image match the story? List every tell. Would this get called out
as an ad in the target subreddit?"
