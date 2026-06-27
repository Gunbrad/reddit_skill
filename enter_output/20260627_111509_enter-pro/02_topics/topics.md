# Enter Pro - 选题 (Topics) - 2026-06-27

> 来源：01_product_brief/product_brief.md
> 原则：每个选题从真实用户痛点/场景出发，产品作为"解决痛点时偶然发现的东西"出现，绝不做标题党硬广。
> 选题分组在 3 条互斥主线下，stage 3 每个选题派生 2 条长尾 query。

---

## 主线一：Demo 之后的工程化鸿沟（Post-Demo Infrastructure）

### 选题 1. AI 生成的 app demo 很漂亮，但接真实 auth + database 时整个卡住
- 内容类型：troubleshooting / experience recap（求助 + 复盘）
- 叙事思路：从"我用 AI 几小时生成了一个看起来能用的 app，但一到要真实登录、真实数据隔离就发现全是假数据/没有后端"这一真实落差切入；讲自己踩的坑（手动拼 Supabase、RLS 配错、用户能看到别人数据），结尾抛一个真实问题：大家是怎么把 AI demo 接到真后端的。产品在评论或正文里作为"后来发现有平台把 auth/db 内置了"自然出现。
- 素材/调研：可引用通用工程痛点（auth、RLS、数据隔离）；Enter Cloud 的 Auth/Database/RLS 为已验证能力可提及；不展示截图（无生图/无实测截图）。
- 品牌词露出：仅 1 次，作为"内置了 Auth + Postgres + RLS 的一类平台之一"，不罗列功能、不吹"best"。
- 选择理由：直击核心叙事"first demo is easy, the hard part is after demo"，搜索意图强（大量人卡在 demo→production），平台风险低（求助贴最自然）。

### 选题 2. 非技术 founder 把 AI app 推到生产前，到底要补哪些东西
- 内容类型：discussion / checklist 复盘（但写成"我漏了哪些"而非教程）
- 叙事思路：以非技术创始人口吻，列自己上线前才发现没做的环节（secrets 暴露、webhook 不可靠、部署不可复现），引导大家补充"还有什么坑"。产品作为"有人推荐用一站式平台少拼几个工具"出现一次。
- 素材/调研：通用 production checklist 痛点；Enter 的 Secrets/Functions/部署为已验证；不可说：Stripe 完整链路、Analytics 真实数据 → 不展开断言。
- 品牌词露出：≤1 次，弱露出，强调"不同工具适合不同阶段"。
- 选择理由：非技术 founder 是优先人群，长尾搜索意图明确，讨论性强。

---

## 主线二：代码所有权与平台锁定（Code Ownership & No Lock-in）

### 选题 3. 用 AI app builder 做的项目，代码到底是不是我的、能不能导出
- 内容类型：discussion（顾虑型提问）
- 叙事思路：从"想用某 AI builder 但怕被锁死、怕导不出代码、怕以后请的开发者接不了手"的真实顾虑切入；问大家选平台时怎么看 code ownership / export。产品作为"听说有的支持完整源码导出 + GitHub sync"自然带过。
- 素材/调研：code ownership / export / GitHub sync 为 Enter 已验证能力；边界："export ≠ zero migration"必须诚实带到，不能吹零迁移。
- 品牌词露出：≤1 次，且要带"导出不等于零迁移成本"的诚实限定。
- 选择理由：lock-in 是 AI builder 用户高频顾虑，搜索意图强，差异化壁垒（代码所有权）天然契合。

### 选题 4. AI 生成的代码后期还敢不敢改、怎么交接给真正的开发者
- 内容类型：experience recap（交接复盘）
- 叙事思路：从"项目跑起来了，但代码是 AI 黑盒，想加功能/请人维护时没人敢动"切入；讲自己怎么处理 handoff（看完整文件树、本地 agent 接管）。产品作为"后来用了能看到全部源码 + 本地 terminal agent 接管的方案"出现一次。
- 素材/调研：Code Panel（完整文件树）、Enter Code（本地接管/跑测试/rewind）为已验证；不吹"替代开发者"。
- 品牌词露出：≤1 次，强调"仍需人工 review"。
- 选择理由：维护性/交接是 demo-after 的延伸痛点，与主线一互补但角度不同（所有权 vs 工程化）。

---

## 主线三：一站式 vs 拼装工具链（Solo Builder 的工具选择）

### 选题 5. solo founder 到底该用一站式平台还是自己拼 Supabase+Stripe+Vercel
- 内容类型：discussion / cost-benefit 对比（中立）
- 叙事思路：以一人开发者口吻纠结"拼装灵活但维护累，一站式省心但怕锁定"，列各自利弊请大家投票/补充。产品作为一站式那一类的"其中之一"被提及，明确"不同阶段不同选择"。
- 素材/调研：一站式闭环（prompt→auth→db→payment→analytics→deploy）为卖点；Stripe 需自带账号、Analytics 无真实数据 → 诚实带边界。
- 品牌词露出：≤1 次，中立对比口吻，不攻击拼装方案。
- 选择理由：solo founder 是核心人群，"一站式 vs 拼装"是高搜索量决策类话题，讨论性极强。

### 选题 6. 想让已有的 AI coding agent（Claude Code/Cursor）直接操作部署平台，可行吗
- 内容类型：discussion / 技术可行性提问
- 叙事思路：从"我已经在用 Claude Code/Cursor 写代码，但 build/publish/domain 还要手动切到网页操作很烦"切入，问有没有办法让 agent 直接驱动部署平台。产品（Enter CLI）作为"发现有 CLI 能让 agent 跑 build/edit/publish/domain"自然出现一次。
- 素材/调研：Enter CLI 让 Claude Code/Codex/Cursor 操作 enter.pro（build/edit/publish/domain）为已验证；不混淆 Enter CLI 与 Enter Code。
- 品牌词露出：≤1 次，聚焦 CLI 能力，不展开其他模块。
- 选择理由：面向 AI-native developer 扩展人群，长尾且技术意图明确，与前几条人群/角度互斥。

---

## 互斥性说明
- 主线一 = 工程化/后端补全（auth/db/payment/deploy）
- 主线二 = 代码所有权/可维护/交接（ownership/handoff）
- 主线三 = 工具选择/集成（一站式 vs 拼装、agent 驱动 CLI）
三条主线语义不重叠，保证 stage 3 派生的搜索方向互斥。
