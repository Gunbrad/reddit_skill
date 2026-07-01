# EVALS - Community Topic Retrieval + Topic Cards (Stage 3)

Run by a separate evaluator worker. The evaluator receives `retrieval_round.json`,
`reference_post_cards.json`, `topic_cards.json`, `topic_cards.md`, `feishu_links.md`, this file,
and schemas. Blocking criteria must pass before mechanism generation.

## Gate A - Retrieval

| # | Criterion | Blocking | Pass condition |
|---|---|:---:|---|
| A1 | Embeddings ready | ✅ | Embeddings status was checked and retrieval did not proceed against missing embeddings |
| A2 | Query preserves requirement | ✅ | Retrieval query reflects the user's topic requirement and product boundary |
| A3 | top_k respected | ✅ | Round result count and requested `top_k` are recorded |
| A4 | Reference cards saved | ✅ | Retrieved cards include rank, score, card_id, subreddit, title, and source_card ids where returned |

## Gate B - Topic Card Quality

| # | Criterion | Blocking | Pass condition |
|---|---|:---:|---|
| B1 | Count valid | ✅ | Generated count is 12, 18, or 24 according to config/user selection |
| B2 | Required fields present | ✅ | Each card has title direction, content form, post format, mechanism, brand exposure, source ids, target subreddit |
| B3 | Grounded in retrieved cards | ✅ | Each card cites at least one source card or clear reference logic from retrieval |
| B4 | Community-map fit | ✅ | Cards reflect captured community positioning, themes, content forms, motivations, or risks |
| B5 | Varied angles | ⬜ | Cards are not near-duplicates of the same hook/post format |
| B6 | Not ad-heavy | ✅ | Brand exposure is natural and light; no card is a direct product pitch |

## Gate C - Feishu Topic Doc

| # | Criterion | Blocking | Pass condition |
|---|---|:---:|---|
| C1 | Topic doc written | ✅ | `feishu_links.md` contains the Topic Card doc URL |
| C2 | Feishu content complete | ✅ | Feishu doc includes all generated cards with ids, target subreddit, mechanism, and source reference logic |
| C3 | Secrets absent | ✅ | No cookies, passwords, or internal eval notes in Feishu content |

## Failure -> action

- A fail -> redo retrieval with a sharper query or wait for embeddings.
- B fail -> regenerate Topic Cards with stronger supplemental context.
- C fail -> repair Feishu write before continuing.

## Reviewer prompt (MANDATORY evaluator worker)

"Review Stage 3 retrieval and Topic Cards. Does the retrieval query match the user's topic
requirement and return saved reference cards? Are Topic Cards grounded in retrieved posts and
community maps, with required fields, valid count, varied angles, and non-ad brand exposure?
Was the Topic Card set written to a Feishu doc with no secrets? List all blocking issues."
