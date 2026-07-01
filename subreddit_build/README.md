# Subreddit Build Workflow Skills

This folder contains the SmartContent community-building workflow skill family. It mirrors the
existing Reddit posting workflow shape: an orchestrator dispatches isolated stage workers,
each stage writes a canonical artifact, and a separate evaluator worker must approve the stage
before its `handoff_packet.json` can move downstream.

The workflow is intentionally scoped to `subreddit_build/`.

## Execution Model

1. Orchestrator reads `run_config.json` and `skills/subreddit-build-workflow/PIPELINE_CONTRACT.md`.
2. Orchestrator builds the current stage's `stage_input_packet` from that stage's `INPUTS.md`.
3. An isolated generator worker creates the stage artifact.
4. A separate isolated evaluator worker scores the artifact against `EVALS.md`.
5. Orchestrator records verdicts, retries, API ids, Feishu links, and artifact paths in `run_manifest.md`.
6. Only an approved `handoff_packet.json` moves to the next stage.

## Structure

```text
skills/
  subreddit-build-workflow/
    SKILL.md
    PIPELINE_CONTRACT.md
    CONTEXT_CONTRACT.md
    WORKER_CONTRACT.md
    EVAL_WORKER_CONTRACT.md
    PROMPT_INJECTION_CONTRACT.md
    conventions.md
    verify_contracts.ps1

  product-research/
  community-capture/
  community-topic-retrieval/
  mechanism-variant-selection/
  community-card-draft-generation/
  post-native-rewrite/
  post-feishu-publish/
  feishu-formatting/
```

Each stage directory includes:

- `SKILL.md`
- `INPUTS.md`
- `OUTPUT_SCHEMA.json`
- `HANDOFF_SCHEMA.json`
- `EVALS.md`

## Canonical Stages

1. `product-research` writes `01_product_brief/product_brief.md` plus compressed global fact files.
2. `community-capture` creates/updates the SmartContent project, starts the community crawl, waits for completion, and downloads community artifacts.
3. `community-topic-retrieval` creates the retrieval round, generates Topic Cards, and writes the topic Feishu doc.
4. `mechanism-variant-selection` generates one 8-item mechanism batch per Topic Card, selects the best variant, and applies it.
5. `community-card-draft-generation` chooses TopN cards, writes per-card supplemental contexts with the original topic copied in, chooses length, and generates drafts.
6. `post-native-rewrite` de-AIs and native-rewrites the generated drafts into publish-ready Reddit posts.
7. `post-feishu-publish` writes the final posts into Feishu using CLI/Lark tooling.
8. `feishu-formatting` normalizes the Feishu document layout and verifies final formatting.

## Verification

Run the contract verifier from the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File reddit\接口test\新工作流接口测试\subreddit_build\skills\subreddit-build-workflow\verify_contracts.ps1
```

Useful JSON check:

```powershell
Get-ChildItem reddit\接口test\新工作流接口测试\subreddit_build\skills -Recurse -File -Include OUTPUT_SCHEMA.json,HANDOFF_SCHEMA.json |
  ForEach-Object { Get-Content -Raw -Encoding UTF8 -LiteralPath $_.FullName | ConvertFrom-Json | Out-Null }
```

Secrets never go in `run_config.json`, prompts, manifests, Feishu docs, or downloaded artifacts.
