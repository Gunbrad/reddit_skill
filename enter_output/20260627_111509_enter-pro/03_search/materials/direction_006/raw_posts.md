# Reddit Raw Posts

Generated at: 2026-06-27T03:54:20.414111+00:00
Total posts: 10

## Post 1

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/aiagents
Title: Nobody has figured out how to deploy AI agents reliably and maybe we're all just winging it rn
Post URL: https://www.reddit.com/r/aiagents/comments/1u7b2ak/nobody_has_figured_out_how_to_deploy_ai_agents

Body:

Every team I've talked to deploys agents differently. Some bolt it onto the CI/CD and some run evals manually before pushing. Some just ship directly and then see what's breaking in prod.

Here, the agent itself isn't the confusing part anymore. The actual tricky part is knowing when to redeploy it, how to eval it in staging, what a rollback even means for something non-deterministic, etc. There's clearly a layer missing between "the agent works" and "the agent is reliable in prod." And nobody seems to have agreed on what that layer looks like yet. We're slowly heading toward a "control plane for agents" phase, similar to how Kubernetes became the operational layer for containers. Not sure anyone has nailed that problem yet though.

Anyone else seeing this or is it just the teams I'm talking to?

Score: 6
Comment count: 11

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "Discussion",
  "author": "Meher_Nolan",
  "final_url": "https://www.reddit.com/r/aiagents/comments/1u7b2ak/nobody_has_figured_out_how_to_deploy_ai_agents/"
}
```

Loaded comment tree:

reported_comments: 11
loaded_comments: 9
included_comments: 9
top_level_comments: 9
max_comment_depth: 0

Comment Tree 1:

openclawinstaller: The missing layer is closer to agent ops than normal CI/CD. I'd want every deployed agent to have: a versioned prompt/tool bundle, fixture evals for each allowed action, dry-run mode, capability scopes, run receipts, spend/time budgets, health alerts, and a last-known-good config it can fall back to. The big distinction is "the model answered correctly" vs "the external side effect was verified." Most real incidents seem to happen in the second bucket: email sent, ticket changed, refund issued, browser session stale, webhook silently failed. For rollback, I wouldn't think of it as undoing a non-deterministic model. I'd treat it as: stop new runs, preserve receipts, reroute to manual review, restore the prior policy/model/tool config, and replay only idempotent jobs once fixed.

Comment Tree 2:

44KEFISAN: i think a lot of teams are quietly winging it more than they admit

Comment Tree 3:

Jazzlike_Syllabub_91: How are you deploying things to prod?

Comment Tree 4:

serifonlyif: More frameworks are converging on using state machines / graphs to gate agent actions / tool calls and audit workflows. At the very least I think relying on brute force prompting for anything beyond one-off sessions and intended for production is a mistake. I have my own open-source wrapper around Burr that wraps agent behavior in a state machine as MCP, there's also Statewright which is similar, and for sure a couple of others.

Comment Tree 5:

llmobsguy: Yes. But the right approach is to do it by wave. Assume it will be shit. Then revisit and go from there. You don't know what you don't know

Comment Tree 6:

Future_AGI: That missing layer has a shape, even if nobody has branded it yet: a saved eval set you run in staging on every change, traces from prod that feed new cases back into that set, and versioned prompt/config artifacts so "rollback" means pinning the exact version that last passed your evals. Rollback feels weird for something non-deterministic only until you treat the prompt, tools, and routing config as the artifact, because that part is fully deterministic and pinnable even when the model's outputs are not. "When to redeploy" then becomes a threshold on your eval score plus production signal, the same way you would gate a normal service on test coverage and error rate. This "works vs reliable" gap is the whole thing we build at Future AGI, and it is open-source if you want to see one concre

...[truncated]

Comment Tree 7:

havnar-: Having nice context management, a good code base structure and agents file is all you need. Work your tickets but 2x faster. Anything else is overengineering for scaled misery

Comment Tree 8:

dsolo01: I think everyone was just winging it even before agents. So… yes.

Comment Tree 9:

Crafty_Disk_7026: Hers how I do it reliably with open source tools https://github.com/imran31415/kube-coder

## Post 2

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/AI_Agents
Title: How are you deploying agents to nontechnical teams?
Post URL: https://www.reddit.com/r/AI_Agents/comments/1uaanvi/how_are_you_deploying_agents_to_nontechnical_teams

Body:

I'm building agents with Agent SDK or direct LLM api calls. These are basically Python scripts that are running locally.

What is the easiest way to share this with non-technical users who don't want to touch a terminal?

Once you have something working in a script, how do you integrate it to your team?

Score: 4
Comment count: 7

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "Discussion",
  "author": "night_cmw",
  "final_url": "https://www.reddit.com/r/AI_Agents/comments/1uaanvi/how_are_you_deploying_agents_to_nontechnical_teams/"
}
```

Loaded comment tree:

reported_comments: 7
loaded_comments: 5
included_comments: 5
top_level_comments: 5
max_comment_depth: 0

Comment Tree 1:

AutoModerator: Thank you for your submission, for any questions regarding AI, please check out our wiki at https://www.reddit.com/r/ai_agents/wiki (this is currently in test and we are actively adding to the wiki) I am a bot, and this action was performed automatically. Please contact the moderators of this subreddit if you have any questions or concerns.

Comment Tree 2:

theluk246: A few approaches, in order of lift: Wrap it in a simple web UI Streamlit or Gradio. You write ~20 lines of Python on top of your existing script, and you get a browser-based interface. No terminal, no installs for the user. If they're on your network, they can hit a URL. This is the fastest path for internal team use. Deploy it behind an endpoint Wrap the agent logic in a FastAPI route, deploy to Fly.io or Railway. Your non-technical users interact with it via a form, Slack bot, or whatever frontend makes sense. You stay in Python, they never see the backend. Plug it into Knolo If you want to skip the infrastructure entirely — this is what I built Knolo for. You describe what the agent should do, it hosts the execution, and non-technical users interact through a clean chat interface or fro

...[truncated]

Comment Tree 3:

Interstellar_031720: I would avoid jumping straight from “Python script” to “production app.” There is a middle layer that usually works better for non-technical internal users: make the agent boring and constrained first, then wrap it. My rough order would be: Define the input/output contract. What can the user ask for, what artifact comes back, and what does the agent never do? Add a run log before the UI. Store prompt/input, tool calls, result, errors, cost/latency, and whether a human approved it. Put a tiny UI on top: Streamlit/Gradio for internal prototypes, or a Slack command/form if that is where the team already lives. Add a review step for anything with side effects. Draft-only is fine for docs/reports. Human approval for sending emails, changing tickets, touching CRM, etc. Only then make it nicer wi

...[truncated]

Comment Tree 4:

ilovefunc: I actually built TeamCopilot to solve this exact handoff problem. You just turn your script into a workflow once, share it, and your team can run it from a web UI without ever touching a terminal. Check it out if you're interested: https://teamcopilot.ai

Comment Tree 5:

oriben2: I'm building https://zooid.dev exactly for this

## Post 3

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/vibecoding
Title: I Ship Software with 13 AI Agents. Here's What That Actually Looks Like
Post URL: https://www.reddit.com/r/vibecoding/comments/1rhew9h/i_ship_software_with_13_ai_agents_heres_what_that

Body:

This is my terminal right now.

13 Claude Code agents, each in its own tmux pane, working on the same codebase. Not as an experiment. Not as a flex. This is how I ship software every single day.

The project is Beadbox, a real-time dashboard for monitoring AI coding agents. It's built by the very agent fleet it monitors. The agents write the code, test it, review it, package it, and ship it. I coordinate.

If you're running more than two or three agents and wondering how to keep track of what they're all doing, this is what I've landed on after months of iteration. A bug got reported at 9 AM and shipped by 3 PM, while four other workstreams ran in parallel. It doesn't always go smoothly, but the throughput is real.

The Roster

Every agent has a CLAUDE.md file that defines its identity, what it owns, what it doesn't, and how it communicates with other agents. These aren't generic "do anything" assistants. Each one has a narrow job and explicit boundaries.

Group	Agents	What they own

Coordination	super, pm, owner	Work dispatch, product specs, business priorities
Engineering	eng1, eng2, arch	Implementation, system design, test suites
Quality	qa1, qa2	Independent validation, release gates
Operations	ops, shipper	Platform testing, builds, release execution
Growth	growth, pmm, pmm2	Analytics, positioning, public content

The key word is boundaries. eng2 can't close issues. qa1 doesn't write code. pmm never touches the app source. Super dispatches work but doesn't implement. The boundaries exist because without them, agents drift. They "help" by refactoring code that didn't need refactoring, or closing issues that weren't verified, or making architectural decisions they're not qualified to make.

Every CLAUDE.md starts with an identity paragraph and a boundary section. Here'

...[truncated]

Score: 0
Comment count: 100

Media:

```json
{
  "post_type": "multi_media",
  "media_urls": [],
  "outbound_url": "https://preview.redd.it/i-ship-software-with-13-ai-agents-heres-what-that-actually-v0-siksnhhv1bmg1.png?width=1674&format=png&auto=webp&s=58abc34c395277fdf28149832fc061d8e0eb8be1",
  "flair": "",
  "author": "beadboxapp",
  "final_url": "https://www.reddit.com/r/vibecoding/comments/1rhew9h/i_ship_software_with_13_ai_agents_heres_what_that/"
}
```

Loaded comment tree:

reported_comments: 100
loaded_comments: 94
included_comments: 30
top_level_comments: 24
max_comment_depth: 7

Comment Tree 1:

gopietz: I give you the benefit of the doubt, but all people who I respect in terms of their coding abilities use a pretty vanilla setup. Whereas only on reddit will you find people with 13 agents in parallel and the most complicated meta framework you can imagine. I'm just not convinced.
	FreeEye5 reply to gopietz: Yup. Bug reported at 9am and shipped by 3pm after passing through 13 hands doesn't sound like a flex to me. Sounds like why even bother with AI.
	Marcostbo reply to gopietz: If you know what you are doing you can do much better and cheaper than this mess by using a single Claude Code terminal and Copilot if you want some hands on action
	beadboxapp (OP) reply to gopietz: Curious if you find the end result interesting though. It’s that Beadbox app I linked in the post. Tauri app.
		gopietz reply to beadboxapp (OP): I just really don't know when I'd need it. I mean it looks good, props, but it's outside my imagination how I'd be more productive in what I do.
			beadboxapp (OP) reply to gopietz: Got it
		GhrackenfouZen reply to beadboxapp (OP): Hey, I love it. I'm going to add it to my projects shttps://github.com/CraigThomasParsons
	AManHere reply to gopietz: Very short minded of you. You can't even articulate "why" you think something, you just delegate that the SWEs you have seen before have simple setups

Comment Tree 2:

Marcostbo: It's so sad that a part of SWE became this mess

Comment Tree 3:

lunatuna215: I'm not trying to hate, but posts like this REALLY validate my personal choice of having opted out of integrating LLMs into my workflow entirely. They're just not for me. This is just such an unintuitive way of interacting with a computer for me, and if creating things in general. Glad it's all working well for you though.
	LibertyCap10 reply to lunatuna215: I feel like it's largely overthinking the problem. I literally just tell Opus 4.6 what to do and make sure it's using scalable patterns. It creates the subagents and manages all that complexity. I think people who are working this way, coordinating agents manually, are just engaging in technical masturbation
		Pagedpuddle65 reply to LibertyCap10: Agreed. This is a short-sighted solution to a short-lived problem. If this is the best way for AI to work, the platforms themselves will make a better abstraction than this IMO.
	beadboxapp (OP) reply to lunatuna215: Respect. To each their own 🤷
		lunatuna215 reply to beadboxapp (OP): Appreciate that, that's how it should be!
	itsgreater9000 reply to lunatuna215: running 13 agents concurrently feels like the monkeys writing shakespeare problem. we really are trying to figure out how to force the probability in our favor.
	Available_Ostrich888 reply to lunatuna215: Seems like OP could be a person who likes to masturbate with condoms.
		lunatuna215 reply to Available_Ostrich888: Could help with cleanup, I guess?
	god_damnit_reddit reply to lunatuna215: good luck lmao
		lunatuna215 reply to god_damnit_reddit: see this kind of bitterness in response to a person making a personal choice kinda proves my point.
			god_damnit_reddit reply to lunatuna215: i don't know what you're talking about. the original post here is extremely cringe and should honestly be ignored. but "wow i am not going to ever use llms for technical work" is just honestly even more cringe than whatever ai slop generated the original post. like i said - good luck brother. many of my colleagues have similar dispositions today. they are maybe, some of them, still better and more correct (if substantially slower) than llm output is today. but in 6 months? maybe. 1 year? maybe. 2 years? i mean come on. if you're not engaging with any of this tooling then you aren't seeing how quickly it's improving. it will very likely continue to improve much quicker than your hand rolled bespoke output. you call me bitter for laughing at your response but going out of your way to comment

...[truncated]
				lunatuna215 reply to god_damnit_reddit: Dude you're just so offended and that's what is "cringe". It's not for me. It's simple.
					god_damnit_reddit reply to lunatuna215: also insta downvoting the second i post is, like your original comment, silly and cringe.
						[deleted] reply to god_damnit_reddit: ok then you refreshing the page and instantly downvoting my comments as i typed them was cringe and silly
							god_damnit_reddit reply to [deleted]: ok then you refreshing the page and instantly downvoting my comments as i typed them was cringe and silly
	justacow reply to lunatuna215: If you’re looking to validate yourself you can surely do it as Reddit is a feedback chamber, but you’d be doing yourself more of a favor not to
		lunatuna215 reply to justacow: Uhhh... not that deep duder.
			justacow reply to lunatuna215: It’s not lol, just sounds like an old person wanting to stay in their old inefficient ways bc new technology is too much of a hassle
				lunatuna215 reply to justacow: That's such a shallow viewpoint. Do you mindlessly adopt the latest thing, no matter what it is, despite whatever you've already invested your time in beforehand? Like why would I bail on processes and I've built through life experience, that are continuing to work for me as well as have a future of their own? "Get on the latest shit" and assuming it's more efficient without really taking a look at the holistic picture and whether it's actually the right fit for you personally is not a great way to go through life. It's really insufferable honestly when something new and shiny comes along and the people who jump on board right away think they're better than other people just because they did a thing.
					justacow reply to lunatuna215: Do you callously ignore technological advances just because they supersede your abilities that you’ve devoted time into? Calligraphers sure did hate the printing press.
						lunatuna215 reply to justacow: "callously" lmfao bro... nobody is being hurt, and you have not tried EVERY technology that came around, either. And guess what - there are still calligraphers. There's still pen and paper. There's still horses. This idea that you have to adopt everything that's new is STUPID lol. What have you callously ignored being a farmer in life? Wow, how callous of you. Farming is the future, everyone needs to learn to farm. (honestly that holds more water to it than everyone needing AI, too)

## Post 4

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/AI_Agents
Title: I helped a 300-person company deploy agents. A few more lessons learned
Post URL: https://www.reddit.com/r/AI_Agents/comments/1uceklp/i_helped_a_300person_company_deploy_agents_a_few

Body:

Helping a friend deploy agents inside his company feels very different from building stuff for myself, and some of the differences were worth writing down.

1 Small companies shouldn't waste too much time on cheap models at the beginning

DeepSeek is probably the default starting point for a lot of small companies. A lot of teams begin there, and it makes sense from a cost perspective. But for small and medium-sized companies, I still think it is better to start with top-tier models from day one.

The early goal of agent deployment is usually not cost reduction. At that stage, the real goal is to make a skeptical CFO believe this thing is worth continuing.

Spending $0.50 to build an automated report sounds efficient, but it usually does not change anyone's mind. Spending $1,000 to solve a painful problem is much more useful in the early stage, because management can actually feel the difference.

The worst early result is making management think, "Yeah, this is okay, but nothing special." Once that happens, the project usually stops there. What you want is more like, "That was expensive, but damn, it actually worked." That is what keeps the project alive long enough to change how the company works. I think GMI Cloud helped a lot here. In the early demo stage, I was using a lot of expensive models because I just wanted to prove that the idea actually worked. If the results were good, I was fine spending a bit more. What mattered more to me was that the token cost stayed pretty stable and did not suddenly spike like crazy. When I had a few agents running at the same time, the system did not crash, and I did not have to keep watching the deployment side either.

2 The real value of specs is hidden in the 5% of edge cases

I pushed a spec-based workflow from the beginning.

...[truncated]

Score: 28
Comment count: 17

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "Discussion",
  "author": "Johannascot",
  "final_url": "https://www.reddit.com/r/AI_Agents/comments/1uceklp/i_helped_a_300person_company_deploy_agents_a_few/"
}
```

Loaded comment tree:

reported_comments: 17
loaded_comments: 17
included_comments: 17
top_level_comments: 15
max_comment_depth: 1

Comment Tree 1:

chonghaoju: point 3 hits. most multi-agent stuff i've seen just compounds errors across handoffs and you cant tell which agent poisoned the run. one loop with a clear goal + hard stop is easier to debug and gets you most of the way. multi-agent only earned it for actually-parallel work imo
	Johannascot (OP) reply to chonghaoju: Less is more. Try not to add more agents unless you really have to.

Comment Tree 2:

Future_AGI: The error-compounding point is the one that bites hardest: when six agents hand off in a chain, a small wrong assumption in step two looks fine until step five produces confident nonsense. What helped us was tracing every handoff with span-level detail, so we could localize which agent introduced the bad output without re-reading the whole transcript. We open-sourced our tracing and error-localization stack for this at Future AGI: https://github.com/future-agi/future-agi

Comment Tree 3:

AutoModerator: Thank you for your submission, for any questions regarding AI, please check out our wiki at https://www.reddit.com/r/ai_agents/wiki (this is currently in test and we are actively adding to the wiki) I am a bot, and this action was performed automatically. Please contact the moderators of this subreddit if you have any questions or concerns.

Comment Tree 4:

LanguageFew2703: the point about convincing a skeptical CFO early really tracks. i've seen projects die not because the tech failed but because the first demo was "meh, saves us 40 cents per report" and nobody cared enough to push it further the spec vs vibe coding thing is basically the same lesson from every engineering discipline, it just takes people a few painful incidents to learn it themselves
	Johannascot (OP) reply to LanguageFew2703: They are skeptical of agent, so you have to show them a really convincing case the first time and shut them up.

Comment Tree 5:

pranav_mahaveer: the cheap model point is something most people learn the wrong way... by watching a proof of concept die in a budget meeting because it "worked but wasn't impressive" the CFO buy in framing is exactly right. the goal of the first deployment isn't efficiency, its belief. you can optimise costs in month 3 after they're already convinced the spec vs vibe coding observation about edge cases matches what i see too. the 95% that works is basically the same either way, nobody notices the difference. the 5% that breaks is where the decision to spec properly either saves you or destroys the timeline the loops point is genuinely underrated and nobody talks about it. most of what gets marketed as sophisticated multi agent orchestration is just a well structured loop with clear state management and a

...[truncated]

Comment Tree 6:

tingutingutingu: Great post. #1 was a great insight that can apply to many other initiatives than just AI agents.

Comment Tree 7:

yangastas_paradise: Can you elaborate more on the stack you use ? Which orchestration framework or sdk ? Thanks

Comment Tree 8:

sccrwoohoo: When you say you deploy agents - what does that mean? What layer are you at? Can you talk about the systems and platforms you use

Comment Tree 9:

FarVermicelli6708: Oiòiooooooooôo ppl

Comment Tree 10:

Markkos1983: What does "spec-based workflow" actually mean for an LLM call? Prompts are probabilistic, not deterministic. How do you regression test when the model updates under you?

Comment Tree 11:

Substantial-Key1581: The rollback plan mattered more than the model picker in our rollout, nobody trusts agents without a clean undo path.

Comment Tree 12:

RecentTale6192: Point 1 - I believe quality should not be compromised

Comment Tree 13:

Surfer_Tali25: starting with top models is good advice becuase the debugging time u save is worth way more than the api bill. i think a lot of people get stuck trying to optimize for cost before they even know if the agent flow is actually working right...

Comment Tree 14:

nikeiptt: Can you elaborate on the first point? I've got a workflow where I use Claude to dispatch to Deepseek which is then reviewed by Claude. For basic tasks the savings seem worth it?

Comment Tree 15:

Substantial_Doubt139: Point 2 is the one I want to push on because I think it's even sharper than you're framing it. The reason vibe coding hits a wall at the 5% edge cases isn't really that the spec process produces better code in those moments. It's that the spec process produces better context for whoever (or whatever) has to debug it three months later. The vibe-coded project might have shipped perfectly, but the rationale for why it's structured a certain way lives in a chat transcript nobody can find, so when an edge case appears the team is rediscovering the original reasoning from scratch. Specs survive their authors and chat threads don't. That's the asymmetry that compounds, and it gets worse at the scale you're describing because you have multiple people debugging code multiple other people wrote wit

...[truncated]

## Post 5

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/EngineeringManagers
Title: Clients asking about AI coding platform enterprise deployments and we have no good answers yet
Post URL: https://www.reddit.com/r/EngineeringManagers/comments/1sn1dzz/clients_asking_about_ai_coding_platform

Body:

Three of our mid-market clients (300–800 employees each) have asked us in the last month to help evaluate and deploy AI coding platforms. The pattern is striking enough that I'm wondering if other MSPs are seeing the same thing.

Client A is in healthcare. They need HIPAA-compliant AI coding tools, want on-prem deployment, and have 120 developers.

Client B is a defense contractor that needs air-gapped deployment and wants the tool to actually understand their codebase before making suggestions.

Client C is in financial services with around 200 developers. They're currently spending $15k/month on Copilot inference and leadership wants that cut in half.

What's interesting is none of these conversations are saying, should we use AI coding tools. They've already decided yes. The questions are about how to deploy securely, how to manage costs, and how to actually govern usage across teams.

Is there enough consistent demand here to build a formal practice around this? And for those already doing it, what tools are enterprises actually choosing once compliance requirements enter the picture?

Score: 8
Comment count: 13

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "",
  "author": "AccountEngineer",
  "final_url": "https://www.reddit.com/r/EngineeringManagers/comments/1sn1dzz/clients_asking_about_ai_coding_platform/"
}
```

Loaded comment tree:

reported_comments: 13
loaded_comments: 9
included_comments: 9
top_level_comments: 9
max_comment_depth: 0

Comment Tree 1:

devironJ: Curious to see what you come up with, I’m in big pharma and what our corporate IT has done so far is expose some Claude models on Bedrock that’s tweaked for our proprietary data, PII and possibly HIPAA, I’m not too close on the details there. It’s exposed via a URL and we have to request an API key for it, but we’ve configured our Claude code to point to use those hosted models. I’m assuming you could do something similar with hosting a LLM on one of their on prem servers with more restrictive tweaks and use which ever tool and only point it to their hosted model.

Comment Tree 2:

kayakyakr: On prem of the big models is very, very expensive. $$ for the servers. $$$$ for the licenses to run the models. Look into minimax m2.5 (m2.7 exists, but I found it to be more prone to hallucinations and less token efficient). You can self host for $2k straight up. Budget a little higher and you can get into faster servers that can handle more tasks in parallel. You still need to work with it as a tool for development rather than just vibe coding, but it's quite capable for a self host model. Your defense company wanting the model to understand the full codebase seems like they would do well with retraining the model on their codebase to develop a custom model. Maybe a weekly task to create a model with that training data?

Comment Tree 3:

Vegetable_Sun_9225: 15k/month is peanuts for a 200 person department. Sounds like either they haven't measures the ROI or the team isn't using it effectively as the return should far outweigh that investment if used right

Comment Tree 4:

Traditional-Hall-591: The answer is always a slop off. Pit the slop generators against each other and see who makes the tastiest slop.

Comment Tree 5:

VVFailshot: If they have budget then its deployment problem. Like estimate load, select servers, setup provisioning etc, run vllm connect claude code. What gets scary is the price tag of Nvidia GPUs

Comment Tree 6:

Longjumping-Cat-2988: Most companies have already decided to use AI but they don’t know how to handle security, governance or costs yet. Especially with on-prem and compliance requirements, it’s less about the tool and more about how you control and integrate it. From what I’ve seen, nobody has a clean setup yet. It’s all tradeoffs between usability and control and a lot of figure it out as we go. If you build a practice, I’d focus on governance and workflows around AI, not just deployment.

Comment Tree 7:

boghy8823: Curious to know if any of your clients are using API based or subscription pricing?

Comment Tree 8:

Hopeful_Stretch_9707: This is exactly the pattern I’ve been seeing too most companies have already decided yes, we’re using AI coding tools the only open questions for them are around security, compliance, and cost not “Should we?” In my experience, that’s where the real danger starts. Once the yes is done, the tool quietly becomes the default way of working, and teams slowly stop reading deeply, owning the code, or asking whether the model is right. You end up with systems that are technically compliant and properly governed, but where no one really understands the code anymore. And the people who bear the real cost the engineers, the junior devs, the people who trusted the AI re the last to be asked what they think.

Comment Tree 9:

AffectionateHoney992: Seeing a tonne of this demand right now, you're not alone. Two things worth knowing. First, Claude is now decoupled from Anthropic's hosted endpoint. Claude Code (the CLI/agent) works against third party gateways: AWS Bedrock, GCP Vertex, Azure, or your own self hosted inference. That single change unlocks all three of your client scenarios. The HIPAA client routes Claude through Bedrock under their existing BAA. The defense client points it at a local gateway inside the air gap. The FinServ client routes through a cost optimised gateway that mixes Claude for hard work with cheaper models for autocomplete. Same agent, same dev experience, very different compliance and cost posture. Second, we build and install the self hosted infrastructure that sits around it. That's what I do. Source ava

...[truncated]

## Post 6

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/buildinpublic
Title: Building a terminal IDE for AI coding agents — 2 months in, here's what I've learned
Post URL: https://www.reddit.com/r/buildinpublic/comments/1r0yqas/building_a_terminal_ide_for_ai_coding_agents_2

Body:

Solo dev building PATAPIM — a terminal-first IDE for developers who use AI coding agents (Claude Code, Gemini CLI, Codex).

How it started: I was running 3-4 Claude Code sessions in separate terminal windows, constantly alt-tabbing, and had no way to check progress from my phone. Built a simple remote terminal wrapper. Scope crept. Now it's a full product.

What it does:

Multi-terminal grid (up to 9 in 3x3) with color-coded status (red = AI working, green = needs input)

Voice dictation (local Whisper or cloud) for talking to your AI instead of typing

Embedded browser AI agents can control directly

Remote access from phone via QR code

Context preservation across coding sessions

What I've learned building in public:

Features you didn't plan can become your best ones. Voice dictation was a "nice to have" I added in week 2. It's now one of the top reasons people try the product.

Reddit > paid ads for dev tools. Finding the 5-10 subreddits where your exact target audience hangs out and genuinely engaging there beats any ad spend. But you have to actually participate, not just drop links.

Lifetime pricing converts surprisingly well. Offering $30 one-time alongside $7/month — most people pick the lifetime deal. It's great for cash flow early on even if it's less revenue per user long-term.

Ship fast, polish later. Launched Windows-only. macOS is coming March 1st. Waiting for both platforms would've meant another month of zero feedback.

Numbers so far: ~2 weeks since public launch. Modest downloads, growing organic traffic from Reddit. No paid marketing yet.

https://patapim.ai — feedback welcome, especially on the UX.

Score: 2
Comment count: 10

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "https://patapim.ai/",
  "flair": "",
  "author": "germanheller",
  "final_url": "https://www.reddit.com/r/buildinpublic/comments/1r0yqas/building_a_terminal_ide_for_ai_coding_agents_2/"
}
```

Loaded comment tree:

reported_comments: 10
loaded_comments: 8
included_comments: 8
top_level_comments: 5
max_comment_depth: 1

Comment Tree 1:

Otherwise_Wave9374: Multi-terminal grid with status colors is such a good idea. The biggest pain for me with coding agents is just knowing when theyre blocked vs still thinking. How are you detecting "needs input" reliably, stdout patterns or something more explicit in the agent protocol? Ive been following a bunch of agent UX patterns too: https://www.agentixlabs.com/blog/

Comment Tree 2:

Key-Boat-7519: Your main edge is you’re treating the terminal like a control room for multiple agents, not just “another Claude wrapper,” so I’d double down on workflows, not features. The patterns I’d design around: - “Refactor + write tests” across multiple services at once (one pane per service, shared context) - “Exploration + execution” where an agent drives the browser, a second handles code edits, and a third runs tests/logs - “Hands-free coding” for people who pair voice + minimal typing (accessibility angle is strong here). Your 3x3 grid is begging for saved layouts: presets like “backend triage,” “LLM eval runs,” “frontend build fix,” each with pre-wired prompts and tools. On the growth side, keep doing the Reddit-first thing but get more systematic: I’ve seen people track dev subreddits with t

...[truncated]
	germanheller (OP) reply to Key-Boat-7519: this is really solid feedback, appreciate the detail. the saved layouts idea is something ive been thinking about -- right now you can arrange terminals however you want but theres no way to save a preset and recall it. 'backend triage' and 'frontend build fix' presets would be killer, adding that to the roadmap the hands-free angle is interesting too, the voice dictation is already there but i havent marketed it as an accessibility feature. good callout for the reddit tracking -- yeah ive been doing it manually which is.. not scalable. will check out those tools you mentioned

Comment Tree 3:

joshuadanpeterson: Nice work on the multi-terminal grid. Warp has similar thinking with AI agents - keeps everything in one place so you're not jumping between tools.
	germanheller (OP) reply to joshuadanpeterson: thanks! yeah warp is doing cool stuff with the AI integration. main difference is patapim doesnt replace your terminal -- it wraps whatever CLI tool you already use (claude code, gemini cli, codex, whatever) and gives you the grid + real-time status colors on top. so you keep your existing setup, just with a bird's eye view of all your agents at once

Comment Tree 4:

Visible-Ground2810: Good luck 😅. Read the vim and neovim summed decades of real engineering work and good luck with that. Dude now honestly, why not neovim with tmux and other peripherals around this stack? For instance I have created an mcp server and tui for llms to manage epics features and projects plus a tui to read, manage and edit. But all into the terminal quickly accessible with my existing workflow with neo vim and tmux
	germanheller (OP) reply to Visible-Ground2810: fair question honestly. neovim + tmux is a legit setup and ive used it for years. the reason i went electron was the visual layer -- color-coded status per terminal (red = agent blocked, green = working, neutral = idle), voice dictation with local whisper running in-process, and remote access from your phone via QR code. you can definitely do multi-agent with tmux panes but the automatic state detection (knowing which agent is thinking vs waiting vs done without checking each pane) would need custom scripting on top. your mcp server + tui for epics sounds interesting tho, is it public? always curious how people wire llms into project management

Comment Tree 5:

yr-kidding-me: crystl terminal helps a lot with the lost windows and tabs. It sends you notifications when you are needed.

## Post 7

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/kubernetes
Title: How are you handling AI coding agents that want to deploy to your clusters?
Post URL: https://www.reddit.com/r/kubernetes/comments/1t2cltd/how_are_you_handling_ai_coding_agents_that_want

Body:

I'm Romaric, founder of Qovery (K8s management platform).

I've been thinking about a problem that I don't see discussed much here: AI coding agents are starting to need deployment access, and most Kubernetes setups aren't ready for it.

Developers on my team and at companies we work with are using Claude Code, Cursor, Copilot to write code. The code quality is fine. The problem is what happens next. The agent wants to deploy, and it has roughly three options:

Raw kubectl/helm. The agent gets a kubeconfig and runs kubectl apply. This works, but there's no audit trail distinguishing agent actions from human actions, and most teams grant the same broad credentials they'd give a CI pipeline.

Bypass K8s entirely. The developer deploys to Vercel/Railway because it's frictionless. Now you have Shadow IT in a K8s-first org. (I wrote about real cases of this going wrong - including the Vercel/Context.ai breach where an unsanctioned AI tool's OAuth tokens were compromised and used for lateral movement.)

Open a ticket. The developer waits for the platform team. The AI speed advantage disappears.

The underlying challenge is that Kubernetes RBAC wasn't designed with AI agents in mind. There's no native concept of "this action was initiated by an agent on behalf of user X" vs "this action was initiated by user X directly." The audit trail can't distinguish them. And most admission controllers don't have policies for agent-initiated deployments.

Some approaches I've seen or considered:

Scoped service accounts per agent session with short-lived tokens - but this requires custom tooling to provision and revoke

OPA/Gatekeeper policies that tag agent-initiated requests differently - possible but requires custom admission webhooks

Routing agent actions through an API layer that en

...[truncated]

Score: 0
Comment count: 23

Media:

```json
{
  "post_type": "multi_media",
  "media_urls": [],
  "outbound_url": "https://www.qovery.com/blog/shadow-it-is-back-and-vibe-coding-made-it-worse",
  "flair": "",
  "author": "ev0xmusic",
  "final_url": "https://www.reddit.com/r/kubernetes/comments/1t2cltd/how_are_you_handling_ai_coding_agents_that_want/"
}
```

Loaded comment tree:

reported_comments: 23
loaded_comments: 23
included_comments: 23
top_level_comments: 10
max_comment_depth: 3

Comment Tree 1:

ModernOldschool: You can’t be serious man. You founded a K8s management platform and dont know about one of the most popular and (IMO) best way to deploy? Hint it ends with Ops and can be done automatically with existing and established tools without really changing any workflows
	ev0xmusic (OP) reply to ModernOldschool: Hey, good point. GitOps (ArgoCD, Flux..) is definitely a solid pattern and one I'm very familiar with. But it doesn't fully solve the problem I'm raising here. GitOps works great when the workflow is: developer pushes code → CI builds → PR to a gitops repo → ArgoCD syncs. The governance comes from the Git PR review process. But what happens when an AI agent is the one creating that PR? You still need to answer: which agent opened this PR, with what permissions, on behalf of which developer, and should it be auto-merged? The "who initiated this and should they be allowed to" question doesn't disappear just because you have a gitops pipeline - it shifts to the Git layer instead of the cluster layer. GitOps is a great deployment mechanism, but the agent access governance question remains rega

...[truncated]
		TonyBlairsDildo reply to ev0xmusic (OP): All work should be ticketed; all branches in git should be named after tickets; all merges in git should attract review; all releases should be triggered by a state change in git. which agent opened this PR, If an agent works autonomously it will have it's own credentials. We use Renovate, not an AI but a "bot" that bumps our system components automatically. There are emerging use cases for limited AI bots making pull requests for work they created without oversight and they should have their own credentials for pull requests. "who initiated this and should they be allowed to" If a developer was overseeing an agent using a tool like a Cursor, then it's their name on the PR as the developer will be responsible person it shifts to the Git layer instead of the cluster layer. GitOps is a great

...[truncated]
		znpy reply to ev0xmusic (OP): not gonna like, this reply reads like it's llm generated.

Comment Tree 2:

JalanJr: I didn't encounter the issue (yet) but I would suggest a gitops approach. With this your agent submit PR which you can validate and you get a second layer of approval.
	ev0xmusic (OP) reply to JalanJr: Thanks for the suggestion! GitOps with a PR-based approval flow is definitely a strong pattern - the PR review step gives you that human-in-the-loop checkpoint which is great. Where it gets interesting is when you start thinking about scale: if you have 10 developers each with an AI agent submitting PRs to your gitops repo multiple times a day, that approval layer can become a bottleneck pretty quickly. And then teams start auto-merging "low-risk" changes, which brings you back to the original question - how do you define what's low-risk, and how do you enforce that policy per agent/developer? Curious if you've thought about how you'd handle that as adoption grows, or if for now the PR review step feels sufficient for your team size.
		No_Cattle_9565 reply to ev0xmusic (OP): I don't think you should ever deploy any code written by AI without a review. Letting agents deploy into a Cluster would never come to my mind
			ev0xmusic (OP) reply to No_Cattle_9565: I actually agree with you - I don't think unreviewed AI-generated code should hit a production cluster either. The question is more about what the review + deployment workflow looks like. Today it's mostly "human reviews PR, CI/CD deploys." But as agents get more capable and teams want to move faster, the pressure to auto-merge certain categories of changes (config updates, scaling changes, dependency bumps) is going to grow. That's where having clear policy enforcement matters, whether it's through GitOps PR rules, an API layer, or admission controllers.
		OGicecoled reply to ev0xmusic (OP): You’re creating a problem that doesn’t exist. If I have 10 developers how many changes are they making to a gitops repo a day? It isn’t enough to create a bottleneck. I find it odd that you completely overlooked gitops in your pitch. Gitops solves your original problem statement of “this action was initiated by an agent on behalf of user x”. So I pose three questions: what exactly are you trying to solve? Why did you omit GitOps from your pitch? How do you solve whatever the answer to question one is?
			ev0xmusic (OP) reply to OGicecoled: What am I trying to solve? The governance gap when AI agents initiate deployments - specifically: identity (which agent, on behalf of whom), policy enforcement (what should this agent be allowed to deploy), and audit trail (distinguishing agent-initiated vs. human-initiated actions). Why did I omit GitOps? Genuine oversight in the original post - I should have included it, and I've updated the post to add it as an approach. You're right that GitOps with PR review addresses a big chunk of the problem, especially the audit trail through Git history and the approval layer through PR review. How does Qovery solve it? The agent interacts with our API instead of the cluster directly. The API enforces the same RBAC and permissions as a human user, logs every action with the initiator's identity,

...[truncated]
		JalanJr reply to ev0xmusic (OP): tbh my current company is a bit late on AI adoption so I don't have the answer... But I agree about the merge fatigue. Everytime I discuss with some AI enthusiast we get to the same point: the issue is IA is too prolific and at a certain point we tend to validate things without proper review of the code so next step is strengthen our test pipelines enough to catch all the errors and have serious dev/qual/prod environments ?
			ev0xmusic (OP) reply to JalanJr: You're touching on something really important here - the merge fatigue problem is real and I think it's going to be one of the defining challenges of AI-assisted development. The pattern I keep seeing is: AI generates code fast → PRs pile up → reviewers start rubber-stamping → bugs slip through → team reaction is "we need better tests and more environments." And you're right, that's the correct next step - stronger test pipelines and proper dev/qual/prod separation become non-negotiable when the volume of code changes increases 5-10x. But here's the thing that keeps me up at night: test coverage is only as good as the tests someone writes, and most teams are already behind on test coverage before AI enters the picture. So the real question becomes: can AI also help write meaningful tests,

...[truncated]

Comment Tree 3:

aleques-itj: Why would I want the agent to deploy directly to my cluster - there's already deployment mechanisms that are good It can submit to git - done.
	ev0xmusic (OP) reply to aleques-itj: Fair point - and I actually agree with you for established projects. If you already have a gitops pipeline set up with ArgoCD/Flux, the agent pushing to git and letting the existing CI/CD take over is the right call. No argument there. Where it gets more interesting is the greenfield scenario - and with AI agents, there's never been a lower barrier to spinning up new projects and services. A developer can go from idea to working app in an afternoon with Cursor or Claude Code. But that new project doesn't have a gitops pipeline yet. It doesn't have a CI/CD workflow, a Helm chart, or an ArgoCD Application manifest pointing at it. Someone still needs to set all of that up before "just submit to git" works. So the question becomes: who sets up that deployment infrastructure for the 5th microse

...[truncated]
		TonyBlairsDildo reply to ev0xmusic (OP): But that new project doesn't have a gitops pipeline yet. It doesn't have a CI/CD workflow, a Helm chart, or an ArgoCD Application manifest pointing at it. Someone still needs to set all of that up before "just submit to git" works. So make the pipeline? It doesn't take two days to set up GitOps pipeline anymore than it takes two days to throw up a kubernetes cluster. It takes more than two days to set up a good CICD pipeline, as it does to set up a good Kubernetes cluster. No app is going to live or die because you're taking the time to set up code scanning, dependency/supply chain scanning, audit logs, RBAC, etc.

Comment Tree 4:

jarofgreen: > There's no native concept of "this action was initiated by an agent on behalf of user X" vs "this action was initiated by user X directly." The audit trail can't distinguish them. Why is this a problem? Either way, user X is responsible for any problems caused. EDIT: I did mean this as a serious question OP. It seems like this is the whole root of your problem, and you are going to great lengths to try and solve it but I just don't understand the problem. Maybe if you were clearer about the problem you are trying to solve it would help people suggest ideas? Also I'm genuinely curious.

Comment Tree 5:

schmurfy2: "the agent wants to deploy" 😑 Take that agent in a corner for a discussion about processes and problem is solved.

Comment Tree 6:

TheGraycat: GitOps. AI is making things go faster but it’s still not trustworthy. All our changes have to go through change management process first audit purposes plus the pipelines all have automated checks before it gets to human review. I don’t see that changing any time soon.

Comment Tree 7:

samehmeh: GitOps is the right layer, but the audit trail problem you're describing is specifically solved by giving each agent its own k8s service account with a unique name, then tying the ArgoCD or Flux application to that SA. When the agent pushes to git and the controller applies it, your audit log shows the SA identity, not just 'kubectl'. Admission webhooks like Kyverno can then enforce policies per SA.

Comment Tree 8:

External-Train5055: We ended up treating AI agents like untrusted automation: you can’t “trust and execute”, you have to gate side effects and make it observable. Curious what has actually broken in your pipeline so far? Things I’ve seen kill “deploy-to-cluster” agents: – Hidden state drift (agent mutates context and the human sees the wrong thing) – Silent retries that turn a harmless tool call into multiple writes – Missing rollback path (no “undo” for a deployed change) – Approvals happening too late (after the agent already moved the system) If you share your architecture (GitOps/Argo? direct kubectl? CD), I can share the guardrail patterns we’re collecting + a mini checklist. We’re running a beta for aidesignblueprint.com focused on this “production-ready agent workflow” problem.

Comment Tree 9:

replicatedhq: Most teams we talk to are pushing AI-assisted deployments through self-hosted control planes or GitOps workflows instead of handing agents direct cluster access. The key shift is treating the agent like an untrusted automation layer: no kubeconfigs, short-lived scoped permissions, and every action tied back to a human identity with a clear audit trail. Self-hosted environments make this even more important because the governance, compliance, and blast radius concerns are much higher than in standard SaaS deployments.

Comment Tree 10:

znpy: This works, but there's no audit trail distinguishing agent actions from human actions there are multiple ways to implement what you're citing. I'm Romaric, founder of Qovery (K8s management platform). if have serious doubts about the capability of your software if you don't know yourself how to do the things you're supposed to automate and guard. I'll save the text of your post to make sure i can link if your software gets proposed to me in any way.
	znpy reply to znpy: u/ev0xmusic wrote: I'm Romaric, founder of Qovery (K8s management platform). I've been thinking about a problem that I don't see discussed much here: AI coding agents are starting to need deployment access, and most Kubernetes setups aren't ready for it. Developers on my team and at companies we work with are using Claude Code, Cursor, Copilot to write code. The code quality is fine. The problem is what happens next. The agent wants to deploy, and it has roughly three options: Raw kubectl/helm. The agent gets a kubeconfig and runs kubectl apply. This works, but there's no audit trail distinguishing agent actions from human actions, and most teams grant the same broad credentials they'd give a CI pipeline. Bypass K8s entirely. The developer deploys to Vercel/Railway because it's frictionles

...[truncated]

## Post 8

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/OnlyAICoding
Title: devcontainer-mcp - I got tired of AI agents installing random crap on my machine
Post URL: https://www.reddit.com/r/OnlyAICoding/comments/1st3dkz/devcontainermcp_i_got_tired_of_ai_agents

Body:

You know that moment when your AI coding agent decides npm install -g is totally fine and now your global Node setup is haunted? Or when it installs some native package that will eventually conflict with something else? I got tired of that.

So I built devcontainer-mcp, an MCP server that gives AI agents their own dev containers to work in instead of yours. It's like giving your agent a playpen so it stops redecorating your living room and does its business in its own room.

What it does:

33 MCP tools that let agents create, manage, and run commands inside dev containers

Works with local Docker, DevPod, or GitHub Codespaces. Agent works and communicates with the MCP, you approve

Built-in auth broker so the agent never sees your actual tokens (it gets opaque handles)

Self-healing: if th container build fails, the agent gets the raw error and can fix the Dockerfile itself, rebuild.

One-liner install: curl -fsSL .../install.sh | bash  sets up the MCP server, installs DevPod if missing, and drops a SKILL.md and MCP config so Copilot/Claude/Cursor automatically know to use containers

The irony was that this project was itself built inside a dev container. The AI agent that helped write it accidentally installed Rust on my host machine in the first 10 minutes. That's when I knew we were onto something.

Written in Rust (I used AI assistance, but idea, design choices, direction etc are mine). ~6MB binary.

Open Source, MIT licensed.

Landing page | GitHub

Happy to answer questions. Also happy to hear "this already exists" because I looked and there was nothing that could do all of the things I wanted it to do - a devcontainer swiss-army knife for AI agentic coding.

Hope it's useful to folks!

Score: 2
Comment count: 5

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "https://www.anionline.me/devcontainer-mcp/",
  "flair": "",
  "author": "anionreddit",
  "final_url": "https://www.reddit.com/r/OnlyAICoding/comments/1st3dkz/devcontainermcp_i_got_tired_of_ai_agents/"
}
```

Loaded comment tree:

reported_comments: 5
loaded_comments: 4
included_comments: 4
top_level_comments: 2
max_comment_depth: 2

Comment Tree 1:

Spare_Spirit6762: what?

Comment Tree 2:

blazarious: Never had an agent do npm install-g on me.
	anionreddit (OP) reply to blazarious: I totally get that. If your workflow is mostly high-level JS, you're usually safe! The 'why' behind this is really for two other scenarios: Native/System Deps: For folks in ML, Rust, or C++, installs often touch system-level libraries. One hallucinated command can bork a local dev environment in ways that take hours to untangle. The 'Security Blast Radius': With recent stuff like the LiteLLM supply chain attack and various token exfiltration exploits (like the recent Codex branch injection), giving an agent host access is risky. If the agent is in a container, it can't accidentally (or via prompt injection) 'see' your personal SSH keys or global .env files. This is also about reproducibility for complex software development that needs multiple tools, system libraries and configuration. Dev

...[truncated]
		blazarious reply to anionreddit (OP): ML stuff I mostly do in Python and have the agent operate in a venv. But still good for you for finding a solution to your problem.

## Post 9

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/SideProject
Title: I run 4 AI coding agents at once, so I built a dashboard to stop losing track of them
Post URL: https://www.reddit.com/r/SideProject/comments/1ufn0wu/i_run_4_ai_coding_agents_at_once_so_i_built_a

Body:

Working solo, I lean on Claude Code and Codex a lot — usually 3-4 of them going at the same time across different repos. The actual work was fine; the problem was me.

I'd burn minutes alt-tabbing between terminals just to answer "which one's done? which one's stuck? which one is waiting for me to approve something?"

So I built Pitwall for myself: one browser tab, one tile per agent, with status-colored frames so a glance tells you who needs you. It pings when an agent stalls on a permission prompt, you can pair two agents on the same repo side by side, and broadcast one prompt to several at once.

It's local-first — binds 127.0.0.1, runs the agent CLIs under your own logins (never touches API keys), reads status passively from the transcript files Claude Code already writes. No cloud, no telemetry.

Open source and very early (v0.0.1). I've been dogfooding it for two months; sharing it today. Feedback welcome:

https://github.com/ujjeeq/pitwall

Score: 0
Comment count: 5

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "http://127.0.0.1/",
  "flair": "",
  "author": "Forsaken-Dog6942",
  "final_url": "https://www.reddit.com/r/SideProject/comments/1ufn0wu/i_run_4_ai_coding_agents_at_once_so_i_built_a/"
}
```

Loaded comment tree:

reported_comments: 5
loaded_comments: 2
included_comments: 2
top_level_comments: 2
max_comment_depth: 0

Comment Tree 1:

Head-Foundation3312: Claude code has this natively just run "claude agents" in your terminal then "/color" and pick a color lol

Comment Tree 2:

CarsonBuilds: If you use both, you should checkout my project. I've been building Crewplane, a CLI-first orchestrator where you define which tasks run, which CLI handles them, what they depend on, and where the workflow should stop or wait via markdown files. Every input, intermediate output, log, manifest, and final result is preserved on disk so you can trace a run after the fact instead of just trusting it in the moment. https://github.com/crewplaneai/crewplane If you find it helpful, a star on GitHub or a share with someone who might find it useful would mean a lot, thanks.

## Post 10

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/SideProject
Title: I built a tool that lets AI agents scaffold, deploy, and return a live URL for full-stack apps directly in your terminal chat
Post URL: https://www.reddit.com/r/SideProject/comments/1te9ymm/i_built_a_tool_that_lets_ai_agents_scaffold

Body:

Hi everyone. I’ve been building a tool called PinMe and shared it here last year. It started as a simple frontend deploy CLI, but I recently rebuilt it into a tool protocol for AI coding agents (Claude Code, Codex, Cursor etc.).

If you use these agents, you know code comes out fast. But sharing or testing a quick experiment still sucks. You have to create a repo, push, connect to Vercel/Render, set up database credentials, configure transactional email, and wire it all together. For a project that took less than 10 minutes to generate, it would be too much efforts to deploy it in traditional ways.

I wanted to fix that workflow so I let PinMe integrated into ai agent, so that I can scaffold and deploy full-stack apps using natural language without leaving that terminal chat.

How it works

It's pretty easy.

Just copy paste this to your agent and add it to your agent's skills:

npx skills add glitternetwork/pinme

Once installed, you just pass your prompt directly to the agent:

/pinme [ you can describe your app idea using natural language...]

To test it, I asked my agent (which is Claude Code ) to build a full-stack AI Agent Workshop, equipped with these functions:

Auth via email OTP.

Custom AI personas with system prompts.

Private, persistent chat history in parallel.

Shareable deployment links.

The entire setup, frontend, backend, database (Cloudflare D1), email routing, LLM API integration, and final live deployment only took a few seconds.

Under the hood, it abstracts away Cloudflare Workers, D1, OpenRouter, and Resend. You don't need to create accounts, configure domains, or manage billing for any of them. The agent & PinMe handles the whole stack.

I've also successfully created some small games in minutes and shared with friends. You may find more examp

...[truncated]

Score: 3
Comment count: 5

Media:

```json
{
  "post_type": "multi_media",
  "media_urls": [],
  "outbound_url": "http://pinme.dev/",
  "flair": "",
  "author": "Particular_Tea8954",
  "final_url": "https://www.reddit.com/r/SideProject/comments/1te9ymm/i_built_a_tool_that_lets_ai_agents_scaffold/"
}
```

Loaded comment tree:

reported_comments: 5
loaded_comments: 4
included_comments: 4
top_level_comments: 3
max_comment_depth: 1

Comment Tree 1:

Accurate-Beyond-9627: The live URL part is the strongest bit. I'd show one tiny failure/recovery demo too because deploy/setup edge cases are where I usually stop trusting these workflows.

Comment Tree 2:

benjmadi: This is a really cool idea!!

Comment Tree 3:

TechnicalSoup8578: This feels less like a deploy tool and more like a full execution layer for agent-driven development. How do you handle rollback or state recovery when a generated stack deploys but the agent context changes mid-iteration? you should share this in VibeCodersNest too
	Particular_Tea8954 (OP) reply to TechnicalSoup8578: You can just talk to agent and ask them to update the project and then Pinme will help you generate a new link based on that new info. Still you don’t need to switch out, everything done in a window.
