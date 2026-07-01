param(
  [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
)

$ErrorActionPreference = 'Stop'

$skillsRoot = Join-Path $Root 'skills'
$workflowRoot = Join-Path $skillsRoot 'subreddit-build-workflow'
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
  'community-capture',
  'community-topic-retrieval',
  'mechanism-variant-selection',
  'community-card-draft-generation',
  'post-optimization',
  'post-native-rewrite',
  'post-fact-brand-check',
  'post-subreddit-image',
  'post-feishu-publish',
  'feishu-formatting'
)

$contractFiles = @(
  'SKILL.md',
  'CONTEXT_CONTRACT.md',
  'WORKER_CONTRACT.md',
  'PIPELINE_CONTRACT.md',
  'EVAL_WORKER_CONTRACT.md',
  'PROMPT_INJECTION_CONTRACT.md',
  'conventions.md'
)

foreach ($file in $contractFiles) {
  Require-File (Join-Path $workflowRoot $file) "subreddit-build-workflow/$file" | Out-Null
}

Require-Text (Join-Path $Root 'README.md') 'subreddit_build/README.md' @(
  'stage_input_packet',
  'isolated generator worker',
  'separate evaluator worker',
  'INPUTS.md',
  'OUTPUT_SCHEMA.json',
  'HANDOFF_SCHEMA.json',
  'EVALS.md',
  'community-capture',
  'community-topic-retrieval',
  'mechanism-variant-selection',
  'community-card-draft-generation',
  'post-optimization',
  'post-fact-brand-check',
  'post-subreddit-image'
)

Require-Text (Join-Path $workflowRoot 'PIPELINE_CONTRACT.md') 'PIPELINE_CONTRACT.md' @(
  'community_builder_rpa_init',
  '02_community_capture',
  '03_topic_retrieval',
  '04_mechanism_selection',
  '05_optimized_cards',
  'community_insights',
  'post-optimization',
  'post-fact-brand-check',
  'post-subreddit-image',
  '06_optimized/final_posts.md',
  '07_format',
  'do not'
)

Require-Text (Join-Path $workflowRoot 'SKILL.md') 'subreddit-build-workflow/SKILL.md' @(
  'stage_input_packet',
  'isolated generator worker',
  'isolated evaluator worker',
  'approved handoff packet',
  'run_manifest.md'
)

foreach ($stage in $stageDirs) {
  $dir = Join-Path $skillsRoot $stage
  foreach ($file in @('SKILL.md', 'INPUTS.md', 'OUTPUT_SCHEMA.json', 'HANDOFF_SCHEMA.json', 'EVALS.md')) {
    Require-File (Join-Path $dir $file) "$stage/$file" | Out-Null
  }

  $inputs = Join-Path $dir 'INPUTS.md'
  if (Test-Path -LiteralPath $inputs -PathType Leaf) {
    Require-Text $inputs "$stage/INPUTS.md" @(
      'Agent prompt packet',
      'Role prompt',
      'Required instruction files',
      'Optional instruction files',
      'Business input files',
      'Read order',
      'Allowed extra reads',
      'Allowed global files',
      'Allowed stage files',
      'Forbidden files',
      'PROMPT_INJECTION_CONTRACT.md'
    )
  }

  foreach ($schemaFile in @('OUTPUT_SCHEMA.json', 'HANDOFF_SCHEMA.json')) {
    $schemaPath = Join-Path $dir $schemaFile
    if (Test-Path -LiteralPath $schemaPath -PathType Leaf) {
      try {
        Get-Content -Raw -Encoding UTF8 -LiteralPath $schemaPath | ConvertFrom-Json | Out-Null
      } catch {
        Fail "$stage/$schemaFile is not valid JSON: $($_.Exception.Message)"
      }
    }
  }

  $evalPath = Join-Path $dir 'EVALS.md'
  if (Test-Path -LiteralPath $evalPath -PathType Leaf) {
    $evalText = Read-Text $evalPath
    if ($evalText -notmatch 'MANDATORY evaluator worker|separate evaluator worker|SEPARATE evaluator worker') {
      Fail "$stage/EVALS.md does not make the evaluator worker mandatory"
    }
    if ($evalText -notmatch 'Blocking|BLOCKING|阻塞') {
      Fail "$stage/EVALS.md does not define blocking criteria"
    }
  }
}

Require-Text (Join-Path $skillsRoot 'community-capture\SKILL.md') 'community-capture/SKILL.md' @(
  'community_builder_rpa_init',
  'does not',
  'community_insights'
)
Require-Text (Join-Path $skillsRoot 'community-topic-retrieval\SKILL.md') 'community-topic-retrieval/SKILL.md' @(
  'retrieval/search',
  'topic-cards/generate',
  'Feishu',
  'community_insights'
)
Require-Text (Join-Path $skillsRoot 'mechanism-variant-selection\SKILL.md') 'mechanism-variant-selection/SKILL.md' @(
  '8 mechanisms',
  'apply',
  'community_insights'
)
Require-Text (Join-Path $skillsRoot 'community-card-draft-generation\SKILL.md') 'community-card-draft-generation/SKILL.md' @(
  'supplemental_context',
  'length_multiplier',
  'viral_intent',
  'community_insights'
)
Require-Text (Join-Path $skillsRoot 'post-native-rewrite\OUTPUT_SCHEMA.json') 'post-native-rewrite/OUTPUT_SCHEMA.json' @(
  '06_optimized/native_posts.md'
)
Require-Text (Join-Path $skillsRoot 'post-optimization\SKILL.md') 'post-optimization/SKILL.md' @(
  'Stage 6 coordinator',
  'post-native-rewrite',
  'post-fact-brand-check',
  'post-subreddit-image',
  'post-feishu-publish'
)
Require-Text (Join-Path $skillsRoot 'post-fact-brand-check\OUTPUT_SCHEMA.json') 'post-fact-brand-check/OUTPUT_SCHEMA.json' @(
  '06_optimized/checked_posts.md'
)
Require-Text (Join-Path $skillsRoot 'post-subreddit-image\OUTPUT_SCHEMA.json') 'post-subreddit-image/OUTPUT_SCHEMA.json' @(
  '06_optimized/final_posts.md'
)
Require-Text (Join-Path $skillsRoot 'post-feishu-publish\INPUTS.md') 'post-feishu-publish/INPUTS.md' @(
  '03_topic_retrieval/feishu_links.md',
  '06_optimized/final_posts.md',
  '06_optimized/6c_handoff_packet.json'
)

if ($failures.Count -gt 0) {
  Write-Host "Contract verification failed:"
  foreach ($failure in $failures) {
    Write-Host " - $failure"
  }
  exit 1
}

Write-Host "Contract verification passed."
