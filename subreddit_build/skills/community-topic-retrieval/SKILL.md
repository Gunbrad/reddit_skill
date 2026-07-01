---
name: community-topic-retrieval
description: Use after community capture succeeds, when entering a topic requirement, semantically retrieving reference Post Cards, generating 12/18/24 Topic Cards, and writing Topic Cards to a Feishu topic document. Stage 3 of the subreddit build workflow.
---

# Community Topic Retrieval + Topic Cards (Stage 3)

## Overview

Turn the user's topic requirement into a semantic retrieval round over the captured community
post cards, then generate Topic Cards grounded in the retrieved references, community maps,
and Stage 2 community insights.
This stage also creates or updates the Feishu topic document.

**Core principle:** Topic Cards must be grounded in retrieved posts, community content maps,
and `community_insights`; do not invent generic marketing angles.

## Inputs

- Stage 2 handoff with `project_id`, `run_id`, content maps, community insights, and embeddings status.
- `run_config.topic_requirement` or the user's latest topic requirement.
- `run_config.retrieval_top_k` (default 8).
- `run_config.topic_card_count` (allowed 12, 18, 24; default 12).
- Global fact and brand files.

## Required Output

Write to `03_topic_retrieval/`:

- `retrieval_round.json` - round id, query, top_k, scores, retrieved card ids.
- `reference_post_cards.json` - normalized retrieved cards for downstream evidence.
- `topic_cards.json` - generated Topic Cards.
- `topic_cards.md` - human-readable Topic Cards for Feishu and review.
- `feishu_links.md` - Topic Card Feishu doc URL.
- `handoff_packet.json`.

## API Flow

1. Confirm embeddings exist with `GET /api/projects/{project_id}/runs/{run_id}/embeddings`.
2. `POST /api/projects/{project_id}/runs/{run_id}/retrieval/search`.
3. `POST /api/projects/{project_id}/runs/{run_id}/retrieval/rounds/{round_id}/topic-cards/generate`.
4. `GET /api/projects/{project_id}/runs/{run_id}/retrieval/rounds/{round_id}/downloads`.
5. Download `topic_cards_json` and `topic_cards_md` only if the download list exposes them.
6. Write the Topic Cards to Feishu via the available Feishu CLI/Lark doc tooling.

## Process

1. Rewrite the user's topic requirement into a retrieval query that preserves intent, audience,
   product boundary, and desired community semantics.
2. Create the retrieval round with `top_k`.
3. Save retrieved cards with rank, score, subreddit, title, and card id.
4. Generate Topic Cards with `count` 12/18/24 and concise supplemental context that references
   relevant community positioning, themes, transferable patterns, motivations, and risk warnings.
5. Evaluate card grounding and variety. Regenerate with `overwrite:true` only when evaluation fails.
6. Write Topic Cards to Feishu and record the doc URL.
7. Write `handoff_packet.json`.

## Common Mistakes

- Generating Topic Cards before embeddings are ready.
- Letting Topic Cards drift into generic product promotion.
- Ignoring `community_insights` and using only broad subreddit stereotypes.
- Skipping the Feishu topic document.
- Guessing download keys instead of reading `/downloads`.
