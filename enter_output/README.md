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

## Python Runtime

The lightweight Python layer is an execution shell for the existing Skill contracts. It does
not redesign stages, schemas, handoff names, eval rules, Feishu policy, or SmartContent rules.

### Install

The runtime uses the Python standard library. Tests require `pytest`:

```powershell
python -m pip install pytest
```

### Model providers

DeepSeek is the default real provider. Do not put API keys in files.

```powershell
$env:DEEPSEEK_API_KEY = "..."
$env:DEEPSEEK_MODEL = "deepseek-v4-flash"
```

Dry run without model spend:

```powershell
python enter_output\pipeline.py start --provider mock --config enter_output\live_run\run_config.json
```

OpenAI-compatible provider for future GPT-compatible gateways:

```powershell
$env:MODEL_API_KEY = "..."
$env:MODEL_API_BASE_URL = "https://api.example.com/v1"
$env:MODEL_NAME = "model-name"
python enter_output\pipeline.py start --provider openai-compatible --config enter_output\live_run\run_config.json
```

Other providers can be added by implementing `ModelClient.complete()` in
`runtime/model_client.py`; the runner only depends on that interface.

### Commands

Start a run:

```powershell
python enter_output\pipeline.py start --config enter_output\live_run\run_config.json --provider deepseek
```

By default, every `start` creates a fresh run folder beside `enter_output/`:

```text
temp_output/YYYYMMDD_HHMMSS_project-name/
```

For example, running project `hoto` twice creates two different folders such as
`temp_output/20260629_153000_hoto/` and `temp_output/20260629_153015_hoto/`. If you need a
stable name for a manual debug run, pass `--run-id`; otherwise omit it so normal runs never
reuse a previous project folder.

Resume a paused or failed run:

```powershell
python enter_output\pipeline.py resume --run-id enter_001 --provider deepseek
```

Rerun one stage and continue:

```powershell
python enter_output\pipeline.py rerun-stage --run-id enter_001 --stage topic-card-selection --provider deepseek
```

Limit stages for a smoke test:

```powershell
python enter_output\pipeline.py start --provider mock --config enter_output\live_run\run_config.json --stages product-research,topic-selection
```

Stdout is one short JSON status object. Detailed responses, candidates, evals, manifests, and
approved artifacts are written under `temp_output/{run_id}/`.

### Run artifacts

For each stage, the runtime writes:

- `{stage_dir}/input_manifest.json`
- `{stage_dir}/runtime/attempt_001/generator_raw_response.json`
- `{stage_dir}/runtime/attempt_001/candidate_output.json`
- `{stage_dir}/runtime/attempt_001/candidate_handoff_packet.json`
- `{stage_dir}/runtime/attempt_001/eval_raw_response.json`
- `{stage_dir}/runtime/attempt_001/eval_result.json`
- `{stage_dir}/approved_output.json`
- `{stage_dir}/handoff_packet.json` for top-level stages

Stage 6 sub-stage handoffs are written as `06_optimized/6a_handoff_packet.json` through
`06_optimized/6d_handoff_packet.json`. After 6d passes, Python synthesizes the coordinator
`06_optimized/handoff_packet.json` with `stage_id: stage_6_post_optimization`.

### Generator response convention

Existing schemas define the stage output and handoff, but not a machine envelope for model
responses. The runtime adds this minimal convention:

```json
{
  "output": {},
  "handoff": {},
  "files": {
    "run-relative/path.md": "file content"
  },
  "external_actions": []
}
```

`output` must match the stage `OUTPUT_SCHEMA.json`. `handoff` is promoted only after the
independent evaluator passes; Python injects the final `eval_result` and validates it against
`HANDOFF_SCHEMA.json`.

### Feishu actions

Python never runs `lark-cli`. If a generator returns an external Feishu action, the run pauses
and writes `actions/{action_id}.json`:

```json
{
  "status": "needs_external_action",
  "action_id": "feishu_001",
  "action_type": "feishu.create_document",
  "title": "Document title",
  "content_file": "06_optimized/final_posts.md",
  "result_file": "actions/feishu_001.result.json"
}
```

The host conversation creates/updates the Feishu document with `lark-cli`, writes the result
JSON containing the document id and URL to `result_file`, then runs `resume`.

### Search placeholder project

Optional search placeholder creation is enabled only after `product-research` has passed
schema and eval. This uses the SmartContent contract already documented in
`skills/search-query-occupancy/api-reference.md`:

- Base URL: `https://smartcontent.shifenglab.com`
- Auth: `Cookie: planner_session=<PLANNER_SESSION>`
- Endpoint: `POST /api/search-occupancy/projects`
- Body: `{name, product_brief, notes}`

Environment:

```powershell
$env:PLANNER_SESSION = "..."
```

Run config:

```json
{
  "search_project_placeholder": {
    "enabled": true,
    "base_url_env": "SMARTCONTENT_BASE_URL",
    "session_env": "PLANNER_SESSION"
  }
}
```

The runtime uses `run_id` as the idempotency key and saves the receipt to
`external/search_project.json`. API failure pauses the run and does not regenerate the product
brief; `resume` retries only the external call.
