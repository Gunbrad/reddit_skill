# Reddit Raw Posts

Generated at: 2026-06-26T16:33:58.014208+00:00
Total posts: 8

## Post 1

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/nocode
Title: can AI App builders really create a full app if you can't code
Post URL: https://www.reddit.com/r/nocode/comments/1ucoiu6/can_ai_app_builders_really_create_a_full_app_if

Body:

i have zero coding experience but keep seeing tools like Lovable, Bolt, Replit, Bubble, FlutterFlow, and others claiming they can build apps from simple prompts

for people who have actually used them, how far can you realistically get without learning to code? can you build and launch a functional app, or do you eventually hit a wall where technical knowledge becomes necessary?

interested in hearing real experience, especially from non-developers who have launched something beyond a simple prototype

Score: 10
Comment count: 58

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "",
  "author": "jimmybobjoeflow",
  "final_url": "https://www.reddit.com/r/nocode/comments/1ucoiu6/can_ai_app_builders_really_create_a_full_app_if/"
}
```

Loaded comment tree:

reported_comments: 58
loaded_comments: 6
included_comments: 6
top_level_comments: 2
max_comment_depth: 2

Comment Tree 1:

Few-Garlic2725: full app" is doing a lot of work here. prompts can get you to a demo; production is mostly debugging, edge cases, and operations. if you can't inspect/own the underlying project, you'll hit a wall-appwizzy exists because the workspace part matters more than the prompt.
	Anxious_Cap1029 reply to Few-Garlic2725: Exactly this. The wow moment is fast. The boring work of making it not break for real users is where it gets hard.
	InevitableSpring2828 reply to Few-Garlic2725: Absolutely. I spent 3 days making it look functional and 3 months making it actually work. You can use Claude and MCP Superbase to build it, but the real work will start with store submissions and marketing.

Comment Tree 2:

solaza: Yeah but with caveats. If you want any kind of complex thing, you will need to learn a lot to make it functional and secure. Also you will want to use tools like Codex or Claude Code. The apps you mentioned are not as powerful.
	artahian reply to solaza: You will be literally using the same model with Claude Code as most app builders, it is just more convenient to use on a larger project once you've decided to continue developing it locally, but there is practically no difference - same underlying models, slightly different agentic loop. Pricing is the bigger difference, since you can pay a flat fee for a Claude Max subscription instead of alternatively paying thousands for app builder usage.
		solaza reply to artahian: Nah. Codex and Claude Code are better harnesses, straight up. Not the same. But yeah, the token subsidy is wild.

## Post 2

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/EntrepreneurRideAlong
Title: I spent 18 months building four apps with AI code tools and learned some expensive lessons.
Post URL: https://www.reddit.com/r/EntrepreneurRideAlong/comments/1srjqqq/i_spent_18_months_building_four_apps_with_ai_code

Body:

I'm not a developer. I can read code based off a period of ADHD hyperfocus and obsessive reading, debug when things break, and understand how pieces fit together. I can't build an app from a blank file. But I've shipped four apps over the last 18 months, starting from copy-pasting AI-generated code into GitHub through the browser because I didn't know what a code editor was. Every feature was a back and forth over weeks, reading what was generated, questioning it, breaking it, learning why it broke, and gradually understanding enough to catch problems before they shipped rather than after.

The technical side was steep but predictable. What actually cost me money was the infrastructure stuff nobody warns you about when you're laser focused on features and have what feels like unlimited ability to build with zero experience telling you to slow down.

First expensive lesson was vanity. I saw a nicer looking design system on someone else's project and decided to rebuild my entire app using it. Completely destroyed the application. I'd only just found out what VS Code was and had no idea what a git commit was, so there was nothing to roll back to. Had to start from scratch. Save your progress before you let AI touch anything that already works. Boring lesson but a permanent one.

Second was a slow bleed that turned into a proper scare. I was testing API calls without spending limits set and racked up about £300 before I checked the billing dashboard. Assumed it was my own fault so I built a full rate limiting system across the entire app to make sure it couldn't happen again. Costs kept climbing. When I actually sat down and calculated what my testing should have cost it came to pennies. Turned out I'd accidentally left a GitHub repo public after packaging it up. Someone ha

...[truncated]

Score: 10
Comment count: 29

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "Ride Along Story",
  "author": "Glittering-Pie6039",
  "final_url": "https://www.reddit.com/r/EntrepreneurRideAlong/comments/1srjqqq/i_spent_18_months_building_four_apps_with_ai_code/"
}
```

Loaded comment tree:

reported_comments: 29
loaded_comments: 22
included_comments: 22
top_level_comments: 13
max_comment_depth: 2

Comment Tree 1:

Relative_Ad9261: The API key lesson is brutal and important. And the over-engineering point hits hard — building for millions when you have zero users is such an easy trap to fall into, especially with ADHD hyperfocus making everything feel urgent and important at the same time. The boring stuff being the actual app, not the features — that's the most honest thing I've read about solo dev in a while.

Comment Tree 2:

mrtrly: Copy-pasting from the browser into GitHub is a rite of passage I wish more founders would admit to. The infrastructure bite that got a client of mine last year was a public OpenAI endpoint with no per-user cap. App worked great until a bot discovered it and ran up $400 in a weekend before anyone noticed. The other silent killer is secrets in the bundle, worth popping open your deployed site's devtools network tab and searching for any sk_ or key= floating around.
	Glittering-Pie6039 (OP) reply to mrtrly: Good devtools tip, I've done that check a few times since the Gemini incident and it's caught a couple of things I'd missed. The per user cap thing is something I didn't even think about until after my key got scraped, I just had a global rate limit and assumed that was enough I rotate keys now so even if it did get leaked damage would be minimal. Your client's $400 weekend sounds familiar costly lesson.
		mrtrly reply to Glittering-Pie6039 (OP): Rotating keys is a solid habit, I started doing that after a client of mine got their Claude key scraped off a Netlify preview URL last year. Per-user cap is usually the harder one to add retroactively since it needs session logic the app probably did not ship with. Happy to go deeper if you hit that one.

Comment Tree 3:

gardenia856: I went through a very similar arc, just slower because I kept pretending “I’ll fix infra later.” The two things that saved me on the next projects were brutal constraints and weekly “boring checks.” I started forcing myself to ship the ugliest working version first, then froze it. Any AI refactor or shiny new UI went in a throwaway branch or a duplicate project so if it blew up, I still had something that worked. That alone killed like 80% of the “let’s rebuild everything” disasters. I also ended up with a standing hour every week where I only look at logs, quotas, keys, and backups. Cloud dashboards, db consistency, test a failed payment, kill an API key on purpose and see what breaks. It’s dull, but it’s where all the near-misses show up. For discovery/marketing, what worked for us was h

...[truncated]

Comment Tree 4:

CopyBurrito: the struggle to get traction without a following is real. for ai visibility, shift focus to being cited, not just ranked, as ai models prioritize specific sources. we track what gets cited with promptopti.

Comment Tree 5:

TechnicalSoup8578: Sharing the reality of the boring infrastructure phase helps others transition from building demos to shipping reliable applications. Do you think that the risk of over engineering is higher with AI tools because the cost of generating complex code structures has dropped to zero? You sould share it in VibeCodersNest too
	Glittering-Pie6039 (OP) reply to TechnicalSoup8578: Yes the over-engineering risk is higher with AI tools specifically because generating complex code costs nothing but maintaining it costs the same as always I built a database structure meant for millions of users when my target was 40 subscribers, the AI generated it without pushback because it had no concept of "this is too much for your scale" inside the IDE. The complexity only became a problem weeks later when data was scattered across paths that contradicted each other. AI tools don't warn you when you're building beyond your needs. They just build whatever you ask for, and the more complex the request, the more confident the output looks, this is actually better inside webchat as I will get pushback on these issues but unless your using multiple sources and pushing back and question

...[truncated]

Comment Tree 6:

CrazyRemarkable2199: The over-engineering trap is so real. It's easy to build what feels right instead of what people actually need. The gap between a demo and something users actually trust is usually in the stuff nobody sees, not the features. On the marketing without a following thing, the way I've been approaching it is showing up where the problem already exists. Not trying to create awareness from scratch, just being useful in places where people are already asking the question.

Comment Tree 7:

ViewSmart2007: yeah, security and error handling are the boring but crucial parts. if you skip those, your app’s gonna bite you later.

Comment Tree 8:

Deep_Ad1959: the leaked api key turning into 7,200x normal usage is the one infrastructure horror story every vibe coder eventually has, billing dashboards on most providers don't trip alerts until you're already three figures in because default thresholds assume real usage patterns. the part that always shocks people is github scraping speed, public commits with secrets get keys harvested within minutes not days, by the time you notice the bot has already sold the credentials forward. the over-engineering trap is the other universal one, building for million-user scale at 40 subscribers is a way of avoiding the harder marketing question by burying yourself in technical work that feels productive. the fake feature thing is honestly the scariest of the four because you can't trust your own codebase, the

...[truncated]

Comment Tree 9:

Deep_Ad1959: the demo-vs-app distinction in this post is the most underrated insight in vibe coding right now. most builders ship a thing that runs on their laptop and call it done, then panic when a real user creates an edge case the model never imagined. the api key + spending limit story is a rite of passage but the deeper pattern is that ai-built code has no instinct for blast radius, it'll happily expose a key, leave a console.log of session data, or spawn a 10x cost increase in a refactor because the model is optimizing for "works" not "doesn't catastrophically fail". the over-engineering trap is the other side of the same coin: when generating code is free, you stop asking whether you need it. honestly the part that surprised me is that you got through 4 apps without a single migration disaster,

...[truncated]

Comment Tree 10:

[deleted]: Honestly I don't manage it well two of the four are basically in maintenance mode where I check in once a week and fix anything that's broken and marketing them to get presence on socials. The other two get most of my time. The content side is what was killing me because every app needs its own social presence and that's a volume problem more than a skill problem when competing with big marketing companies and now with the advent of AI. I ended up building the fourth app specifically to deal with that so I wasn't spending hours making copy across five platforms for every one, I'm also running a personal training business and have a part time job, so it is very easy to get burnt out on the side hustle, at least now every time I post something I'm not losing my voice just to keep up with the

...[truncated]
	Glittering-Pie6039 (OP) reply to [deleted]: Honestly I don't manage it well two of the four are basically in maintenance mode where I check in once a week and fix anything that's broken and marketing them to get presence on socials. The other two get most of my time. The content side is what was killing me because every app needs its own social presence and that's a volume problem more than a skill problem when competing with big marketing companies and now with the advent of AI. I ended up building the fourth app specifically to deal with that so I wasn't spending hours making copy across five platforms for every one, I'm also running a personal training business and have a part time job, so it is very easy to get burnt out on the side hustle, at least now every time I post something I'm not losing my voice just to keep up with the

...[truncated]

Comment Tree 11:

[deleted]: The shadcn thing is reassuring to hear honestly, felt like such a stupid mistake at the time but clearly it's common. The walking into shops thing is interesting because I've been going back and forth on whether local businesses would even bother when they have a face attached to it. Did you find they actually stuck around as users or was it more of a one time demo situation?
	Glittering-Pie6039 (OP) reply to [deleted]: The shadcn thing is reassuring to hear honestly, felt like such a stupid mistake at the time but clearly it's common. The walking into shops thing is interesting because I've been going back and forth on whether local businesses would even bother when they have a face attached to it. Did you find they actually stuck around as users or was it more of a one time demo situation?

Comment Tree 12:

[deleted]: The four apps aren't restarts. They're separate products in different markets, all still live. MealPreppyPro, AthleticHive, and a PT business site each do different things for different people. SplitPost came from managing marketing content across all three, alongside a full-time and part-time job. It wasn't "I'll try this one instead", it was "I need a tool that handles the content workload the first three created" The incognito testing point is the best advice in this thread though that's exactly how I caught the fake feature system I mentioned in the post. The code looked correct on read-through. Named the right functions, imported the right modules, logged the right events. It only fell apart when I tested as a new user and realised every single person got the same default profile rega

...[truncated]
	Glittering-Pie6039 (OP) reply to [deleted]: The four apps aren't restarts. They're separate products in different markets, all still live. MealPreppyPro, AthleticHive, and a PT business site each do different things for different people. SplitPost came from managing marketing content across all three, alongside a full-time and part-time job. It wasn't "I'll try this one instead", it was "I need a tool that handles the content workload the first three created" The incognito testing point is the best advice in this thread though that's exactly how I caught the fake feature system I mentioned in the post. The code looked correct on read-through. Named the right functions, imported the right modules, logged the right events. It only fell apart when I tested as a new user and realised every single person got the same default profile rega

...[truncated]
		Deep_Ad1959 reply to Glittering-Pie6039 (OP): my read on the four was wrong then, fair. a portfolio of separate live products with one tool that emerged from running them is a stronger setup than any single launch i'd have argued for. the SplitPost path, building it because you needed it across the other three, tends to produce sharper products than ones started from a whiteboard market gap. operator-as-user skips most of the discovery loop other founders end up paying for in time.
	AutoModerator reply to [deleted]: Your comment in r/EntrepreneurRideAlong was automatically removed because it contained a URL or a markdown link. To keep our community focused and prevent spam, we do not allow URLs or links (including Reddit internal links) in comments at this time. If you believe this removal was a mistake, please contact the moderators. I am a bot, and this action was performed automatically. Please contact the moderators of this subreddit if you have any questions or concerns.

Comment Tree 13:

[deleted]: Never used Runable, I have my own tool for all my social content works great.
	Glittering-Pie6039 (OP) reply to [deleted]: Never used Runable, I have my own tool for all my social content works great.

## Post 3

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/VibeCodeCamp
Title: I built and shipped an iOS app with zero coding knowledge – using AI as my entire dev team
Post URL: https://www.reddit.com/r/VibeCodeCamp/comments/1txyeb1/i_built_and_shipped_an_ios_app_with_zero_coding

Body:

Hey r/SideProject!

A few months ago I had an idea for a daily streak app. The problem? I have zero coding knowledge and zero budget for developers.

So I built the whole thing with AI (Claude) as my developer. Every single line of code was written by AI, while I focused on the product decisions, design direction and testing.

The result is Pushfeud – a daily streak app for iOS where you press a button every day and compete with friends. You can see each other's streaks, build shared streaks together, and chat in the app. There's also a timer game built in.

Tech stack (for those curious): React Native + Expo, Firebase, AdMob, RevenueCat, EAS Build.

We're now on version 1.1.3 and improving fast. Would love any feedback – and if you try it, let me know what you think!

📱 Download on App Store: https://apps.apple.com/us/app/pushfeud/id6769160509

Score: 1
Comment count: 15

Media:

```json
{
  "post_type": "multi_media",
  "media_urls": [],
  "outbound_url": "https://apps.apple.com/us/app/pushfeud/id6769160509",
  "flair": "Vibe Coding",
  "author": "Andy2083",
  "final_url": "https://www.reddit.com/r/VibeCodeCamp/comments/1txyeb1/i_built_and_shipped_an_ios_app_with_zero_coding/"
}
```

Loaded comment tree:

reported_comments: 15
loaded_comments: 5
included_comments: 5
top_level_comments: 3
max_comment_depth: 1

Comment Tree 1:

Economy-Manager5556: lol . and ? did you ask an llm for the idea as well? this is just another daily habit tracker from the million of the other ppl here lol no one will pay for this bs

Comment Tree 2:

CharlestonChewChewie: How many downloads and users? Cool that it was entirely vibe coded
	Andy2083 (OP) reply to CharlestonChewChewie: Just launched so downloads are still very early days! And yes, every single line of code was written by AI – I just described what I wanted and tested the result. Wild that it actually works.

Comment Tree 3:

HotInvestigator8877: which llm you used for coding , is it free
	Andy2083 (OP) reply to HotInvestigator8877: Claude by Anthropic — mostly Claude Sonnet via the Claude.ai interface with a Pro subscription ($20/month). Completely worth it considering I built and shipped a full iOS app with Firebase, AdMob, RevenueCat and push notifications without writing a single line of code myself.

## Post 4

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/nocode
Title: I burned $700+ and 3 months testing 11 AI app builders. Here's my final list.
Post URL: https://www.reddit.com/r/nocode/comments/1rw8r7s/i_burned_700_and_3_months_testing_11_ai_app

Body:

I kept seeing the same five tools recommended everywhere so I just subscribed to all of them. And then some more. I built a few personal projects across each one , a lot of them overlapping as well to check quality

I also scrapped through hundreds of reddit and other forum threads to check what other people were using and if I my experiences matched theirs . Note : I try to use latest data and forums given these AI tools have updates almost every 2 weeks and sometimes they might bring significant change .

Lovable The first session was fast. I described what I wanted, a working UI showed up in under a minute, and it felt like I'd skipped months of work. Then I tried to change the login flow. Fixing that broke two other pages. Fixing those cost me more credits. I got stuck in a fix-and-break cycle that burned through a week's worth of credits in one sitting. The credit system punishes iteration, and iteration is how software actually gets built at least at this stage Lovable is good at that first version. I wouldn't trust it much past that.

Bolt Very similar experience to Lovable. Fast, browser based, no local setup. StackBlitz built it so there's more code visibility than most prompt-only tools. But after using both side by side, the differences were small. Bolt uses token-based pricing instead of message credits, and heavy iteration burned through tokens fast. I also ran into stability issues once my project hit around 15-20 components . A lot of files got overwritten and context gets lost along iterations . It Works for demos, needs serious cleanup for anything real and final

Replit This felt closer to a real development environment than anything else I tried. The AI agent writes code, reads its own errors, and fixes them without me having to paste anything back in

...[truncated]

Score: 20
Comment count: 50

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "Discussion",
  "author": "Open-Editor-3472",
  "final_url": "https://www.reddit.com/r/nocode/comments/1rw8r7s/i_burned_700_and_3_months_testing_11_ai_app/"
}
```

Loaded comment tree:

reported_comments: 50
loaded_comments: 5
included_comments: 5
top_level_comments: 2
max_comment_depth: 2

Comment Tree 1:

Realistic_Low_3115: I have built diraigent. It is an app builder where you can use claude code for example. I focus on "vibecoding" for my own needs (Software Engineer). Git Based. And i can use it from my phone. it is self hosted. But I will open a hosted version soon. https://github.com/diraigent/diraigent
	Ok_Substance1895 reply to Realistic_Low_3115: Nice! I find this type of tool works best. If it works for a real software engineer it will be much more complete with less gaps or gaps that can be filled in more easily.
		Realistic_Low_3115 reply to Ok_Substance1895: True. That was my idea behind it. It now takes about 90% of my tasks, the rest i still do in a real IDE, but the boring part is taken care of.
	kidproquo reply to Realistic_Low_3115: This is slick. Thanks for making it public. Btw the license file link in the readme is broken.

Comment Tree 2:

BrilliantDesigner518: I have had bad experiences with these kind of no code tools, Replit etc and I prefer a pure coding tool like Claude - sure it doesn’t have all the bells and whistles but it’s much better at strategic thinking and this is really valuable for complexed apps. I would say don’t be fooled by nice looking mvp’s produced by the above tools none of them manage backend workflows and logic and stage management well and you will spend forever bug fixing. I would recommend starting with Figma Make it handles UI beautifully and an even manage state and dependencies plus it’s dirt cheap. Once you have the app looking and working the way you want in Make then export designs as code using a plugin you will be 95% close to complete build. Take this and finish with Claude. You will save a ton of money and t

...[truncated]

## Post 5

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/webdev
Title: The handoff between no code builders and developers is completely broken
Post URL: https://www.reddit.com/r/webdev/comments/1rgt074/the_handoff_between_no_code_builders_and

Body:

a bunch of my non technical friends have started building in lovable, bolt, base44 etc. their current workflow is this:

start build (ohh this is easy) > continue building (drag and drop is amazing) > finish build (my start up is ready/ima raise hella capital) > slowly realise they know nothing about back end, databases, security, api's, plugins etc > find dev > cant explain what they don't know > both client and dev confused > fin.

Anybody have experience with this? like is the a universal pain that is people are experiencing? Cause the back and forth with unclear requirements, plain english and dev speak have led to multiple projects just being abandoned.

Score: 104
Comment count: 85

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "",
  "author": "dmc_3",
  "final_url": "https://www.reddit.com/r/webdev/comments/1rgt074/the_handoff_between_no_code_builders_and/"
}
```

Loaded comment tree:

reported_comments: 85
loaded_comments: 85
included_comments: 30
top_level_comments: 30
max_comment_depth: 7

Comment Tree 1:

mq2thez: Sounds like nothing of value was lost
	dmc_3 (OP) reply to mq2thez: You’d be surprised how many ideas are DOA, simply because people cannot code them into existence. 98% of tech companies have technical founders
		sweetbeems reply to dmc_3 (OP): While the ability to code is definitely a huge hindrance, there’s more to developing a product than coding. If there’s no one on the founding team that can articulate a product roadmap and vision then the product absolutely is DOA
			Expensive-Manager-56 reply to sweetbeems: It’s this right here. The idea is easy.. the coding is generally straightforward. Actually developing the product from a small idea into a fully fleshed out product that meets customer needs and is good to use takes a lot of work.
				dmc_3 (OP) reply to Expensive-Manager-56: Exactly and that’s the piece most non-technical founders don’t realise until they’re already deep in it. The idea feels simple, the prototype feels like proof, but there’s a whole layer of product thinking that needs to happen before a developer can actually build something that meets customer needs properly
					xian0 reply to dmc_3 (OP): The ideas are obviously worthless because anyone can go "it's like a microwave but it makes cupcakes". The prototype issue is common though, even in a regular company if you show non-technical management a user interface for something they'll think "great it looks like it's almost done" regardless of whether there are any internals. They have no idea how their magic boxes work (as we all did at one point). I have no solution other than avoiding them and in the case of vibe coders just letting them hit a brick wall on their own.
						sweetbeems reply to xian0: While I agree that good ideas are almost entirely dependent on their execution, I can also personally that there are some inherently just bad ideas, no matter the execution 😆
		C2664 reply to dmc_3 (OP): Yeah, fuck them.
		mylsotol reply to dmc_3 (OP): Lol. Yeah. People who can do real work and provide real value.

Comment Tree 2:

mekmookbro: I was building my best friend's app idea (which in itself is a big mistake, I know it now) when the app was close to done he set up a meeting with potential investors in his area. About 3 days before the meeting, his sister got into his head, saying things like "why are you partnering with someone else instead of your sister" (someone else, aka me, being his best friend of 10 years). So he told me that the investors cancelled and he lost motivation about the app. So I stopped working on it. While within these 3 days his sister built a landing page for our app using lovable. "The great app idea" was the exact same thing as tinder but instead of sending text and pictures to each other, you sent voice notes only. I built all of its features, and her sister made a barely working "landing page"

...[truncated]
	fucklockjaw reply to mekmookbro: Isn't it crazy what people will do once there's a chance of success and money on the table? You built your friends dream for him and the moment you two were about to POSSIBLY get some returns for YOUR hard work he turns his back on you and you have forgiven him (not forgotten) and are still friends. I get that people make mistakes but that's not best friend material. I get that your bond is deeper than this one reddit post but I'm disgusted by their actions. You just can't trust anyone out there completely and it's really sad. Imagine they got away with it and were millionaires?
	VipeholmsCola reply to mekmookbro: Id cut him off honestly
	CappuccinoCodes reply to mekmookbro: Once they get what money?
		mekmookbro reply to CappuccinoCodes: investors'

Comment Tree 3:

Firm_Ad9420: We might need a new role “technical translator” between vibe builders and engineers. Someone who can formalize messy intent into system design.
	CosmicDevGuy reply to Firm_Ad9420: And that right there is probably one example of how AI tech firms believe they are contributing to future job creation.
		Expensive-Manager-56 reply to CosmicDevGuy: This is just people misusing AI and trying to use it beyond its capabilities. They are just able to do part of their job faster/easier/better but it doesn’t necessarily make the next persons job easier. They haven’t actually built products before and are confusing their new gains in output with what actually has to be done further downstream from their prototype/vibe coded fever dream.
			CosmicDevGuy reply to Expensive-Manager-56: Maybe it's how I said it, but my point is that for these AI tech firms having there to be more people getting involved in the process is better. I'm neither advocating nor supporting it, I'm merely laying out a, what I can call, certainty or reality. So if people get into the mindset of building an app or tool they cannot maintain using AI, someone else can come along and fix it and then it goes off to actual developers to maintain it, then this is a "positive" because now you'll have courses and job titles relating to the process such as the one you mentioned "technical translator". The current roles of system and business intelligence analysts are already responsible for the translation of business logic/requirements into technical specifications that can be codified/developed. So it isn

...[truncated]
	Both-Fondant-4801 reply to Firm_Ad9420: Thats called an architect... not a new role. basically a dev/engineer with communication and business sense.
		Coppice_DE reply to Both-Fondant-4801: I would say this is more in the domain of requirement engineers: Understand the business intent, formulate requirements and communicate in both directions, making sure that everyone is one the same page.
	aidencoder reply to Firm_Ad9420: That has been a job since... Forever really.
	Nerwesta reply to Firm_Ad9420: Would be nice if that would lead cutting through the chase and attracting people again to us technicians on the first place.
	grensley reply to Firm_Ad9420: That’s basically my job these days.
	brankoc reply to Firm_Ad9420: "What would you say you do here?" https://www.youtube.com/watch?v=hNuu9CpdjIo
	fizzl reply to Firm_Ad9420: We have always needed that! But we never got that. Product owners, project managers, non technical leads, non cosing architects. In the end, I still have a hope and prayer and just code whatever my imagination conveys from their half baked brains. Then present a half baked prototype and start iterating.
		Coppice_DE reply to fizzl: What? Requirement Engineers fill this role. If anything, companies don't want to pay for this.
	[deleted] reply to Firm_Ad9420: Is this post just an ad for this, lol
		TheStorm007 reply to [deleted]: Is this post just an ad for this, lol
			56killa reply to TheStorm007: duh. These shills aren't even slick. Always posing some stupid engagement bait post and eventually sneaking in their product/service/etc.
		fligglymcgee reply to [deleted]: Wow none of us could have seen that coming

## Post 6

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/directorymakers
Title: A new directory: No-code / AI App Builders
Post URL: https://www.reddit.com/r/directorymakers/comments/1syj47m/a_new_directory_nocode_ai_app_builders

Body:

Hi all!

Just launched this directory, so it doesn't have many items yet. Spent some time for automatic generating builders' properties so now, adding one app takes from 1 (fully automatic) to several minutes (when a website is dynamic and you need to copy-paste the text).

Anyway, I keep working on this directory, currently, working on programmatic SEO (dynamic generation of sitemaps and pinging Google Console are already done).

My tech stack:

Python/Flask hosted on Hetzner (Cabby)

PostgreSQL, also there

React/Ant.Design for dashboard, Bootstrap for front-end

Design: Claude, Coding: GithubCopilot + Claude + manual refactoring and coding.

I'd be happy to get feedback, here is the link: https://buildbutton.co

Thanks!

Score: 6
Comment count: 19

Media:

```json
{
  "post_type": "multi_media",
  "media_urls": [],
  "outbound_url": "https://buildbutton.co/",
  "flair": "",
  "author": "AStubbornDeer",
  "final_url": "https://www.reddit.com/r/directorymakers/comments/1syj47m/a_new_directory_nocode_ai_app_builders/"
}
```

Loaded comment tree:

reported_comments: 19
loaded_comments: 18
included_comments: 18
top_level_comments: 6
max_comment_depth: 5

Comment Tree 1:

addicted-coffee: Nicee, make sure to launch it on shipboost
	AStubbornDeer (OP) reply to addicted-coffee: Thanks, is shipboost your platform?
		addicted-coffee reply to AStubbornDeer (OP): Yes, it’s a launch + discovery platform for bootstrapped SaaS founders. the goal is to help products stay discoverable after launch day, not just get a one day spike
			addicted-coffee reply to addicted-coffee: Also you get high quality backlink if you pay for premium launch only for $9
				AStubbornDeer (OP) reply to addicted-coffee: Great, I will consider it as soon as I have more (I think at least 100 apps) in my directory haha
					addicted-coffee reply to AStubbornDeer (OP): Hahah, sure. Good luck on your project

Comment Tree 2:

Admirable_Gazelle453: This is essentially a structured dataset + programmatic SEO play, so long-term value depends on schema consistency, internal linking, and crawl efficiency more than the stack itself. You could offload some static pages to Horizons to reduce complexity and keep costs lower, using the vibecodersnest code

Comment Tree 3:

Exotic-Particular405: Directories like this are pretty useful! but only if they stay curated instead of becoming noisy lists.. how are you deciding what actually gets included? I tried building something similar and used Horizons to test structure fast with the code vibecodersnest

Comment Tree 4:

Deep_Ad1959: my read on these directories is they index by features and stack but skip the dimension that actually matters: friction. the gap between 'open a url and start typing' and 'sign up, pick a template, wait for the workspace to spin up' is huge for tinkerers, but invisible in feature matrices. the typical failure mode is lovable, bolt, replit, v0 all blur together because they're being compared on output capability instead of where they fall apart on iteration. another column worth adding is 'what happens when you hit the wall.' some let you eject to code, some lock you in, some just silently get worse the more you prompt. that's the part people remember three weeks in. written with ai
	AStubbornDeer (OP) reply to Deep_Ad1959: Sorry, even with AI, it's not clear what are you trying to say. May be you'd just describe which features you lack?
		Deep_Ad1959 reply to AStubbornDeer (OP): two concrete columns to add. time-to-first-edit, meaning can i type into a working app in 5 seconds, or do i sign up, pick a template, then wait on workspace spin-up. and escape hatch, meaning when i hit the wall can i export raw code and fork to my own repo, or am i vendor-locked. those two would let me filter the list in 30 seconds. right now i'd have to open every tool just to find out. written with ai
			AStubbornDeer (OP) reply to Deep_Ad1959: The second one is already provided in the builder's features as "You own / can export the code Whether the user can export and fully own the underlying source code" We didn't provide the search by it yet, but will son. The first one is interesting and not in the system but I bet there is no app builder that allows you to create an app without signing up. Or, are they? Can you name one?
				Deep_Ad1959 reply to AStubbornDeer (OP): my honest read is most builders gate signup at save/deploy, not at the first prompt. v0 and bolt let you generate something without an account but anything you actually want to keep pushes you through auth. so the friction column might not be 'signup yes/no' but 'how many prompts before signup hits.' some break at prompt 1, some at prompt 5, some let you get to a working artifact and only gate on persistence. that's the gradient that actually maps to whether tinkerers stick around past the first session.
					AStubbornDeer (OP) reply to Deep_Ad1959: Interesting points. Will think to add it.

Comment Tree 5:

TechnicalSoup8578: Programmatic SEO won’t carry this unless each page has unique decision making value beyond scraped properties. What makes your directory better than just searching AI app builders list? you should share this in VibeCodersNest too
	AStubbornDeer (OP) reply to TechnicalSoup8578: pSEO pages will contain: - comparison charts - use cases showing real using of app builders - problems they can solve Mostly, these pages will be used rather for visibility. I want to make my directory a community not just directory. Right now, I'm adding reviews, ratings, and showcases functionality that people could share their experience with others. Do any other AI app builders list have it? Thanks for pointing at that sub, I will post it there (when it will be more mature haha).

Comment Tree 6:

[deleted]: Not sure what do you mean.
	AStubbornDeer (OP) reply to [deleted]: Not sure what do you mean.

## Post 7

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/cybersecurity
Title: AI code generation has made my AppSec workload unmanageable. Here’s how I’m attempting to manage it.
Post URL: https://www.reddit.com/r/cybersecurity/comments/1rsav4a/ai_code_generation_has_made_my_appsec_workload

Body:

I’m responsible for the security of thousands of repositories and billions of lines of code across mission critical healthcare applications used globally. People’s lives depend on these systems working correctly and securely.

Developers are great at solving problems. Security is almost always an afterthought. I’ve managed this gap for years with SAST, DAST, manual fuzzing and pen tests. It was never perfect but it was manageable.

Then AI code generation happened and my workload roughly quadrupled overnight.

SAST scans were already noisy – roughly 10 findings for every 1 legitimate vulnerability. At scale across thousands of repos that’s an impossible manual review burden. We don’t have the headcount to go line by line and we never will.

I’m using Checkmarx for SAST but the same workflow applies to anything with similar noise problems – Semgrep, CodeQL, whatever you’re running. The accuracy issues are not unique to any one tool. At scale they all produce more false positives than any human team can manually review. That’s not a criticism of the tools, it’s just the reality of static analysis.

So… I built a pipeline. It went through a few iterations:

First I was copy-pasting scan results into local LLM prompts and manually reacting to recommendations. Useful but not scalable. Then I standardized the prompts, built structured artifacts, and wrote Python scripts to run deterministic triage logic inside GitHub Actions. That alone caught the obvious false positives (the low hanging fruit) without any AI inference cost.

For what remained I got approval and funding to run Claude Haiku on AWS Bedrock. Probabilistic analysis on the results the deterministic logic couldn’t confidently resolve. That knocked out another 40% of the remaining false positives.

End results: 60-7

...[truncated]

Score: 83
Comment count: 50

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "Business Security Questions & Discussion",
  "author": "Idiopathic_Sapien",
  "final_url": "https://www.reddit.com/r/cybersecurity/comments/1rsav4a/ai_code_generation_has_made_my_appsec_workload/"
}
```

Loaded comment tree:

reported_comments: 50
loaded_comments: 45
included_comments: 30
top_level_comments: 16
max_comment_depth: 6

Comment Tree 1:

ResilientTechAdvisor: The triage pipeline you built is genuinely clever engineering, and the deterministic-first approach before burning inference budget is the right call. One thing worth pressure-testing though: SAST was designed to pattern-match against known vulnerability signatures. AI-generated code is introducing a different class of problem, specifically logic flaws and subtle misuse of secure APIs that look syntactically clean. Your pipeline is getting better at filtering the noise, but the signal it's preserving may itself be incomplete. The findings that make it through triage are the ones your existing rules already know to look for. In healthcare especially, that matters a lot. A missed injection flaw is a compliance problem. A missed access control logic error in a clinical workflow is a patient s

...[truncated]
	Idiopathic_Sapien (OP) reply to ResilientTechAdvisor: I keep a human in the loop by setting results to proposed not exploitable and setting detailed comments. This reduces time dramatically, retains human approval and generates evidence to the reasoning.
		ResilientTechAdvisor reply to Idiopathic_Sapien (OP): Nice. That's a solid workflow design. "Proposed not exploitable" with a comment trail is exactly the kind of human-in-loop structure that holds up under scrutiny - both internally and if a regulator ever asks how a finding was dispositioned. The one thing I'd watch at scale is review fatigue. When volume is high enough, human approval can drift toward rubber-stamping, especially if the AI commentary is consistently well-reasoned and reviewers start trusting the pattern. (Our brains are made of meat.) Worth occasionally auditing the approvals themselves to make sure the human gate is still functioning as a real check.
			Idiopathic_Sapien (OP) reply to ResilientTechAdvisor: That’s where agent enabled posture management comes into play.
				madmorb reply to Idiopathic_Sapien (OP): I’m not an appsec guy, but is there any value at all in things like adding owasp type guardrails in something like Claude.md and is that what you mean by agent-enabled posture? Be gentle..my subject matter expertise is in defense broadly but we’re all struggling with how to advise properly on these topics. Appreciated!
					Idiopathic_Sapien (OP) reply to madmorb: We use a posture management platform to correlate and prioritize. The coding agents to act on the findings. I use owasp guidance (in rag) to ground the analysis agants and keep their temperature settings relatively low.
					Idiopathic_Sapien (OP) reply to madmorb: I think that it might be prudent to see how I can add owasp guidance to each developers copilot config.
						madmorb reply to Idiopathic_Sapien (OP): I know in claude for example you can add some explicit statements to the Claude.md file. Claude seems to decide if it wants to follow them 😎

Comment Tree 2:

Senior_Hamster_58: Your threat model now includes autocomplete.
	Idiopathic_Sapien (OP) reply to Senior_Hamster_58: So true

Comment Tree 3:

Mammoth_Ad_7089: The 10:1 false positive ratio you mentioned is actually conservative for AI-generated code. We were seeing closer to 40:1 on some repos after a team started leaning heavy on Copilot. Checkmarx kept flagging the same injection patterns in auto-generated boilerplate that nobody was ever going to execute. At some point you're just drowning your engineers in noise and they start ignoring the scanner entirely, which is obviously worse than the original problem. The deterministic filter before LLM triage is the right instinct. The thing that helped us a lot was being ruthless about suppression rules for known-safe patterns first, before touching any AI layer. Get your signal-to-noise down to maybe 3:1 through pure rules, then let the LLM handle the genuinely ambiguous stuff. Trying to use LLMs t

...[truncated]
	Idiopathic_Sapien (OP) reply to Mammoth_Ad_7089: I had the noise ratio very low with tons of cxql customizations but then mass adoption of GitHub copilot, then devs just relying on ChatGPT or (hopefully) Claude. I had to come up with this on the fly just to keep up.
	Idiopathic_Sapien (OP) reply to Mammoth_Ad_7089: For items not identified by the triage script or agent, those default to “to verify” status. I also use nucleus to aggregate the remaining results then send tickets out on open issues.

Comment Tree 4:

_reverse_god: Could you explain this bit in more detail please? I'm not sure I understand, but I want to: "Then I standardised the prompts, built structured artifacts, and wrote Python scripts to run deterministic triage logic inside Github Actions."
	Idiopathic_Sapien (OP) reply to _reverse_god: Initially I tried to see if LLMs could out perform SAST and I found it to be highly inefficient and I was essentially running deterministic code within an agent context. So, I took the formulas I had fed into the analysis prompt and converted them to a python script. This python script updates the state settings in Checkmarx, while sending the remain results to the instance on bedrock for further analysis. This bedrock agent (using haiku because it’s faster) then performs additional analysis and sets states to proposed not exploitable (with notes) or “to verify” and me or another software engineer looks at it. Beyond that the results are aggregated to Nucleus for correlation to SCA results and CMDB. From there we either assign an agent to fix it or send it to a team.

Comment Tree 5:

gslone: I‘m still unsure. I always think it‘s ironic when we work on problems caused by AI‘s inability to think critically (bad coding, prompt injection,…) but then come around with „the solution to this is the same imperfect AI“. I think its more defensible if you prioritise deterministic solutions (like you did) and make the problem much smaller than the original problem the AI solved, because this makes it less error prone (vibe coding an entire app vs. analysing a single line/function) Just recently we had a security vendor do a demo. First part: „AI is horrible for security, Agents are unsafe and do crazy things“ Second part: „BY THE WAY that dangerous stuff? we put it all over our product lol“

Comment Tree 6:

Immediate-Welder999: That looks like you're doing manual reachability analysis assisted with AI. Have you thout about using auto-fix tools? Reason being, the way you might be doing reachability can be hard to be precise. Interesed to learn more if you plan on open-sourcing your repo
	Idiopathic_Sapien (OP) reply to Immediate-Welder999: To some extent. But taking people out of the loop is how we got into this mess.

Comment Tree 7:

ghostin_thestack: One thing worth considering in healthcare specifically: not all repos carry equal risk, so it might be worth tagging them by data sensitivity and adjusting triage confidence thresholds accordingly. A finding that Haiku calls 70% probable false-positive in a utility lib probably gets auto-dismissed. Same finding in code that processes patient records probably needs human eyes regardless. Saves you from having to choose one global threshold that's either too tight or too loose.
	Idiopathic_Sapien (OP) reply to ghostin_thestack: Yes. I am taking a risk based approach for prioritization of work.

Comment Tree 8:

venom_dP: This is really cool! I'm working on a project right now that involves a panel analysis of vulnerability findings. I'm leveraging gpt, sonnet, and gemini to do an initial analysis of the findings. Then I have opus reviewing the final verdicts and providing actionable responses. It's working pretty well in test, very excited to let it run at our live env.
	Jeremandias reply to venom_dP: i’d be cautious getting too reliant on that system for the inevitable day that all of these companies start charging what they actually want to/need to
		venom_dP reply to Jeremandias: Absolutely agree. The Claude Code review cost was a shocker for many. The cost can be somewhat mitigated by running your own models, which we do in some cases.
	[deleted] reply to venom_dP: Yup, the models do disagree at times unless its a blatantly obvious issue or completely unused dependency. Opus mediates those disagreements, but ultimately the human at the end of the chain makes the final decision. I also output the reasoning each model generates for review. I have a set of known vulns that I'm using for test and an intentionally vulnerable code base. It's very interesting how each model tends to ultimately agree, but then provide different severities. Some are more cautious on downgrading stuff, which makes sense to a certain degree.
		venom_dP reply to [deleted]: Yup, the models do disagree at times unless its a blatantly obvious issue or completely unused dependency. Opus mediates those disagreements, but ultimately the human at the end of the chain makes the final decision. I also output the reasoning each model generates for review. I have a set of known vulns that I'm using for test and an intentionally vulnerable code base. It's very interesting how each model tends to ultimately agree, but then provide different severities. Some are more cautious on downgrading stuff, which makes sense to a certain degree.
		Idiopathic_Sapien (OP) reply to [deleted]: Human supervision and approval of state changes (for now)

Comment Tree 9:

YSFKJDGS: I love posts about AI either for it or against it, that are obviously written by AI, like this OP. Like how the fuck am I supposed to treat you seriously when you cannot form your own clear thoughts about what you do?
	Idiopathic_Sapien (OP) reply to YSFKJDGS: Thank you for keeping it respectful. I what you’re saying. You have a valid perspective. You don’t know me and I don’t known you and this is Reddit so… keep your critical thinking hat on. Here is my perspective, I’m somewhat tired of explaining myself over and over again. But since you’re being respectful, I will give it a shot. Not everyone can communicate in every method well. I can write in code and speak endlessly about computer science and cybersecurity. But interpersonal communications are quite difficult. I have a disability (2 or 3 if we are counting) which impares my communication abilities. I am hyperlexic at time but ”putting pen to paper” can be extremely difficult. Most times I dictate to my computer or phone. I use ai tools as assistive technology to help me clarify my though

...[truncated]

Comment Tree 10:

fandry96: With 7 year olds being able to prompt scripts. This is starting to get to the point where AI writes code, then AI checks the other guys work. It's happening at every level from school, college, work, music, images. I'm not sure how anyone keeps up. Have you looked into Gemma?
	Idiopathic_Sapien (OP) reply to fandry96: I have been doing some initial research into it. But I’m trying to keep it low latency and segregated within a stig’d vpc

## Post 8

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/vibecoding
Title: Got stuck building your app with AI? AMA
Post URL: https://www.reddit.com/r/vibecoding/comments/1udl3kx/got_stuck_building_your_app_with_ai_ama

Body:

I've been building software for ~10 years and have worked on products used daily by millions of people (Airbnb, Deloitte, Liverpool FC, and others).

A very large number of people can now build mobile apps and SaaS products. Sadly, most of those projects end up getting stuck and are never shipped.

So I'd like to do an experiment.

If you didn't ship your project, reply with your situation.
AMA I’ll try to help you unblock it and move your project forward.

Note: I'm doing this mostly to understand where builders struggle and hopefully help a few people ship their projects.

Score: 0
Comment count: 7

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "",
  "author": "hardworkonly",
  "final_url": "https://www.reddit.com/r/vibecoding/comments/1udl3kx/got_stuck_building_your_app_with_ai_ama/"
}
```

Loaded comment tree:

reported_comments: 7
loaded_comments: 5
included_comments: 5
top_level_comments: 2
max_comment_depth: 2

Comment Tree 1:

_ragtagthrone: are you wearing underwear
	actionscripted reply to _ragtagthrone: I took them off for this thread

Comment Tree 2:

maddietendo: What are you selling, chief?
	hardworkonly (OP) reply to maddietendo: I’m a dev with a regular job. I personally get a lot of productivity out of using AI for coding (Cursor and Claude.), and I’m honestly curious about something: Where exactly do people get stuck? From my side, it often feels pretty smooth, so I’m trying to understand what breaks down in practice. Is it architecture decisions? ability to debug? deployment? scaling? or something else. What I’m curious about: why so many projects end up getting stuck or abandoned how people are actually using AI tools in real projects what the real blockers are in practice Just trying to understand how others are experiencing it. If there are clear patterns, I might try to do something useful with it later. For now, I’m just collecting signals from real projects.
		maddietendo reply to hardworkonly (OP): Cool. Cool. I totally understand. What are you selling, chief?
