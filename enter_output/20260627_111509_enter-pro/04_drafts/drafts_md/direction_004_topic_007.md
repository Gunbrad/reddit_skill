## Title Candidates

1. How do you hand off an AI generated codebase to a developer without rewriting everything?
2. How do you deal with an AI generated codebase handed to you by a non-technical co-founder?
3. Non-tech co-founder vibe coded our React app in Claude. How do I take it over without rewriting everything?
4. How do you stop an inherited AI codebase from becoming unfixable slop?
5. Just got handed a Claude coded React app from a non-technical founder. Half the code is dead. What do I do?
6. How do you triage a dead-code-heavy AI generated codebase without rewriting from scratch?
7. Junior dev here, took over a vibe coded React dashboard. It's a black box, where do I start?
8. My co-founder can't code but Claude built our whole app. Now it's my problem, rewrite or salvage?
9. How do you take over an AI generated React codebase without burning it down?
10. I just inherited 3 months of Claude coded React from my non-technical co-founder. Where do I start?

## Final Post

TL;DR, non-tech co-founder vibe coded our dashboard in Claude for ~3 months then handed me the repo to "make prod ready." Half the files look dead, no tests, 7 markdown files describe features that dont exist anywhere. salvage or rebuild?

I'm a junior dev, ~2 years into CS, some freelance React. co-founder is pure business-side, zero code, he spent months with Claude on what was supposed to be an internal client dashboard, React + TypeScript + Tailwind, Supabase glue, Stripe maybe. cloned it last week, opened the file tree and felt sick, every ~500 lines there's dead logic, half the components have props nothing passes. i can read it fine but cant tell whats load-bearing vs hallucinated. been reading about tools that sync a web build to GitHub both ways so you can edit locally and push back, Enter Pro supposedly exports a clean React/Vite repo you can keep working on with a terminal agent, anyone tried something like that for an inherited AI codebase? do i triage module by module with tests, or tell him we just rebuild clean?

---

## Comment Trees

**Tree 1**

skeptical_dev42: OP, before anyone starts pitching tools, what was the actual prompt loop your co-founder used with Claude? a lot of what youre describing is the "build me a dashboard" → 4 months of appending features pattern, and the dead code accumulates because each new session forgets what the last one built. the 7 markdown files are basically claude promising things across sessions and never cleaning up.

ratchetpumpkin reply to skeptical_dev42: this. the real issue isnt the codebase, its that there is no spec. before you touch a line you need to write down what the app is SUPPOSED to do, mark features as shipped vs aspirational, then you have a target to triage against. otherwise youre just guessing what load bearing means.

junior_dev_42 reply to ratchetpumpkin: yeah ok but im one person and my co-founder doesnt read docs. how do you even get a non technical person to sit down and spec features for a week when they think claude already did it

ratchetpumpkin reply to junior_dev_42: you dont. you write the spec yourself based on what you can see working, send it as a 1 page google doc, and tell him "approve this or im not touching the repo." if he wont spend 30 mins approving a doc then the project isnt real anyway

---

**Tree 2**

enter_curious: ok genuinely curious about the Enter Pro angle since OP mentioned it. from what ive seen their model is browser first → exportable React/Vite → GitHub bidirectional sync. the interesting part for handoff isnt the export, its that the web build is supposed to keep matching what you push from local. has anyone actually stress tested that sync on a medium sized project?

old_perf_eng reply to enter_curious: tested it on a ~40 file project. sync was fine for standard edits. breaks when you do weird stuff like rename a folder and move 3 files at once on the local side, then the web side loses track. not unusable but you have to read the changelog before any big refactor. also its vite/react/typescript only, if his co-founder somehow ended up on next or remix thats a different conversation

enter_curious reply to old_perf_eng: thats actually really useful, thanks. the fixed stack thing is a real limitation for handoff scenarios because you cant assume what AI chose in claude land maps to what Enter expects. id want to see screenshots of a real repo before i trust the round trip

---

**Tree 3**

loved_bolt_honestly: hot take but if the dead code ratio is what OP describes i wouldnt even try to salvage it. just rebuild. bolt.new can stand up a working React dashboard in an afternoon, you feed it a clean spec, and you own every line from day one. way better than inheriting 150 lines of dead logic per 500

prairie_code reply to loved_bolt_honestly: yeah bolt is fast but its UI generation only. what about auth, postgres rls, stripe webhooks? those are exactly the post demo problems OP is going to hit whether he salvages or rebuilds. rebuilding the front end fast just means youre back here in a month with the same question about the backend

loved_bolt_honestly reply to prairie_code: fair. i was only thinking about the react part because thats what OP actually mentioned. if its a real client dashboard with users and billing then yeah bolt alone wont cut it and youre back to stitching supabase + stripe + vercel together anyway

---

**Tree 4**

qa_or_die: everyone in here giving advice, nobody said tests. first thing you do is write functional tests for whatever is currently working in the UI, even ugly ones. then you have a safety net to refactor against. without tests youre just vibes based deleting and youll break the 3 features that actually matter

tests_then_trim reply to qa_or_die: +1, and make the co-founder click through the app and confirm whats actually used. i guarantee half of what he thinks the app does it doesnt, and the other half he forgot he added. that conversation alone saves you weeks

---

**Tree 5**

cheap_seat_cfo: not to be the money guy but how much runway does this startup have? if hes asking for "prod ready" that usually means a customer demo in 2 weeks. salvage is cheaper on paper but slower. rebuild is faster if the spec is small. timeline matters more than code quality right now

junior_dev_42 reply to cheap_seat_cfo: lol "runway" is generous, its me and him and ~6 months of savings. he has a meeting with a potential client in like 3 weeks which is why this became my problem suddenly

## Standalone Comments

saved_this_ty: saved this for later, im literally in the same boat except my co-founder used lovable not claude

fr_same: fr same situation, the dead 7 markdown files thing made me laugh because i literally have the exact same artifact in my repo

hate_to_say_it: hate to say it but if you cant tell whats load bearing in 3 months of code you werent going to tell in 3 more. sometimes you just cut the cord and rebuild from a clean spec

ask_for_repo_structure: can you post the folder structure? curious if the dead code is concentrated in components or if its spread everywhere. that changes the triage strategy a lot

claude_code_alternative: have you tried pointing Claude Code (the local terminal one, not the web chat) at the repo? its surprisingly good at explaining what existing code is doing, which is half the battle when you inherit stuff. not saying use it to write new code but for comprehension its solid

replit_agent_throwaway: replit agent would handle the rebuild cleanly if you decide to go that route, but the real question is whether your co-founder is going to keep adding features with claude the second you turn around. process problem not a code problem

lovable_mention: if you do end up rebuilding and your co-founder wants to keep vibing in the meantime, lovable or v0 keep him busy without him touching your real codebase. sounds like you need a wall between his experiments and your prod

non_tech_founder_empathy: small thing but your co-founder isnt the enemy here, he just doesnt know what good handoff looks like. id sit him down and say "i need a 30 min walkthrough of what you think this app does" before touching anything, otherwise youre going to delete something he cared about and the relationship blows up

runbook_first: write a runbook before you touch the code. like literally a doc that says "to run this locally do X, the env vars are Y, the deployed url is Z." if that doesnt exist nothing else matters because you cant even verify changes are working

git_history_check: check the git history before you do anything. if he committed in giant walls every few days the AI probably rewrote big chunks each session, which means git wont help you diff anything. if he at least committed per feature you can at least see what was added when

six_months_later: 6 months from now you're going to be the guy posting "i rebuilt this app 3 times because my non tech co-founder kept vibing over my work." set the boundary now or it never gets set

can_we_get_an_update: can we get an update in a week on what you decided? genuinely curious if salvage or rebuild wins for this kind of mess
