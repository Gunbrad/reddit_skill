# Enter Pro 搜索 Query (run 20260627_114808_search)

> 6 个长尾搜索方向，一个选题派生 1 条强长尾 query（平台单次最多 6 方向）。
> 跑完地图后从 success 方向里挑 3 个互斥方向，各生成 12 张 topic card = 36 张。
> 这些 query 全部是第一人称意图短语，与历史 run 的关键词式 query 不同。
>
> 注：首个 run（20260627_113021_search）在 generate_post_cards 阶段服务端确定性崩溃
> （抓到的某条 Reddit 帖子内容把服务端 JSON 解析打断，固定在 char 142），重试同 run 无效；
> 故用语义相同但措辞不同的 query 重新跑，规避那条坏帖。

## 主线一：Demo 之后的工程化鸿沟

- direction_001 | "AI generated my app frontend but I still need real login and a real database"
  - 长尾理由：锁定 demo→真实后端这一具体阶段，含 auth+database 双意图，不是 "AI app builder" 这种宽词。
- direction_002 | "checklist before a non technical founder launches an AI built web app to real users"
  - 长尾理由：限定人群（非技术 founder）+ 场景（上线前清单），是复盘型自然提问。

## 主线二：代码所有权与平台锁定

- direction_003 | "do AI website builders let you fully own and export your source code"
  - 长尾理由：直指 code export / lock-in 顾虑，疑问句式贴合真实搜索。
- direction_004 | "how to hand off an AI generated codebase to a developer without rewriting everything"
  - 长尾理由：handoff 具体动作 + 不想重写的痛点，区别于纯 export 话题。

## 主线三：一站式 vs 拼装工具链

- direction_005 | "is an all in one builder better than wiring supabase stripe and vercel for a solo project"
  - 长尾理由：决策对比型长尾，含具体工具栈名，强购买/选型意图。
- direction_006 | "drive my deployment platform from the terminal with an AI coding agent"
  - 长尾理由：技术可行性意图，限定 agent 驱动 CLI 部署，与其余方向语义不重叠。
