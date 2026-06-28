# EVALS — Post Subreddit Picks + Image Packaging (Stage 6c)

Run by a SEPARATE evaluator worker (EVAL_WORKER_CONTRACT.md), per post, on
`06_optimized/final_posts.md` (+ `images/`). **Blocking** must pass.

The two sub-systems: (E) subreddits, (I) images. A carry-forward check (Y) confirms 6c didn't
drop the text/titles/comments produced by 6a/6b.

---

## E. Subreddits

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| E1 | ≥3 subreddits, correct format | ✅ | `r/xxx or r/xxx or r/xxx`, ordered fit→audience→reach |
| E2 | Subreddits viable | ⬜ | Each >10k, allows advice/experience, low brand-filter risk |

---

## I. Images (only when an image exists / is required)

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| I1 | Image scenario matches body | ✅ | No conflict (e.g. pristine new-product hero when body is about an old/struggling setup) |
| I2 | Not an ad image | ✅ | No hero/studio/poster shot, no logo, no text overlay, no fake futuristic UI |
| I3 | Prompt + rationale saved locally | ✅ | images/prompts.md records prompt, which post, image class (实体/虚拟), why scenario changed; png saved (or marked pending) |
| I4 | Image passes IMAGE_PROMPT_EVALS | ✅ | Classified 实体/虚拟 and passes that class rubric (blocking + ≥85) on prompt AND output |
| I5 | No secret leaked | ✅ | No API key / cookie in prompts.md or any artifact |

If `generate_images:false` or a post has no image idea, I1-I4 are N/A; record "no image" for it.

---

## Y. Carry-forward integrity

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| Y1 | Titles + 备用标题 preserved | ✅ | final_posts.md keeps the main Title and ≥3 备用标题 from 6a |
| Y2 | Body + comments preserved | ✅ | The fact-/brand-checked Body and Comment design from 6b are present, not re-summarized |

---

## Failure → action

- E1 fail → add subreddits to ≥3 in the exact format before handoff.
- I1/I2 fail → rewrite the image scenario before (re)generating.
- I4 fail → re-score against IMAGE_PROMPT_EVALS.md; rewrite prompt or repair via image2 edits.
- I5 fail → strip the secret immediately; secrets stay in env only.
- Y1/Y2 fail → restore the dropped block from `checked_posts.md` / `native_posts.md`.
- Record per-post E/I verdicts in `run_manifest.md`.

## Reviewer prompt (MANDATORY evaluator worker)

Under isolated-worker execution, this reviewer must run as a separate evaluator worker. It is
not optional. If the runtime does not support subagents, emulate this with a fresh evaluation
session that receives only final_posts.md, images/prompts.md when present, this EVALS.md,
OUTPUT_SCHEMA.json, and minimal brand-safety files.

"For each post: (1) Are there ≥3 viable subreddits in `r/x or r/y or r/z` format, ordered by
fit then reach? (2) If there's an image, does it match the story and avoid ad/AI tells? (3) Are
the title, ≥3 alternate titles, body, and comment section all still present (not dropped)? List
every violation."
