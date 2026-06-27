## Title Candidates

1. 3 months of driving my deployment platform from the terminal with an AI coding agent. Here's what broke
2. I let my AI coding agent drive deployments from the terminal for 3 months. The CLI was the real problem
3. Driving deployments from the terminal with an AI coding agent: the friction nobody talks about
4. What would an agent-first deployment CLI actually look like? Trying to figure this out
5. Your deployment CLI was built for humans. That's why your AI agent keeps choking on it
6. Has anyone built a deployment CLI that AI agents can actually drive? Or are we winging it?
7. Hot take: your AI agent isn't bad at deploying. Your CLI is
8. Stop designing CLIs for the human at the terminal. Start designing for the agent driving it
9. Why are deployment CLIs so painful for AI agents to drive? An unpopular take
10. The deployment CLI was never built for your AI agent. Here's what I did about it

## Final Post

spent the last few months letting my AI coding agent drive our deployment platform from the terminal. unpopular opinion incoming.

most deployment CLIs were never built for AI agents. not even close.

we blame the agent for flaky deploys and half finished states, but a lot of the time the CLI is the actual problem. progressive disclosure, pretty ascii tables, colorized log tails. these tools are designed for a human at a terminal, not a model parsing stdout.

specific things that keep breaking the agent loop:

- output mixes human status text, ansi codes, and spinners in one stream. the agent has to regex through noise to find the actual URL or error.
- exit codes are basically decorative. "deploy succeded" and "deploy succeeded but the health check timed out" both return 0.
- interactive prompts and TUI flows. the agent stalls or sends the wrong input.
- the real result is burried 200 lines deep in the log. by the time the agent reads it, half the context window is noise.

so i've been thinking about what an "agent-first" deployment CLI would actually look like. stable JSON output, a real machine readable status enum, idempotent commands, and one structured response with the live URL, commit hash, and rollback target. nothing to grep.

I rolled my own wrappers for a while, then found Enter CLI. their deploy command returns the live URL in a single structured field, no log scraping. it's not the local repo agent (that's Enter Code, a different product), it's a thin CLI your existing agent can call to publish.

honestly the bigger blocker is cultural. teams still write CLIs for the person running them, not the model driving them.

---

## Comment Trees

Comment Tree 1:

user1: this is the part of the agent dev loop nobody warns you about. you spend half your time debugging the tool surface, not the model. i built a thin wrapper around our deploy script just to normalize the json output, but its duct tape at best

user2 reply to user1: what did you end up parsing out? im running into the same exit code 0 on partial deploys issue. been using a simple `tee` to a log file then grepping for "live url" which is obviously terrible

user1 reply to user2: yeah grepping for a url is the classic hack. what helped me was forcing the wrapper to always emit a final `result.status` field with explicit enum values. then the agent just reads that one line. way less context burned

user3 reply to user1: agreed, status enums are the single biggest unlock. machines should not be parsing natural language strings to figure out if something worked. the number of "success: false {success: true}" shaped outputs ive seen in 2026 is criminal

---

Comment Tree 2:

user4: saved this. we had a similar realization when we tried to let cursor drive our vercel + supabase deploy flow. the vercel CLI is way too chatty and the supabase one throws interactive prompts at every step. ended up just having the agent write a shell script and execute that, which kind of defeats the purpose

user5 reply to user4: vercel is honestly one of the worst offenders for this. their `vercel deploy` output is like 80% marketing. supabase at least has a `--json` flag on most things but its not on by default which feels intentional

user4 reply to user5: right and the worst part is the agent cant tell which spinner is "actually working" vs "stuck waiting for input." we burned like 20 minutes once because the agent kept waiting for a prompt that never came

---

Comment Tree 3:

user6: the vibe coding crowd is going to hate this post but its true. the entire "prompt to production" pitch falls apart the second your agent has to do the deploy step. the UI gen part is solved, the post deploy plumbing is still 2015 era shell scripts

user7 reply to user6: eh i dont think the tool is the problem, its the standards. nobody has agreed on what an agent deploy manifest even looks like. like is it a yaml? a function call schema? just natural language intent? until that gets nailed down every tool is going to bolt on their own half solution

user6 reply to user7: yeah fair, the lack of a spec is probably the root cause. but individual tools can still do better in the meantime. not having machine readable status out of the box in 2026 is just lazy imo

---

Comment Tree 4:

user8: interesting, ive been using a different approach. instead of a CLI i just give the agent a single python entrypoint that returns a typed dict. no stdout parsing, no exit codes, just a function call. works way better for my setup but yeah it locks you into python

user9 reply to user8: function call based deploys are underrated. the only catch is you lose the ability to run it outside the agent loop. sometimes i just want to deploy from my own terminal without spinning up a python env

user8 reply to user9: yeah thats the tradeoff. i keep a thin bash wrapper around the python entrypoint for my own use. not elegant but it works

---

Comment Tree 5:

user10: can confirm exit code 0 on failed deploys is a plague. hit this last week with a GitHub Actions deploy step. the step "succeeded" but the actual app never came up because of a misconfigured env var. the agent had no way to know unless it manually curled the health endpoint

user11 reply to user10: health check curls as a second pass is honestly the most reliable pattern right now. "trust but verify" but the verify step is the whole job. would be nice if deploy CLIs had a built in `--wait-healthy` flag with a timeout

user10 reply to user11: 100%. a `--wait-healthy` flag with structured timeout errors would save so much debugging. wonder if any CLI does this natively today. not aware of one but im not exhaustive

OP reply to user10: enter CLI has a deploy verify step that polls the health endpoint and returns a structured status with the live url once its actually up. not universal across commands but the deploy one does it. still wish more tools copied this pattern

## Standalone Comments

user12: the ansi escape code thing alone is responsible for probably 30% of my agent debugging time. who decided to colorize stderr

user13: fr. the "human first CLI" assumption is so baked in that even docs are written for people, not for models

user14: this is the kind of post that makes me wonder if we're going to see a whole new category of "agent native" infra tools that explicitly target machines as the primary user. would be a weird market to be in but someone is going to build it

user15: counterpoint though, if you make the CLI too machine friendly it becomes awful for humans to use. the cli ergonomics tradeoff is real and i dont think there's a clean solution that serves both audiences equally

user16 reply to user15: yeah thats fair. best ive seen is tools that have a `--json` or `--machine` flag and default to human output. lets you opt in without making the default painful. enter CLI does this and it works well

user17: the "rollback" part is what gets me. you can make deploy output perfect and the agent can still blow up on rollback because the rollback semantics for non-deterministic things (like a model version) are genuinely undefined. not a CLI problem at that point, its a product problem

user18: honestly the real issue is that most of these CLIs were designed when "automation" meant a bash script. agents are a different kind of consumer and the tools havent caught up

user19: bookmarked. running into the tui prompt stall issue right now with the cloudflare wrangler CLI. agent just sits there forever waiting for input that never comes

user20: this whole thread is making me want to write a spec for machine readable deploy output. someone has to do it. might as well be reddit

user21: "the cli was never built for your agent" should be the tagline for an entire product category. someone in yc is definitely building this rn
