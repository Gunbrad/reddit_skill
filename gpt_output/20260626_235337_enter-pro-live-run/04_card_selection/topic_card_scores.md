# Topic Card Scores

## Selection Summary

- Project: Enter Pro
- Requested topN: not specified by user
- Working assumption: select topN = 6
- Pool considered: 36 generated Topic Cards from `direction_002`, `direction_003`, and `direction_006`
- Selected topic IDs:
  - `direction_006/topic_011`
  - `direction_003/topic_002`
  - `direction_002/topic_003`
  - `direction_003/topic_007`
  - `direction_006/topic_004`
  - `direction_002/topic_007`
- Coverage logic: two client-portal/Auth/RLS posts, two code ownership/handoff posts, and two prompt-drift/workflow posts. This keeps the final set directionally distinct while staying inside verified Enter Pro facts.
- Main rejection principle: reject cards requiring external reports, real screenshots, fake personal outcomes, live-product proof, full Stripe claims, or product-comparison assets that are not available in this run.

## Scoring Rules

- 90-100: select unless the portfolio is already saturated.
- 80-89: strong backup or niche angle.
- 70-79: usable only with heavy supplement.
- Below 70: reject for this run.

## Scores

| Rank | Direction ID | Topic ID | Title Direction | Target Subreddit | Score | Decision | Reason |
| ---: | --- | --- | --- | --- | ---: | --- | --- |
| 1 | direction_006 | topic_011 | Defensive workflows for avoiding AI MVP codebase disaster | vibecoding | 95 | SELECT | Strong Reddit checklist, verified Plan Mode / code ownership fit, no extra material. |
| 2 | direction_003 | topic_002 | Developer checklist for taking over an AI-generated app | webdev | 94 | SELECT | High-trust developer handoff angle; naturally fits export/GitHub/local takeover facts. |
| 3 | direction_002 | topic_003 | No-code client portal role exists but data is not isolated | nocode | 93 | SELECT | Precise troubleshooting pain, strong RLS/Auth fit, low material risk. |
| 4 | direction_003 | topic_007 | Browser builder plus terminal agent handoff workflow | vibecoding | 92 | SELECT | Distinct collaboration/workflow frame; showcases Enter Pro + Enter Code without hard selling. |
| 5 | direction_006 | topic_004 | Managing context across parallel features in an existing codebase | ClaudeAI | 92 | SELECT | Strong community fit and prompt-drift discussion potential; Plan Mode mention can stay modest. |
| 6 | direction_002 | topic_007 | AI-built client portal has half-built Auth/security boundaries | vibecoding | 91 | SELECT | Good question-thread energy; security boundary pain is concrete and product-relevant. |
| 7 | direction_006 | topic_002 | Prompt drift mechanism after 3 days of vibe coding | vibecoding | 89 | BACKUP | Strong educational angle, but overlaps selected prompt-drift cards. |
| 8 | direction_003 | topic_001 | Why AI app builder code export becomes a handoff problem | webdev | 88 | BACKUP | Good angle, but topic_002 is more actionable and less rant-like. |
| 9 | direction_002 | topic_010 | Stop using frontend filters for client portal data isolation | nocode | 86 | BACKUP | Strong warning post, but title may feel alarmist and overlaps topic_003. |
| 10 | direction_006 | topic_007 | Can you audit what the coding agent added to your codebase? | ClaudeAI | 86 | BACKUP | Good control/audit theme; lower than topic_004 because it risks sounding fear-based. |
| 11 | direction_003 | topic_012 | Do not hardcode API keys in AI-builder prompts | cybersecurity | 85 | BACKUP | Safe, useful security point; less direct Enter Pro fit unless Secrets are the focus. |
| 12 | direction_002 | topic_008 | Post-demo infrastructure checklist for privacy-sensitive portals | softwarearchitecture | 84 | BACKUP | Strong but broad; "production" wording needs weakening. |
| 13 | direction_003 | topic_003 | Demo looks perfect but post-demo infrastructure breaks | nocode | 84 | BACKUP | Relevant, but overlaps many selected angles and risks generic "demo after" messaging. |
| 14 | direction_006 | topic_001 | Six months of vibe coding became unmaintainable | vibecoding | 84 | BACKUP | Strong hook but would require avoiding fake personal story. |
| 15 | direction_002 | topic_011 | Can your AI/no-code client portal be exported for custom Auth rules? | vibecoding | 83 | BACKUP | Good code-ownership tie; overlaps direction_003 selected handoff posts. |
| 16 | direction_002 | topic_001 | Multi-tenant portal security boundary design | softwarearchitecture | 82 | BACKUP | Solid architecture discussion but broad and less Reddit-native. |
| 17 | direction_003 | topic_009 | Local terminal agent vs browser builder | vibecoding | 82 | BACKUP | Useful but "only bridge" style claim must be avoided. |
| 18 | direction_006 | topic_005 | Handoff day reveals black-box AI-builder pain | vibecoding | 82 | BACKUP | Strong but overlaps selected code handoff cards. |
| 19 | direction_003 | topic_008 | $3000 rebuild of an AI-generated product | nocode | 80 | BACKUP | Hook works, but fake cost/story risk is high without evidence. |
| 20 | direction_002 | topic_002 | Indie dev building client portal with AI tools | vibecoding | 79 | REJECT | Requires pretending to have tried several tools; too easy to sound fabricated. |
| 21 | direction_006 | topic_010 | Productivity dependency when AI tools disappear | vibecoding | 78 | REJECT | Interesting discussion but product fit is soft. |
| 22 | direction_003 | topic_010 | AMA about cleaning up AI-exported code | vibecoding | 78 | REJECT | AMA requires real authority and ongoing responses; not suitable as generated post. |
| 23 | direction_006 | topic_009 | V0/Lovable UI breaks when connecting Stripe/Auth/RLS | vibecoding | 76 | REJECT | Payment-chain claims are not verified enough. |
| 24 | direction_002 | topic_005 | Migrating client portal Auth/data isolation from Supabase | Supabase | 76 | REJECT | Competitor-community risk and migration claim risk. |
| 25 | direction_002 | topic_009 | Clientless web app instead of VPN | AZURE | 72 | REJECT | Wrong community fit for Enter Pro and too enterprise-infra heavy. |
| 26 | direction_003 | topic_006 | 2026 AI app builder code-ownership comparison | nocode | 70 | REJECT | Needs screenshots and current competitor verification. |
| 27 | direction_006 | topic_012 | Visual architecture map before prompting | ClaudeAI | 68 | REJECT | Requires before/after visuals not available. |
| 28 | direction_002 | topic_006 | Client portal with 2000 records and Stripe | nocode | 68 | REJECT | Unsupported Stripe and data-scale specificity. |
| 29 | direction_003 | topic_004 | SAST cleanup for AI-generated code | cybersecurity | 67 | REJECT | Needs AppSec proof and SAST data. |
| 30 | direction_002 | topic_012 | Stripe webhook, user permission, data isolation | nocode | 64 | REJECT | Requires Stripe diagram and unverified product claims. |
| 31 | direction_002 | topic_004 | 380k leaked AI apps security report | devsecops | 62 | REJECT | External report proof unavailable; high moderation risk. |
| 32 | direction_003 | topic_005 | Two B2B apps launched in three months | EntrepreneurRideAlong | 60 | REJECT | Would require fake public links and screenshots. |
| 33 | direction_003 | topic_011 | 10+ AI app builder comparison directory | directorymakers | 58 | REJECT | Needs broad comparison artifact and current data. |
| 34 | direction_006 | topic_003 | Scan dozens of AI-generated repos for drift metrics | LLMDevs | 57 | REJECT | Would require fabricated research data. |
| 35 | direction_006 | topic_006 | Outdoor lifestyle photo with code panel | vibecoding | 55 | REJECT | Needs image and risks ad-like lifestyle framing. |
| 36 | direction_006 | topic_008 | Weird Claude debug output screenshot | claude | 54 | REJECT | Needs screenshot and can drift into fake evidence. |

## Supplemental Contexts For Draft Generation

| Direction ID | Topic ID | Supplemental Context | Product Facts | Avoid | Material Needed |
| --- | --- | --- | --- | --- | --- |
| direction_006 | topic_011 | Emphasize defensive workflow advice for people whose AI MVP became harder to edit after repeated prompts. Write in natural English for r/vibecoding: half checklist, half "what I wish I had done earlier." Keep brand mention late and disclosed as one tool being evaluated, not as the whole answer. Mention skepticism: planning tools help but do not replace tests or code review. | Plan Mode is read-only planning with scope/assumptions/steps; code panel/export/GitHub sync exist; Enter Code can help local handoff; generated code still needs review. | Avoid "production-ready", "replaces developers", "no lock-in", fake case study, fake metrics, and full Stripe claims. | None. |
| direction_003 | topic_002 | Emphasize a developer-facing intake checklist for when a non-technical founder hands over an AI-generated web app. Make it useful even without Enter Pro: auth boundary, DB/RLS, secrets, deploy, code ownership, local run instructions. Brand mention should be soft/disclosed and framed as an example of the kind of handoff surface to check. | Enter Pro generates React/Vite/TypeScript/Tailwind web apps; has visible code panel/export/GitHub sync; Enter Cloud includes Auth/Postgres/Storage/Functions/Secrets/RLS; Enter Code is a local terminal agent. | Avoid pretending to have audited real customer apps, naming competitors as bad without proof, "zero migration", and guaranteed security. | None. |
| direction_002 | topic_003 | Emphasize a troubleshooting question for no-code builders who added a "client" role but are still only filtering data in the frontend. Explain why frontend filters are not data isolation, ask how people handle RLS/server-side checks. Brand mention late as one platform being evaluated because Enter Cloud includes Auth/Postgres/RLS-style pieces. | Enter Cloud includes Auth, PostgreSQL, Secrets, Functions, and RLS-related infrastructure; app stack is web app focused; security-sensitive work needs review. | Avoid saying Enter guarantees compliance/security, avoid fake breach story, avoid claiming users can skip engineering review. | None. |
| direction_003 | topic_007 | Emphasize a team workflow question: non-technical teammate builds UI/flows in browser, developer takes over locally when logic gets real. Write as a genuine "has anyone tried this split?" discussion. Brand mention as a disclosed example: Enter Pro for browser-side building plus Enter Code/local handoff. | Enter Pro is browser-based; code panel/export/GitHub sync exist; Enter Code is local terminal agent; not a native mobile builder. | Avoid claiming Enter is the only option, avoid "seamless" marketing language, avoid fake team story with results. | None. |
| direction_006 | topic_004 | Emphasize existing-codebase context management: multiple parallel features, AI keeps losing assumptions, naming, schema, or file boundaries. Make it a question for r/ClaudeAI, with concrete workflow asks: specs, CLAUDE.md-style docs, small sessions, review gates. Mention Enter Pro Plan Mode only as one read-only planning pattern. | Plan Mode lists scope/assumptions/steps before editing; multi-session project workstreams exist; generated code still needs tests/review. | Avoid claiming Plan Mode prevents all drift, avoid hard product pitch, avoid "magic fix" framing. | None. |
| direction_002 | topic_007 | Emphasize the vibe-coded client portal problem: UI looks done, but auth/session/data isolation is half-built. Keep it as a question about how people patch the boundary before letting real clients in. Brand mention late/disclosed as one tool being looked at because it bundles Auth/Postgres/RLS-style infrastructure with visible code. | Enter Cloud includes Auth/Postgres/Storage/Functions/Secrets/RLS; code panel/export/GitHub sync exist; Enter Pro is for web apps. | Avoid saying Stripe state sync is fully handled, avoid "secure by default" guarantee, avoid fake client incident. | None. |

## Rejected High-Risk Cards

- `direction_002/topic_004`: depends on an external security report and specific leak numbers that were not verified in this run.
- `direction_002/topic_012`: depends on Stripe webhook-to-permission architecture that is not verified.
- `direction_003/topic_005`: requires real public products, screenshots, and founder outcomes.
- `direction_003/topic_006` and `direction_003/topic_011`: require current competitor screenshots/comparison data.
- `direction_006/topic_003`: requires fabricated drift metrics and research-style charts.
- `direction_006/topic_006`, `direction_006/topic_008`, `direction_006/topic_012`: require unavailable images/screenshots.

## Draft API Handoff

- Draft request file: `04_card_selection/draft_request.json`
- Length multiplier: 1
- Overwrite: true
- Draft jobs:
  - `direction_002`: `20260626_165133_c66bf0cb` -> completed, `failed_count=0`
  - `direction_003`: `20260626_165326_0386b141` -> completed, `failed_count=0`
  - `direction_006`: `20260626_165514_9476bb0e` -> completed, `failed_count=0`
- Raw drafts path: `04_card_selection/raw_drafts.md`
