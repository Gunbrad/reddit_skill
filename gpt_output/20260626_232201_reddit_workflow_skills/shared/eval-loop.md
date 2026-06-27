# Eval Loop

Use this loop after every workflow step.

## Pass Conditions

An artifact passes only when:

1. No hard gate fails.
2. The weighted score is at or above the eval threshold.
3. All required output sections are present.
4. All downstream handoff fields are present or explicitly marked blocked.
5. The artifact was revised after any failed eval.

## Eval Report Format

Save each report to:

```text
{task_folder}/eval_reports/{step_number}_{step_name}_eval.md
```

Use this structure:

```markdown
# Eval Report: {step name}

- Artifact: `{path}`
- Evaluated At: {ISO timestamp}
- Result: PASS | FAIL
- Score: {score}/100

## Hard Gates

| Gate | Result | Evidence | Required Fix |
| --- | --- | --- | --- |

## Weighted Rubric

| Criterion | Weight | Score | Evidence | Required Fix |
| --- | ---: | ---: | --- | --- |

## Revision Log

- Attempt 1: ...
- Attempt 2: ...

## Handoff Notes

- Preserved facts:
- Blockers:
- Next-step inputs:
```

## Rework Rule

If the result is `FAIL`, revise the source artifact first, then rerun the eval. Do not hand off a failed artifact unless the user explicitly accepts the risk.

## Scoring Guidance

- 90-100: ready to hand off.
- 80-89: usually usable, but only if there are no hard-gate failures and the eval threshold is 80.
- 70-79: revise before handoff.
- Below 70: rebuild the artifact from source context.

Prefer specific fixes over vague critique. A useful eval says exactly what to change, where, and why.
