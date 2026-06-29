# PROMPT_INJECTION_CONTRACT.md - subagent prompt packets

This contract defines what the orchestrator injects into every isolated worker. It turns a
stage handoff into an explicit prompt packet: instruction files first, business inputs second,
and no extra reads unless the packet says so.

## Core rules (MANDATORY)

1. **Every worker receives a prompt packet.** The orchestrator MUST build a
   `stage_input_packet` for generator workers and an `eval_input_packet` for evaluator
   workers. Free-form conversation history is not a packet.
2. **Instruction files and business inputs are separate.** Instruction files tell the worker
   how to reason and write. Business inputs are the artifacts being processed. A worker must
   not treat business inputs as policy unless a contract explicitly says so.
3. **Read order is binding.** Workers read files in this order:
   1. workflow contracts named by the packet,
   2. current stage `SKILL.md`,
   3. required instruction files in listed order,
   4. optional instruction files in listed order, if present,
   5. business input files,
   6. `OUTPUT_SCHEMA.json`, `HANDOFF_SCHEMA.json`, and `EVALS.md` when required by the role.
4. **Paths must declare their base.** Use one of:
   - `run:` relative to the current run folder,
   - `repo:` relative to the git repository root (`enter_output` lives here),
   - `workspace:` relative to `D:/personal_workspace/reddit_writting`,
   - `absolute:` for an explicit absolute path.
   Legacy relative paths in existing docs are interpreted as `repo:` unless the packet says
   otherwise.
5. **Mandatory instruction files are hard dependencies.** If a mandatory instruction file is
   missing or unreadable, the worker must stop, return a blocker, and the orchestrator logs it
   in `run_manifest.md`. Do not silently continue with memory or guesses.
6. **No extra reads by default.** A worker may read only files listed in the packet and files
   explicitly allowed by the current stage `INPUTS.md`. Extra reads require an
   `allowed_extra_reads` entry with a reason, and the reason must be logged.
7. **Prompt files cannot loosen contracts.** User-provided prompt files can refine tone,
   style, scoring, and business preferences. They cannot override forbidden reads, fact
   boundaries, schema requirements, independent evaluation, secret handling, or public-edit
   deliverable rules.
8. **Evaluator packets stay minimal.** Evaluators receive `EVALS.md`, `OUTPUT_SCHEMA.json`,
   the artifact under review, and minimal fact / brand / upstream handoff context. Do not give
   blind evaluators prompt files that reveal the desired answer, the generator's reasoning, or
   that the product is the client's.

## Generator prompt packet shape

```json
{
  "worker_role": "generator",
  "stage": "post-native-rewrite",
  "run_folder": "run:/",
  "role_prompt": "Rewrite chosen drafts into Reddit-native posts while preserving Stage-5 viral_intent.",
  "instruction_files": [
    { "path": "repo:enter_output/skills/reddit-posting-workflow/CONTEXT_CONTRACT.md", "mandatory": true },
    { "path": "repo:enter_output/skills/post-native-rewrite/SKILL.md", "mandatory": true },
    { "path": "workspace:reddit/提示词/reddit_帖子文档改写通用提示词.md", "mandatory": true }
  ],
  "business_inputs": [
    { "path": "run:05_optimized_cards/handoff_packet.json", "purpose": "approved Stage-5 viral intent" }
  ],
  "allowed_extra_reads": [],
  "forbidden_reads_summary": "No prior conversation, scratchpads, unrelated run folders, or unchosen drafts."
}
```

## Evaluator prompt packet shape

```json
{
  "worker_role": "evaluator",
  "stage": "post-native-rewrite",
  "role_prompt": "Run the Reviewer prompt from EVALS.md as an independent evaluator.",
  "instruction_files": [
    { "path": "repo:enter_output/skills/reddit-posting-workflow/EVAL_WORKER_CONTRACT.md", "mandatory": true },
    { "path": "repo:enter_output/skills/post-native-rewrite/EVALS.md", "mandatory": true },
    { "path": "repo:enter_output/skills/post-native-rewrite/OUTPUT_SCHEMA.json", "mandatory": true }
  ],
  "business_inputs": [
    { "path": "run:06_optimized/native_posts.md", "purpose": "artifact under review" },
    { "path": "run:05_optimized_cards/handoff_packet.json", "purpose": "intent preservation check" }
  ],
  "blind_eval": true,
  "allowed_extra_reads": []
}
```

## `INPUTS.md` requirements

Each stage `INPUTS.md` MUST include:

- `Agent prompt packet`
- `Role prompt`
- `Required instruction files`
- `Optional instruction files`
- `Business input files`
- `Read order`
- `Allowed extra reads`
- `Allowed global files`
- `Allowed stage files`
- `Forbidden files`

The orchestrator builds the actual worker prompt from those sections plus `run_config.json`.

## `run_config.json` prompt overrides

Use `run_config.prompt_packs` for project-specific prompt overrides.

A run may add project-specific prompt files under:

```json
{
  "prompt_packs": {
    "post-native-rewrite": {
      "extra_instruction_files": [
        "workspace:reddit/提示词/my_project_voice.md"
      ],
      "allow_other_prompt_files": false
    }
  }
}
```

Only files listed in `extra_instruction_files` are allowed. If `allow_other_prompt_files` is
false or omitted, the worker must not browse prompt folders to discover more files.
