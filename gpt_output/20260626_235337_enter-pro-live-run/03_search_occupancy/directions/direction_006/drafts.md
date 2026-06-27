# Search Occupancy Drafts

## Title Candidates

1. vibe coding on existing codebases is a nightmare, how do you stop prompt drift across multiple features?
2. 6 months of vibe coding and my codebase is basically unmaintainable. here's where the drift started
3. anyone else's vibe-coded project become untouchable once you add a second feature in parallel?
4. how do you actually manage context when claude is juggling 3 features in one codebase
5. my codebase isn't broken, it just drifted. vibe coding + parallel features is a mess
6. the codebase is unmaintainable and it's not the AI's fault, it's the workflow. anyone fixed this?
7. vibe coding prompt drift is real. is there a workflow that survives past month 2 on an existing codebase?
8. existing codebase, multiple features in flight, agent keeps losing the "why". what worked for you?

## Final Post

first 4 weeks on this project were magic. greenfield, single feature, prompt to ship in an afternoon. everything one-shotted, everything worked.

then i added a second feature. the model that shipped feature 1 in a day now looks at the repo like it's never seen it. renames a function i already named, "fixes" a bug by reverting something we shipped last month, breaks auth while adding a settings page.

two things are killing me.

1) parallel features. keep everything in one chat and feature A's decisions bleed into feature B, the agent "remembers" a schema we never agreed on. open a new chat and i spend half the session re-explaining the project, the conventions, what's already been tried.

2) assumption drift. the AI keeps losing the why behind each piece. CLAUDE.md helps a little but it's static, it doesn't update as the project changes, and the agent goes off and reinvents decisions we already settled.

git worktrees help for code isolation but they don't solve the conversation context problem. i tried smaller scoped sessions with a read-only planning pass first (scope, assumptions, steps before any edits), enter pro's plan mode is one version of this, and isolating one feature per chat session. for stuff that touches shared files i've been switching to a local terminal agent like enter code instead. not a silver bullet, just less bleed.

so my real question is, when you're past the demo stage and you actually have revenue and users on a vibe-coded product, how are you keeping the codebase maintainable without slowing down to manual dev speed? anyone got a workflow that holds up past month 2, or is the rewrite at month 6 basically inevitable?

---

## Comment Trees

**Tree 1: Multi-session separation**

user1: this is pretty much exactly where im at. parallel features in one chat is genuinely a disaster, the agent just merges everything into one big mush of context

user2 reply to user1: same. i split by feature now, one chat per feature, and i keep a CLAUDE.md at the repo root with the architecture decisions and the "dont do this" list. its not perfect but its the only thing that hasnt bit me

user1 reply to user2: how big is your CLAUDE.md though? mine keeps growing and im worried the agent is gonna start ignoring half of it

user2 reply to user1: i split it. architecture.md, conventions.md, current-sprint.md. then i tell the agent to read the relevant one at the start of each session. keeps the blast radius smaller

user3 reply to user2: this is basically what i do too. the trick i found is to make the agent write those docs itself as it goes, not me maintaining them by hand. otherwise they go stale in a week

---

**Tree 2: Claude Code vs Cursor comparison**

user1: if youre on an existing codebase and juggling multiple features, have you tried claude code in the terminal? i bounced off cursor for the same reason you described, the chat just becomes a junk drawer

user2 reply to user1: claude code is way better for this imo. the per-feature sessions actually feel isolated. cursor sessions all share too much implicit state for my taste

user3 reply to user2: counterpoint, i ran into hard API limits on claude code way faster than i expected. cursor is more predictable cost-wise for me

user2 reply to user3: yeah the rate limits are real, i hit them on a 2 hour session last week. its annoying but the workflow itself is still better for what the op is describing

user4 reply to user1: bolt and lovable were not even in the same conversation for me. theyre great for greenfield, the second you have a real repo they get in the way

---

**Tree 3: The "skill issue" skeptic**

user1: not gonna lie, half of this is a skill issue. if youre letting the agent make schema decisions on the fly across features, of course it drifts. you need to lock the schema and conventions first, then let it build features against that contract

user2 reply to user1: easier said than done when you're a solo founder. i dont have a senior dev sitting next to me to design the schema. thats the whole point of using the agent

user1 reply to user2: then you spend 2 days writing the spec yourself, not the agent. the agent implements, you design. otherwise you get exactly the mess in the op

user3 reply to user1: i agree with the principle but "just write the spec" kind of ignores why people are using vibe coding in the first place. if i could write a full spec i wouldnt need the agent

---

**Tree 4: Plan Mode / read-only planning discussion**

user1: the read-only planning step changed things for me. scope, assumptions, steps, then i approve, then it edits. catches like 60% of the drift before it happens because the agent has to commit to a plan first

user2 reply to user1: enter pro's plan mode does basically this, lists scope/assumptions/steps before touching code. its not a magic fix but the plan is reviewable which is the whole point

user3 reply to user2: tried it. helpful for the first feature, by feature 5 i was skipping it to save time and thats when everything broke. its a discipline problem not a tool problem

user2 reply to user3: yeah fair. the plan only helps if you actually read it. i got lazy once and approved something the agent clearly didnt understand, that was a 3 hour revert

---

**Tree 5: The "just rewrite it" camp**

user1: honestly at month 6 the answer is usually rewrite. the tech debt compounds faster than you can pay it down with vibe coding

user2 reply to user1: unless you have users and revenue, in which case you cant just rewrite. the ship has sailed

user1 reply to user2: then you pay someone to incrementally refactor while the AI keeps shipping features in a frozen "do not touch" section. its not fun but it works

user3 reply to user2: this is the part nobody talks about. the op's whole point is that vibe coding gets you to revenue fast and then the cleanup is the nightmare. theres no clean answer

## Standalone Comments

user1: saved this thread, im literally in the same spot with feature B right now and the agent just "forgot" our auth pattern from feature A

user2: the parallel features problem is the real one. single feature vibe coding still feels like magic to me, the moment i added a 2nd one everything went sideways

user3: the cleanup is a nightmare is so real. generation is fast, maintenance is impossible, this is basically the whole vibe coding arc in one sentence

user4: anyone else find that the agent does fine until you cross like 30-40 files, then it just starts guessing at how your code is organized? feels like a context window thing more than a workflow thing

user5: hot take but i think lovable and bolt are worse for this than cursor because they hide the code from you. the second you cant see the repo you cant steer the agent

user6: the multi-session isolation thing is the part i keep underestimating. i kept forcing everything into one mega-session because i didnt want to lose context, that was a mistake. one feature per chat, doc handoff between them

user7: this is exactly why i moved to a local terminal agent. browser-based tools make it too easy to just keep prompting without a plan, the friction of opening a terminal slows me down in a good way

user8: not the AI's fault its the workflow, agreed. but the workflow is the hard part. nobody ships a CLAUDE.md and architecture.md for a side project, you just wanna build the thing

user9: fr the part about "tried to refactor it myself last week, gave up after 2 hours" hit me in the chest. same exact experience on a bolt project

user10: for the people saying "just write a better spec", thats not wrong but it ignores the actual value prop of vibe coding. if writing the spec took 2 days i wouldnt be vibe coding, id just be coding

---

## Title Candidates

1. Vibe coded for 4 months. My codebase is basically untouchable.
2. Anyone else's vibe-coded codebase become unmaintainable after a few sessions?
3. Vibe coding codebase unmaintainable? 5 things I do now to keep the agent oriented
4. 4 months of vibe coding and prompt drift almost killed my MVP
5. How to keep a vibe-coded codebase from drifting into the trash (5 habits I wish I started with)
6. The point of no return on a vibe-coded project, and the 5 guardrails I use now
7. What I wish someone told me before I let the agent ship 200 commits to my MVP
8. 6 months of vibe coding taught me: you don't have a drift problem, you have a rails problem
9. If vibe coding ruins codebases, why am I still shipping in 2026?
10. Anyone else hitting the point of no return on a vibe-coded SaaS?

## Final Post

Shipped a vibe-coded MVP in February. By April, every new prompt from the agent either broke something else or invented a pattern I never approved. Refactored 3 times, rewrote once, shelved the whole thing. The agent wasn't broken, I just never gave it a way to stay oriented as the codebase grew.

After that project died I sat down and wrote out the rules I should've been using from week one. half checklist, half wish I'd done this earlier:

1. never stack features in one session. open a fresh thread per feature. the moment context bleeds, contradictions start piling up.
2. force a read-only plan before any build. scope, assumptions, steps, in writing, saved to disk, committed to git. I won't let an agent touch code until I've seen the plan first. Enter Pro's Plan Mode is the cleanest version of this I've used, a custom instruction in Cursor gets you halfway there.
3. keep a /docs folder the agent writes to itself. architecture notes, completed task summaries, what I tried and abandoned. future sessions actually read it.
4. snapshot before every prompt. I use Enter Code locally for the git rewind, others swear by worktrees. either way you need a one-click escape when the agent goes sideways.
5. review the diffs, not the file. you can't read everything, catch the structural breaks, trust the granular functions until they misbehave.

generated code still needs a human reading it, that part isn't changing. these 5 habits are the difference between a codebase I can keep shipping on and one I abandon by month four. I currently evaluate Enter Pro / Enter Code for parts of my workflow, mentioned above as one option among others.

what's missing from this list. specifically interested in how people handle the part where you need to add a feature that touches 4 unrelated systems at once, thats the one that still wrecks me.

---

## Comment Trees

**Tree 1**

user1: saved this, the /docs folder one is what I wish I started doing 6 months ago. how do you keep the agent from writing garbage documentation tho. mine just ends up restating what the code does in the most obvious way possible
user2 reply to user1: honestly the trick for me was telling it explicitly "write this for a future agent session that has zero context, assume they have never seen this codebase." otherwise yeah it just paraphrases the function names
user3 reply to user2: this. I also tell mine to document the WHY not the WHAT. what was the constraint, what did you reject, whats the next thing you'd build. changed everything

**Tree 2**

user1: been using Lovable for about 8 months and the drift problem is exactly why I stopped adding features. every new prompt I open I basically pray. is Enter Pro actually better at this or is it the same trap with better marketing
user2 reply to user1: different problem space tbh. Lovable is great for the first demo, the moment you need auth, database rules, webhook state, it falls apart. Enter Pro covers more of that post-demo infra but its not magic, you still have to review what it ships
user1 reply to user2: yeah thats fair. the "review what it ships" part is what kills me on these tools. feels like the AI moves 10x faster than I can verify

**Tree 3**

user1: hot take but I think the multi-session thing is overblown. I've shipped a 40k line vibe-coded app in a single conversation by just being aggressive about /clear and a CLAUDE.md that I update weekly. the real problem is people letting the context window fill up with old failed attempts
user2 reply to user1: 40k lines in a single session? what model. I hit context limits way before that on Sonnet
user1 reply to user2: Opus 4 mostly, and I do a lot of "summarize what we've done so far into a doc, then /clear" loops. its annoying but it works

**Tree 4**

user1: this list is good but its missing the testing piece. none of this matters if you cant actually run the code and see what broke. how are you all handling test coverage on a vibe-coded project where the agent keeps changing the architecture
user2 reply to user1: yeah this is the one I never see people talk about. I tried getting Cursor to write tests and it just writes tests that test the implementation, not the behavior. so when the implementation changes the tests still pass
user3 reply to user2: same. I gave up on unit tests and just do manual smoke tests before each commit. its slower but at least I know it works

**Tree 5**

user1: the git rewind habit saved me last week. agent decided to "refactor" my entire auth layer at 2am and I didnt notice until morning. one rewind later, back to a working state. genuinely dont know how people ship without this
user2 reply to user1: fr. I started doing this after losing a weekend to a bad merge. worktrees also work but the rewind UX is faster

## Standalone Comments

user1: point 2 is the big one. plan mode in Enter Pro is the only thing that stopped my agent from inventing fake APIs that dont exist in my stack

user2: can confirm the /docs thing works. I have a /Architecture folder the agent updates at the end of every session, onboarding new sessions takes like 2 minutes now instead of 30

user3: 4 months in and my codebase is exactly where yours was. the contradiction problem is real, files that import from each other in ways that make no sense. going to try the plan mode thing this week

user4: tbh I think the entire vibe coding space is in a weird spot rn. tools like Lovable and Bolt are amazing for the first 2 weeks then become liability. not sure anyone has actually solved the long-term maintenance problem yet

user5: how does this compare to just using Claude Code in a terminal with a good CLAUDE.md. I feel like the browser builders are solving a problem I dont have

user6: the review the diffs not the file tip is underrated. I spent so much time reading every file before realizing I was never going to catch the structural issues that way

user7: counterpoint: if you need 5 defensive workflows to use a tool maybe the tool isnt ready. I say this as someone who shipped a 6 figure vibe-coded SaaS, but I also rewrote it twice

user8: Enter Code rewind is genuinely the best part of that whole stack. I use it 3-4 times a week minimum

user9: this is the post I needed 3 months ago. the "agent invents patterns I never approved" line hit hard

user10: what does your /docs folder actually look like in practice. I keep starting one and abandoning it after 2 weeks because the agent stops referencing it
