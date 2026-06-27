<h1>Post 1: Client Portal Role Filter vs Real Isolation</h1>
<p><b>Target Subreddit Name:</b> r/nocode; alternates: r/webdev, r/SaaS, r/Supabase</p>

<h2>Title</h2>
<p>No-code client portal: is a role filter actually data isolation?</p>

<h2>Body</h2>
<p>Working through a client-portal build and I want to sanity check something before I get too far.</p>
<p>A lot of no-code tools make it really easy to add a `client` role, hide some nav items, and filter a table where `client_id == current_user.client_id`. From the UI it looks fine.</p>
<p>But that is not the same thing as isolation.</p>
<p>The parts I'm trying to verify are:</p>
<p>1. If Client A guesses or receives a Client B record URL, does the server reject it?</p>
<p>2. If someone calls the API directly, does the backend enforce the same rule?</p>
<p>3. Is the policy attached to the data layer, or only to the page/query/view?</p>
<p>4. Can I write a repeatable test for "user X cannot read row Y" without manually logging in and clicking around?</p>
<p>I'm looking at a few routes: Supabase/Postgres RLS with a custom tenant claim, a traditional backend where every endpoint checks tenant access, AI/no-code builders that expose backend policies instead of only UI filters, and tools like <span background-color="light-yellow">Enter Pro</span>, which I'm evaluating because <span background-color="light-yellow">Enter Cloud</span> includes Auth, Postgres, Secrets, Functions, and RLS-style infrastructure in the same workspace.</p>
<p>Disclosure: I'm involved with <span background-color="light-yellow">Enter Pro</span>, so don't treat this as a neutral review. I'm mainly trying to pressure-test the model because "role-based view" seems to mean very different things across tools.</p>
<p>For people who have shipped a no-code or AI-built client portal with real customer data, what did your isolation layer actually look like?</p>
<p>What tests did you run before letting clients in?</p>

<h2>评论设计</h2>
<p><b>User 1</b></p>
<p>If the rule is only in the page query, assume it does not exist. The basic test is a token from org A trying to fetch a row from org B. Do that outside the UI.</p>
<p><b>User 2 replies to User 1</b></p>
<p>This is the part no-code tutorials skip. They show role-based menus, not malicious or accidental cross-tenant reads.</p>
<p><b>User 3 replies to User 1</b></p>
<p>Also test detail routes. List pages are usually filtered first; detail pages are where people forget the check.</p>
<hr/>
<p><b>User 1</b></p>
<p>Postgres RLS is nice but it is not automatic. You still need a tenant column, a trustworthy claim, and policies on every table that matters.</p>
<p><b>User 2 replies to User 1</b></p>
<p>Yep. "RLS enabled" with a policy like authenticated users can read all rows is basically decorative.</p>
<p><b>User 3 replies to User 1</b></p>
<p>The hard part is membership changes. User moves orgs, org gets disabled, contractor loses access, etc. That stuff gets messy fast.</p>
<hr/>
<p><b>User 1</b></p>
<p>The vendor angle here is a little suspicious, but the question is good. A shocking amount of "client portal" stuff is just a table with a login screen.</p>
<p><b>User 2 replies to User 1</b></p>
<p>Agree. I don't care which tool people pick, but they need to know whether the backend rejects the row.</p>
<p><b>User 3 replies to User 1</b></p>
<p>The disclosure makes it less annoying to me. At least the post isn't pretending to be a random founder story.</p>
<hr/>
<p><b>User 1</b></p>
<p>I'd add audit logs to the checklist. Isolation answers "can they read it"; logs answer "who did read it."</p>
<p><b>User 2</b></p>
<p>Bubble privacy rules are server-side, but you can still misconfigure them. Learned that one the annoying way.</p>
<p><b>User 3</b></p>
<p>For a small portal, I usually seed two fake tenants and run the same API tests before every deploy.</p>
<p><b>User 4</b></p>
<p>The phrase "role-based view" should make everyone nervous. Views are not permissions.</p>

<h1>Post 2: Vibe-Coded Portal Auth Boundary</h1>
<p><b>Target Subreddit Name:</b> r/vibecoding; alternates: r/nocode, r/webdev, r/SaaS</p>

<h2>Title</h2>
<p>AI built the client portal UI. Auth is the part I don't trust.</p>

<h2>Body</h2>
<p>The weird part about AI builders is how convincing the first 80% looks.</p>
<p>You prompt for a client portal and get a nice dashboard, login page, tables, empty states, maybe even an admin screen. It feels like a product for about ten minutes.</p>
<p>Then you ask the boring questions:</p>
<p>1. Are sessions actually validated server-side?</p>
<p>2. Are roles enforced in the API, or are buttons just hidden?</p>
<p>3. Can one client ever read another client's rows?</p>
<p>4. Are secrets in server env/config, or did the AI put something in the frontend bundle?</p>
<p>5. Is there any repeatable way to test the permission model?</p>
<p>That's where I keep seeing the "vibe-coded portal" fall apart. The UI is coherent. The boundary is not.</p>
<p>I'm comparing a few approaches right now: wiring Supabase/Clerk into a generated frontend, rebuilding the backend myself, or using a builder that treats Auth + Postgres + policies as first-class pieces.</p>
<p>Disclosure: I'm involved with <span background-color="light-yellow">Enter Pro</span>, and one reason I'm looking at it for this use case is that <span background-color="light-yellow">Enter Cloud</span> includes Auth, Postgres, Storage, Functions, Secrets, and RLS-style infrastructure, while the code remains visible/exportable. That sounds closer to what a real portal needs, but I would still want a dev to review the policies before putting client data behind it.</p>
<p>For people who have actually taken an AI-built portal past the demo stage: what did you do for auth, roles, and tenant isolation?</p>
<p>Did you patch the generated app, layer another backend underneath it, or stop trusting the builder and rebuild the sensitive parts?</p>

<h2>评论设计</h2>
<p><b>User 1</b></p>
<p>My rule is simple: if I cannot test the permission model with curl/Postman, I do not trust the UI.</p>
<p><b>User 2 replies to User 1</b></p>
<p>Same. Clicking around as two users catches maybe half the mistakes. Direct API calls catch the scary ones.</p>
<p><b>User 3 replies to User 1</b></p>
<p>This is why generated apps need seed data for two tenants. Otherwise nobody tests the ugly path.</p>
<hr/>
<p><b>User 1</b></p>
<p>I would be careful with "RLS-style" wording. Either it is enforced at the database layer or it is app code doing checks before queries.</p>
<p><b>User 2 replies to User 1</b></p>
<p>Fair. The useful question is whether a bad query can bypass the policy.</p>
<p><b>User 3 replies to User 1</b></p>
<p>Exactly. If the answer depends on every generated function remembering a `where tenant_id = ...`, that is not enough for me.</p>
<hr/>
<p><b>User 1</b></p>
<p>The builder wars are less interesting than the checklist. Auth, row policies, secrets, logs, deploy rollback. If those are not visible, you are gambling.</p>
<p><b>User 2 replies to User 1</b></p>
<p>And pricing. A lot of these tools get expensive once the portal is not just a demo.</p>
<p><b>User 3 replies to User 2</b></p>
<p>True, but paying more for a tool is still cheaper than explaining a cross-client leak.</p>
<hr/>
<p><b>User 1</b></p>
<p>The hidden-button auth pattern is terrifyingly common.</p>
<p><b>User 2</b></p>
<p>I usually keep the AI-generated frontend and rebuild the backend in a stack I can audit.</p>
<p><b>User 3</b></p>
<p>The phrase "the AI added auth" needs a mandatory follow-up: "where?"</p>
<p><b>User 4</b></p>
<p>I'd add password reset and invite flows to your list. Those are where role bugs show up.</p>

<h1>Post 3: Developer Handoff Checklist</h1>
<p><b>Target Subreddit Name:</b> r/webdev; alternates: r/freelance, r/nocode, r/startups</p>

<h2>Title</h2>
<p>Code export isn't enough: my intake checklist for AI-generated web apps</p>

<h2>Body</h2>
<p>I'm seeing more founders show up with AI-builder apps that "just need a developer to finish the last 10%."</p>
<p>That last 10% is usually not 10%.</p>
<p>Before I would quote or accept one of these handoffs, this is the checklist I'd run.</p>
<p>1. Can it run locally?</p>
<p>I want a repo, install command, env example, dev script, and a working localhost. A zip export is better than nothing, but if the project only lives behind a dashboard button, the handoff is already fragile.</p>
<p>2. What is the auth model?</p>
<p>Who can sign up, who can invite users, who can reset passwords, and how are roles represented? "There is a login page" is not an auth model.</p>
<p>3. Is data isolation enforced below the UI?</p>
<p>Create two test users or tenants. Try to read tenant A's records as tenant B. Do it through the API, not just the app screens.</p>
<p>4. Where are secrets stored?</p>
<p>Search the repo and built bundle for API keys. If the builder put provider keys in frontend code, rotate them before doing anything else.</p>
<p>5. Is deploy reproducible?</p>
<p>Can someone deploy from a clean checkout, or is the production app only reproducible inside the builder's UI?</p>
<p>6. What happens around payments?</p>
<p>If the app has subscriptions or a paywall, verify the webhook and access state. A checkout button is not the same as a working billing system.</p>
<p>7. Do you actually own enough code to maintain it?</p>
<p>Code panel, export, GitHub sync, file tree, readable stack, logs. The point is not "zero lock-in." That is not real. The point is whether a dev can inspect and change the app without fighting a black box.</p>
<p>8. Can you rewind or recover?</p>
<p>Generated code changes fast. If a prompt breaks auth or rewrites half the app, you need a rollback path that is not "prompt again and hope."</p>
<p>Disclosure: I'm involved with <span background-color="light-yellow">Enter Pro</span>, so I'm biased here. The reason it comes up in my checklist is that it is trying to solve this exact handoff shape: browser builder, visible React/Vite/TypeScript/Tailwind code, export/GitHub sync, <span background-color="light-yellow">Enter Cloud</span> for Auth/Postgres/Storage/Functions/Secrets/RLS, and <span background-color="light-yellow">Enter Code</span> for local terminal work. I would still verify every item above by hand.</p>
<p>Curious how other devs price or scope these handoffs. Do you treat AI-builder projects like normal inherited codebases, or do you add a discovery/audit phase before touching anything?</p>

<h2>评论设计</h2>
<p><b>User 1</b></p>
<p>The "can it run locally" test saves so much time. If I cannot get localhost working in under an hour, the quote changes.</p>
<p><b>User 2 replies to User 1</b></p>
<p>Founders hate hearing this because the app looked finished in the browser.</p>
<p><b>User 3 replies to User 1</b></p>
<p>I ask for a README, env example, and seed data before the first call now. Filters out a lot of chaos.</p>
<hr/>
<p><b>User 1</b></p>
<p>Code export helps, but a lot of exported code is still rough. People need to stop acting like source access means maintainable source.</p>
<p><b>User 2 replies to User 1</b></p>
<p>Yep. Source access is the floor, not the finish line.</p>
<p><b>User 3 replies to User 1</b></p>
<p>I'd rather rewrite ugly React than be stuck clicking around a closed dashboard, though.</p>
<hr/>
<p><b>User 1</b></p>
<p>The disclosure makes this read less sneaky, but it still feels close to a product post.</p>
<p><b>User 2 replies to User 1</b></p>
<p>True, but the checklist is vendor-agnostic enough. I'd run the same thing on Lovable, Bolt, Replit, whatever.</p>
<p><b>User 3 replies to User 1</b></p>
<p>The risky part is the comments. OP should not jump in and defend the tool.</p>
<hr/>
<p><b>User 1</b></p>
<p>Payment/webhook state is where "just finish it" turns into two weeks.</p>
<p><b>User 2</b></p>
<p>I add a paid discovery phase for anything generated by an AI builder now.</p>
<p><b>User 3</b></p>
<p>"Login page is not an auth model" should be framed somewhere.</p>
<p><b>User 4</b></p>
<p>Also check license/package weirdness. Some exports pull in random dependencies nobody noticed.</p>

<h1>Post 4: Browser Builder Plus Local Terminal Split</h1>
<p><b>Target Subreddit Name:</b> r/vibecoding; alternates: r/webdev, r/startups, r/freelance</p>

<h2>Title</h2>
<p>Has anyone kept a browser AI builder + local dev workflow alive past the prototype?</p>

<h2>Body</h2>
<p>Question for teams doing AI-assisted product work with mixed technical ability.</p>
<p>Has anyone kept a split workflow alive past the prototype stage?</p>
<p>The pattern I mean:</p>
<p>1. non-technical founder/PM/ops person builds screens and simple flows in a browser AI builder</p>
<p>2. developer takes over when auth, data model, edge cases, tests, or deploy complexity show up</p>
<p>3. code needs to move into a real repo without becoming a frozen export nobody wants to touch</p>
<p>In theory this split makes sense. The non-dev person can move faster on product shape, and the dev does not spend a week turning vague screen descriptions into UI.</p>
<p>In practice, I worry about the handoff boundary:</p>
<p>Is the exported code readable enough to maintain? Does GitHub sync become the actual source of truth, or just a one-time zip? Can the browser side and local side coexist, or does the project eventually fork? Who owns schema/auth decisions when the browser tool made the first version? At what point should the browser builder become "prototype only" and the dev side take over?</p>
<p>Disclosure: I'm involved with <span background-color="light-yellow">Enter Pro</span>, and this is one of the workflows I'm trying to understand better. <span background-color="light-yellow">Enter Pro</span> is browser-based, has a visible code panel/export/GitHub sync, and <span background-color="light-yellow">Enter Code</span> is the local terminal agent side. That sounds promising for a clean handoff, but I do not want to oversell it as live magic. A git bridge still needs discipline.</p>
<p>If your team has tried this kind of browser + local split, where did it break?</p>
<p>Was it merge conflicts, unclear ownership, bad generated code, backend assumptions, or just communication?</p>

<h2>评论设计</h2>
<p><b>User 1</b></p>
<p>The split works until both people edit the same abstraction. UI copy changes are fine. Auth or schema changes need one owner.</p>
<p><b>User 2 replies to User 1</b></p>
<p>This. We ended up with a rule: browser person can change screens, dev owns data model and permissions.</p>
<p><b>User 3 replies to User 2</b></p>
<p>That rule sounds obvious, but it would prevent half the disasters in this category.</p>
<hr/>
<p><b>User 1</b></p>
<p>GitHub sync is not a workflow by itself. You still need branching, review, and an agreement on what gets pushed back into the builder.</p>
<p><b>User 2 replies to User 1</b></p>
<p>Exactly. A clean export is useful, but it does not solve product ownership.</p>
<p><b>User 3 replies to User 1</b></p>
<p>I like browser builders for getting stakeholders unstuck. I do not like them as the long-term source of truth.</p>
<hr/>
<p><b>User 1</b></p>
<p>This is why I usually say "prototype in whatever, rebuild the app when real users show up."</p>
<p><b>User 2 replies to User 1</b></p>
<p>That is clean from a dev perspective, but a lot of startups cannot afford the full rebuild right when users show up.</p>
<p><b>User 3 replies to User 2</b></p>
<p>Then the handoff audit matters. You have to know which parts can survive and which need rewriting.</p>
<hr/>
<p><b>User 1</b></p>
<p>The best version I've seen was browser for mockups, local repo for everything after the first customer.</p>
<p><b>User 2</b></p>
<p>If the non-tech person cannot explain the data model, no tool fixes that.</p>
<p><b>User 3</b></p>
<p>I would require a changelog after every browser edit. Otherwise the dev opens the repo and plays archaeology.</p>
<p><b>User 4</b></p>
<p>The risk is not the browser builder. The risk is everyone thinking the browser builder removed the need for engineering decisions.</p>

<h1>Post 5: Existing Codebase Prompt Drift</h1>
<p><b>Target Subreddit Name:</b> r/ClaudeAI; alternates: r/vibecoding, r/cursor, r/webdev</p>

<h2>Title</h2>
<p>Vibe coding on an existing codebase: how do you stop context drift across parallel features?</p>

<h2>Body</h2>
<p>Greenfield AI coding is a completely different game from editing an existing codebase.</p>
<p>When the app is small and the feature is isolated, the model can feel unreal. You describe a screen or endpoint, it builds the thing, you tweak it, done.</p>
<p>Then the repo has history.</p>
<p>Feature A established a naming pattern. Feature B touches the same schema. Feature C needs auth changes. A previous prompt tried an approach and you backed it out. Half of the important context is not in the current files; it is in decisions you already made.</p>
<p>This is where I keep seeing drift:</p>
<p>1. one long chat turns into a junk drawer of old assumptions</p>
<p>2. a fresh chat loses the reasons behind prior decisions</p>
<p>3. the agent "fixes" something by undoing a trade-off you intentionally made</p>
<p>4. docs like CLAUDE.md help, but they go stale unless they are maintained</p>
<p>5. parallel features bleed into each other unless you isolate them</p>
<p>What workflows are actually holding up for people?</p>
<p>I've seen a few approaches: one session per feature, docs split into architecture/conventions/current task, git worktrees for code isolation, read-only planning before edits, and stricter review gates around shared files.</p>
<p>Disclosure: I'm involved with <span background-color="light-yellow">Enter Pro</span>, and its Plan Mode is one example of that read-only planning pattern. I do not think planning mode magically prevents drift. The useful part is that the plan is visible before the edit happens, so you can catch wrong assumptions earlier.</p>
<p>For people using Claude/Cursor/terminal agents on non-trivial repos: what is your setup for keeping context clean across multiple features?</p>
<p>Do you maintain docs manually, make the agent update them, or just reset context aggressively and rely on tests?</p>

<h2>评论设计</h2>
<p><b>User 1</b></p>
<p>One session per feature helped me, but only after I started writing a handoff note at the end of each session.</p>
<p><b>User 2 replies to User 1</b></p>
<p>Same. The handoff note needs to include what was rejected, not just what changed.</p>
<p><b>User 3 replies to User 2</b></p>
<p>"Why not this approach" is the missing piece in most AI-written docs.</p>
<hr/>
<p><b>User 1</b></p>
<p>Worktrees solve code isolation, not context isolation. People conflate those.</p>
<p><b>User 2 replies to User 1</b></p>
<p>Yep. You can have a clean branch and still have the agent hallucinate a schema from yesterday's chat.</p>
<p><b>User 3 replies to User 1</b></p>
<p>The branch protects the repo. It does not protect the reasoning.</p>
<hr/>
<p><b>User 1</b></p>
<p>The planning step works until you get impatient and skip reading it.</p>
<p><b>User 2 replies to User 1</b></p>
<p>Painfully true. The tool can write the plan; it cannot make you review the plan.</p>
<p><b>User 3 replies to User 1</b></p>
<p>I approve plans too quickly when the change looks small. Those are usually the ones that hit shared files.</p>
<hr/>
<p><b>User 1</b></p>
<p>Splitting CLAUDE.md into multiple docs helped more than making one giant file.</p>
<p><b>User 2</b></p>
<p>I tell the agent to update an "assumptions ledger" after every meaningful change.</p>
<p><b>User 3</b></p>
<p>The failure mode is not forgetting code. It is forgetting intent.</p>
<p><b>User 4</b></p>
<p>Tests are the only thing that keep me honest. Docs drift too.</p>

<h1>Post 6: Defensive Workflow Guardrails</h1>
<p><b>Target Subreddit Name:</b> r/vibecoding; alternates: r/ClaudeAI, r/cursor, r/webdev</p>

<h2>Title</h2>
<p>Vibe coding does not need less speed. It needs more rails.</p>

<h2>Body</h2>
<p>The failure mode I keep seeing with vibe coding is not "the AI cannot write code."</p>
<p>It can write plenty of code.</p>
<p>The failure mode is that the project slowly loses its rails. The agent changes patterns between sessions, forgets why a decision was made, invents a new abstraction next to an old one, and the human only notices after the repo feels heavy.</p>
<p>The guardrails I would put in place from day one:</p>
<p>1. One feature, one session.</p>
<p>Don't let bug fixes, UI tweaks, auth changes, and schema edits live in the same endless chat. You are saving context in the short term and creating ambiguity in the long term.</p>
<p>2. Require a read-only plan before edits.</p>
<p>Scope, assumptions, files likely to change, risks, test plan. Written down before code changes. If the plan sounds wrong, stop there.</p>
<p>3. Keep project memory in files, not vibes.</p>
<p>Architecture notes, conventions, rejected approaches, current sprint notes. Make future sessions read the relevant docs before editing.</p>
<p>4. Snapshot before risky prompts.</p>
<p>Git commit, branch, worktree, whatever. The exact tool matters less than having a fast escape route when the agent "helpfully" rewrites the wrong layer.</p>
<p>5. Review diffs for structure, not every line.</p>
<p>You cannot manually re-derive every generated function. Look for architecture shifts, new dependencies, auth/data boundary changes, and duplicated patterns.</p>
<p>Disclosure: I'm involved with <span background-color="light-yellow">Enter Pro</span>. The relevant product angle is that <span background-color="light-yellow">Enter Pro</span> has a read-only Plan Mode and code visibility/export/GitHub sync, and <span background-color="light-yellow">Enter Code</span> can be part of the local handoff. That can support the workflow above, but it does not replace tests, reviews, or judgment.</p>
<p>What would you add?</p>
<p>The one case I still find hard is a feature that touches four systems at once: UI, data model, auth, and background jobs. Do you split it across sessions or keep it together so the agent sees the whole thing?</p>

<h2>评论设计</h2>
<p><b>User 1</b></p>
<p>"Keep project memory in files, not vibes" is the whole thing. The model cannot preserve decisions you never wrote down.</p>
<p><b>User 2 replies to User 1</b></p>
<p>The best docs are the ones that say why a path was rejected. Otherwise the agent rediscovers the bad path later.</p>
<p><b>User 3 replies to User 2</b></p>
<p>I keep a `decisions.md` now. Ugly file, saves hours.</p>
<hr/>
<p><b>User 1</b></p>
<p>If you need this many guardrails, maybe the tooling is not mature enough for anything serious.</p>
<p><b>User 2 replies to User 1</b></p>
<p>Maybe, but humans need guardrails too. Branches, tests, code review, tickets. This is the AI version of normal engineering discipline.</p>
<p><b>User 3 replies to User 1</b></p>
<p>The problem is people expected AI coding to remove process. It mostly makes process more important.</p>
<hr/>
<p><b>User 1</b></p>
<p>The read-only plan is underrated. It catches wrong assumptions before they become a 600-line diff.</p>
<p><b>User 2 replies to User 1</b></p>
<p>Only if you actually read it. I started skipping plans for "small" changes and that is where the mess came from.</p>
<p><b>User 3 replies to User 2</b></p>
<p>Same. Small changes touching shared auth code are never small.</p>
<hr/>
<p><b>User 1</b></p>
<p>I'd add "make the agent write tests before implementation" but I know that starts a fight.</p>
<p><b>User 2</b></p>
<p>Worktrees are the boring answer. Boring is good.</p>
<p><b>User 3</b></p>
<p>Reviewing diffs for architecture shifts is a useful framing. I waste too much time reading generated helper functions.</p>
<p><b>User 4</b></p>
<p>The four-systems-at-once feature is where I usually write the spec myself and let the agent do smaller chunks.</p>

