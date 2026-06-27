# Enter Pro Product Brief

## Source Inventory

| Source | Type | Date Checked | Reliability | Notes |
| --- | --- | --- | --- | --- |
| Existing Enter Pro product outline | Customer/workflow material | 2026-06-26 | customer-provided + previously consolidated | Used as the source of record for this dry run. |

## One-Line Positioning

Enter Pro is an AI-native product building platform for moving from an AI-generated demo toward a real web product with backend, code ownership, deployment, and ongoing iteration concerns handled in one workspace.

## Product Capability Tree

- AI app / website / agent builder
  - Natural-language prompt to web app, website, or agent.
  - Browser-based building experience for non-developers and early-stage builders.
  - Templates / remix to avoid starting from scratch.
- Planning and iteration
  - Plan Mode for read-only planning before implementation.
  - Multi-session project workstreams.
  - Visual Editor for style/text/layout changes.
  - Rewind / version-related workflow via Enter Code context where verified.
- Backend and cloud layer
  - Auth.
  - PostgreSQL database.
  - Storage.
  - Functions.
  - Secrets.
  - RLS / permissions concepts.
  - Deployment and custom domain workflows.
- Code ownership and handoff
  - Code panel with visible source tree.
  - Source export / download.
  - GitHub import/export/sync.
  - Enter Code can take over locally for developer workflow.
- AI / agent workflow
  - AI All model gateway across major model providers.
  - Skills, Memory, MCP, Knowledge Base, and shareable agent workflow concepts.
  - Enter CLI for agents/scripts to operate Enter platform commands.
- Analytics and payments
  - Analytics is described as an independent capability, but no real analytics data is available for this run.
  - Stripe/payment can be discussed as a pain and possible workflow area, but full payment chain needs proof before strong claims.

## Product Boundary

### Verified Capabilities

- Enter Pro builds web applications in a browser-based workflow.
- The verified stack boundary for Enter Pro is React / Vite / TypeScript / Tailwind.
- Enter Cloud includes Auth, PostgreSQL database, Storage, Functions, Secrets, and RLS-related infrastructure.
- Code panel/source visibility, download, GitHub sync/import/export, and domain/version/settings entries are observed or included in source materials.
- Enter Code is a local terminal agent for developers; Enter CLI is a platform automation interface and should not be conflated with Enter Code.
- AI All is the current naming visible in materials; do not rename it unless the client confirms.

### Unverified / Needs Client Confirmation

- Stripe full checkout-to-webhook-to-subscription-state implementation details.
- Agent Builder end-to-end flow and external integrations.
- Team members/collaboration permissions.
- Analytics screenshots or real metrics.
- Pricing and credit numbers.
- Visual Editor before/after screenshots.

### Must Not Claim

- "Production-ready in minutes."
- "Replaces developers."
- "No lock-in" or "zero migration."
- "Fully handles Stripe end to end" without proof.
- Fake user revenue, fake customer reviews, fake benchmarks, fake app-store results, or fake screenshots.
- Native mobile app support for Enter Pro.
- Arbitrary stack generation inside Enter Pro.

## Target Users

| Persona | Situation | Pain | Buying Trigger | Objections | Best Reddit Context |
| --- | --- | --- | --- | --- | --- |
| Non-technical founder | Has a demo from an AI builder and wants to ship | Auth, database, payments, permissions, and deployment become confusing | First real user, first payment, or investor/customer demo | Lock-in, cost, lack of technical control | r/nocode, r/SideProject, r/SaaS, r/startups |
| Solo founder / indie builder | Builds MVPs quickly and iterates alone | Demo is easy, maintenance and handoff become hard | Needs production-ish backend and code ownership | Fear of platform trap and brittle generated code | r/indiehackers, r/SaaS, r/webdev, r/vibecoding |
| AI-native developer | Uses AI agents but still owns code quality | Prompt loops create messy code and context loss | Needs planning, code access, tests, local takeover | Prefers local tools and custom stack | r/ClaudeAI, r/cursor, r/webdev, r/vibecoding |
| Freelancer / agency builder | Builds client portals or internal tools for clients | Client-specific auth, roles, domains, and future handoff | Client asks "can we own the code?" | Needs reliability and export/handoff confidence | r/freelance, r/webdev, r/nocode |
| Small business / ops builder | Wants a portal, dashboard, workflow app | No in-house engineering team, but static site builders are insufficient | Needs a working web tool, not just a website | Setup complexity, monthly cost, support | r/smallbusiness, r/nocode, r/productivity |

## Competitor Matrix

Pricing is marked `unknown` where no current official source was checked during this dry run.

| Product | Primary Persona | Pricing Status | Code Export | Backend / Cloud | Planning Workflow | Local Dev Handoff | Agent / MCP / Skills | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Enter Pro | Non-technical founders, solo builders, PMs, small teams | needs current official check | yes, source visible/export/GitHub sync per materials | Auth, Postgres, Storage, Functions, Secrets, RLS per materials | Plan Mode | Enter Code + export/GitHub | Skills, MCP, Memory, Knowledge Base | Strongest story is "after the demo." |
| Lovable | No-code / prompt-to-app builders | unknown | likely supports code/GitHub workflows; needs current check | Often associated with Supabase-style app backend; verify before claiming | unknown | unknown | unknown | Strong mindshare in AI app builder space. |
| Replit Agent | Builders who want coding + hosted workspace | unknown | code lives in Replit workspace; export specifics need check | Replit hosting/database/services vary by project | agent-driven | yes inside Replit dev environment | unknown | Strong developer-adjacent hosted IDE. |
| Bolt | Browser-based full-stack prototyping users | unknown | export/GitHub details need current check | browser dev environment; backend story needs verification | unknown | unknown | unknown | Known for fast browser prototyping. |
| v0 | Frontend/UI generation and deployment users | unknown | generates real code; export details need current check | strongest around UI/frontend; backend depends on stack | unknown | developer handoff via generated code | unknown | Better framed as UI/code generation than full product workflow. |
| Base44 | AI product building users | unknown | needs check | needs check | unknown | unknown | unknown | Category-adjacent AI builder. |
| Cursor | Professional developers | unknown | local codebase by default | not a hosted product backend | planning depends on user workflow | strong local dev workflow | MCP/agent-like workflows vary | Strong coding environment, not a no-code product cloud. |
| Claude Code | Professional developers / terminal agent users | unknown | local codebase by default | not a hosted product backend | strong planning possible through prompts | terminal-native | MCP/skills concepts possible | Competes with Enter Code more than Enter Pro. |

## Differentiation

Enter Pro's most defensible Reddit angle is not "make an app with AI"; that space is crowded. The stronger angle is: AI builders made demos easy, but shipping requires backend, permissions, payment state, secrets, deployment, code ownership, and handoff. Enter Pro can be framed as a tool trying to close that post-demo gap while keeping export and developer handoff in view.

Use trade-off language. The product should not be positioned as magic or zero-lock-in. Better wording: "one workspace for the pieces I kept duct-taping together", "closer to a real web app than a mock-data demo", "still something you'd review before charging users", "export/GitHub sync helps with handoff, but migration is never literally free."

## Reddit Messaging Angles

- "The first demo is easy; the second month is where things break."
- "What happens when your AI-built app needs roles, permissions, and client data?"
- "Code export only matters when a real developer has to take over."
- "Planning before prompting as an antidote to codebase drift."
- "AI app builders versus local coding agents: different jobs, not one winner."
- "Backend, secrets, and model keys are the boring parts that decide whether a demo survives."

## Fact Bank

| Claim | Status | Evidence | Safe Wording |
| --- | --- | --- | --- |
| Enter Pro builds browser-based web apps from natural language | verified/customer-provided | Product outline | "Enter Pro is a browser-based AI app/website builder for web apps." |
| Enter Pro uses React/Vite/TypeScript/Tailwind for generated web apps | verified/customer-provided | Product outline | "The Enter Pro stack is React/Vite/TypeScript/Tailwind, not arbitrary stacks." |
| Enter Cloud includes Auth, Postgres, Storage, Functions, Secrets, RLS | verified/customer-provided | Product outline | "Enter Cloud brings auth, Postgres, storage, functions, secrets, and RLS-style infrastructure into the same workspace." |
| Code is visible/exportable and can sync with GitHub | verified/customer-provided | Product outline | "Code panel, download/export, and GitHub sync are part of the ownership story." |
| Enter Pro removes all lock-in | do-not-use | Product boundary | Do not claim. Say export helps handoff but migration still has trade-offs. |
| Enter fully handles Stripe end-to-end | needs-confirmation | Product outline lists missing proof | Do not claim as fact; discuss payment/webhook pain or request proof. |
| Enter replaces developers | do-not-use | Product boundary | Do not claim; say generated code still needs review for security/payment/permissions. |
| AI All is the current model gateway name | verified/customer-provided | Product outline | Use "AI All" unless client confirms a rename. |

## Open Questions For Client

- Can we show a Stripe test-mode flow screenshot or describe the exact payment-state boundary?
- Which pricing numbers are approved for public comparison?
- Which screenshots can be used for code panel, GitHub sync, Enter Cloud, and Plan Mode?
- Are there subreddit restrictions or brand-disclosure rules from the client side?
