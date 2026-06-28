# EVALS — Post Feishu Publish Prep (Stage 6d)

Run by a SEPARATE evaluator worker (EVAL_WORKER_CONTRACT.md) after the Feishu docs are created,
verifying against `06_optimized/feishu_links.md`, `06_optimized/final_posts.md`, and the live
docs (re-read with `lark-doc`). **Blocking** must pass.

The two sub-systems: (G) image-doc + anchors, (F) Feishu deliverables.

---

## G. Image Feishu doc + anchors (only when images exist)

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| G1 | Image Feishu doc built | ✅ | If images exist: a 生图 doc exists; each combo = prompt + image, one per image-bearing post |
| G2 | Anchor link correct | ✅ | Each combo links to the SAME post_id's title block in the 帖子 doc (`url#block_id`); no mis-wired anchor |
| G3 | Mapping recorded | ⬜ | `images/image_feishu.md` records image-doc URL + `post_id → block_id` mapping |
| G4 | No secret leaked | ✅ | No API key / cookie in the image doc, image_feishu.md, or feishu_links.md |

If no images, G1-G3 are N/A; `feishu_links.md` must explicitly say no image doc was created.

---

## F. Feishu deliverables

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| F1 | 选题 doc exists | ✅ | `02_topics/feishu_links.md` contains the 选题 Feishu URL; if stage 2 deferred it, 6d created it from `02_topics/topics.md` |
| F2 | 帖子 doc exists | ✅ | `06_optimized/feishu_links.md` contains the 帖子 Feishu URL |
| F3 | 帖子 doc content complete | ✅ | Each post in the doc has main Title + ≥3 备用标题 + Body + Target Subreddit line + comment design |
| F4 | 生图 doc handled conditionally | ✅ | If images/prompts exist, the 生图 doc URL is recorded; if no images, feishu_links.md explicitly says none was created |
| F5 | Expected doc count met | ✅ | The run has 2 Feishu docs when no images, or 3 when images exist; never only the 帖子 doc |
| F6 | Docs public-editable | ✅ | Every created doc set to "anyone on the internet with the link can edit" (conventions.md §3) |

---

## Failure → action

- G1/G2 fail → build/repair the 生图 doc and re-verify each combo→post anchor before handoff.
- G4 fail → strip the secret immediately; secrets stay in env only.
- F1 fail → create the 选题 doc from `02_topics/topics.md`, set public-edit, record the URL.
- F3 fail → restore the missing block in the doc from `final_posts.md`.
- F5 fail → create/repair the missing doc(s) so the count is right.
- F6 fail → set the doc permission via lark-drive directly (no user confirmation).
- Record the verdict in `run_manifest.md`.

## Reviewer prompt (MANDATORY evaluator worker)

Under isolated-worker execution, this reviewer must run as a separate evaluator worker. It is
not optional. If the runtime does not support subagents, emulate this with a fresh evaluation
session that receives only feishu_links.md, final_posts.md, live doc detail, this EVALS.md,
OUTPUT_SCHEMA.json, and minimal image anchor mapping.

"Check the run's Feishu deliverables. (1) Do the 选题 doc and 帖子 doc both exist (URLs in the
link files)? If any post has an image, does a 生图 doc exist with one prompt+image combo per
image-bearing post, each anchor-linking to the correct post? (2) Does each post in the 帖子 doc
have its main title, ≥3 alternate titles, body, target-subreddit line, and comments? (3) Is the
doc count right (2 without images, 3 with) and is every doc public-editable? List every gap."
