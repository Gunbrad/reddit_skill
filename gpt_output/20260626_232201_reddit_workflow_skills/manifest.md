# Reddit Promotion Skill Family

This package defines a six-step skill family for turning client product facts into Reddit-native posts, with evaluation gates after every step.

## Execution Order

1. `reddit-product-brief` - product research, capability boundary, personas, competitor matrix, differentiation.
2. `reddit-topic-planning` - Reddit topic directions and Feishu topic doc handoff.
3. `reddit-search-occupancy` - long-tail search queries, SmartContent search occupancy run, maps, direction selection, topic card generation.
4. `reddit-topic-card-selection` - score 36 topic cards, choose topN, write supplemental context, trigger draft generation.
5. `reddit-post-optimization` - optimize raw drafts, create Feishu draft doc, handle image prompts/images, target subreddits, product-fact checks.
6. `reddit-post-formatting` - final Feishu/local formatting, comment cleanup, brand highlighting, formatting QA.

## Shared Files

- `shared/workspace-and-handoff-contract.md` - project folder, naming, and cross-step handoff fields.
- `shared/smartcontent-api-contract.md` - API endpoints, polling, download rules, and failure handling.
- `shared/eval-loop.md` - common pass/fail loop used by all evals.
- `shared/output-templates.md` - required Markdown shapes for workflow artifacts.

## Evals

Each skill must run its paired eval before handing work to the next step:

- `evals/01-product-brief-eval.md`
- `evals/02-topic-planning-eval.md`
- `evals/03-search-occupancy-eval.md`
- `evals/04-topic-card-selection-eval.md`
- `evals/05-post-optimization-eval.md`
- `evals/06-post-formatting-eval.md`

Passing means: no hard-gate failures, score meets the threshold, and the artifact has been revised until the eval passes.
