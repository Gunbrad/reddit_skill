# Reddit Posting Workflow Skills

This folder contains the portable Reddit posting workflow skill family. The workflow is built
around an orchestrator plus isolated stage workers, minimal input packets, structured handoff
files, and mandatory evaluator workers.

The current repository is intentionally scoped to `enter_output/`.

## Execution Model

The pipeline is no longer "one agent runs seven stages in one long context." It is:

1. Orchestrator reads `run_config.json` and `skills/reddit-posting-workflow/PIPELINE_CONTRACT.md`.
2. Orchestrator builds the current stage's `stage_input_packet` from that stage's `INPUTS.md`.
3. An isolated generator worker creates the stage artifact.
4. A separate isolated evaluator worker scores the artifact against `EVALS.md`.
5. Orchestrator records the verdict in `run_manifest.md`.
6. Only an approved `handoff_packet.json` moves to the next stage.

Use whatever isolation mechanism the runtime supports: isolated worker, subagent, child agent,
task agent, worker thread, fresh session, or equivalent context-isolated execution. If the
runtime has no worker support, emulate isolation with a fresh task/run that receives only the
current stage input packet.

## Structure

```text
skills/
  reddit-posting-workflow/
    SKILL.md                  # orchestrator / dispatcher
    CONTEXT_CONTRACT.md       # context isolation rules
    WORKER_CONTRACT.md        # generator vs evaluator roles
    PIPELINE_CONTRACT.md      # canonical 7-stage I/O
    EVAL_WORKER_CONTRACT.md   # mandatory independent evaluation
    PROMPT_INJECTION_CONTRACT.md # subagent prompt packets and read order
    conventions.md
    verify_contracts.ps1

  product-research/           # Stage 1
  topic-selection/            # Stage 2
  search-query-occupancy/     # Stage 3
  topic-card-selection/       # Stage 4
  topic-card-optimization/    # Stage 5
  post-optimization/          # Stage 6 coordinator
  post-native-rewrite/        # Stage 6a content optimization
  post-fact-brand-check/      # Stage 6b fact / brand gate
  post-subreddit-image/       # Stage 6c subreddit + image packaging
  post-feishu-publish/        # Stage 6d Feishu publishing
  feishu-formatting/          # Stage 7
```

Each main stage directory and each Stage 6 sub-stage directory includes:

- `SKILL.md`
- `EVALS.md`
- `INPUTS.md`
- `OUTPUT_SCHEMA.json`
- `HANDOFF_SCHEMA.json`

## Canonical Stages

1. `product-research` writes `01_product_brief/product_brief.md` and compressed global files:
   `global/product_fact_index.json`, `global/claim_boundary_table.json`,
   `global/brand_safety_rules.md`.
2. `topic-selection` writes `02_topics/topics.md` and the topic Feishu link.
3. `search-query-occupancy` writes query artifacts, topic cards, run metadata, and
   `03_search/occupancy_heat_evidence.json`.
4. `topic-card-selection` screens all cards with a binary pass/fail gate.
5. `topic-card-optimization` ranks passed cards, generates drafts, and writes structured
   `viral_intent` handoff data for Stage 6.
6. `post-optimization` coordinates the split Stage 6 workers:
   content optimization, fact/brand gate, subreddit/image packaging, and Feishu publishing.
7. `feishu-formatting` normalizes the final Feishu doc layout and verifies formatting.

## Context Rules

Downstream stages read compressed global files by default instead of the full product brief.
The full `product_brief.md` may be re-read only when the compressed fact index lacks necessary
information, and the reason must be logged in `run_manifest.md`.

Workers must not inherit full prior conversation history, scratchpads, failed drafts, old run
folders, raw Reddit dumps, or unrelated Feishu docs. Pass artifacts and handoff packets, not
conversation context.

## Subagent Prompt Packets

Every generator worker receives a `stage_input_packet` built from that stage's `INPUTS.md`.
The packet must include a `Role prompt`, `Required instruction files`, optional instruction
files, business input files, read order, and allowed extra reads. Instruction files are read
before business inputs. Files not listed in the packet or whitelisted by `INPUTS.md` are
forbidden.

Project-specific prompt files can be injected only through `run_config.prompt_packs.<stage>`.
Those prompt files may refine tone, style, and business preferences, but they cannot loosen
workflow contracts, forbidden reads, schema requirements, fact boundaries, or the independent
evaluator rule.

## Evals

Every stage artifact must be evaluated by a separate evaluator worker. The generator cannot
pass its own work. Evaluators receive only the artifact, `EVALS.md`, `OUTPUT_SCHEMA.json`, and
minimal fact/brand context.

Stage 6a has a blocking "Viral intent preserved" rule: final title/body/comment design must
preserve Stage 5 handoff values for `core_hook`, `emotional_trigger`, `comment_engine`, and
`must_preserve`.

## Verification

Run the contract verifier from the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File enter_output\skills\reddit-posting-workflow\verify_contracts.ps1
```

Useful additional checks:

```powershell
Get-ChildItem enter_output\skills -Recurse -File |
  Where-Object { $_.Name -in @('OUTPUT_SCHEMA.json','HANDOFF_SCHEMA.json') } |
  ForEach-Object { Get-Content -Raw -Encoding UTF8 -LiteralPath $_.FullName | ConvertFrom-Json | Out-Null }
```

## Runtime Notes

Secrets never go in `run_config.json`, prompts, Feishu docs, or manifests. Use environment
variables for API cookies and keys.

All final user-facing Feishu docs must be public-editable according to the workflow
conventions.
