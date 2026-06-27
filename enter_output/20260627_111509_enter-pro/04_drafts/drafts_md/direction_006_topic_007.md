## Title Candidates

1. 2 months of driving my deployment platform from the terminal with an AI coding agent. here's what actually happened
2. Building a terminal-first deploy workflow with an AI coding agent, 2 months in: here's what I learned
3. I drove my deployment platform from the terminal with an AI coding agent for 60 days. what broke
4. 2 months of running deploys from the terminal with an AI coding agent. the honest log
5. what happens when you stop opening your deploy dashboard and let an AI coding agent drive it from the terminal
6. can you actually drive a deployment platform from the terminal with an AI coding agent? a 2 month test
7. driving my deployment platform from the terminal with an AI coding agent: wins, bugs, and one thing I won't do again
8. I let an AI coding agent drive my deployment platform from the terminal for 2 months straight
9. how I drove my deployment platform from the terminal with an AI coding agent for 2 months without touching the UI
10. terminal-only deploys: 2 months of driving my deployment platform with an AI coding agent

## Final Post

Solo dev here. Two months ago I made a small bet: stop opening my deployment platform's web dashboard. All of it: deploys, env vars, domain bindings, auth setup. Done by an AI coding agent running in my terminal.

Quick disclosure: I use Enter (specifically Enter CLI) for this. Writing this because the workflow is interesting and I have honest opinions about where it breaks. Not a paid post.

**The setup**

tmux, 2 panes. One pane runs Claude Code. The other is for me to watch what the agent is doing. When I want to ship a change I type "deploy this" and the agent handles the rest.

What made this click was Enter CLI. It's a thin command wrapper that lets Claude Code (or Codex, Cursor) talk to the Enter Pro platform. From the agent's side it just gets new verbs: build, edit, publish, domain. The boring infra stuff.

Before this I was either copy-pasting from the agent's output into a web UI, or writing my own shell scripts for each step. Both sucked. One breaks my flow. The other turns into a part-time scripting job.

**What it actually looks like**

Yesterday morning I wanted to ship a small auth tweak on a side project.

me: "add forgot password to the login page, then deploy"

agent: runs the code change locally, runs the test, then goes through Enter CLI to publish the build, set the new env var, rebind the custom domain.

me: refreshes the URL, it's live, I close tmux and go make coffee.

Total time I spent clicking anything in a browser: zero.

The PostgreSQL + auth + storage stuff all lives in Enter Cloud, which the CLI can also provision. So when I said "add password reset" the agent had to wire up the reset token table, the email send, the rate limit. I watched it do it. I did not write any of that SQL.

**Things that broke**

Webhook reliability. Stripe sends a webhook, that goes through the Enter Cloud Functions layer. The agent can redeploy it but I hadd to inspect the function logs manualy twice because the first deploy had a bad env var reference. The CLI dont surface function logs well yet. I ended up tailing them with a separate command.

domain SSL propagation. First time I bound a custom domain through the CLI it took 20 minutes and the agent kept reporting "still propagating." I had to verify in DNS myself. Fine, but the agent didn't know to check.

secrets. Anything sensitive (Stripe keys, Resend keys) I still type into the agent's prompt myself. I'm not letting an AI agent handle raw secret values in its context. I'd rather lose the convenience.

when the agent gets stuck. Sometimes it loops. Tries a deploy, fails, retries, fails again, tries the same thing. I added a small "if it fails 3 times, stop and ask me" rule into my CLAUDE.md. Without that I would have burned credits.

**Things I didn't expect**

i ship more often. When deploy is a chat message I ship the tiny change instead of letting it sit. Noticed this around week 3, my commit history got denser.

i read code more carefully. Counter-intuitive. When the agent is doing the deploy too I feel more responsible for what it actually shipped, because I'm the one who said "ship it."

i miss the dashboard a little, only for analytics. Enter Analytics has dashboards I can't quite reproduce from the CLI yet. I still open the browser for that, once a week.

**Where I'd warn people off**

Don't do this for anything that touches money or PII without you reviewing the diff. The agent can wire up Stripe but you still need to verify the webhook handler. AI still hallucinates auth code in ways that look fine and aren't.

if you're a solo dev shipping small stuff this is the fastest workflow I've found. team scale or anything regulated, the terminal-only thing isn't there yet for me.

---

## Comment Trees

**Tree 1**

user1: How are you handling the deploy logs though? If the agent runs the publish step and something silently fails inside Enter Cloud Functions, do you have to ssh in or is there a CLI command to tail function logs in real time? I tried something similar with Replit Agent last year and the moment anything went wrong on the infra side I had to context-switch back to the browser anyway.

user2 reply to user1: yeah this is basically what the post was getting at. the CLI exposes build/publish/domain but the function runtime logs feel like an afterthought. I worked around it by writing a small wrapper that tails the Enter Cloud console output and pipes it back into the tmux pane, but its hacky.

user3 reply to user1: replit agent is great for getting something up fast but the moment you want reproducible deploys + custom domain + actual database rules it falls apart. thats why i ended up moving my side stuff off it. enter's cloud + cli combo is closer to what i wanted but the logs piece is genuinely missing.

**Tree 2**

user1: im a bit confused about the stripe piece. you said the agent wires up the webhook handler. does enter actually handle the subscription state for you (cancel at period end, failed payment retry, grace period) or do you still have to write that logic yourself? because that part is what kills me on every AI builder i try, the moment a payment fails im writing webhook code by hand

user2 reply to user1: from what i can tell enter handles the infrastructure (receiving the webhook, exposing an endpoint) but the subscription state machine is still on you. which honestly is fine, i would not trust any AI builder to make that decision for me anyway. the value is just not having to deploy a separate service for it

user1 reply to user2: yeah that tracks. i keep seeing founders on twitter claim their AI tool "handles stripe" and then their customers get double charged during a retry. at least the post is being honest about where the line is

**Tree 3**

user1: how does this compare to lovable? i have been using lovable for a few months and the auth + database + stripe path is pretty smooth. the part thats missing for me is the local terminal agent piece, which is exactly what you are describing. curious if you tried lovable before going this route

user2 reply to user1: tried lovable, the UI gen is fast but the moment i wanted to actually own the code + run tests locally i had to download the zip and pretend it was a normal repo. enter's "you can run enter code in the same project" thing is the differentiator for me. not saying its better for everyone but for the terminal-first crowd it clicks

**Tree 4**

user1: the "agent loops and retries the same failing deploy 3 times" thing is exactly why i cant fully trust terminal-driven deploys. what stops the agent from eating your credits during a bad retry storm? is there a rate limit on the enter CLI side or do you have to enforce it on the agent prompt level only

user2 reply to user1: rate limit exists but its generous. the real guardrail i added was a hard rule in CLAUDE.md: "if a deploy returns the same error twice, stop and surface it to me." before that i once burned through a weeks worth of credits in an afternoon because the agent kept re-running the same broken migration

user1 reply to user2: yeah that is the kind of thing no marketing page will ever tell you. appreciate the honesty

**Tree 5**

user1: genuine question, do you ever worry about the agent shipping something you didnt intend? like a slightly different schema or a "fix" that quietly changes a query. with a web dashboard at least you can eyeball the change before clicking deploy. with a chat message it feels like the review step gets skipped

user2 reply to user1: it does, thats the tradeoff. what i started doing is asking the agent to print a diff summary before it runs the publish step, and i have to reply "go" before it actually deploys. annoying but its the only way i found to keep the review step. would be nice if the CLI had a dry-run mode that just shows what it would change

## Standalone Comments

user1: saved this, exactly the kind of honest 2 month log i was looking for

user2: the postgres + auth + storage all in one CLI call is the bit that gets me. that alone is worth trying for me, ive been duct taping supabase to vercel to stripe for too long

user3: the secrets part is where i draw the line too. AI agent + raw API keys in context = no thanks

user4: curious if you tried base44 before settling on this. they market themselves as the "post-demo" platform and i wondered how they compare on the terminal side

user5: fr this is what i want from every AI builder, stop making me click deploy in a browser like its 2019

user6: can confirm the function logs thing is real, i hit the same wall last week and had to open a tab anyway. hoping they ship a `enter logs` command soon

user7: the "i ship more often because deploy is a chat message" observation is so underrated. friction is the real enemy of side projects

user8: im a bit skeptical of the "no code review" angle but your diff summary workaround is smart. what does that look like in practice, is it a custom skill or just a prompt prefix

user9: what stack is enter code running on under the hood? react + vite? trying to figure out if i can plug in my existing component library or if im starting from scratch

user10: the part about AI hallucinating auth code is the most honest sentence in the whole post. every AI builder ad on my timeline should be required to print this in the footer
