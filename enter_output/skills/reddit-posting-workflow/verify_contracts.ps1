param(
  [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
)

$ErrorActionPreference = 'Stop'

$skillsRoot = Join-Path $Root 'enter_output\skills'
$workflowRoot = Join-Path $skillsRoot 'reddit-posting-workflow'
$failures = New-Object System.Collections.Generic.List[string]

function Fail($message) {
  $script:failures.Add($message) | Out-Null
}

function Require-File($path, $label) {
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
    Fail "Missing $label at $path"
    return $false
  }
  return $true
}

function Read-Text($path) {
  return Get-Content -Raw -Encoding UTF8 -LiteralPath $path
}

function Require-Text($path, $label, [string[]]$patterns) {
  if (-not (Require-File $path $label)) { return }
  $text = Read-Text $path
  foreach ($pattern in $patterns) {
    if ($text -notmatch [regex]::Escape($pattern)) {
      Fail "$label does not mention '$pattern'"
    }
  }
}

$stageDirs = @(
  'product-research',
  'topic-selection',
  'search-query-occupancy',
  'topic-card-selection',
  'topic-card-optimization',
  'post-optimization',
  'feishu-formatting'
)

$stage6SubStageDirs = @(
  'post-native-rewrite',
  'post-fact-brand-check',
  'post-subreddit-image',
  'post-feishu-publish'
)

$contractFiles = @(
  'CONTEXT_CONTRACT.md',
  'WORKER_CONTRACT.md',
  'PIPELINE_CONTRACT.md',
  'EVAL_WORKER_CONTRACT.md'
)

foreach ($file in $contractFiles) {
  Require-File (Join-Path $workflowRoot $file) $file | Out-Null
}

$readmePath = Join-Path $Root 'enter_output\README.md'
Require-Text $readmePath 'enter_output/README.md' @(
  'CONTEXT_CONTRACT.md',
  'WORKER_CONTRACT.md',
  'PIPELINE_CONTRACT.md',
  'EVAL_WORKER_CONTRACT.md',
  'INPUTS.md',
  'OUTPUT_SCHEMA.json',
  'HANDOFF_SCHEMA.json',
  'stage_input_packet',
  'isolated generator worker',
  'isolated evaluator worker',
  'approved `handoff_packet.json`',
  'post-optimization',
  'post-native-rewrite',
  'post-fact-brand-check',
  'post-subreddit-image',
  'post-feishu-publish'
)

Require-Text (Join-Path $workflowRoot 'CONTEXT_CONTRACT.md') 'CONTEXT_CONTRACT.md' @(
  'isolated worker',
  'fresh session',
  'input packet',
  'worker depth = 1'
)
Require-Text (Join-Path $workflowRoot 'WORKER_CONTRACT.md') 'WORKER_CONTRACT.md' @(
  'Stage Generator Worker',
  'Stage Evaluator Worker',
  'A worker never plays both roles'
)
Require-Text (Join-Path $workflowRoot 'EVAL_WORKER_CONTRACT.md') 'EVAL_WORKER_CONTRACT.md' @(
  'No self-grading',
  'Always launch an evaluator',
  'Reviewer prompt is mandatory'
)
Require-Text (Join-Path $workflowRoot 'PIPELINE_CONTRACT.md') 'PIPELINE_CONTRACT.md' @(
  'product_fact_index.json',
  'claim_boundary_table.json',
  'brand_safety_rules.md',
  'occupancy_heat_evidence.json',
  'viral_intent'
)

foreach ($stage in $stageDirs) {
  $dir = Join-Path $skillsRoot $stage
  foreach ($file in @('INPUTS.md', 'OUTPUT_SCHEMA.json', 'HANDOFF_SCHEMA.json')) {
    $path = Join-Path $dir $file
    if (-not (Require-File $path "$stage/$file")) { continue }
    if ($file -eq 'INPUTS.md') {
      Require-Text $path "$stage/INPUTS.md" @(
        'Allowed global files',
        'Allowed stage files',
        'Forbidden files'
      )
    } else {
      try {
        Get-Content -Raw -Encoding UTF8 -LiteralPath $path | ConvertFrom-Json | Out-Null
      } catch {
        Fail "$stage/$file is not valid JSON: $($_.Exception.Message)"
      }
    }
  }
}

foreach ($stage in $stage6SubStageDirs) {
  $dir = Join-Path $skillsRoot $stage
  foreach ($file in @('INPUTS.md', 'OUTPUT_SCHEMA.json', 'HANDOFF_SCHEMA.json')) {
    $path = Join-Path $dir $file
    if (-not (Require-File $path "$stage/$file")) { continue }
    if ($file -eq 'INPUTS.md') {
      Require-Text $path "$stage/INPUTS.md" @(
        'Allowed global files',
        'Allowed stage files',
        'Forbidden files'
      )
    } else {
      try {
        Get-Content -Raw -Encoding UTF8 -LiteralPath $path | ConvertFrom-Json | Out-Null
      } catch {
        Fail "$stage/$file is not valid JSON: $($_.Exception.Message)"
      }
    }
  }
}

$evalFiles = Get-ChildItem -LiteralPath $skillsRoot -Recurse -File -Filter 'EVALS.md'
foreach ($file in $evalFiles) {
  $text = Read-Text $file.FullName
  $legacyOptionalPattern = ('optional ' + 'subagent') + '|' + ('optional ' + 'reviewer')
  if ($text -match $legacyOptionalPattern) {
    Fail "$($file.FullName) still contains legacy reviewer wording"
  }
  if ($text -notmatch 'MANDATORY evaluator worker|separate evaluator worker|SEPARATE evaluator worker') {
    Fail "$($file.FullName) does not make the evaluator worker mandatory"
  }
}

$orchestrator = Read-Text (Join-Path $workflowRoot 'SKILL.md')
foreach ($term in @(
  'CONTEXT_CONTRACT.md',
  'WORKER_CONTRACT.md',
  'PIPELINE_CONTRACT.md',
  'EVAL_WORKER_CONTRACT.md',
  'stage_input_packet',
  'isolated generator worker',
  'isolated evaluator worker',
  'approved handoff packet',
  'run_manifest.md'
)) {
  if ($orchestrator -notmatch [regex]::Escape($term)) {
    Fail "orchestrator SKILL.md does not mention '$term'"
  }
}
foreach ($toolSpecific in @(
  ('Claude ' + 'Code' + '''s Task tool'),
  ('Cod' + 'ex child tasks'),
  ('this ' + 'CLI' + '''s')
)) {
  if ($orchestrator -match [regex]::Escape($toolSpecific)) {
    Fail "orchestrator SKILL.md contains tool-specific execution wording '$toolSpecific'"
  }
}

$stage6Coordinator = Read-Text (Join-Path $skillsRoot 'post-optimization\SKILL.md')
foreach ($term in @(
  'Stage 6 coordinator',
  'post-native-rewrite',
  'post-fact-brand-check',
  'post-subreddit-image',
  'post-feishu-publish',
  'Stage-5 handoff',
  'chosen drafts',
  'compressed global files',
  '06_optimized/final_posts.md',
  '06_optimized/feishu_links.md',
  '06_optimized/handoff_packet.json'
)) {
  if ($stage6Coordinator -notmatch [regex]::Escape($term)) {
    Fail "post-optimization/SKILL.md does not mention '$term'"
  }
}
if ($stage6Coordinator -match [regex]::Escape('01_product_brief/product_brief.md')) {
  Fail 'post-optimization/SKILL.md must not read full product_brief.md'
}
if ($stage6Coordinator -notmatch 'coordinator' -or $stage6Coordinator -notmatch 'does not generate|does not write|does not perform') {
  Fail 'post-optimization/SKILL.md must describe Stage 6 as a coordinator, not a monolithic execution skill'
}

Require-Text (Join-Path $skillsRoot 'product-research\SKILL.md') 'product-research/SKILL.md' @(
  'product_fact_index.json',
  'claim_boundary_table.json',
  'brand_safety_rules.md'
)
Require-Text (Join-Path $skillsRoot 'search-query-occupancy\SKILL.md') 'search-query-occupancy/SKILL.md' @(
  'occupancy_heat_evidence.json'
)
Require-Text (Join-Path $skillsRoot 'topic-card-optimization\SKILL.md') 'topic-card-optimization/SKILL.md' @(
  'occupancy_heat_evidence.json',
  'viral_intent',
  'title_pattern_to_preserve',
  'expected_comment_types',
  'subreddit_risk_note'
)
Require-Text (Join-Path $skillsRoot 'post-optimization\SKILL.md') 'post-optimization/SKILL.md' @(
  'content-optimization',
  'packaging',
  'viral_intent',
  'isolated worker'
)
Require-Text (Join-Path $skillsRoot 'post-native-rewrite\EVALS.md') 'post-native-rewrite/EVALS.md' @(
  'Viral intent preserved',
  'core_hook',
  'emotional_trigger',
  'comment_engine',
  'must_preserve'
)

foreach ($subStage in @(
  'post-native-rewrite',
  'post-fact-brand-check',
  'post-subreddit-image',
  'post-feishu-publish'
)) {
  Require-File (Join-Path $skillsRoot "$subStage\SKILL.md") "$subStage/SKILL.md" | Out-Null
  Require-File (Join-Path $skillsRoot "$subStage\EVALS.md") "$subStage/EVALS.md" | Out-Null
  Require-File (Join-Path $skillsRoot "$subStage\INPUTS.md") "$subStage/INPUTS.md" | Out-Null
  Require-File (Join-Path $skillsRoot "$subStage\OUTPUT_SCHEMA.json") "$subStage/OUTPUT_SCHEMA.json" | Out-Null
  Require-File (Join-Path $skillsRoot "$subStage\HANDOFF_SCHEMA.json") "$subStage/HANDOFF_SCHEMA.json" | Out-Null
}

if ($failures.Count -gt 0) {
  Write-Host "Contract verification failed:"
  foreach ($failure in $failures) {
    Write-Host " - $failure"
  }
  exit 1
}

Write-Host "Contract verification passed."
