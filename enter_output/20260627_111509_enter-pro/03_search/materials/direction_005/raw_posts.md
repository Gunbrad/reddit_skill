# Reddit Raw Posts

Generated at: 2026-06-27T03:54:20.398523+00:00
Total posts: 10

## Post 1

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/Supabase
Title: Solo dev at a small company — how should I structure Supabase for multiple internal products? (And is Supabase even the right call?)
Post URL: https://www.reddit.com/r/Supabase/comments/1u1ppfp/solo_dev_at_a_small_company_how_should_i

Body:

Hi everyone. I'm a frontend dev (~2 years) working as the sole developer at a small company.

I'm building an internal admin tool and an app/web service. The frontend side has been manageable with my existing skills — Next.js + Vercel for web, React Native + Expo for mobile. The part I'm unsure about is the database.

Some background: on personal projects, I'd just spin up a new Supabase project for each one without much thought. My previous company used MongoDB on a Hetzner server. But now I'm the only one handling everything, so instead of managing my own servers (AWS, Hetzner, etc.), I want to consolidate on a managed backend.

Here's where I'm stuck. On the Pro plan, the first project is included but each additional project costs $10/month. We'll likely have around 3 internal products. So I started thinking it might be better to put everything (admin data, app data, web data) into a single Supabase project separated by schemas, rather than one project per product.

My questions:

For multiple internal products under one company, is a single project split by schemas the right approach? Or are there real reasons (cost aside) to separate into multiple projects?

Some of this data has different access levels — admin data should only be accessible by internal staff, while app data is accessed by end users. In a single DB, what's the right way to cleanly separate this? Is schema separation the mechanism for that, or should I rely on RLS + key strategy (server-side secret key for admin, publishable key + RLS for the app)? I'm trying to understand which layer actually enforces access control.

One more thing I'd like a reality check on: Given that I'm a solo dev with no infra background, I leaned toward Supabase specifically to avoid managing my own DB (backups, patching, n

...[truncated]

Score: 1
Comment count: 11

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "tips",
  "author": "legoo23",
  "final_url": "https://www.reddit.com/r/Supabase/comments/1u1ppfp/solo_dev_at_a_small_company_how_should_i/"
}
```

Loaded comment tree:

reported_comments: 11
loaded_comments: 11
included_comments: 11
top_level_comments: 7
max_comment_depth: 3

Comment Tree 1:

uberneenja: it sounds like you'll have 3 different things that dont share business logic, code, etc. 3 distinct services/apps. i'd say bite the bullet and do 3 supabase projects. Here's a few reasons off the top of my head: - If 1 grows really big, you can scale the 1 without scaling the others - Every update, you'll have to worry about vulnerabilities between all 3 apps - which is easy in postgres with RLS if you're not careful - multiple schemas vs just public - leaked data across apps if someone gets in - unified auth but 3 different apps (could be a good thing or a bad thing) On the self hosting ... which is what i personally do, i have coolify with like 4 supabase instances. it's funny b/c i still pay like $50 / mo for that hetzner vps, but there's other stuff on there too and i mostly do mobile

...[truncated]

Comment Tree 2:

wessex464: I'm using neon after realizing supabase had database number limitations.
	ivasilov reply to wessex464: Hi, can you explain what you mean by "database number limitations"? We may have an error in the docs, so I'm trying to fix it.
		wessex464 reply to ivasilov: Sorry, I wasn't clear. I meant limitations on the free account only being allowed 1 database(maybe two?) before you need to move to a paid plan. Neon allows users to have multiple databases on the free plan. I was creating multiple tenants of the same very small app and neon was just a better fit.
			ivasilov reply to wessex464: Oh, yeah, that makes sense. We allow 2 projects per user on the free tier. Glad you found a solution that works for you, I hope your project becomes successful 😄
	LettuceBasic3679 reply to wessex464: Wait until you discover you can self host

Comment Tree 3:

Life-Profit-3484: What is the difference between admin, app and web data. Do they have any relationship? If the data has relationship and you dont anticipate the data to get super large in the next 2 years then you can put them in the same DB and archive any old data to a Data warehouse. If you dont want to pay the extra $10 look into self hosted Supabase or just plain psql if thats possible.

Comment Tree 4:

peetabear: Separate schemas might be a nice idea. You can dump schemas into separate projects in the future. I would opt for one project right now because you have Auth data in the one project as well, which means less complexity for now. Role and permissions is something you can have as a simple configuration file for now then expand into a more complex architecture when needed. Just keep things simple and stupid for now and migrate when complexity arises

Comment Tree 5:

Emotional-Stand-9987: I'm basically building something very similar in terms of architecture, though mobile is last on my list. There is the unified business web app, which includes operations/management activities. There are two separate public facing websites. I've definitely made the decision to move the websites to their own project. I originally wanted the public facing websites to have a lot of interactive stuff for clients, but the security risks are too high. Right now, separating the management stuff like clients and invoicing and stuff unrelated to my actual service business is still integrated. It will be harder to separate this. The tools are all there for projects to communicate with each other. So it's very possible. The cost is more money, migration time, and some added maintenance complexity. It

...[truncated]

Comment Tree 6:

Radiant-Chipmunk-239: I've done it many ways. Each environment gets its own instance. Each product gets its own instance and each environment gets its own persistent branch. that is where I am now, each product with persistent branches for dev, qa, prod. I have not run into scalability issues as of yet. My next thought would be to have a dedicated production database and then all other environments would share another.

Comment Tree 7:

swiftbursteli: If you DO go selfhosted like I did. Do not look at anything else: just setup supabase. It’s literally the best thing on the market and there’s nothing that comes close. For managed, multi project management when you’re a full stack eng/ the whole team I would use railway. I found it to be easier to setup the webserver to work - just like you want it to. I don’t have to write in deno or rely on some magic box to figure something out… just throw an Opus 4.8 at a node.js project and tell it to wire up your webserver. Pros for supa: - Supabase offers secure REST and graphQL endpoints for every data table. - Their UI is second to none. - I think their magic link and OAuth is more foolproof - Basically makes a 2-tier architecture. The BaaS and the client. Pros for Railway: - Simpler pricing, che

...[truncated]

## Post 2

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/Supabase
Title: Billing on Supabase + Stripe: the edge cases nobody warns you about
Post URL: https://www.reddit.com/r/Supabase/comments/1u8o4od/billing_on_supabase_stripe_the_edge_cases_nobody

Body:

Just shipped subscriptions (checkout, upgrades, downgrades, cancel flow,
customer portal) on a Next.js + Supabase app. Estimated 2 days. Took ~2.5
weeks. Sharing the stuff that ate the time so you don't repeat it:

Webhooks are the whole game. The client redirect after checkout lies —
the user can close the tab. `customer.subscription.updated` (and
`.deleted`) is your real source of truth. Build your state off webhooks,
not the success URL.

Raw body or bust. Stripe signature verification needs the RAW request
body. If any JSON middleware touches it first, verification fails with a
cryptic error. On Next.js route handlers this bites everyone once.

Idempotency. Stripe retries webhooks. Without a dedupe layer you'll
double-apply events (double-grant access, double-email). Store processed
event IDs.

Proration math — don't do it yourself. Let Stripe compute it
(`proration_behavior: 'create_prorations'`). Hand-rolling mid-cycle
upgrade/downgrade math is a bug factory.

The portal + feature gating gap. Stripe gives you a billing portal, but
mapping "this plan = these features unlocked" back into your app is on
you. That sync (and keeping it correct on plan changes) was half my time.

Failed payments. Card declines are silent unless you handle
`invoice.payment_failed` + dunning. Easy to forget until revenue quietly
leaks.

Happy to answer questions / look at anyone's webhook handler if you're
stuck. What did the rest of you use to handle this - roll your own or a tool?

Score: 23
Comment count: 17

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "tips",
  "author": "kush0007",
  "final_url": "https://www.reddit.com/r/Supabase/comments/1u8o4od/billing_on_supabase_stripe_the_edge_cases_nobody/"
}
```

Loaded comment tree:

reported_comments: 17
loaded_comments: 5
included_comments: 5
top_level_comments: 2
max_comment_depth: 2

Comment Tree 1:

Cast_Iron_Skillet: Why are there So many weird new lines in your post?
	Varquel reply to Cast_Iron_Skillet: It reminds me of the formatting gore from copy pasting text from the Claude Code terminal.
		TalosStalioux reply to Varquel: You are absolutely right. claude 2026
		qu1etus reply to Varquel: Without the courtesy of fixing it Before clicking Post.

Comment Tree 2:

ashkanahmadi: Thank you for sharing, ChatGPT.

## Post 3

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/SaaS
Title: A Vercel + Supabase scaling lesson from building my SaaS
Post URL: https://www.reddit.com/r/SaaS/comments/1t2xj78/a_vercel_supabase_scaling_lesson_from_building_my

Body:

I'm building a SaaS on Vercel + Supabase, and I ran into an issues that looks like a small production warning thing first, but turns into a useful architecture review once I actually pulled the thread and did a proper audit session.

The warning was around database connections. (random error when uploading small files)

The upload itself worked most of the time, but I saw a Supabase connection warning and the random errors in production and decided to dig into it.

It was more the usual SaaS stack adding up..

Next.js layouts doing auth/account/program reads

tRPC calls kicking off right after render

dashboard widgets fetching their own state

status/checklist components polling

Vercel cron jobs touching the database in the background

Supabase pooling configuration being more important than it looks in local dev

service functions doing a few clean reads each, which is nice for code clarity until the page-level fanout gets high

Individually, all of that is normal. Together, it can quietly become connection pressure.

With Vercel serverless + Supabase, you don’t just think in “is this query fast?” You also have to think in:

how many separate DB touches happen per page load?

how many happen again from client-side hydration?

what is polling in the background?

what do cron jobs do every minute?

are we using the right Supabase pooler mode for this runtime?

do our indexes match real access patterns, not just schema relationships?

These are the types of things, probably most of vibe coders will miss completely and will cause the SaaS crashing, once you get actual users.

I am lucky to have some development background, so I managed to realise what's going on or rather where I have to dig.

It’s adding a few boring guardrails:

explicit pooler/env checks for productio

...[truncated]

Score: 5
Comment count: 7

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "",
  "author": "TheBanq",
  "final_url": "https://www.reddit.com/r/SaaS/comments/1t2xj78/a_vercel_supabase_scaling_lesson_from_building_my/"
}
```

Loaded comment tree:

reported_comments: 7
loaded_comments: 4
included_comments: 4
top_level_comments: 2
max_comment_depth: 1

Comment Tree 1:

[deleted]: Low-Effort/AI content is auto-removed. I am a bot, and this action was performed automatically. Please contact the moderators of this subreddit if you have any questions or concerns.
	AutoModerator reply to [deleted]: Low-Effort/AI content is auto-removed. I am a bot, and this action was performed automatically. Please contact the moderators of this subreddit if you have any questions or concerns.

Comment Tree 2:

[deleted]: Yes, that’s exactly the direction I’m taking now. It's really misleading, when the app feels fast while the total DB touch count is already too high. I’m going route by route now: layouts, tRPC, widgets, polling, cron, webhooks. I like the idea of a hard page budget and one shaped 'page payload' instead of every widget doing its own clean little query. Also agree on making live diagnostics opt-in, not default background noise.
	TheBanq (OP) reply to [deleted]: Yes, that’s exactly the direction I’m taking now. It's really misleading, when the app feels fast while the total DB touch count is already too high. I’m going route by route now: layouts, tRPC, widgets, polling, cron, webhooks. I like the idea of a hard page budget and one shaped 'page payload' instead of every widget doing its own clean little query. Also agree on making live diagnostics opt-in, not default background noise.

## Post 4

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/devops
Title: Confused DevOps here: Vercel/Supabase vs “real” infra. Where is this actually going?
Post URL: https://www.reddit.com/r/devops/comments/1quver2/confused_devops_here_vercelsupabase_vs_real_infra

Body:

I’m honestly a bit confused lately.

On one side, I’m seeing a lot of small startups and even some growing SaaS companies shipping fast on stuff like Vercel, Supabase, Appwrite, Cloudflare, etc. No clusters, no kube upgrades, no infra teams. Push code, it runs, scale happens, life is good.

On the other side, I still see teams (even small ones) spinning up EKS, managing clusters, Helm charts, observability stacks, CI/CD pipelines, the whole thing. More control, more pain, more responsibility.

What I can’t figure out is where this actually goes in the mid-term.

Are we heading toward:

Most small to mid-size companies are just living on "platforms" and never touching Kubernetes?

Or is this just a phase, and once you hit real scale, cost pressure, compliance, or customization needs, everyone eventually ends up running their own clusters anyway?

From a DevOps perspective, it feels like:

Platform approach = speed and focus, but less control and some lock-in risk

Kubernetes approach = flexibility and ownership, but a lot of operational tax early on

If you’re starting a small to mid-size SaaS today, what would you actually choose, knowing what you know now?

And the bigger question I’m trying to understand: where do you honestly think this trend is going in the next 3-5 years?
Are “managed platforms” the default future, with Kubernetes becoming a niche for edge cases, or is Kubernetes just going to be hidden under nicer abstractions while still being unavoidable?

Curious how others see this, especially folks who’ve lived through both

Score: 11
Comment count: 31

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "Ops / Incidents",
  "author": "Abu_Itai",
  "final_url": "https://www.reddit.com/r/devops/comments/1quver2/confused_devops_here_vercelsupabase_vs_real_infra/"
}
```

Loaded comment tree:

reported_comments: 31
loaded_comments: 30
included_comments: 30
top_level_comments: 13
max_comment_depth: 3

Comment Tree 1:

hijinks: Vercel/Supabase are just modern day heroku. I've been hearing my whole career that serverless is gonna take my job. I'm now paid more then most devs for what I do. Try to run a app with a lot of traffic on vercel and either it's gonna fall over or yor will be paying 10x the costs of running it on AWS Vercel/Supabase is fine to start. Dont spend where you dont have to. If you need an app up and updated when you git commit then that's a great option. Just dont keep the mindset of because you started there it needs to run there. When you start your saas its silly to think you need to be in AWS/Kubernetes more so if you don't have experience there. Get your stuff running. The worst thing founders do is think they need to deploy to something that'll handle 100k req/s when they only have 2 custo

...[truncated]
	Abu_Itai (OP) reply to hijinks: The question is what happen if they will scale in the future and will need that capacity, how easy is the transition to more “robust” infra?
		Rollingprobablecause reply to Abu_Itai (OP): All migrations are very much "it depends" you're never going to get a good answer to this simply because every app is built with such a wide diversity of languages, handling, memory, infra, etc.
			worldofzero reply to Rollingprobablecause: If you were using PAAS tools with the goal of shipping fast migrations are going to end up somewhere between a full rewrite and massive amounts of time honestly. Part of the design of those systems is to give you pieces that if you build upon can't be used anywhere else.
		emanuele232 reply to Abu_Itai (OP): If the applications are designed with a somewhat intelligent design it should not be a major problem, but: If you are accepting the (insert heroku flavour) vendor lock in, it is because you do not have the capabilities/time to think about a “and what if we need to serve 50 million customers?” This postpones the migration until you are forced to (due to the saas tax eating your margins) and then it is a bloodbath. The point is that majority of startups fail long before that, so that’s a problem to be solved by the big ass corp that is going to buy the startup E.g. you talk about not deploying your monitoring stack, but at scale saas monitoring is going to cost you 10x the applications it is monitoring
		ShoneBoyd reply to Abu_Itai (OP): Depends, if they have not planned for it then they will probably eat up the cost until they get someone to migrate their backend to a suitable offering.
		hijinks reply to Abu_Itai (OP): depends on the person/people doing the migration
	InfraScaler reply to hijinks: Try to run a app with a lot of traffic on vercel and either it's gonna fall over or yor will be paying 10x the costs of running it on AWS The debate used to be "(on AWS) you will be paying 10x the costs of running it on bare metal". This is funny!

Comment Tree 2:

Rollingprobablecause: This has been around forever and is nothing new. All of this is known as PaaS (or some adjacent typing). Startups use these services for a myriad of reasons: lots of cash to burn, lack of infra dedicated folks to help them, needing to prototype quickly, or the code is very simple at the moment PaaS services like these (I think you're missing another big player in Heroku) are very good at piecemeal infrastructure and silo'd or simplified systems but they are incredibly expensive as you get bigger. There's also an insane amount of limitations to them in terms of flexibility and customization and rightfully so as they are designed as highly availably/low touch ecosystems For example: our companys has a massive AWS blueprint and we have a large infra team that handles the day to day devops/pla

...[truncated]
	Abu_Itai (OP) reply to Rollingprobablecause: Nice, thanks for this response, maybe they are here for 10 years or more, but we see more and more “soloprenuers” building their stuff on those platforms what raise questions if this is the actual form of”the future” companies

Comment Tree 3:

FromOopsToOps: Remember that "cloud is just someone else's on prem"? Paas is just someone else's k8s. This trend will lead exactly to where the other trends led: on prem guys keep getting pushed up the food chain, working for the Paas providers. The same way they (including me) were pushed from on prem to cloud. Take the short path in career and you will end up doing deployments to Paas for a while, then you study a lot and move up the chain.
	Abu_Itai (OP) reply to FromOopsToOps: The question is if it’s not cheaper to get this “high costs” in paas what on the other side save some money from hiring a professional
		FromOopsToOps reply to Abu_Itai (OP): That's a business decision. Sometimes paying more for infra will be cheaper than hiring a dedicated person, sometimes having a dedicated person will be cheaper. All in all it's a business decision. Not a technical one.
		phoenix823 reply to Abu_Itai (OP): If it's more work and more risk to pay a professional (build) rather than throw money at it (buy) the buy option is very often a better business decision. A product has to get pretty big before it needs professional infra IMO.

Comment Tree 4:

TheOwlHypothesis: I think PaaS like Vercel and others that make deployment "magical" are the future. Like I host on railway because even though I'm capable of rolling EKS myself and building app/infra end to end, I don't want to at the end of the day lol. I just want to ship.
	emanuele232 reply to TheOwlHypothesis: You do not want to manage infra -> you notice that the four middlemans you’re paying cost more than dev cost -> you manage your infra Rinse and repeat at every management change
	bit_herder reply to TheOwlHypothesis: it always trade offs. price / ease of use / control of data. my entire career has been moving things around between cloud, on prem, and PaaS. i don’t see any of them as “the future” they are juts different choices and the best one depends on several factors
	Abu_Itai (OP) reply to TheOwlHypothesis: Did you encounter and difficulties in the past that made you question yourself? Or it’s just a clear advantage? And you think it’s good for scale as well? Thanks

Comment Tree 5:

schmurfy2: It all depends how much you want to pay someone else to manage your infrastructure, vercel, heroku habdle a lot for you and cost a lot and on the opposite end you have your own servers you manage with a lot in between.

Comment Tree 6:

noobbtctrader: These out of the box infrastructures can only support up to so much concurrency. Once you start getting some real ass traffic I'd expect headaches. At that point youd be relying on their engineers vs your own. And if time is money... youre fucked. But, some small fry SaaS with 30 concurrent users or a lil demo/poc, no sweat. The only reason there was such a resurgence in managed infra is due to all the devs vibe coding who are trying to avoid the infra aspect and just want some turnkey shit. Its not really for prod IMO.
	phxees reply to noobbtctrader: I don’t know which ones, but some of those services have/will prove to be rock solid and over built. I know some of those teams left top companies and took what they learned to make services which can likely handle more traffic then their customers could ever reasonably send them.

Comment Tree 7:

Express-Category8785: One of the earliest lessons I was taught is that engineering is not "how can we do this?" If anything, that's science. The engineering question is "how do we do this practically?" Which effectively means maximizing the doing versus the cost. What's left out of the platform vs ops comparisons above is that PaaS costs more than SaaS costs more than on prem, often integer multiples more. Very quickly, those differences add up to FTE salaries.

Comment Tree 8:

JasonSt-Cyr: When I'm having something small, going the Vercel route (or Netlify/Supabase/whatever platform) is always the easy choice. It's easy to get started, you can accelerate quickly, and the low-end usage tiers are extremely cost efficient for what you get. The OOTB low-end plans for Vercel are ridiculously good. But they have built in limits to make sure that when you really start to push the platform you are either going to be paying overages or going up a tier, and those are NOT cheap. They aren't going after the small mom-and-pop shops, that low-level tier is really about getting devs into their technology to be dependent on it so they champion it internally at a bigger enterprise. Groups like Vercel want to sell to a big corp and make $150K a year on them. That's why they go after things li

...[truncated]

Comment Tree 9:

nihalcastelino1983: Use vercel/netlify for initial setups and demos and quick proof of concepts. But they may not scale.supabase is hosted postgres. I use them and it's good I like them .
	emanuele232 reply to nihalcastelino1983: Every saas service is OSS + ui + automagic configurations or a collection of multiple services that are coherent among them. Not that I don’t see value in that but there are drawbacks

Comment Tree 10:

faridmmv: Solid for MVPs, but the non-linear pricing makes scaling expensive fast. Plus, you lose flexibility by having to wait for their specific feature updates. It’s fine for starting small, but once you need more control and resources, a migration to proper infrastructure is almost inevitable.
	Abu_Itai (OP) reply to faridmmv: The question is at which stage a startup will decide to make that move to a “real” infra managed by the company

Comment Tree 11:

road_laya: I've seen smaller businesses going deep on infra and make a profit, but they did so by hiring foreigners far below market rates for ops, undercutting AWS prices for storage at large scale and have their staff being 24/7 on call. Spinning up Kubernetes clusters is needed for some applications, but for many smaller businesses it's wasted effort on capacity they will never need.

Comment Tree 12:

orphanfight: It's an old trend, tl;dr - gets too costly.

Comment Tree 13:

duxbuse: So my take is that serverless is great, but so is fixed predictable costs. As such I think the only future where you can achieve both is `Kubernetes just going to be hidden under nicer abstractions `. But its worth noting I'm pretty biased as I work for suga.app

## Post 5

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/SideProject
Title: If you’re using vercel, firebase, supabase, render, etc … what are you paying and why not just use your own server?
Post URL: https://www.reddit.com/r/SideProject/comments/1mg7tec/if_youre_using_vercel_firebase_supabase_render

Body:

If you have personal projects, side apps, maybe a saas… how are you hosting them?

Are you using things like supabase, fly.io, vercel, firebase, render, planetscale, or other similar services?

What are you paying per month? How many apps are you running? What made you pick that solution?

Every time I see someone paying for multiple services just to keep a few small apps online, I think they could probably run all of that on a $6 vps. I have a single server. I have a number of small projects on there, databases, multiple domains, running a mix of different stacks.

But I get why that doesn’t always happen. Not everyone wants to deal with linux, nginx, firewalls, updates, and everything else that comes with running a server.

So I’m curious. What’s keeping you from using a single vps and putting all your apps on there? Is it a time thing? Too much setup? Not worth the hassle?

I just want to hear how people are approaching this. Thanks in advance if you’re willing to share.

Score: 46
Comment count: 54

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "",
  "author": "ryantxr",
  "final_url": "https://www.reddit.com/r/SideProject/comments/1mg7tec/if_youre_using_vercel_firebase_supabase_render/"
}
```

Loaded comment tree:

reported_comments: 54
loaded_comments: 46
included_comments: 30
top_level_comments: 24
max_comment_depth: 9

Comment Tree 1:

Jaydgaitin: I’m a dumb ass. And don’t know how so I use the easiest option. Lol
	SamWest98 reply to Jaydgaitin: [Deleted

Comment Tree 2:

Mr_Matt_Ski_: I pay Vercel and DO about $80 a month to host my SaaS which generates about $6k MRR. I have no interest in dealing with infrastructure and it really frees me up, so I can do what I find enjoyable like build features and make sales.
	AssCooker reply to Mr_Matt_Ski_: Do you use a single managed database instance?

Comment Tree 3:

imagei: What’s stopping me? Security. I can set up a server and the services just fine, but securing it all is a whole different matter (and yes, some dev/test servers I had before had been pwned). Right now the time has come for me to do it right, so I’m teaching myself how to build and secure a Kubernetes cluster using Talos Linux… it’s a significant time investment that I hope will pay out, but it is not for inexperienced people.
	Suspicious-Engineer7 reply to imagei: Seconded. Security and other concerns are domains that I might be interested in but realistically it's something that you'll always have to keep up with and that can cost a lot of time. It's a penny wise dollar foolish type of situation.
	Unhappy_Meaning607 reply to imagei: In what ways have you pwned setting up your own servers? Genuinely curious because one person I follow (DHH) has been on a anti-AWS "let's go back to setting up baremetal servers on-prem" tirade.
		imagei reply to Unhappy_Meaning607: Forgetting to do something or not knowing it had to be done. That’s why Kube with a strict network manager like Cilium is a better solution, for us at least — on a traditional server everything is allowed until you block it; here you can set the „everything is disabled until you explicitly enable it” policy, you have policy analysers, anomaly detection etc. If you think of migrating from AWS you’ll find the concepts quite comparable. It won’t be on prem though, probably on Scaleway.
			1coon reply to imagei: You could have another layer of redundancy by setting up a Proxmox (or similar hypervisor) cluster and then run a Talos cluster within it. Set up your own VPN, use Cloudflare tunnels or something like Tailscale for access control and route anything public-facing through an OPNsense VM that has a default deny-all rule. Then selectively enable traffic for individual services or routes as needed. It’s somewhat complicated to wrap your head around at first, but Proxmox gives you such an easy way to store snapshots and backups either on-prem or on a different server and roll them back that learning it can actually be super fun if you’re into this kind of thing. However I’d probably recommend starting out with a homelab before deploying something like this on baremetal or the cloud.
				imagei reply to 1coon: Yes, that’s pretty much what I have in mind, minus the Proxmox bit — I’m not sure I feel good about securing everything with a zillion rules and then having the nuclear option just a login away. Talos is immutable and with atomic auto-rollback upgrades but I suppose having one more safety net layer can’t hurt. I may look into securing access to Proxmox better. Thanks for super informative hints!!
		cmd-t reply to Unhappy_Meaning607: Basecamp can hire people to manage their servers full time.
	top_ziomek reply to imagei: so that's basically it then, those hosting operations are basically preying on security fud of their customers
		AsleepDeparture5710 reply to top_ziomek: No, they are also useful. Plenty of customers are behind NAT policies that make it hard to impossible to self host, and most cloud provider business is still commercial, where servers are a cost.

Comment Tree 4:

Warlock2111: It costs 20/month for me (vercel) The app generates way too much relative to that to me even bother spending my time optimising it to save a potential 12/month. I can understand needing to worry about infra costs if you can significantly bring it down. But if you are even making 1k/mo, the $20 is negligible. Put the time you’ll save in marketing, sales or product

Comment Tree 5:

Scary_Statistician98: I use Firebase (free tier) and host the website on GitHub—so there’s no monthly cost.

Comment Tree 6:

[deleted]: I pay $30 a month for a VPS with Hetzner. It runs coolify, and about 8 different projects. Have had zero issues in the last year, spinning up a database or new service is just 2 or 3 clicks away, couldn’t be easier.
	AssCooker reply to [deleted]: You use Hetzner US server?
		[deleted] reply to AssCooker: Their servers are in Germany.

Comment Tree 7:

ulrichgero: Vercel on front-end and render as back-end. Don't have time to setup everything on own VPS.

Comment Tree 8:

TreeTopologyTroubado: I’ll preface this by saying I’m a software dev with a decade of experience with cloud deployment. I’ve worked with or for the top three CSPs out there so I know how to deploy scalable web applications with enterprise grade observability and security. I don’t want to deal with all that for my personal projects. I’ll gladly pay an extra $20/month to someone else so that they can deal with it.
	BadOwn8308 reply to TreeTopologyTroubado: Which Front-End, Database, and Backend do you prefer? I'm seeing a lot of Vercel, Supabase, Render combos. I've also wondered how that compares to a full-stack in Firebase.

Comment Tree 9:

A_Sherminator: ryantxr, I'm with you on this one. I use a VPS hosted by hosting.com. I've had it for 4 years and never had a problem. I pay $250 per year for unlimited domains, unlimited databases, unlimited traffic. It's Webuzo based (similar to cPanel). I host over 15 websites using 7 different databases. Yes, I have to deal with the setup of the DBs and the SQL user security. Yes, I get a nightly email saying that the database has backed up successfully. Minor hassle but I've never had a problem. The good part is in addition to my SaaS projects I get to provide hosting for my clients and upcharge them. Would I do this for a client in the healthcare of financial industry... hell no. But for non-critical websites/clients, a VPS works great.

Comment Tree 10:

TheInterestingSoul: At least these tools enable (and actually encouraging) more users without some decent technological backgrounds to participate in indie dev, startups, etc., or at least building their own gateway on the Internet. That said, there is some attempts to save the pain of handling VPS while remain flexibility. One of solutions I tried was Kamal, coming from Ruby on Rails community but suitable with any stacks. Basically it tracks your local change using Git and pack them in a Docker image.

Comment Tree 11:

WishIWasOnACatamaran: For me it’s the timeline I’m on. Started a month ago and YC application deadline is this Monday. My platform has eaten up essentially this entire month, and I don’t have more time or money to worry about hosting. Can worry about self-hosting once I get funding for it. If I was doing something simple and cheap I’d self-host for sure though.

Comment Tree 12:

azdbacks02: One of this better than the other?

Comment Tree 13:

Substantial_Can_700: I recently launched a small SaaS tool to help freelancers analyze vague client briefs and turn them into structured project plans — something I’ve often needed myself. I built it in a couple of evenings and hosted it on Vercel. Honestly, I’m only paying for the domain. Since it’s built with Next.js and doesn’t rely on a database, the free tier is more than enough. I totally understand the appeal of a VPS — I’ve used one before for personal stuff — but for something I wanted to test quickly, Vercel was a no-brainer. Minimal setup, great DX, and deploys in seconds. If it grows, I might move to something more scalable like Fly.io or a VPS, but right now, simplicity > control.

Comment Tree 14:

top_ziomek: all the answers here basically boil down to "they don't know how"

Comment Tree 15:

MohammadAbir: it's a time thing for me. i could spin up a vps and configure everything myself, but then i'm also the one dealing with security patches, monitoring, backups, and all the random stuff that breaks at 2am. platforms like Render handle that for you, plus you get things like automatic scaling and zero-downtime deploys.

Comment Tree 16:

wtjones: It’s hard to beat Vervcel for build and deploy setup.

Comment Tree 17:

bmazz731: There are so many distractions when you get started, I think using free tiers is worth starting. Once you make money, you assess the cost savings for self hosting vs focusing on your project.

## Post 6

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/vibecoding
Title: Vibe Coder Here: Need Help Choosing a Database for My First Full-Stack Apps (Supabase vs Firebase vs Others?)
Post URL: https://www.reddit.com/r/vibecoding/comments/1qv0mqh/vibe_coder_here_need_help_choosing_a_database_for

Body:

Hey everyone!

I'm what you might call a "vibe coder" – I've been prompting my way through building frontends, UI/UX projects, and intermediate n8n automations with zero traditional coding background. It's been working great so far, but now I want to level up and build fully functional apps with actual databases.

The problem? I know absolutely nothing about databases or how to integrate them. I've heard names thrown around like Supabase, PostgreSQL, Firebase, and MongoDB, but I'm honestly lost on where to start.

What I'm looking for:

Free tier options (I'm totally fine with limitations – just want to test things out before committing)

Something beginner-friendly enough for someone with no backend experience

Works well with the vibe coding/AI-assisted workflow

Good for building frontends that need to store user data, authentication, etc.

My use case:

Building web apps and websites with dynamic data

User authentication

CRUD operations (I think that's what it's called?)

Mostly frontend-focused, but need a reliable backend

I've heard Supabase mentioned a lot and it seems popular with the no-code/low-code crowd. Firebase also keeps coming up. Are these good starting points? What would you recommend for someone in my position?

Would really appreciate any guidance, resources, or even just a nudge in the right direction!

Thanks in advance 🙏

P.S. If anyone has tutorials or resources specifically for integrating databases with AI-assisted coding workflows, that would be amazing!

Score: 6
Comment count: 38

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "",
  "author": "Mission-Dentist-5971",
  "final_url": "https://www.reddit.com/r/vibecoding/comments/1qv0mqh/vibe_coder_here_need_help_choosing_a_database_for/"
}
```

Loaded comment tree:

reported_comments: 38
loaded_comments: 34
included_comments: 30
top_level_comments: 17
max_comment_depth: 3

Comment Tree 1:

rjyo: Supabase is the move for vibe coders, hands down. I went through the same decision and here is why: Supabase is built on Postgres (the most battle tested database), so you get real SQL if you ever need it Auth is built in and works out of the box with email, Google, GitHub etc The dashboard lets you see your data visually which is huge when you are learning Free tier is generous (500MB database, 50k monthly active users) Claude and other AI tools already know Postgres/Supabase syntax really well, so your vibe coding workflow stays smooth Firebase works too but you will hit NoSQL quirks that are harder to debug when things go wrong. Supabase feels more predictable. For CRUD operations specifically, Supabase has a JavaScript client that makes it dead simple: const { data } = await supabase.f

...[truncated]
	dkracket reply to rjyo: Tip: copy the docs page into ChatGPT and it'll guide and help you to navigate supabse. It can also write SQL prompts for you to run if necessary.
		Mission-Dentist-5971 (OP) reply to dkracket: I was thinking of self hosted version of supabase for testing purposes, what’s your thoughts on it?
			Training-Flan8092 reply to Mission-Dentist-5971 (OP): I’d go this route for dev. Local postgre with supabase wrapper on it (AI will know what to do). After you figure out what your storage and egress is, then take a look. This will also protect you from getting some minor charges or nasty emails as you’re building and learning.
	Mission-Dentist-5971 (OP) reply to rjyo: THANK YOU!!
		x365 reply to Mission-Dentist-5971 (OP): Supabase is great. Before you launch spend some serious time understanding RLS (Row Level Security). It’s make or break in terms of security with Supabase (and Postgres).

Comment Tree 2:

SeeeRGo88: Supabase is a great choice to start. Very friendly to vibecoders. I'd like to also mention Convex.dev It seems models are less trained to work with it and sometimes struggle with using convex, but there are two main advantages: 40 projects on free tier instead of 2 and reactivity out of the box - you don't have to write any code to keep up with actual state of the DB. Otherwise they pro idea pretty much the same features

Comment Tree 3:

Sergiowild: supabase is the right pick here. everyone else already said why so i'll add the part most people skip - how to actually wire it up with vibe coding: start with supabase's table editor to create your tables visually (no SQL needed at first) grab the supabase js client, paste your project URL and anon key when prompting your AI, paste the table schema and say "use supabase-js to query this" - it'll handle the CRUD for you for auth, supabase has a built-in auth module that handles email/password, google login, etc. honestly the hardest part is just understanding row level security (RLS) policies but you can skip those while prototyping. don't bother self-hosting for testing. the free tier gives you 2 projects which is plenty to experiment with.

Comment Tree 4:

domgaulton: I built a cool boilerplate for this purpose - very easy set up and you'll have a working supabase backend and deployed frontend with vercel in no time. https://tanstack-start-supabase.vercel.app/

Comment Tree 5:

eninja: I have used Supabase for hashed user verification, Simple text data or chunks, & user presets. I use pinecone for vector storage

Comment Tree 6:

Ibrasa: I use supabase as a DB and as Auth. Literally the easiest thing to integrate I have two production systems running with supabase

Comment Tree 7:

[deleted]: Totally depends on the scale of your application and how many users are accessing. I like to build the database into my backend so you have no need for a third-party.
	Mission-Dentist-5971 (OP) reply to [deleted]: Elaborate please Its mainly for MVP purposes
		[deleted] reply to Mission-Dentist-5971 (OP): Here's a live application to open your mind. This is running entirely on my device over LTE right now. I'm simply using a free cloudflare to tunnel to proxy to localhost... The database, server, application live solely on my device. When you connect to my server you are directly interacting with memory on my phone. Even a low powered device like my phone could a large amount of simultaneous access to my data base. Try and make a app that you can spin up on a vps with no outside services...a machine, and internet connection is all that's actually needed. Edit: link turned off :)
			Mission-Dentist-5971 (OP) reply to [deleted]: WOW

Comment Tree 8:

Beneficial_Paint_558: I recommend 100% supabase. It has everything you need, easy to use, great UI/UX, a great MCP server to connect to Cursor and amazing pricing
	Mission-Dentist-5971 (OP) reply to Beneficial_Paint_558: I was thinking of self hosted version of supabase for testing purposes, what’s your thoughts on it?
		Beneficial_Paint_558 reply to Mission-Dentist-5971 (OP): forget about it, much more difficult to maintain and connect
			Mission-Dentist-5971 (OP) reply to Beneficial_Paint_558: What about using claude code/google antigravity to setup it up for me?

Comment Tree 9:

Your-Startup-Advisor: Supabase.

Comment Tree 10:

Exact_Audience8829: SQLite… simple file based sql database.
	Region-Acrobatic reply to Exact_Audience8829: I would recommend this too especially for starting out! I’ve used lightweight auth libs on top that were a breeze

Comment Tree 11:

Rook_Newbie: I’ve used both Firebase and Supabase. Supabase in my option is 10x better - will never use Firebase again. In supabase you can view your records in Excel like tables. Scales better from what I’m told. Integrates very well. I built my app using AntiGravity’s IDE using Opus and it is has been nearly flawless. Depending on your use case, you’ll likely have to run number of SQLs as you build it out by Opus writes them for you and you copy/paste/run in supabase. The other trick I learned with databases is ask Opus to write text scripts that your run inside the DevTools (F12) in your dev browser. Saving and retrieving records can be tricky as your tables evolve and running test scripts to test connections is much easier than running your app, making changes to a record and then trying to find it

...[truncated]

Comment Tree 12:

DevOps-B: Why don’t people just roll with MS SQL?

Comment Tree 13:

AntiqueIron962: Use the supabase local mcp. Opus done everything for you ^ you dont need to understand supabase, it work 😬💪

Comment Tree 14:

Dense_Gate_5193: all in one memory bank with vector embeddings managed for you. compatible with neo4j drivers and qdrant drivers for the same database. (it maps pretty neatly) and 0.17ms p95 for write latency. https://github.com/orneryd/NornicDB 3-50x faster than neo4j 40% faster than qdrant proper written in golang MIT license

Comment Tree 15:

SubjectHealthy2409: Try pocketbase, you'll learn backend and deployment basics

Comment Tree 16:

[deleted]: Please elaborate
	Mission-Dentist-5971 (OP) reply to [deleted]: Please elaborate
		[deleted] reply to Mission-Dentist-5971 (OP): Thank youu!!

## Post 7

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/vibecoding
Title: Simple stack sanity check: Lovable + Supabase + Stripe + Vercel
Post URL: https://www.reddit.com/r/vibecoding/comments/1rqddzp/simple_stack_sanity_check_lovable_supabase_stripe

Body:

Right now I have Lovable, Supabase, and GitHub connected, and I’m deciding on the best path forward.

Originally I planned to migrate the project to Claude Code, but now I’m considering just keeping the stack simple and building/deploying with:

•	Lovable (frontend + AI-assisted edits)

•	Supabase (auth + database + backend)

•	Stripe (subscriptions + transactions)

•	Vercel (deployment)

I’ve run the specs and project structure through a few LLMs and they all say this stack should handle what I need.

Core requirements:

•	User profiles

•	Stripe integration

•	Dashboards

•	Subscription model + fee-based transactions

My main concern is long-term maintainability.

Specifically:

•	Is it reasonable to rely on Lovable for managing the frontend and future edits, instead of moving everything into something like Claude Code?

•	Are there any scaling or flexibility downsides to sticking with this stack?

Curious if anyone here has built something similar or has strong opinions on this setup.

Appreciate any insight!

Score: 1
Comment count: 8

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "",
  "author": "chizton",
  "final_url": "https://www.reddit.com/r/vibecoding/comments/1rqddzp/simple_stack_sanity_check_lovable_supabase_stripe/"
}
```

Loaded comment tree:

reported_comments: 8
loaded_comments: 5
included_comments: 5
top_level_comments: 2
max_comment_depth: 3

Comment Tree 1:

CemJamX: Just checking if I follow your setup: You develop the frontend in Lovable, push it to GitHub, and then Vercel takes over the hosting? Sounds like a solid pipeline! A quick security note: Since you don't have a dedicated backend to communicate with Supabase, your anon key is exposed in the frontend. Make sure you have RLS (Row Level Security) active on all your tables to prevent unauthorized access.

Comment Tree 2:

[deleted]: What's your main use case for Vercel? is it just managed hosting. Could get expensive fast
	chizton (OP) reply to [deleted]: Yes, instead of using lovables hosting. That is the idea
		[deleted] reply to chizton (OP): I'll DM you some options that would be worth a look at before jumping all in on Vercel. There's a few players in the managed hosting space
			DreamKiller5982 reply to [deleted]: Can i also get a DM about hosting I am looking to do something very similar but have gone the route of using Cursor instead of Lovable. I currently plan on using Vercel as hosting but if there are different options then help would be appreciated a ton.

## Post 8

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/SaasDevelopers
Title: Change my mind: this is the best stack right now for a solo SaaS
Post URL: https://www.reddit.com/r/SaasDevelopers/comments/1q7j9fx/change_my_mind_this_is_the_best_stack_right_now

Body:

I’ll say it plainly because I’m tired of “it depends”.

If you’re a solo dev building a SaaS in 2026 and you want to move fast without turning your project into a maintenance job, I think the best stack right now looks roughly like this:

- I run everything as a monorepo using Bun and Turborepo. Separate packages for the web app, landing/blog, mobile wrapper, database layer, shared UI, analytics, docs, etc. Clear boundaries, shared types, but still one place to reason about the whole system.
- Next.js + React + TypeScript for the core app, with backend logic kept inside the same codebase. Not because it’s perfect architecture, but because one repo and one mental model matter more than theoretical purity when you’re solo.
- Astro for the landing page and blog, so marketing content stays fast and simple and doesn’t leak complexity into the app.
- Supabase for Postgres, auth, and storage because it gets you to a real product quickly, with Prisma on top so schema changes don’t become a source of stress.
- Tailwind + shadcn/ui because you need consistency and speed, not a custom design system you’ll abandon in two weeks. (+ TweakCN to customize styles)
- Stripe for payments if you can use it. I personally use Polar because Stripe isn’t available in my country, and honestly it’s been solid and removes a lot of billing overhead.
- n8n for automations and cron jobs outside the app, so background logic doesn’t bloat your main codebase.
- Capacitor if you need mobile access without committing to full native development.
- Vercel for hosting because it’s boring and works, Cloudflare for domains, DNS, and email routing for the same reason. Hetzner VPS if you need more than what Vercel offers for free.
- On top of that, AI tooling matters now. Cursor + MCPs has become part of the st

...[truncated]

Score: 39
Comment count: 72

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "",
  "author": "Powerful_Driver8423",
  "final_url": "https://www.reddit.com/r/SaasDevelopers/comments/1q7j9fx/change_my_mind_this_is_the_best_stack_right_now/"
}
```

Loaded comment tree:

reported_comments: 72
loaded_comments: 65
included_comments: 30
top_level_comments: 31
max_comment_depth: 5

Comment Tree 1:

Moceannl: So funny all Saas devs want speed, CDN's, deployment strategies etc. etc. and then can't find 3 customers or a problem to solve?
	Powerful_Driver8423 (OP) reply to Moceannl: That’s true 😄 no stack ever found customers for me. Building is the easy part. I’ve noticed a lot of devs (myself included) use tech as a comfort zone, while the real work is validating, talking to people, and selling. I guess the stack discussion only comes after one is confident about the problem to solve. At that point, speed and low maintenance matter because they buy time to actually talk to users and iterate. What do you think actually moves the needle early on?
		Moceannl reply to Powerful_Driver8423 (OP): I followed Lean Startup in the past:- Ship early, when you are still ashamed- The only validation is by real (paying) users- Just choose fast and refactor when needed- Pivot often- Test a lot (on real customers)
			Powerful_Driver8423 (OP) reply to Moceannl: Yeah, I agree on that Lean the best approach, specially nowadays with everything changing so fast. I also think that iterations (quantity) > quality at first. Using a tech stack that allows for fast iteration helps with speeding up validation, pivoting, testing and shipping. However, that alone won't get you customers. What do you suggest for finding the first users to test on?
				Moceannl reply to Powerful_Driver8423 (OP): Build for a niche you know, not just from an 'idea'.
					Powerful_Driver8423 (OP) reply to Moceannl: ❤️ Yeah, 100%. I agree that starting from a niche you know is a great shortcut. But I think it has limits too. You can only know so many niches, and sometimes the ones you know best aren’t the ones that pay for software. What’s changed for me recently is realizing you don’t necessarily need to know a niche upfront if you can borrow the knowledge from the people in it. With AI tools and direct outreach, you can research a space pretty deeply, then validate by actually talking to users before writing a single line of code. In some cases I try to get users or commitments first (waitlists, pre-sales, interviews), and let them teach me the niche instead of guessing. I’m leaning more toward a repeatable validation process: test multiple ideas, score them, kill the weak ones early, and only commi

...[truncated]
				[deleted] reply to Powerful_Driver8423 (OP): This one wasn’t AI, but I do use AI the help me writing sometimes. English isn’t my first language, so it helps me express ideas more clearly.Honest question: what makes it an “AI comment” to you? And would that actually make the point less valid or less true?
					Powerful_Driver8423 (OP) reply to [deleted]: This one wasn’t AI, but I do use AI the help me writing sometimes. English isn’t my first language, so it helps me express ideas more clearly.Honest question: what makes it an “AI comment” to you? And would that actually make the point less valid or less true?
	Designer-Rub4819 reply to Moceannl: Yeah. As a successful saas founder myself; wasting time on things we do not need YET is a huge big no no. MVP is where you want to head for the first year(s)

Comment Tree 2:

0xr3adys3tg0: Sveltekit + Convex. Done

Comment Tree 3:

KwongJrnz: My quick MVP stack: Install Create T3 (Nextjs, TRPC, an orm- I use Drizzle, a driver to your selected DB- I use PG, and your preferred linter- I've swapped to biome these days, tailwind CSS). Install Jotai for super easy setup for state management Use Clerk for multi tenant and auth simplicity Host on railway.app for easy deployment, no lock like Vercel, and super boosted speeds because node to node is internal networking. A standard startup SaaS is somewhere in the $3-8 in fee, but you'd likely want the $20/mo base rate for good compute speeds. I've found this setup both incredibly effective at prototyping, but also really easy to scale replicas, split out your BE, introduce new micro services etc.

Comment Tree 4:

parzival0012: Django + Render(Hosting and DB) is my go to - to get a web app up and running quick Highly recommend this stack because I think Django supports both beginners if you follow it’s very opinionated framework but you’re free to deviate out of it while still getting the benefits of the overall structure
	pangolin44 reply to parzival0012: great stack + PaaS. Ive been swapping out Render for Railway recently though
		parzival0012 reply to pangolin44: Curious, what makes Railway better than Render?
	shifra-dev reply to parzival0012: Totally agree! Render gives you Postgres with auto-backups, the Next.js app with zero-config deploys, cron, and preview environments all in one place. And you can still use Prisma the exact same way. The monorepo setup works great with Render's build filters too, so you're only rebuilding what changed. The cognitive overhead of managing one platform instead of three made a huge difference when I was moving fast solo

Comment Tree 5:

thePleasantFellow: Totally agree. Only thing I'd add is Claude Code.
	Powerful_Driver8423 (OP) reply to thePleasantFellow: It hurts my pocket and I don't like the limits. I prefer cursor $20 subscription + pay per usage when limited. It also stills allows you to use Claude models, but provides other options. I've liked Gemini Pro 3 a lot for coding and it's much cheaper than Claude 4.5 Opus for example
		thePleasantFellow reply to Powerful_Driver8423 (OP): Yeah totally. I sucked it up and paid the $99 Claude Max. I'm still playing Cursor too :/
	CulturalPresence1812 reply to thePleasantFellow: Agree. Just did Claude Code last week to build app from scratch. It got it 90% right on first go. Then fixing and tweaking was iterative.

Comment Tree 6:

Commercial_Safety781: this stack is super solid for moving fast, but the first place i see it breaking is the local dev experience with turborepo and bun as the project grows. once you hit a certain number of packages and shared types, keeping everything synced without constant restarts can get annoying.

Comment Tree 7:

cpreid: Stacks literally don't matter. Whatever you work best in, can produce things, can keep stability. But like others said, all of that is just a distraction from the hard part of SaaS.
	Powerful_Driver8423 (OP) reply to cpreid: I agree, it doesn’t matter that much. You can have a great product and no users, and you can have lots of users with a bad product. For me it’s about reducing decisions. After trying a lot of different setups, having fewer choices speeds things up and lowers mental overhead. It doesn’t create success, but it makes repeated attempts more sustainable, faster, and more consistent.

Comment Tree 8:

Yakut-Crypto-Frog: Solid stack! 1 question - why would you even bother with N8N with this stack?
	Powerful_Driver8423 (OP) reply to Yakut-Crypto-Frog: I find it very useful for fast prototyping, specially when it comes to AI, automations, multi agent systems, and agentic workflows in general. AI changes very fast, like every week you have a new model or tool. n8n makes it very easy to update (change models, providers, prompts, context), test, debug, evaluate and integrate (it has thousands of integrations that work out of the box). It's a very specific use case that might not apply to everyone.

Comment Tree 9:

korn3los: Ok now build your todo app.
	who_am_i_to_say_so reply to korn3los: That’s on my todo list. Stalemate.
	Powerful_Driver8423 (OP) reply to korn3los: What’s wrong with todo apps? Some of them make very good money! 🤣 btw, what are you building?
		korn3los reply to Powerful_Driver8423 (OP): Just kidding but most young devs spent days or weeks to get the „perfect stack” and then they build another todo app which they dump after one month. Idk maybe its a generation thing but for instance why would I ever use n8n for my cronjobs? Why supabase and not local? Why vercel and not own vps. I mean what if your product succeeds, do you rebuild it or pay them the hundreds or thousands of dollars every month? It seems most devs just build apps and dont even believe it could succeed. Currently I’m building an extension to my ERP system to automate invoices, bookkeeping, bank transfers etc. The stack: python

Comment Tree 10:

SP-Niemand: May I ask what's your portfolio? Otherwise why would anyone take this seriously if you got no results building in this stack?
	Powerful_Driver8423 (OP) reply to SP-Niemand: I'd be happy to share a few results and success stories using this stack over dm if you’re genuinely interested. And you don’t need to take me seriously at all, the post isn’t about convincing anyone, it’s about sharing experiences and learning from others. I’d actually love to be proven wrong if there’s a better setup/tech or trade-offs I’m missing. What stack are you using these days?

## Post 9

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/SaaS
Title: After building 17+ MVPs, here's the tech stack we use for 90% of projects
Post URL: https://www.reddit.com/r/SaaS/comments/1nxt90x/after_building_17_mvps_heres_the_tech_stack_we

Body:

After building 17+ MVPs, here's the tech stack we use for 90% of projects:

(And why most founders are overthinking it)

The Boring Stack That Makes Money:

Frontend: Next.js

Backend: Supabase

Payments: Stripe

Hosting: Vercel

Email: Resend

Analytics: PostHog

Cost: $86/month

Setup time: 2 hours

Scales to: Millions

What we DON'T use for MVPs:

❌ Microservices (you're not Netflix)
❌ Kubernetes (you have 10 users, not 10 million)
❌ Redis (PostgreSQL is fast enough)
❌ React Native (PWA works fine)
❌ TypeScript (controversial: JS for speed, TS for scale)

Real client results with this "basic" stack:

Jake Thompson (3D Omega):

1,000+ businesses 5,000+ artists $32K MRR Still on the $86/month stack

Emily Parker:

40% conversion rate 3x faster than previous build 94% customer satisfaction Zero scaling issues

The expensive lesson:

- We had a client who insisted on "enterprise architecture."
- Microservices. GraphQL. The works.
- 8 months. $100K. Never launched.

Their competitor used our boring stack.
- 6 weeks. $3.5K. Now at $50K MRR.

Your tech stack doesn't matter if you have no users.

Instagram scaled to 1 billion on 13 engineers.
WhatsApp supported 900 million users with 50 engineers.

You're not Instagram. Use boring technology.

The One Rule: Can you explain your stack in 30 seconds? If not, it's too complex for an MVP.

Our stack explanation: "Next.js for the app, Supabase for data, Stripe for payments. Done."

That's it. That's the stack generating millions in client revenue.

Stop debating React vs Vue.
Stop optimizing for problems you don't have.
Stop architecting for scale you haven't earned.

Ship something people pay for.
Then worry about the tech.

What part of your stack could you delete today?

Score: 307
Comment count: 169

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "",
  "author": "d_sourav155",
  "final_url": "https://www.reddit.com/r/SaaS/comments/1nxt90x/after_building_17_mvps_heres_the_tech_stack_we/"
}
```

Loaded comment tree:

reported_comments: 169
loaded_comments: 94
included_comments: 30
top_level_comments: 33
max_comment_depth: 3

Comment Tree 1:

brad9991: $86/month is pretty misleading. For how many users? Supabase and Vercel costs are going to be dependent on that. You're not scaling to "millions" of users for $86/month
	lykhonis reply to brad9991: Exactly. People pump vercel and supabase yet once you look at the pricing on scale it goes parabolic. Even basic load on supabase requires higher instances. Forget about PITR for database, that’s another $100 per week! I have been proposing looking at Cloudflare, from D1 to hyperdrive, to opennextjs, workers, and so much more. Pricing is unbeatable.
		hambatuhan reply to lykhonis: Need to be careful with D1 as there's many limitation with SQLite based DB. Might be better to use postgres with hyperdrive
		Straight-Gazelle-597 reply to lykhonis: we're going to try Cloudflare but it seems that nextjs is not completely compatible with Cloudflare. Do you have any concrete experience with nextjs and cloudflare?
			lykhonis reply to Straight-Gazelle-597: Yes I have deployed several apps. You can use opennextjs. I also built BaaS on top of Cloudflare, hosting several apps no problem at all. Given, I don’t bundle backend APIs within nextjs, I use CF workers separately.
		Asdenby reply to lykhonis: Yeah, I’ve noticed the same with Supabase once you hit a certain point the bills really add up. Have you tried migrating fully to Cloudflare yet?
			lykhonis reply to Asdenby: To mitigate you can put Cloudflare in front of it. Based on where bills are coming from you can choose products from CF. In my case it was egress so we went with R2 and images products cutting off supabase egress by a lot. I didn’t try, but there is hyperdrive you can wrap connection to database for example. Functions can move to workers. You get the idea.
	who_am_i_to_say_so reply to brad9991: Yeah and I’m finding out just now that Supabase isn’t that great for data that changes a lot. In order to get my use case copacetic, I need the XL $400 a month plan for my needs- and I barely have 10 users on the app. I ended up breaking a part of the data model into a managed DO database for $14 a month. So, a longwinded way of saying that a $10-30 a month managed database is even more boring, scalable, and suitable for most needs.
		brad9991 reply to who_am_i_to_say_so: Same, that's why I called it out. Options like Vercel and Supabase sound good as they are easy to setup and can scale on their own. However they don't offer predictable costs and can be expensive depending on your use case. For 99% of the people here the best option is the most boring and least flashy. A VM and docker running Node and Postgresql. It's predictable cost and gets you to the point where you might need to scale...case let's be honest, a lot of us never even make it to that point.
	HovercraftRemote5830 reply to brad9991: True, but he is right in the sense of deploying MVPs for some bucks is a good approach. I have an MVP site with 0 USD cost on Vercel, 0 on Supabase, 0 on Posthog, 0 for GitHub and Github Actions, etc., and it won't scale to paid tiers for a time (until thousands or maybe hundreds of thousands of visitors). The only cost is 1 USD / month for the domain on Namecehap.
	obanite reply to brad9991: Yeah what a load of crap. next.js is just as "enterprise tech" as microservices. It's over complicated and SSR can cause all manner of difficult to fix issues with your app. Only use it if you're building something that REALLY NEEDS SSR.

Comment Tree 2:

pianoceo: This is an example of content marketing for those that aren’t familiar. OP is offering a free piece of content, to create an inbound funnel to his agency, via his Reddit profile, so he/they can sell services of scoping and building a product for you. The advice isn’t particularly bad. And I respect the hustle. It just comes off as relatively junior. PM’s wouldn’t talk with such certainty without knowing more about the scope of your project, and what stack it would require.
	RandomPantsAppear reply to pianoceo: This advice is terrible. Source: 20 years of engineering experience, 6 as a technical CEO
	Other-Winner1324 reply to pianoceo: It really is terrible advice. Saying JS speeds up development don’t use typescript is equivalent to saying “don’t put your seat belt on when you get in a car. It’s a waste of time”
	NorCalAthlete reply to pianoceo: They’re spamming it everywhere too.
	strawbellaa reply to pianoceo: Thank you for pointing this out
	max-crstl reply to pianoceo: Monitoring and Logging are missing entirely too...
	HighnessAtharva reply to pianoceo: This is the exact tech stack I’d pick again if I had to build a SaaS from zero. Optimized for speed, fewer decisions, and avoiding infra rabbit holes. https://atharvashah.substack.com/p/the-tech-stack-i-bet-my-career-on
		pianoceo reply to HighnessAtharva: At the speed that Lovable is improving, for the non-technical person, why do this instead of just building on Lovable?
			HighnessAtharva reply to pianoceo: Lovable is great, if you are building a website. Not if you are building the next million dollar SaaS imo, down the line you'll need much more and this is not just the dev stack but also the email, payments and integration stack for a holistic tech product strategy.

Comment Tree 3:

cajmorgans: When I saw ”❌Typescript” I immediately knew this was shit advice
	[deleted] reply to cajmorgans: I worked for a small company that had the entire codebase 100% in JS. Grew over 7 years by 15 different devs. Development came to a complete halt, test suites were all extremely flaky, monkey patching everywhere, not a single IDE auto-complete suggestion was working, every code change required the entire app to be manually re-tested because they already had the issue where they shipped something that broke something else. So they made it mandatory to test everything. Sentry was completely full of error and warn logs. You just couldn't know what the input of a function was supposed to be. Half the code was defensive programming, trying to make sense of the input. Company is almost failed now, they let most people go and are barely afloat thanks to the last customers who haven't left yet. Di

...[truncated]
		Purple_Type_4868 reply to [deleted]: So what’s better than JS for that company and in general? Or it just needs to be JS + TS?
			[deleted] reply to Purple_Type_4868: TS-only
	FIFA94AFIF reply to cajmorgans: Can you share all the correct info as per OPs post? Apart from Typescript what other things are not a good advice.
		cajmorgans reply to FIFA94AFIF: I’m not going to further screen the whole post, but to give another example of bad advice, stating that you don’t need Redis if you have Postgres just shows how little OP understands of these technologies. Deploying a Redis instance in a small app is not something that I would consider particularly difficult nor time consuming given that your app demands it.
			Infamous-While-8130 reply to cajmorgans: Redis is not particularly expensive either
			FIFA94AFIF reply to cajmorgans: Got it, thanks!
	Yayo88 reply to cajmorgans: 100% typescript front end and backend all the way
	Bowl-Repulsive reply to cajmorgans: I come to comment just to write the same stuff

## Post 10

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/lovable
Title: Launched today! Built w/ Lovable, then Vercel+Supabase. AMA!
Post URL: https://www.reddit.com/r/lovable/comments/1pegarf/launched_today_built_w_lovable_then

Body:

After about 1 month of pure vibecoding after leaving my full time SWE job at Blizzard, I finally released my free app on the app store.

Try free on web | Quick Tour

Dev details at the bottom of the post!

Problems GitFit.AI solves for you

Why do I have to count carbs in every nutrition tracking app? Surely this is wasting AI data center water. And is the AI nutrition data even accurate?

What if I just want to track fiber, water, veggie intake instead?...

Why can't I describe my food WITH a picture to add context?

Why can't I see my runs, gym time, food, and code commits all in one place?

Why is there no good place to show off your proudest dedications with the proof?

And lastly, being super dedicated to your goals gets lonely. As a try-hard, I want people to see it for what it is. Faking your lifestyle with an Instagram picture is easy and I refuse to do that :D

My app gitfit.ai solves these problems. You can track anything with image + voice or text.

I learned a lot in the last month, and am happy to share with you all if you have any questions!

About the app:

🍎 Scan food, treadmill display, or anything to let AI scan, count, and log it!

Maybe you just need AI to do a quick vibe check or log your mood, skin texture, or even bad habit, anything works. You can do that too.

Accuracy: long term, only +8 overestimation bias for calories. Full research here.

🌈 Builds you beautiful progress charts with a head-to-head compare mode and a correlation visualizer for getting useful personal insights relating your different metrics

💻 Sync GitHub commits, Discord, and Apple Health.

🟥 Share progress pics and discover others' easily

🏆 Climb leaderboards

👀 Get followers ❤️ share, 🔥react

Hop in the Discord if you like!

https://discord.gg/QcKARqyfAF

Thanks for letti

...[truncated]

Score: 106
Comment count: 50

Media:

```json
{
  "post_type": "gallery",
  "media_urls": [],
  "outbound_url": "https://apps.apple.com/us/app/gitfit-ai/id6754495386",
  "flair": "Showcase",
  "author": "Responsible_Log_8732",
  "final_url": "https://www.reddit.com/r/lovable/comments/1pegarf/launched_today_built_w_lovable_then/"
}
```

Loaded comment tree:

reported_comments: 50
loaded_comments: 50
included_comments: 30
top_level_comments: 20
max_comment_depth: 3

Comment Tree 1:

Advanced_Pudding9228: This looks fantastic, crazy polished for a month of “vibecoding”, and I really like how you broke down the stack + costs so transparently. One small thing you might find useful as you see what traction looks like: Right now you’re basically on a “grown-up” infra bill already (Supabase Large + Vercel Pro, plus the rest). That totally makes sense once revenue is steady – but there is a way to keep a Lovable-style workflow and still get a production-grade frontend for £0–£5/month while you’re still in “prove it” mode. The trick is a Lovable → GitHub → Cloudflare Pages pipeline: Let Lovable keep doing what it’s good at: fast UI and feature work on a dev branch (e.g. main) that only it can touch. Connect that repo to GitHub and create two human-only branches: staging and cloud-live (or whatever

...[truncated]
	AdSafe3343 reply to Advanced_Pudding9228: But lovable is still connected to live Supabase backend? so when it does some bad migration the hosted site will get affected too right?
		Advanced_Pudding9228 reply to AdSafe3343: That will only happen if you’ve effectively given Lovable DB-admin access to your live Supabase – i.e. you’re letting it create/modify tables and run migrations automatically. The real danger isn’t Cloudflare, it’s when the AI has full “DB admin” powers over whatever you treat as production.

Comment Tree 2:

-SpleenBean-: I’d be very interested if you could go into a bit more depth regarding moderation! You said that you’re using OpenAI for free moderation but I don’t quite know how that’s possible and/or to what extent you’re using it. Let me know if you have time and congrats!!!
	Responsible_Log_8732 (OP) reply to -SpleenBean-: For sure! So for context I was worried that OpenAI would be upset if people started sending explicit images or text, potentially banning my API key or account. I am using OpenAI's Moderations API which is free for production applications (https://platform.openai.com/docs/guides/moderation) to pre-check text and image content before sending it off to the real model which services the user's request. I use omni-moderation-latest (latest multimodal model). What Gets Moderated Text content - User prompts and text inputs Images - Base64-encoded images uploaded by users I then score the response to determine severity, and flag the account for human review or automatically ban / suspend them accordingly. If you're feeling naughty, you can say something awful into the onboarding landing page.. You

...[truncated]

Comment Tree 3:

wubstark: Looks great. How did you turn it into an app? Capacitor? Also, how are you monetizing it?
	Responsible_Log_8732 (OP) reply to wubstark: Thank you :) 🛠️ Build – Didn't use Capacitor or anything like that. I used BuildNatively! Super easy, awesome, and cheap. Only like $40 a month. No-code for the app store part but also offered tons of native SDK integrations like push notificaitons, Apple sign-in, healthkit, etc. Handled uploading to app store etc. Absolute timesaver 💰 Purchases – Apple IAP with RevenueCat + Stipe (without RevenueCat) via external Browser (Apple required me to make the Apple IAP take focus though haha.. I just did a markup on them) I have three tiers and an option to buy more credits: - Monthly, annual, lifetime memberships - If you are subscribed and you run out of credits (even though you get daily refills), you can top-up The pro upsell doesn't show until you actually run out of your free initial credit

...[truncated]

Comment Tree 4:

throwaway1233494: What’re the benefits of being on Vercel vs keeping it on Lovable?
	Responsible_Log_8732 (OP) reply to throwaway1233494: Maybe this is fixed now, but at the time, Lovable wouldn't allow me to fix a key part of my onboarding brand trust/reputation, which was the "Continue with Google" string that gets displayed. Google's OAuth sign in dialog would say "Continue to XXXXXXXX.supabase.co" rather than "gitfit.ai". This would immediately raise a red flag in users' heads. I asked Lovable Support and they said they do not support any fix for that at the time. Setting up a standalone Supabase instance allowed me to adjust this, but unfortunately, Lovable Cloud was (at the time) seemingly forcing me to use the managed Supabase instance (the .env db string would always automatically get reset somehow?), so I had to make an escape! Not only that, but not being able to actually manage my Supabase instance directly (being

...[truncated]
		empireave reply to Responsible_Log_8732 (OP): agree totally with this point. Lovable is great for getting it going, then work with VS Code and Open Ai to transfer everything to a more stable environment. It's what I did with what i built and it was a lot of work, but way less headaches (and credit burning)
		AdSafe3343 reply to Responsible_Log_8732 (OP): Same scenario, also got out of lovable. but lovable is not allowing me to unpublish the site for some reason so it's still accessible to the xyz.lovable .app did you experience this too? Would appreciate your help.

Comment Tree 5:

Special_Prompt2052: Thought it is to git-fit (like for coding), coding exercises could have been awesome.. haha Checked the experience, lot of things are off for now, hope you make it cool..
	Responsible_Log_8732 (OP) reply to Special_Prompt2052: Oh no! What went wrong? And you can sync GitHub commits or share progress pics of your development. No coding exercises unfortunately. And thanks, I will try my best.

Comment Tree 6:

UnnecessaryLemon: Cloudflare strikes again .. Anyway, super polished BUT I would take a look once again on RLS policies. I was able to get ALL user profiles, that is not cool.
	Responsible_Log_8732 (OP) reply to UnnecessaryLemon: Ah yikes. Ok I'm taking a look there now. And yes, CloudFlare is indeed down.
	Responsible_Log_8732 (OP) reply to UnnecessaryLemon: Profile metadata is meant to be public so you can search for users. If you got their actual metric data, follower data, snaps, that is bad
		UnnecessaryLemon reply to Responsible_Log_8732 (OP): I don't like `/rest/v1/profiles` being public.
		BroBragster reply to Responsible_Log_8732 (OP): Should be available for users IN the app so should be authenticated If it is for search, why is the endpoint not a real search endpoint and you only see the users you searched for? The real answer here is that it was not meant to be public, you just didn’t plan with your ai agent and let it just do its thing because it “worked”. Just tell the ai to fix it, it was a mistake and an easily fixable one 🤷‍♂️
			Responsible_Log_8732 (OP) reply to BroBragster: Should be available for users IN the app so should be authenticated A feature of the app (actually shut down for the time being) is that you can share your public profile or progress snaps with people who don't have the app, on the web (desktop, mobile, etc.). I haven't totally settled on how much I want to be explorable off the app yet though. Shield your eyes, the light mode needs work: But I agree, that was unintentional and problematic. I'm making sure security is sorted out before continuing with distribution.

Comment Tree 7:

Saymonvoid: Congrats! It looks great! How do you plan to distribute it/promote it? It seems quite expensive to maintain
	Responsible_Log_8732 (OP) reply to Saymonvoid: Glad to hear! And thanks :) A big cost, the captcha service, can be swapped out with Google reCAPTCHA for free at some point. I just really liked the simplicity of hcaptcha not being in this giant cloud console. But yeah, kind of expensive, but I believe the profit margins will be really good from the research I've done so far. I left a big comment breakdown replying to @Competitive-Bag-4034 on here with the promotion / distribution details.

Comment Tree 8:

alborden: Looks like you have done a great job. The UX and design look tight too, which is where a lot of vibe-coded apps fall down. I'm interested to know more about how you then took it and got it ready for iOS, and how the submission process went? I want to create an entirely different app idea and want to put it on iOS. I have built a bunch of web apps, some with Lovable, some with Google AI Studio, etc but nothing to port to iOS yet.
	Responsible_Log_8732 (OP) reply to alborden: Ah thank you, love to hear that. A lot of human instruction did go into getting the design to look how it does. I gave a full breakdown in reply to @Competitive-Bag-4034's comment on this post, hope that helps!
		alborden reply to Responsible_Log_8732 (OP): You're welcome. Okay, thanks, I'll take a look through the other replies.

Comment Tree 9:

LunarLamentations: When for Android?
	Responsible_Log_8732 (OP) reply to LunarLamentations: Hopefully soon! No set date yet. But once there is some traction on Apple I'll probably want to get started there. Might take like a week to do.
		LunarLamentations reply to Responsible_Log_8732 (OP): I thought it's other way round, cause android users might be more interested in such app.
			Responsible_Log_8732 (OP) reply to LunarLamentations: Very true. HabitKit, for instance, has around 3k reviews on Google Play, 1.5k Apple, or something like that, last time I checked.
	Responsible_Log_8732 (OP) reply to LunarLamentations: It is on Android now! https://play.google.com/store/apps/details?id=ai.gitfit.app&pcampaignid=web_share

Comment Tree 10:

Sensitive_Paint4328: I keep running into limits with Lovable very quickly. How much did you spend on credits to create this? How many rounds of iterations of prompts did you go through? Did you refine one big prompt before putting in Lovable or refine from within lovable?
