# PROMPT_INJECTION_CONTRACT.md

The orchestrator builds a `stage_input_packet` for each generator or evaluator worker.

## Generator Prompt Packet Shape

```json
{
  "role_prompt": "string",
  "instruction_files": ["path"],
  "optional_instruction_files": ["path"],
  "business_inputs": ["path"],
  "read_order": ["instruction_files", "optional_instruction_files", "business_inputs", "schemas", "evals_self_check"],
  "allowed_extra_reads": ["path or rule"],
  "forbidden_reads": ["path or rule"]
}
```

Read order is binding. Instruction files come before business inputs. Files not listed in the
packet or current `INPUTS.md` are forbidden.

## Prompt Packs

`run_config.prompt_packs.<stage>.extra_instruction_files` may refine tone, style, and business
preferences. Prompt packs cannot loosen schemas, forbidden reads, fact boundaries, evaluator
requirements, or secret handling.

## Evaluator Prompt Packet Shape

```json
{
  "role_prompt": "separate evaluator worker",
  "artifact_under_review": "path",
  "evals": "path/to/EVALS.md",
  "output_schema": "path/to/OUTPUT_SCHEMA.json",
  "handoff_schema": "path/to/HANDOFF_SCHEMA.json",
  "minimal_context": ["approved upstream handoff or global fact files"]
}
```

No extra reads by default. If the evaluator needs another file, it must name the exact file and
why in its verdict.
