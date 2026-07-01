---
name: product-research
description: Use when starting a new client product before any Reddit posting, when you have raw product facts (official site, client docs) and need a structured product brief, or when a downstream stage reports the product brief is missing or thin. Stage 1 of the Reddit posting pipeline.
---

# Product Research → Product Brief (Stage 1)

## Overview

Turn raw product facts into a single authoritative `product_brief.md` that every later stage
treats as ground truth. The brief defines the product's **capability boundary** so posts
never overclaim. If a fact isn't here (or is marked unverified), downstream stages must not
assert it.

**Core principle:** the brief is a *facts* document, not marketing. Capture what the product
verifiably does, where it stops, and how it differs from competitors — with enough structure
that stage 2 can derive 选题 and stage 3 can derive search queries.

## When to use

- New product / new brand / new client engagement.
- You have source material (website, client-provided docs, screenshots) to distill.
- A later stage says the brief is missing, outdated, or lacks a needed section.

Not for: rewriting posts, choosing topics — those are later stages.

## Inputs

- Official site + any client-provided docs/screenshots.
- Existing client fact-correction or feedback notes, if any.
- The run folder from the orchestrator (create it now if entering here).
- `run_config.json` if present. **Skip this stage** when the user supplied a brief
  (`1 in skip_stages` / `provided_artifacts.product_brief`): normalize their material into
  the structure below, run EVALS on it, and proceed — do not regenerate from scratch.

## Required output structure

Write to `01_product_brief/product_brief.md` (UTF-8). It MUST contain these sections, in
order. Downstream stages parse by these headings.

```
# {Product} 产品资料总结
> 整理日期 / 来源

## 一、产品概述
- 一句话定位
- 核心叙事 (the central tension the product solves)
- 产品矩阵 / 形态 (if multi-product)
- 核心功能模块 (table: 模块 | 功能 | 说明)

## 二、目标用户 (用户画像)
- 优先人群 / 扩展人群 / 非目标人群

## 三、核心卖点 (差异化优势)
- each selling point = name + 1-2 sentence rationale

## 四、竞品分析
- per competitor: 用户画像, 定价, 特色功能
- a horizontal 功能对比表 (see below)
- 我们产品的差异化结论

## 五、限制条件与边界
- 产品能力边界 (table: 限制 | 说明)
- 内容红线 (platform-specific dos/donts)
- 尚未验证的功能 (table: 功能 | 缺失素材) — these are "不可说" until client supplies proof

## 六、当前产品状态速查 (verified facts snapshot, dated)
- 已验证能力 vs 未验证/不可说, per module
```

## Compressed global outputs (MANDATORY — downstream stages read these, not the full brief)

Besides `product_brief.md`, Stage 1 MUST also emit three compressed files under `{run}/global/`.
Stages 2–7 read these instead of the full brief, to keep each stage's context small
(CONTEXT_CONTRACT minimal-context principle). See `OUTPUT_SCHEMA.json` for exact shapes.

1. `global/product_fact_index.json` — claim-level fact index for fact-checking:
   ```json
   {
     "claims": [
       {
         "claim_id": "C001",
         "claim": "Product supports GitHub sync.",
         "status": "verified",
         "source": "product_brief 三、核心卖点",
         "allowed_wording": ["supports GitHub sync"],
         "forbidden_wording": ["zero migration", "instant production handoff"]
       }
     ]
   }
   ```
2. `global/claim_boundary_table.json` — buckets every claim as verified / unverified / forbidden:
   ```json
   { "verified": ["C001"], "unverified": ["C007"], "forbidden": ["C009"] }
   ```
3. `global/brand_safety_rules.md` — brand-exposure boundary, 不可说 content, sensitive wording
   (≤1-2 capabilities per mention, disclosure rule, banned absolutes, competitor-tone rule).

Every claim in the index MUST trace to a `product_brief.md` section. `forbidden`/`unverified`
claims = the "不可说" features; downstream stages must never state them as fact. Keep the
index small but complete: it is the default fact source for stages 2–7.

### The capability tree (能力树)

The "核心功能模块" + "已验证能力边界" together form the capability tree. Each capability
must be tagged verified vs unverified. Example row:

```
| Enter Cloud | Auth、DB(PostgreSQL)、Storage、Functions、Secrets | 已验证 | 不含 Analytics |
```

### The competitor comparison table (横向对比，MANDATORY)

A feature matrix with ✓/✗ so differentiation is visible at a glance. Rows = products
(yours first), columns = differentiating features. Example:

```
| 产品 | 代码导出 | 多模型支持 | CLI工具 | Skills系统 | MCP集成 |
| --- | :--: | :--: | :--: | :--: | :--: |
| Ours | ✓ | ✓ | ✓ | ✓ | ✓ |
| CompA | ✓ | ✗ | ✗ | ✓ | ✗ |
| CompB | ✗ | ✓ | ✗ | ✗ | ✗ |
```

Pick columns that actually separate the products; don't pad with features everyone has.
For every competitor also record 用户画像 + 定价 (or "未公开" if unknown — never guess a price).

## Process

1. Create/confirm the run folder. Make `01_product_brief/`.
2. Gather facts from the site + client docs. Separate **verified** from **claimed/marketing**.
3. Draft each section. For every capability, decide: verified or unverified → tag it.
4. Build the competitor matrix; choose differentiating columns; fill ✓/✗ only where you
   have evidence (mark unknown cells, don't invent).
5. Write the differentiation conclusion: in one paragraph, what only this product does.
6. List the capability boundary + unverified-features table explicitly.
7. **Emit the three `global/*` compressed files** (product_fact_index, claim_boundary_table,
   brand_safety_rules) — every claim traceable to a brief section; 不可说 features bucketed
   as unverified/forbidden. These are what stages 2–7 read by default.
8. Run EVALS (see EVALS.md). Revise until blocking criteria pass.
9. Write `01_product_brief/handoff_packet.json` (per HANDOFF_SCHEMA.json). Log verdict + paths
   in `run_manifest.md`. Hand off to `topic-selection`.

## Common mistakes

- Copying marketing claims as facts (must tag unverified).
- Guessing competitor prices/features instead of marking unknown.
- A comparison table where every cell is ✓ (no differentiation signal).
- Omitting the "尚未验证 / 不可说" table — stage 5 needs it to avoid overclaiming.
- Vague differentiation ("better and faster") instead of a specific, defensible wedge.

