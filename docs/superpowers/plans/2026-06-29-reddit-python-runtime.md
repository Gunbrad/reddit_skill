# Reddit Python Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a lightweight Python execution layer for the existing `enter_output` Reddit workflow without redesigning its stages, inputs, outputs, or eval rules.

**Architecture:** `pipeline.py` is the CLI entry point. `runtime/runner.py` sequences existing stage skills, builds prompt packets from each `INPUTS.md`, calls a pluggable model client for generator and evaluator requests, validates schemas, saves artifacts, pauses for external actions, and resumes from persisted manifests.

**Tech Stack:** Python standard library, `pytest`, existing Markdown/JSON contracts under `enter_output/skills`.

---

### Task 1: Runtime Contract Tests

**Files:**
- Create: `enter_output/tests/test_runtime_contracts.py`

- [ ] Write failing tests for packet building, independent generator/evaluator calls, artifact saving, schema failure, eval retry exhaustion, Feishu action pause/resume, external API idempotence, and resume skipping approved stages.
- [ ] Run: `python -m pytest enter_output/tests -q`
- [ ] Expected: collection/import failures because runtime modules do not exist yet.

### Task 2: Runtime Modules

**Files:**
- Create: `enter_output/pipeline.py`
- Create: `enter_output/runtime/__init__.py`
- Create: `enter_output/runtime/artifacts.py`
- Create: `enter_output/runtime/evaluator.py`
- Create: `enter_output/runtime/external_actions.py`
- Create: `enter_output/runtime/model_client.py`
- Create: `enter_output/runtime/prompt_builder.py`
- Create: `enter_output/runtime/runner.py`
- Create: `enter_output/runtime/validator.py`

- [ ] Implement model client interface with `mock`, `deepseek`, and configurable OpenAI-compatible providers.
- [ ] Implement prompt packet assembly from existing `INPUTS.md`, plus prompt pack injection from `run_config.json`.
- [ ] Implement schema validation and raw/candidate/eval/approved artifact persistence.
- [ ] Implement retry loop with default max retries = 5.
- [ ] Implement external action manifests for Feishu stages and search project placeholder adapter.
- [ ] Implement resume semantics from persisted run state.

### Task 3: Documentation

**Files:**
- Modify: `enter_output/README.md`

- [ ] Document install, environment variables, one-command start, resume, rerun stage, artifact locations, mock mode, external action result files, and provider swapping.
- [ ] Explicitly state that Feishu CLI remains outside Python and local approved artifacts remain canonical.

### Task 4: Verification and Commit

- [ ] Run contract verifier: `powershell -NoProfile -ExecutionPolicy Bypass -File enter_output\skills\reddit-posting-workflow\verify_contracts.ps1`
- [ ] Run tests: `python -m pytest enter_output/tests -q`
- [ ] Check `git status --short`.
- [ ] Commit only files changed for this runtime layer.
