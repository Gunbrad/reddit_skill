# SmartContent 搜索占位功能 API 接口文档

测试站点：`https://smartcontent.shifenglab.com`

测试时间：2026-06-26

测试账号：`cehua4`

本次只测试“搜索占位”功能，不测试“社区建设”。测试项目为 `Enter Pro`，产品大纲来自 `reddit/接口test/新工作流接口测试/用于测试的产品大纲.md`。本次没有调用平台的 AI 推荐搜索方向接口，而是手动提交 6 个搜索方向，每个方向抓取 10 个帖子。

实测关键 ID：

```text
project_id: enter-pro
run_id: 20260626_221552_search
direction_id used for downstream tests: direction_002
draft_job_id: 20260626_144308_c5792262
```

原始抓包/调用证据：

```text
reddit/接口test/新工作流接口测试/smartcontent_search_occupancy_capture.json
reddit/接口test/新工作流接口测试/smartcontent_search_occupancy_generation_capture.json
reddit/接口test/新工作流接口测试/smartcontent_frontend_bundle.js
```

## 1. 认证方式

接口使用 Cookie 会话认证。请求需要带：

```http
Cookie: planner_session=<session>
Accept: application/json
```

当前 cookie 验证接口：

```http
GET /api/auth/me
```

返回示例：

```json
{
  "username": "cehua4",
  "display_name": "阡阡",
  "planner_id": "cehua4"
}
```

## 2. 项目接口

### 2.1 获取搜索占位项目列表

```http
GET /api/search-occupancy/projects
```

返回示例：

```json
[
  {
    "project_id": "enter",
    "planner_id": "cehua4",
    "name": "Enter",
    "notes": null,
    "created_at": "2026-06-26T08:17:02.123096+00:00",
    "updated_at": "2026-06-26T08:17:02.123096+00:00",
    "runs_count": 1
  }
]
```

### 2.2 创建搜索占位项目

```http
POST /api/search-occupancy/projects
Content-Type: application/json
```

请求体：

```json
{
  "name": "Enter Pro",
  "product_brief": "# Enter Pro 产品资料总结\n\n...",
  "notes": "API interface test project: only search occupancy workflow; search directions are manually supplied, not AI-suggested."
}
```

返回示例：

```json
{
  "project_id": "enter-pro",
  "planner_id": "cehua4",
  "name": "Enter Pro",
  "notes": "API interface test project: only search occupancy workflow; search directions are manually supplied, not AI-suggested.",
  "created_at": "2026-06-26T14:15:52.434773+00:00",
  "updated_at": "2026-06-26T14:15:52.434773+00:00",
  "runs_count": 0,
  "directories": {
    "project_dir": true,
    "runs_dir": true
  }
}
```

### 2.3 获取项目详情

```http
GET /api/search-occupancy/projects/{project_id}
```

返回示例：

```json
{
  "project_id": "enter-pro",
  "planner_id": "cehua4",
  "name": "Enter Pro",
  "product_brief": "# Enter Pro 产品资料总结\n\n...",
  "notes": "API interface test project: only search occupancy workflow; search directions are manually supplied, not AI-suggested.",
  "created_at": "2026-06-26T14:15:52.434773+00:00",
  "updated_at": "2026-06-26T14:15:52.434773+00:00",
  "runs_count": 1,
  "directories": {
    "project_dir": true,
    "runs_dir": true
  }
}
```

前端还暴露了项目编辑接口：

```http
PATCH /api/search-occupancy/projects/{project_id}
```

请求体同创建项目的 `name/product_brief/notes`。本次未修改项目资料，未实测 PATCH。

## 3. 搜索资料准备 Run

### 3.1 获取项目 Run 列表

```http
GET /api/search-occupancy/projects/{project_id}/runs
```

返回示例：

```json
[
  {
    "run_id": "20260626_221552_search",
    "project_id": "enter-pro",
    "planner_id": "cehua4",
    "run_type": "search_occupancy_init",
    "project_name": "Enter Pro",
    "status": "succeeded",
    "current_stage": "search_pipeline_completed",
    "stage_index": 6,
    "total_stages": 6,
    "error": null,
    "direction_count": 6,
    "posts_per_query": 10,
    "planned_post_count": 60,
    "created_at": "2026-06-26T14:15:52.950251+00:00",
    "updated_at": "2026-06-26T14:26:16.892133+00:00"
  }
]
```

### 3.2 创建 Run

```http
POST /api/search-occupancy/projects/{project_id}/runs
Content-Type: application/json
```

请求体：

```json
{
  "posts_per_query": 10,
  "search_directions": [
    {
      "direction_id": "direction_001",
      "query": "vibe coding app backend auth payments reddit"
    },
    {
      "direction_id": "direction_002",
      "query": "AI app builder demo to production problems"
    },
    {
      "direction_id": "direction_003",
      "query": "Supabase Stripe RLS AI builder non developer"
    },
    {
      "direction_id": "direction_004",
      "query": "Lovable Bolt Replit alternatives code ownership export"
    },
    {
      "direction_id": "direction_005",
      "query": "Cursor Claude generated app security data isolation"
    },
    {
      "direction_id": "direction_006",
      "query": "AI SaaS builder shipping real users payments"
    }
  ]
}
```

返回示例：

```json
{
  "run_id": "20260626_221552_search",
  "project_id": "enter-pro",
  "planner_id": "cehua4",
  "run_type": "search_occupancy_init",
  "project_name": "Enter Pro",
  "status": "succeeded",
  "current_stage": "finalize",
  "stage_index": 4,
  "total_stages": 4,
  "error": null,
  "direction_count": 6,
  "posts_per_query": 10,
  "planned_post_count": 60,
  "search_directions": [
    {
      "direction_id": "direction_001",
      "query": "vibe coding app backend auth payments reddit",
      "intent": null,
      "reason": null,
      "keyword_focus": [],
      "content_angle": null
    }
  ],
  "artifacts": {
    "search_directions_json": true,
    "search_directions_md": true,
    "search_results_dir": true,
    "direction_dirs_count": 6,
    "search_url_summary_json": false,
    "search_url_summary_md": false,
    "search_preparation_summary_json": false,
    "search_preparation_summary_md": false,
    "search_occupancy_map_summary_json": false,
    "search_occupancy_map_summary_md": false
  },
  "search_url_summary": null,
  "search_preparation_summary": null,
  "search_occupancy_map_summary": null
}
```

说明：

- 创建 Run 只保存搜索方向和基础目录，不会自动完成抓取。
- 前端限制最终搜索方向最多 6 个；本次遵守用户约束，每方向 10 条，未超过 20 条。

### 3.3 启动完整资料准备

```http
POST /api/search-occupancy/projects/{project_id}/runs/{run_id}/prepare-all
```

请求体：无。

返回示例：

```json
{
  "run_id": "20260626_221552_search",
  "project_id": "enter-pro",
  "status": "running",
  "current_stage": "prepare_search_pipeline",
  "stage_index": 0,
  "total_stages": 6,
  "direction_count": 6,
  "posts_per_query": 10,
  "planned_post_count": 60,
  "error": null
}
```

### 3.4 轮询 Run 状态

```http
GET /api/search-occupancy/projects/{project_id}/runs/{run_id}
```

轮询间隔建议 5-15 秒。本次实际阶段变化：

```text
prepare_search_pipeline -> collect_search_urls -> collect_post_details
-> generate_post_cards -> generate_search_occupancy_maps -> search_pipeline_completed
```

最终返回示例：

```json
{
  "run_id": "20260626_221552_search",
  "project_id": "enter-pro",
  "status": "succeeded",
  "current_stage": "search_pipeline_completed",
  "stage_index": 6,
  "total_stages": 6,
  "direction_count": 6,
  "posts_per_query": 10,
  "planned_post_count": 60,
  "artifacts": {
    "search_directions_json": true,
    "search_directions_md": true,
    "search_results_dir": true,
    "direction_dirs_count": 6,
    "search_url_summary_json": true,
    "search_url_summary_md": true,
    "search_preparation_summary_json": true,
    "search_preparation_summary_md": true,
    "search_occupancy_map_summary_json": true,
    "search_occupancy_map_summary_md": true
  },
  "search_url_summary": {
    "total_directions": 6,
    "successful_directions": 6,
    "raw_url_count": 60,
    "unique_url_count": 60,
    "directions": [
      {
        "direction_id": "direction_002",
        "query": "AI app builder demo to production problems",
        "status": "success",
        "target_url_count": 10,
        "raw_url_count": 10,
        "unique_url_count": 10,
        "search_results_url": "https://www.reddit.com/search/?q=AI+app+builder+demo+to+production+problems&...",
        "items": [
          {
            "result_index": 1,
            "post_url": "https://www.reddit.com/r/nocode/comments/1ucoiu6/can_ai_app_builders_really_create_a_full_app_if",
            "post_id": "1ucoiu6",
            "title": "can AI App builders really create a full app if you can't code",
            "subreddit": "nocode",
            "age_text": "4d ago",
            "votes": 10,
            "comments": 58,
            "matched_directions": ["direction_002"]
          }
        ]
      }
    ]
  },
  "search_occupancy_map_summary": {
    "total_directions": 6,
    "successful_directions": 5,
    "failed_directions": 1,
    "directions": [
      {
        "direction_id": "direction_002",
        "query": "AI app builder demo to production problems",
        "status": "success",
        "post_cards_count": 10,
        "subreddit_count": 9,
        "map_json": true,
        "map_md": true
      }
    ]
  }
}
```

注意：本次 Run 总状态为 `succeeded`，但 `direction_001` 的地图生成失败。也就是说，调用方不能只看 run.status，还要看 `search_occupancy_map_summary.directions[].status`。

失败方向示例：

```json
{
  "direction_id": "direction_001",
  "query": "vibe coding app backend auth payments reddit",
  "status": "failed",
  "post_cards_count": 10,
  "subreddit_count": 0,
  "error": "OpenRouter structured JSON response failed schema validation: ... Invalid JSON: key must be a string ...",
  "map_json": false,
  "map_md": false
}
```

## 4. 搜索资料与地图读取接口

### 4.1 获取单个搜索占位地图 JSON

```http
GET /api/search-occupancy/projects/{project_id}/runs/{run_id}/search-occupancy-maps/{direction_id}
```

返回示例：

```json
{
  "direction_id": "direction_002",
  "query": "AI app builder demo to production problems",
  "generated_at": "2026-06-26T14:24:40.396858+00:00",
  "source_post_ids": ["1ucoiu6", "1uesed2"],
  "subreddit_distribution": [
    {
      "subreddit": "nocode",
      "post_count": 2,
      "percentage": 20.0,
      "representative_post_titles": [
        "can AI App builders really create a full app if you can't code",
        "AI can build the app fast. But who maintains it after the demo?"
      ]
    }
  ],
  "front_page_title_patterns": [
    "用 'demo 与生产/真实用户/1000 用户' 的对比制造认知冲突，几乎是所有上榜帖的标题骨架"
  ],
  "common_title_structures": [
    "can [AI app builders] really [verb] if you [constraint]"
  ],
  "content_forms": [
    "纯文本帖（question thread / 求助帖）——最常见载体，靠文字和评论形成讨论"
  ],
  "narrative_logic": [
    "几乎所有帖都从'个人亲历或亲见'切入，先建立情感共鸣再抛出技术问题"
  ],
  "high_frequency_semantic_phrases": [
    "AI app builder",
    "demo to production"
  ],
  "reddit_search_occupancy_rules": [
    "标题必须直接命中 'AI app builder demo to production' 这类痛点组合词，单纯写 'AI app builder' 排名会很弱"
  ],
  "transferable_title_hooks": [
    "对比落差：'demo 看起来很棒 vs 真实用户一碰就崩'"
  ]
}
```

### 4.2 下载接口

下载接口都使用 `GET`。成功时会返回 `Content-Disposition: attachment; filename="..."`。

| 资产 | 接口 | 实测状态 | Content-Type |
| --- | --- | ---: | --- |
| 地图汇总 MD | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/search-occupancy-maps/summary/download/summary_md` | 200 | `text/markdown` |
| 当前方向地图 MD | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/search-occupancy-maps/{direction_id}/download/map_md` | 200 | `text/markdown` |
| 当前方向地图 JSON | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/search-occupancy-maps/{direction_id}/download/map_json` | 200 | `application/json` |
| 搜索 URL JSON | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/search-urls/{direction_id}/download/json` | 200 | `application/json` |
| 搜索 URL MD | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/search-urls/{direction_id}/download/md` | 200 | `text/markdown` |
| 帖子详情 MD | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/search-materials/{direction_id}/download/raw_posts_md` | 200 | `text/markdown` |
| Post Cards JSONL | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/search-materials/{direction_id}/download/post_cards_jsonl` | 200 | `application/octet-stream` |
| Topic Cards MD | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/directions/{direction_id}/download/topic_cards_md` | 200，需先生成 Topic Cards | `text/markdown` |
| Drafts MD | `/api/search-occupancy/projects/{project_id}/runs/{run_id}/directions/{direction_id}/download/drafts_md` | 200，需先生成 Drafts | `text/markdown` |

下载返回示例：搜索 URL JSON

```json
{
  "direction_id": "direction_002",
  "query": "AI app builder demo to production problems",
  "status": "success",
  "target_url_count": 10,
  "raw_url_count": 10,
  "unique_url_count": 10,
  "search_results_url": "https://www.reddit.com/search/?q=AI+app+builder+demo+to+production+problems&...",
  "error": null,
  "items": [
    {
      "result_index": 1,
      "post_url": "https://www.reddit.com/r/nocode/comments/1ucoiu6/can_ai_app_builders_really_create_a_full_app_if",
      "post_id": "1ucoiu6",
      "title": "can AI App builders really create a full app if you can't code",
      "subreddit": "nocode",
      "age_text": "4d ago",
      "votes": 10,
      "comments": 58,
      "duplicate_of_direction": null,
      "matched_directions": ["direction_002"]
    }
  ]
}
```

下载返回示例：地图 MD 文件开头

```markdown
# AI app builder demo to production problems - 搜索占位分析地图

- Direction ID: `direction_002`
- Generated At: 2026-06-26T14:24:40.396858+00:00
- Source Posts: 10

## 社区分布
```

错误示例：在 Topic Cards / Drafts 尚未生成前下载对应 MD

```json
{
  "detail": "Search planning artifact not found."
}
```

错误示例：使用错误下载 kind

```json
{
  "detail": "Invalid search planning download kind."
}
```

## 5. Topic Cards 接口

### 5.1 查询某方向 Topic Cards

```http
GET /api/search-occupancy/projects/{project_id}/runs/{run_id}/directions/{direction_id}/topic-cards
```

生成前返回空数组：

```json
[]
```

生成后返回示例：

```json
[
  {
    "topic_id": "topic_001",
    "title_direction": "非程序员提问：AI App Builder 真的能做出可以上线的真实产品，还是只能画个漂亮的 demo 壳子？",
    "content_form": "讨论帖/问答帖",
    "post_format": "纯文本帖",
    "expression_mechanism": "从小事引起的困惑切入：以非技术创始人的真实痛苦和困惑开篇，质疑 AI 生成工具无法处理 Auth、Stripe 支付和数据库隔离的真实局限，引发广泛共鸣。",
    "brand_exposure_method": "从问题开始，仅在解释解决方案时命名：正文不直接宣传，直到讨论底层设施缺失时，有逻辑地介绍 Enter Pro 是如何通过内置的 Cloud (Auth/DB/RLS) 和 Stripe 同步机制解决这一痛点，最后放上产品链接。",
    "needs_extra_material": false,
    "required_material": null,
    "reference_logic": "借用 card_direction_002_1ucoiu6 和 card_direction_002_1uesed2 的经典问话句式，直接切入非程序员从 demo 走向 production 的最大痛点，挑战大众对 AI builder 的认知局限。",
    "source_card_ids": [
      "card_direction_002_1ucoiu6",
      "card_direction_002_1uesed2"
    ],
    "target_subreddit": "nocode",
    "status": "candidate"
  }
]
```

### 5.2 生成 Topic Cards

```http
POST /api/search-occupancy/projects/{project_id}/runs/{run_id}/directions/{direction_id}/topic-cards/generate
Content-Type: application/json
```

请求体：

```json
{
  "count": 12,
  "supplemental_context": "优先产出面向 Reddit 搜索占位的自然提问/复盘型选题，不要硬广；覆盖 demo-to-production、auth/payment/database、code ownership 等语义。",
  "overwrite": true
}
```

参数说明：

- `count`：前端提供 12 / 18 / 24 三档；本次实测 12。
- `supplemental_context`：选题补充说明，可为 `null`。
- `overwrite`：为 `true` 时覆盖当前方向已有 Topic Cards。

返回示例：

```json
{
  "run_id": "20260626_221552_search",
  "direction_id": "direction_002",
  "generated_count": 12,
  "topic_cards": [
    {
      "topic_id": "topic_001",
      "title_direction": "非程序员提问：AI App Builder 真的能做出可以上线的真实产品，还是只能画个漂亮的 demo 壳子？",
      "content_form": "讨论帖/问答帖",
      "post_format": "纯文本帖",
      "target_subreddit": "nocode",
      "status": "candidate"
    }
  ]
}
```

### 5.3 更新 Topic Card 状态

前端暴露了收藏状态更新接口：

```http
PATCH /api/search-occupancy/projects/{project_id}/runs/{run_id}/directions/{direction_id}/topic-cards/{topic_id}
Content-Type: application/json
```

请求体：

```json
{
  "status": "shortlisted"
}
```

或：

```json
{
  "status": "candidate"
}
```

本次没有使用收藏功能。生成文案时并不需要先调用这个 PATCH；前端“选择 Topic Cards”的本质是把选中的 `topic_ids` 放进 Draft job 请求体。

## 6. Draft / 具体文案接口

### 6.1 查询某方向 Drafts

```http
GET /api/search-occupancy/projects/{project_id}/runs/{run_id}/directions/{direction_id}/drafts
```

生成后返回示例：

```json
[
  {
    "draft_id": "draft_topic_001",
    "topic_id": "topic_001",
    "post_format": "纯文本帖",
    "title_candidates": [],
    "main_post": "## Title Candidates\n\n1. Can AI app builders actually take you from demo to production, or do you hit a wall?\n...",
    "first_comment": "",
    "follow_up_comments": [],
    "variant_notes": [],
    "source_card_ids": [
      "card_direction_002_1ucoiu6",
      "card_direction_002_1uesed2"
    ],
    "created_at": "2026-06-26T14:44:26.199503+00:00",
    "post_v1": null,
    "post_v2": null,
    "comment_design": null,
    "post_v1_markdown": "## Title Candidates\n\n- Can AI app builders actually ship a real product...",
    "post_v2_markdown": "## Title Candidates\n\n1. Can AI app builders actually take you from demo to production...",
    "comment_design_markdown": "## Comment Trees\n\n**Tree 1: The Supabase Skeptical Validator**\n\nuser1 ...",
    "final_markdown": "## Title Candidates\n\n1. Can AI app builders actually take you from demo to production..."
  }
]
```

### 6.2 创建 Draft 生成 Job

```http
POST /api/search-occupancy/projects/{project_id}/runs/{run_id}/directions/{direction_id}/drafts/jobs
Content-Type: application/json
```

请求体：

```json
{
  "topic_ids": [
    "topic_001",
    "topic_002"
  ],
  "topic_supplemental_contexts": {
    "topic_001": "客户反馈：正文可以轻度提到 Enter Pro，但必须先呈现真实痛点和讨论价值；标题不要像广告。",
    "topic_002": "补充说明：希望偏向工具选型/替代方案讨论，保留对平台锁定的审慎语气。"
  },
  "length_multiplier": 1,
  "overwrite": true
}
```

参数说明：

- `topic_ids`：选中的 Topic Card ID 数组。
- `topic_supplemental_contexts`：可选对象，key 为 `topic_id`，value 为该选题的补充说明 / 客户反馈。不需要补充时传 `{}` 或省略对应 key。
- `length_multiplier`：文案篇幅倍率。前端四档为更短/默认/稍长/更长，本次默认值为 `1`。
- `overwrite`：为 `true` 时，同一 `topic_id` 后生成的 Draft 会覆盖前版本。

返回示例：

```json
{
  "job_id": "20260626_144308_c5792262",
  "status": "running",
  "requested_count": 2,
  "requested_topic_ids": [
    "topic_001",
    "topic_002"
  ],
  "started_at": "2026-06-26T14:43:08.231922+00:00",
  "deadline_at": "2026-06-26T14:55:08.231922+00:00"
}
```

### 6.3 轮询 Draft Job

```http
GET /api/search-occupancy/projects/{project_id}/runs/{run_id}/directions/{direction_id}/drafts/jobs/{job_id}
```

建议 5-10 秒轮询一次。前端实测轮询到 `completed` 后停止。本次 2 篇文案约 80 秒完成。

完成返回示例：

```json
{
  "job_id": "20260626_144308_c5792262",
  "status": "completed",
  "requested_count": 2,
  "completed_count": 2,
  "failed_count": 0,
  "pending_count": 0,
  "requested_topic_ids": [
    "topic_001",
    "topic_002"
  ],
  "completed_topic_ids": [
    "topic_001",
    "topic_002"
  ],
  "pending_topic_ids": [],
  "drafts": [
    {
      "draft_id": "draft_topic_001",
      "topic_id": "topic_001",
      "post_format": "纯文本帖",
      "main_post": "## Title Candidates\n\n1. Can AI app builders actually take you from demo to production, or do you hit a wall?\n...",
      "post_v1_markdown": "## Title Candidates\n\n- Can AI app builders actually ship a real product...",
      "post_v2_markdown": "## Title Candidates\n\n1. Can AI app builders actually take you from demo to production...",
      "comment_design_markdown": "## Comment Trees\n\n**Tree 1: The Supabase Skeptical Validator**\n\nuser1 ...",
      "final_markdown": "## Title Candidates\n\n1. Can AI app builders actually take you from demo to production..."
    }
  ],
  "errors": [],
  "started_at": "2026-06-26T14:43:08.231922+00:00",
  "deadline_at": "2026-06-26T14:55:08.231922+00:00",
  "updated_at": "2026-06-26T14:44:31.000000+00:00"
}
```

## 7. 可选但本次未使用的接口

前端暴露了 AI 推荐搜索方向接口，但本次按要求没有使用平台生成的搜索 query。

```http
POST /api/search-occupancy/search-directions/suggest
Content-Type: application/json
```

前端请求体形态：

```json
{
  "product_name": "Enter Pro",
  "product_brief": "# Enter Pro 产品资料总结\n\n...",
  "notes": "可选补充说明",
  "count": 10
}
```

返回预期字段从前端逻辑推断为：

```json
{
  "suggested_count": 10,
  "directions": [
    {
      "direction_id": "direction_001",
      "query": "..."
    }
  ]
}
```

## 8. 推荐调用顺序

```text
1. GET /api/auth/me
2. POST /api/search-occupancy/projects
3. POST /api/search-occupancy/projects/{project_id}/runs
4. POST /api/search-occupancy/projects/{project_id}/runs/{run_id}/prepare-all
5. GET /api/search-occupancy/projects/{project_id}/runs/{run_id} 轮询到 succeeded
6. 检查 search_occupancy_map_summary.directions[].status，选择 status=success 的 direction
7. 下载 search-urls / search-materials / search-occupancy-maps 相关资产
8. POST /directions/{direction_id}/topic-cards/generate
9. GET /directions/{direction_id}/topic-cards 或下载 topic_cards_md
10. POST /directions/{direction_id}/drafts/jobs，传入选中的 topic_ids 和可选 topic_supplemental_contexts
11. GET /directions/{direction_id}/drafts/jobs/{job_id} 轮询到 completed
12. GET /directions/{direction_id}/drafts 或下载 drafts_md
```

## 9. 自动化调用注意事项

- 所有业务接口都依赖 `planner_session` Cookie；无 Cookie 或 Cookie 失效会导致未登录。
- 搜索资料准备耗时较长。本次 60 个帖子完整 prepare-all 约 10 分钟。
- Topic Cards 生成也可能长耗时。前端提示约 5 分钟；本次 12 张约 1-2 分钟内返回。
- Drafts 使用异步 Job 模式。创建接口快速返回 `job_id`，需要轮询 job 详情。
- Run 总状态为 `succeeded` 不代表每个方向都产出了地图。必须检查方向级 `status/map_md/map_json`。
- Topic Cards / Drafts 下载接口在生成前会返回 404 `Search planning artifact not found.`，生成后同一路径返回 200。
- “选择 Topic Cards”没有单独保存接口；生成文案时传 `topic_ids` 即可。
- 错误的下载 kind 会返回 400 `Invalid search planning download kind.`，应使用本文表格中的精确路径。
