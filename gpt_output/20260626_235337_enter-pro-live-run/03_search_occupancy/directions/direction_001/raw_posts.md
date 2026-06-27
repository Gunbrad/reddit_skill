# Reddit Raw Posts

Generated at: 2026-06-26T16:33:57.967335+00:00
Total posts: 10

## Post 1

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/vibecoding
Title: My AI-built app was leaking every user’s data and it looked completely fine
Post URL: https://www.reddit.com/r/vibecoding/comments/1tvlr1t/my_aibuilt_app_was_leaking_every_users_data_and

Body:

I build with AI agents. Not a real developer, I just direct the agent and ship fast. A few weeks ago something made me actually look under the hood of one of my apps, and it scared me.

My supabase tables had row level security off. In plain terms: anyone who opened the network tab in their browser could read every row in my database. Not their data. Everyone’s. The app looked fine. Worked fine. The hole was just sitting there.

Went deeper and found two more. An API key with write access sitting in the frontend bundle, grabbable by anyone who viewed source. And zero email protection on my domain, so anyone could send email pretending to be me.

The agent never warned me about any of it. Nothing broke. I only found out because I got paranoid one night and started digging. The tools that catch this stuff exist, but they’re written for security engineers and might as well be in another language for someone like me.

What gets me is that we can all ship a working product in a weekend now, taking real in signups and real payments, and nobody hands you the “here’s how you’re accidentally leaking your users’ data” checklist. You find out when a customer emails you. Or worse.

So I m trying to figure out if I was just careless or if half of us ares sitting on the same thing without knowing. If you built something with AI:*** ***

did you even know row level security was a thing before reading this?

Score: 2
Comment count: 32

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "",
  "author": "juan_drakes",
  "final_url": "https://www.reddit.com/r/vibecoding/comments/1tvlr1t/my_aibuilt_app_was_leaking_every_users_data_and/"
}
```

Loaded comment tree:

reported_comments: 32
loaded_comments: 22
included_comments: 22
top_level_comments: 12
max_comment_depth: 3

Comment Tree 1:

Big_Elephant_2331: It’s wild but all you have to do is ask the agent to flag security holes and it’ll find them and help you fix them. Is this not obvious to people?
	juan_drakes (OP) reply to Big_Elephant_2331: for people who know to ask, sure. but half the people vibecoding right now dont know rls exists, let alone that they should prompt the agent to check it. you cant ask the agent to find a class of bug you’ve never heard of. thats the gap imo
		Spiritual_Sorbet_901 reply to juan_drakes (OP): And this is the major problem with vibe coded apps. lol
			MaybeABot31416 reply to Spiritual_Sorbet_901: That’s why I get ChatGPT to write some of my bigger prompts (because IDK WTF I’m doing, but at least I know I don’t know)
	Imgonnaarrive reply to Big_Elephant_2331: For real

Comment Tree 2:

SP-Niemand: It's a bait, but I'll bite. "Shipping" something like this is not actually shipping. You are simply deluded by the lack of standards in software engineering. It will probably pass with time as the industry becomes more regulated.
	juan_drakes (OP) reply to SP-Niemand: fair, kinda agree tbh. but the no standards part is the whole thing right, nobody hands you a checklist when you build like this so you ship holes you dont even know are holes. “itll pass once its regulated” doesnt do much for whoever’s leaking data today
		SP-Niemand reply to juan_drakes (OP): Can't recommend you more than getting some actual professional experience as a dev with a team of more serious devs. Maybe finish some course or certification on the topic of your tech stack. I mean, you wanna build bridges - you need to learn systematically. Not much different.

Comment Tree 3:

Cultural_Gur_7441: The agent never warned me about any of it Did you ask it to check these things? If you did, and it did not find them, then that is on the agent. If you didn't dig into security, it is on you. Even with 0 knowledge you can start by asking security vulnerability types, then which apply to your code base, then ask it to check, then ask it to re-evaluate assumptions about vulnerability types after first round of checks...

Comment Tree 4:

agentUi: That is the problem we try to build with agentui a secure vibe coding enviromwnt for real businesses

Comment Tree 5:

Spiritual_Sorbet_901: Supabase does security audits and sends you emails when RLS is not enabled. Do you not get these emails? If you're using a hosted Supabase that is. If you're using Codex to create supabase tables, it will not enable RLS by default. You need to make sure you are adding something to your agents.md file to ensure that it does or specifically call it out in your prompt.

Comment Tree 6:

samurijv2: I worry a lot about this sort of thing as well. It's not that AI can't help implement security controls. It's that, as a non-technical builder, I often don't know what questions to ask or checks to run in the first place. There are all sorts of "unknown unknowns" to navigate. I'm curious how other people are dealing with that. Once you've prompted Claude/Cursor/Lovable to implement the obvious stuff, how can you be confident that what they've done is sufficient and that there isn't some lingering vulnerability sitting in the codebase waiting to be discovered? At what point -- or based on what signal -- do you feel comfortable saying, "okay, this is safe enough to put real user data behind"?

Comment Tree 7:

KenMantle: The prompt I used to start my webstore/Gitea/OfBiz/Stripe based site spawned 21 agents to build it including a security expert. That crew has been teaching me what is available for security as it goes. It set up keys to use for ssh VPS logins, cloudflare, and now it wants me to update my OfBiz password to a new one so it can enable the gold standard of hashing that was released in 2015. Whatever Claude set up it appears to be doing its job. Once something works it keeps adding more to tighten security or harasses me to do something. It wants to enable more advanced features in cloudflare. Last week it set up a bunch of scheduled tasks that run nightly to check that the git packages it uses are up to date and don't have newly reported vulnerabilities. None of this was done with any extra pr

...[truncated]

Comment Tree 8:

VESHZA: yup... lol imagine when i first started using Supabase RLS wasnt even on by default AND anyone could reveal your schema using /rest/v1.... also worth saying that even having RLS turned on is not the same thing as having RLS set up correctly..id recommend creating two test users and trying to access user A’s data while logged in as user B. if that works in any way, even through the browser network tab or a direct request, your policies are not scoped correctly https://dbaudit.app I’m actually building a tool for exactly this, mostly for vibe coders / indie builders using Supabase or Firebase who don’t want to become security engineers just to know if they left something open..it scans for misconfigured RLS/rules, exposed keys, risky policies and stuff like that automatically currently openi

...[truncated]

Comment Tree 9:

Odd-Government8896: Why does reddit keep suggesting this brain rot?

Comment Tree 10:

[deleted]: yeah the agent disabling it to debug and never re-enabling is exactly what i think happened to me. the pre-deploy prompt step is smart. do you actually run it every single deploy or does it slip sometimes when youre moving fast? thats the part i cant trust myself on
	juan_drakes (OP) reply to [deleted]: yeah the agent disabling it to debug and never re-enabling is exactly what i think happened to me. the pre-deploy prompt step is smart. do you actually run it every single deploy or does it slip sometimes when youre moving fast? thats the part i cant trust myself on
	Spiritual_Sorbet_901 reply to [deleted]: From my experience it's not on if Codex creates the table. Unless you specifically call it out.

Comment Tree 11:

[deleted]: yeah thats exactly it, nothing looks broken so you never think to check. the incognito window trick is evil btw, watching your own data load with no auth is a gut punch. did you write that checklist down anywhere or just keep it in your head? feels like everyone gets burned once and then rebuilds the same list from scratch
	juan_drakes (OP) reply to [deleted]: yeah thats exactly it, nothing looks broken so you never think to check. the incognito window trick is evil btw, watching your own data load with no auth is a gut punch. did you write that checklist down anywhere or just keep it in your head? feels like everyone gets burned once and then rebuilds the same list from scratch

Comment Tree 12:

[deleted]: pretty much agree. the agent writes like a junior and theres no senior reviewing. the security stuff is the scariest version of that because a junior at least knows what they dont know. the agent ships it confident and clean looking
	juan_drakes (OP) reply to [deleted]: pretty much agree. the agent writes like a junior and theres no senior reviewing. the security stuff is the scariest version of that because a junior at least knows what they dont know. the agent ships it confident and clean looking

## Post 2

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/degoogle
Title: We built an AI app that runs entirely on your phone. No accounts, no cloud, no telemetry. Then a user helped us identify a  bug for INTERNET permission for image generation and we fixed it here's how.
Post URL: https://www.reddit.com/r/degoogle/comments/1tq3339/we_built_an_ai_app_that_runs_entirely_on_your

Body:

Off Grid](https://github.com/alichherawalla/off-grid-mobile-ai) runs LLMs, image generation, and voice transcription on your phone. The models download once, then everything runs locally. No accounts, no sign-up, no data leaving your device.

Then a user filed this: "Image generation requires INTERNET permission but doesn't use the network. This is not very privacy friendly."

It's more nuanced than it sounds. The app does need INTERNET permission — for downloading models and for connecting to self-hosted servers like Ollama. The image generation engine also uses a local HTTP server on localhost for interprocess communication, which Android requires INTERNET permission for even though no data leaves the device.

But the user's point stands. If you're making a privacy-first app, every permission needs to be clearly justified to the user. We're adding in-app documentation explaining exactly why each permission exists and what it's used for. No hand-waving.

This is the kind of thing that only gets caught when your users actually care about privacy.

What the app does without internet:

- Chat with LLMs (Gemma 4, Qwen 3.5, others) - runs on your CPU/GPU/NPU

- Generate images from text (Stable Diffusion) - fully on-device

- Voice-to-text (Whisper) - no audio leaves your phone

- Knowledge base from your documents - indexed locally

The only time it needs internet: downloading models initially, or connecting to a self-hosted server (Ollama/LM Studio) on your local network.

Fully open source - audit it yourself: https://github.com/alichherawalla/off-grid-mobile-ai

- Android: https://play.google.com/store/apps/details?id=ai.offgridmobile

- iOS: https://apps.apple.com/us/app/off-grid-local-ai/id6759299882

Score: 0
Comment count: 7

Media:

```json
{
  "post_type": "multi_media",
  "media_urls": [],
  "outbound_url": "https://github.com/alichherawalla/off-grid-mobile-ai",
  "flair": "Discussion",
  "author": "Thalesof",
  "final_url": "https://www.reddit.com/r/degoogle/comments/1tq3339/we_built_an_ai_app_that_runs_entirely_on_your/"
}
```

Loaded comment tree:

reported_comments: 7
loaded_comments: 7
included_comments: 7
top_level_comments: 3
max_comment_depth: 2

Comment Tree 1:

UnspeakableToast: AI? No thank you.
	Thalesof (OP) reply to UnspeakableToast: I understand - no worries!, but would still love to hear your views on No AI - it's always useful to learn multiple perspectives.
		UnspeakableToast reply to Thalesof (OP): Why would I waste my battery life and precious time on Earth to generate slop?

Comment Tree 2:

03263: Internet permission isn't inherently privacy unfriendly, it just depends what its used for. I'm used to the old ways before permissions were much of a thing, other than root/admin access. So I guess I learned early that you just have to decide which software you trust, permissions aren't going to protect from malware - just try not to install any in the first place.
	Thalesof (OP) reply to 03263: Agreed, but for us: when we promise: no data leaves your phone then is an angle where users could have thought - hey why do you need permissions? i guess we could have been clearer in our messaging overall especially when we ask permission - for instance: during image gen as mentioned in the post.

Comment Tree 3:

Southern-Setting4229: The app is great and altough I use it rarely because my phone isn't the strongest its still useful
	Thalesof (OP) reply to Southern-Setting4229: I understand - we are constantly figuring out ways to make offgrid useful on more phones, there are issues on some phones < 4GB RAM and some on snapdragon SOCs - Curious: If comfy can you share which phone do you use? will take a look if there's anything we can do.

## Post 3

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/ArtificialInteligence
Title: where should an AI app get useful user context from?
Post URL: https://www.reddit.com/r/ArtificialInteligence/comments/1tx140d/where_should_an_ai_app_get_useful_user_context

Body:

this might be a basic question, but i feel like a lot of AI apps hit the same wall.

they look smart in demos, then the first real user session feels generic because the app knows nothing about the person.

i tried thinking through onboarding quizzes, but they feel like homework. usage history helps, but only after days or weeks. importing data from other apps sounds useful, but privacy gets messy fast.

so maybe the missing layer is some kind of unified user data API or privacy-first user context API.

where do you think AI products should get personalization data from without making users feel watched?

Score: 1
Comment count: 5

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "📊 Analysis / Opinion",
  "author": "joyal_ken_vor",
  "final_url": "https://www.reddit.com/r/ArtificialInteligence/comments/1tx140d/where_should_an_ai_app_get_useful_user_context/"
}
```

Loaded comment tree:

reported_comments: 5
loaded_comments: 3
included_comments: 3
top_level_comments: 3
max_comment_depth: 0

Comment Tree 1:

Tight_Beginning_387: I’d avoid starting with a universal user-data API. That sounds convenient, but it can quickly feel like a hidden profile layer. The less creepy pattern is task-scoped, user-visible context: Let the user connect or import context for a specific job, not “everything about me.” Ask small inline preference questions at the moment they matter instead of a big onboarding quiz. Learn from usage, but expose it as editable memory/preferences the user can see and delete. Summarize external data into narrow facts instead of keeping broad raw histories around. Make context temporary by default unless the user explicitly saves it. The trust test is: could the app explain, in plain language, “I’m using these 3 pieces of context to answer you”? If yes, it feels helpful. If no, even technically privacy-pr

...[truncated]

Comment Tree 2:

Novel_Blackberry_470: Most people will trade some privacy for personalization if the value shows up immediately and they stay in control. The creepy part is when apps silently collect a bunch of stuff and still give generic answers anyway. Asking for tiny bits of context only when it clearly improves the result probably works way better than trying to build some giant profile on day one.

Comment Tree 3:

Kindly_Ganache9027: I think the best personalization comes from data users intentionally provide through their actions, not long onboarding forms or hidden tracking. The sweet spot is giving users clear control over what context is shared while gradually learning from their behavior as they use the product.

## Post 4

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/MicrosoftEdge
Title: Using my face for AI generation without permission?
Post URL: https://www.reddit.com/r/MicrosoftEdge/comments/1u4y4r2/using_my_face_for_ai_generation_without_permission

Body:

(First time posting on reddit, so sorry if this isn't the right place for this)

Opened Edge today, and was met with a new 'what's new' update page, where chrome mostly seems to be pressing their AI features. On the learn a new skill page, there seems to be an ai generated image of my face plastered on to someone playing guitar.

Uhh... is this something that happened to everyone? Frankly I find it uncanny. Is there something I can to to remove their permissions to anything that let's them do that, (images, Webcam, or whatever​), or is the best option to switch browsers?

This is probably all over the top, but I would appreciate a separation from Generative AI having access to my personal info or making images with it.

Score: 54
Comment count: 13

Media:

```json
{
  "post_type": "image",
  "media_urls": [
    "https://i.redd.it/puiigeapd37h1.jpeg"
  ],
  "outbound_url": "",
  "flair": "QUESTION",
  "author": "LeFoolMuahah",
  "final_url": "https://www.reddit.com/r/MicrosoftEdge/comments/1u4y4r2/using_my_face_for_ai_generation_without_permission/"
}
```

Loaded comment tree:

reported_comments: 13
loaded_comments: 13
included_comments: 13
top_level_comments: 8
max_comment_depth: 3

Comment Tree 1:

elmonetta: How Edge have a picture of you? Your profile? Or your files?

Comment Tree 2:

CoolWipped: I updated edge and got the same picture. Looks nothing like me. I'm guessing it's coincidence.
	LeFoolMuahah (OP) reply to CoolWipped: That‘s actually really funny, it seems like it is. I’d say i doxed myself but i don’t even look quite that old or wear glasses. Thanks!
		qmcat reply to LeFoolMuahah (OP): lol wait, did Microsoft just happen to use a photo of a guy that looks like you?
			LeFoolMuahah (OP) reply to qmcat: It was mostly similar hair and skintone and I really just assumed it filtered it or something, but yeah it uh may or may not look like me

Comment Tree 3:

darkbrazuk: if you ever gave AI your picture for any silly reason you gave them permission to do whatever with your face
	Acceptable-Act-6038 reply to darkbrazuk: Donno why the downvotes but this is literally true. 😭 omce you upload anything on ai it will use that
	RamiHaidafy reply to darkbrazuk: Doesn't have to be you who did it. One of your friends could have uploaded a group photo you were in. Or a complete stranger who took a picture in public and you happened to be clearly visible in the background.

Comment Tree 4:

Litz1: Did you ever use AI to edit your picture? Then you gave them the permission already.

Comment Tree 5:

Beardedgeek72: And this is why you should not post images of yourself or your family or friends online.

Comment Tree 6:

CoolkieTW: Now everyone who has edge installed know what OP looks like lmao

Comment Tree 7:

BigDipCoop: X

Comment Tree 8:

Emotional_Food_1700: All I see is a black smudge, unless that's your black smudge on your face

## Post 5

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/AskProgramming
Title: Managing user roles & permissions on multiple applications
Post URL: https://www.reddit.com/r/AskProgramming/comments/1qlletp/managing_user_roles_permissions_on_multiple

Body:

I have been wrestling with this question for a while concerning how to manage roles/permissions on multiple applications. We have multiple applications. Lets call them App-1, App-2 and App-3 and user-management.

The user-management app is a central place to register users and the apps they are assigned to. It is also used to authenticate (not authorization) users. For instance an admin can register a user and assign him multiple two apps. This means the user can access these two apps when he logs into the application

Each app has its own backend that can be deployed separately. Each app has its own database as well.

All the apps can be accessed from the same dashboard. See the example screenshot.

screenshot

When a user clicks on an app from the left sidenav the dashboard of the app is opened at the right side. Each application dashboard can also be deployed separately through micro-frontend

Each app keeps a minimal user info like: user-id, full name, email.

How user registration works at the moment

From the user-management app an admin enters a user email and full name of the new user and then chooses the app(s) he wants the user to have access to. These information is temporarily held in and invitation table.

An invitation/confirmation email is sent to the user's email address. When the user clicks on the link in his email a user account is created for this user in the user-management app using the records in the invitation table. After the account is created the record in the invitation table is deleted (because an account is created for the user) and a message is posted on Kafka. The payload of the message contains the user-id, email and full-name

The app the user is registered to receives the payload (user information) through Kafka and creates a user reco

...[truncated]

Score: 1
Comment count: 6

Media:

```json
{
  "post_type": "multi_media",
  "media_urls": [],
  "outbound_url": "https://i.postimg.cc/L6JYgNSm/ui-design.png",
  "flair": "",
  "author": "Professional-Fee3621",
  "final_url": "https://www.reddit.com/r/AskProgramming/comments/1qlletp/managing_user_roles_permissions_on_multiple/"
}
```

Loaded comment tree:

reported_comments: 6
loaded_comments: 6
included_comments: 6
top_level_comments: 3
max_comment_depth: 3

Comment Tree 1:

tidefoundation: You have just described what an SSO (single sign on) was designed to solve. More specifically, the OAuth2 and OIDC standards. A pattern that often works for multi app setups is to keep user identity and app assignment centralized in an Identity and Access Management system (like Entra, Cognito, Okta if you want to go cloud-base, or Keycloak, Authentik, BetterAuth if you want on-premise open source), but let each app own its own role model and enforce it locally. You can still give your admin a single UI by treating roles in the central service as opaque per app blobs or tokens, rather than mirroring each app's internal schema. The central UI just passes the role payload to the app via an API after user creation, and the app validates and stores it in its own DB. That way you avoid coupling

...[truncated]
	Professional-Fee3621 (OP) reply to tidefoundation: u/tidefoundation thank you for your answer. I appreciate it. I have a few questions concerning the following statements: "You can still give your admin a single UI by treating roles in the central service as opaque per app blobs or tokens, rather than mirroring each app's internal schema. The central UI just passes the role payload to the app via an API after user creation, and the app validates and stores it in its own DB.". What do you mean by treating roles in the central service as opaque per app blobs? 2-a) What will the content(s) of the role payload (opaque per app blobs or token) look like? 2-b) I assume that the content of the role payload must be something the app (the app receiving the payload) already understands. If that is the case then how can the app share that role informa

...[truncated]
		tidefoundation reply to Professional-Fee3621 (OP): The central service stores app-specific role data without understanding it (so the role is opaque to the central service). It doesn't know what "sales_admin" means. For example, it just keeps "for App-1, user Professional-Fee is role ID sales_admin" and sends that to App-1. 2-a. Usually one of these:- Role IDs (best common choice): { appId, userId, roles ["sales_admin","report_viewer"] }- Permission strings: { ..., permissions: ["orders.read","orders.write"] }- Policy reference: { ..., policyRef: "policy:app-1:team-42" }- Token/JWT claims: roles/permissions inside a signed token scoped to the app 2-b. The app shares a role catalog + stable role IDs via an API (or events). Central uses that catalog only to display choices and then sends back assignments using those role IDs (e.g. user X has

...[truncated]
			Professional-Fee3621 (OP) reply to tidefoundation: u/tidefoundation thank you very much for the detail explanation

Comment Tree 2:

KingofGamesYami: We manage roles in a central application (in our case, Microsoft Entra). It simplifies the annual review that the security team does immensely, as we have a couple thousand applications and getting data from each one would be incredibly tedious and require learning hundreds of UIs, APIs, and Database Schemas.

Comment Tree 3:

SnooDoughnuts7934: Why not create the user entry when they are created by admin? You can set the status to pending. When they register you just flip it to active. This allows all other things to work before they click the link, you can create entries and such that require an actual entry in the user table (like roles). You can set a timestamp if the user doesn't register by within X then you can cleanup. It does get weird with auth and I think it depends on how much overlap, how many apps total, and how fact roles/permissions you intend to have per app. If 99% of all users are just users, then central location probably makes sense. If each app has fine grained control to every piece of data, the app should handle it. How did the authentication know about each apps roles? Do they register themselves and pass

...[truncated]

## Post 6

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/AIDangers
Title: Hundreds of AI-powered iOS apps found exposing credentials
Post URL: https://www.reddit.com/r/AIDangers/comments/1uceb7h/hundreds_of_aipowered_ios_apps_found_exposing

Body:

Researchers from Wake Forest University analyzed 444 iOS applications with LLM features and found 282 that exposed exploitable credentials or backend access mechanisms. The affected apps covered 13 categories, including productivity, entertainment, lifestyle, education, utilities, and health and fitness.

https://www.helpnetsecurity.com/2026/06/22/llm-api-credential-leakage-ios-apps/

Score: 25
Comment count: 24

Media:

```json
{
  "post_type": "multi_media",
  "media_urls": [],
  "outbound_url": "https://www.helpnetsecurity.com/2026/06/22/llm-api-credential-leakage-ios-apps/",
  "flair": "Warning shots",
  "author": "sunychoudhary",
  "final_url": "https://www.reddit.com/r/AIDangers/comments/1uceb7h/hundreds_of_aipowered_ios_apps_found_exposing/"
}
```

Loaded comment tree:

reported_comments: 24
loaded_comments: 24
included_comments: 24
top_level_comments: 7
max_comment_depth: 5

Comment Tree 1:

Xorphian: That's going to be nightmare of most non tech vibe coding founders
	sunychoudhary (OP) reply to Xorphian: Yes! The nightmare is not vibe coding itself. It is shipping an app without knowing it contains exposed API keys, weak backend auth, or leaked AI service credentials....
		Xorphian reply to sunychoudhary (OP): Exactly, but what do you think adding an env file is enough to avoid these sensitives or they need to take more steps?
			sunychoudhary (OP) reply to Xorphian: .env is not enough if the app ships to users. In mobile/frontend apps, bundled secrets can usually be extracted. Keep API keys server-side, route through your backend, add auth, rate limits, logging, and secret scanning before launch....//
				Xorphian reply to sunychoudhary (OP): Alright got it ,thank you man!!
					sunychoudhary (OP) reply to Xorphian: You're welcome 😄
				WolfVanZandt reply to sunychoudhary (OP): Maybe I'm just cynical ,(I don't think so. I think I have a realist view of the world), but modern economics is the science of finding loopholes and work around to "natural" laws that prohibit a few individuals from extracting value from everything and everyone else. There doesn't have to be AI in an app to steal personal information. In fact, there have always been unscrupulous actors in transactions.
					sunychoudhary (OP) reply to WolfVanZandt: Yeah, AI didn’t invent data theft.....It just gave the same bad incentives a faster way to ship insecure wrappers around it.

Comment Tree 2:

Mission_Reply_2326: I don’t understand any of this. Do we all have to be IT guys to understand wtf is going on? Or can this be explained in layman terms…. Because I get the concept that “exploitable credentials” and “backend access” are bad but I have no idea what it actually means. Can they get into my banking app and move money? Are they accessing my photos?
	sunychoudhary (OP) reply to Mission_Reply_2326: Think of it less like “hackers get into your phone” and more like “the app accidentally left a company key under the doormat.” If that key only opens the AI bill, bad. If it opens user data or backend access, very bad.
		Mission_Reply_2326 reply to sunychoudhary (OP): Thanks. I really needed that.

Comment Tree 3:

hellogoawaynow: Cool that work has us put all of the work apps into our personal phones. I assume all the personal data I’ve ever had on my phone has been stolen, why not the work stuff? That’s the most interesting part, the serious data and money is at work, not in my personal phone and wallet.
	sunychoudhary (OP) reply to hellogoawaynow: Work put the office on everyone’s personal phone and then acted shocked when the phone became part of the attack surface.....It’s not about whether payroll lives on the device. It’s about tokens, trust, sessions, and access.
		hellogoawaynow reply to sunychoudhary (OP): Yep. If you can access my work MS365 suite from my phone, you can get pretty much anywhere from that as a starting point.

Comment Tree 4:

ReidenLightman: This is why you don't vibe code. Code coded code is not secure. It doesn't understand any concept of security.
	sunychoudhary (OP) reply to ReidenLightman: Vibe coding isn’t the vuln. Shipping code you don’t understand is the vuln.
		ReidenLightman reply to sunychoudhary (OP): And anyone who can't code without vibe coding will never understand the code their putting out.
			sunychoudhary (OP) reply to ReidenLightman: Yes. The issue isn’t AI-assisted coding.....It’s people shipping code they couldn’t explain in a postmortem.
				ReidenLightman reply to sunychoudhary (OP): And anyone who can't code without vibe coding will never be able to explain their code. What point of this are people not getting?

Comment Tree 5:

st0ut717: Without naming the app this article is useless
	sunychoudhary (OP) reply to st0ut717: It’s not useless, but it does leave users stuck in “cool, should I delete everything?” mode......Either name the apps after disclosure or give developers concrete checks. Vague panic helps nobody.

Comment Tree 6:

BertMacklenF8I: Did anyone think vibe coding was a good idea?
	sunychoudhary (OP) reply to BertMacklenF8I: Vibe coding is a good idea until the vibe ships your API keys.

Comment Tree 7:

Ok_Truck2473: It’s not even a surprise

## Post 7

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/lovable
Title: My boss hacked our clients lovable built app in less than half an hour
Post URL: https://www.reddit.com/r/lovable/comments/1tqcw0c/my_boss_hacked_our_clients_lovable_built_app_in

Body:

Please please please get someone to check your app or look for exposed API keys.
Our client built an online tutoring app with teachers and students being able to log in.
Starting as a student, we were able to change out profile permissions into an admin in less than 30 minutes. Got full access to their database with all their user list and permissions and effectively could completely taken over their app.

No joke, there is liability involved if you're taking peoples money make sure you got all your bases covered.

Score: 80
Comment count: 52

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "Discussion",
  "author": "Ok-Dragonfly-6224",
  "final_url": "https://www.reddit.com/r/lovable/comments/1tqcw0c/my_boss_hacked_our_clients_lovable_built_app_in/"
}
```

Loaded comment tree:

reported_comments: 52
loaded_comments: 40
included_comments: 30
top_level_comments: 22
max_comment_depth: 4

Comment Tree 1:

Ok-Memory2809: How exactly did he hack it? What was the issue? [Edit: Since neither I nor anyone else in the comments has received an answer to this question, this is starting to sound like BS]

Comment Tree 2:

Yuukibear: Even apps that are not built with AI generated codes get hacked. Please stop sharing stuff without giving us some basic context like what method he used to gain access to the application. Some agencies are so scared of lose clients there will do everything to show the dangers of DIY.
	Ok-Memory2809 reply to Yuukibear: Please stop sharing stuff without giving us some basic context This has been posted a few times without any context. Honestly, it feels like competitors are just trying to stir up controversy around the company, especially since a lot of users are leaving other major platforms and moving over.

Comment Tree 3:

No-Hamster1228: This isn’t entirely a Lovable problem. It’s mostly a Supabase configuration problem. Lovable’s docs explicitly say the frontend is public and must not be trusted, while the database should be protected by RLS and server-side logic. The problem is usually that builders ship too fast, accept default development settings, or assume “authenticated” means “secure” when the policy layer is still wrong. In other words, the app often exposes data because the underlying Supabase configuration is insecure, not because Lovable is handing out the database directly.

Comment Tree 4:

Background-Success35: Just do security audit via vibe coding

Comment Tree 5:

ArtenesNog: This is gold, a good daily reminder that we still need to make something secure.

Comment Tree 6:

mr_pants99: In 90% cases it's the infamous "verify_jwt=false" in Supabase config.toml. At this point, I see a set of common patterns that are use case-specific, but otherwise pretty ubiquitous. I'm happily offering prospective customers to review their codebase for free (1st time only 😄 )- have an automated tool for that that combines static code analysis and AI.
	Sask-Uchiha reply to mr_pants99: Desculpe perguntar isso, mas o que exatamente significa verify jwt false?
		mr_pants99 reply to Sask-Uchiha: This is a parameter to skip auth check for Supabase edge functions. When AI agents encounter issues with auth (often because of various webhooks), they might just decide that the best way to address that is to disable auth.
			Sask-Uchiha reply to mr_pants99: Entendi, então o recomendado é que sempre esteja em "true"?
				mr_pants99 reply to Sask-Uchiha: Yes, ideally you don’t want unprotected endpoints on the backend unless you know exactly what you’re doing - eg a stripe webhook where you validate the signature.
	nickfmc reply to mr_pants99: or people just not wanted to take the time to setup ENV variables in Supabase early on and just give the API keys to lovable and it pops them in an env file on the frontend and they forget about the fact they are exposing all their credentials in there. seen that more than a few times

Comment Tree 7:

Accomplished-Clue822: Yes you have to get an actual developer to look over the app to make sure everything is correct and secure and make sure to check Supabase

Comment Tree 8:

sideflipp: They added Aikido as a service, for only $100 they will perform penetration test and let you know what to fix. This issue is not a Lovable issue, rather lack of know-how imho

Comment Tree 9:

Ok-Engine-5124: This is the scariest category of vibe-coded bug, because the app looks completely fine until someone pokes at it. What your boss hit is almost always authorization enforced in the frontend instead of the database. The UI hides the admin buttons, but the real permission check is not on the server, so anyone who edits the request or their own user record walks straight in. AI builders tend to generate the happy-path UI and skip the server-side check unless you explicitly ask for it. Two things to verify on any app taking real users. Row-level security rules on the database itself (Supabase supports it, turn it on and actually test it). And confirm role changes can only happen server-side, never from a value the client is allowed to edit. Test it the way your boss did, as a normal user trying

...[truncated]

Comment Tree 10:

sanduckhan: I don't feel like Lovable is a tool to run a software in production for real clients. It's an amazing tool to build but the operational lock-in is causing a ton of issues for commercial builders... Even the plugins and the partnerships. They are nice but builders don't know what they don't know, you need either a developer or a production team to run and monitor an app in production. We are running a lot of vibe coded apps for our clients and the most important part is the service, the peace of mind to not have to worry about it, that's not something a plugin can do...

Comment Tree 11:

whi5tler: Do not build production apps if you do not know what you are doing. Just because it looks easy to service my gas boiler doesn't mean I'm going to do it.

Comment Tree 12:

Electrical-Pie2735: No surprise tbh.

Comment Tree 13:

xjhay: To see is to believe.
	Ok-Dragonfly-6224 (OP) reply to xjhay: Believe. Can’t show you as I didn’t record and either way it would expose the client. But was I with him on a call when he did it and was shocked at how easy he made it look. Just wanted to drop a warning here because this can have real repercussions for people selling unsecured products

Comment Tree 14:

Dramatic_Desk_7626: I think is more supabase issue

Comment Tree 15:

ShelbulaDotCom: RuntimeRiot.com is good for finding these. No LLMs involved.

Comment Tree 16:

aib_fan: That's why I always host my apps inside a sandbox like e2b, InstaVM, Daytona etc

Comment Tree 17:

Sudden_Tax1429: the supabase integration id the issue

Comment Tree 18:

Expert_Cap5167: Jogar o zip do github no claude e pedir pra ele analisar e encontrar lacunas de segurança ou exposição de dados pode ser um caminho? Fiz um teste e ele me entregou um relatório com tudo que estava exposto ou com falhas de segurança e como corrigir. Mas ainda não confio 100%.

Comment Tree 19:

ThinStretch8465: This is exactly why I’m getting a penetration test done before launch. Were the main issues exposed API keys or weak role-based permissions? Any tools you recommend for founders to run basic security checks before going live?

Comment Tree 20:

StatisticianDue428: This is exactly the scary part of the AI app builder wave. Building the UI became 10x faster, but a lot of people forget that "it works" doesn't always mean "it's production ready". Before launching, I usually check things like: - exposed environment variables - database access rules (especially RLS) - test vs production payment settings - webhook permissions - what anonymous users can actually access AI tools are amazing, but the final security review still matters.

Comment Tree 21:

[deleted]: What's the solution?
	Didact1929 reply to [deleted]: What's the solution?
		jsaldana92 reply to Didact1929: Pay a vibe coded website to check your vibe coded apps and give you generic vibe coding feedback. Or at least according to some post I’ve seen regarding ship fast, build often.

## Post 8

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/appdev
Title: I built an AI skill to help analyze App Store and Google Play rejection messages
Post URL: https://www.reddit.com/r/appdev/comments/1t7pt6e/i_built_an_ai_skill_to_help_analyze_app_store_and

Body:

Hey everyone,

I recently created a small open-source AI agent skill called App Store / Play Store Rejection Assistant.

It is meant for developers who get rejected by Apple App Review or Google Play and need help turning the rejection message into a practical fix plan.

The skill helps generate:

Issue summary

Platform and policy classification

Likely root cause

Required fix checklist

Reviewer response draft

Resubmission checklist

Client-friendly explanation

I built it because I’ve seen many developers lose time trying to understand whether a rejection is caused by app functionality, metadata, privacy policy, subscriptions, permissions, data safety, or review access.

GitHub:
https://github.com/AyeshaIftikhar/app-store-play-store-rejection-assistant

It is still an early version, so feedback from anyone who has dealt with real App Store or Play Console rejections would be very helpful.

Score: 0
Comment count: 7

Media:

```json
{
  "post_type": "multi_media",
  "media_urls": [],
  "outbound_url": "https://github.com/AyeshaIftikhar/app-store-play-store-rejection-assistant",
  "flair": "",
  "author": "Prestigious-Try-5372",
  "final_url": "https://www.reddit.com/r/appdev/comments/1t7pt6e/i_built_an_ai_skill_to_help_analyze_app_store_and/"
}
```

Loaded comment tree:

reported_comments: 7
loaded_comments: 7
included_comments: 7
top_level_comments: 2
max_comment_depth: 4

Comment Tree 1:

No-Aioli-4656: See, there are skills, and then theres “it would take me longer to install your skill than make a prompt that does the same thing.” Cool I guess, but it would take me longer to install your skill than make a prompt that does the same thing.
	Prestigious-Try-5372 (OP) reply to No-Aioli-4656: But the setup is one time, once you installed it, it will save you time writing prompts over and over again and worrying about agent hallucinations. If you don’t wanna use the skill don’t no one is forcing you to use the skill or stood holding a gun over your head to use the skill.
		No-Aioli-4656 reply to Prestigious-Try-5372 (OP): Bro, typing at 80wpm and you’re done in 2min max. This saves, no time. Plus, everyone is gonna wanna have bullets look and feel different. What would be valuable is if you take all of your “ai app slop spamming the Apple Store knowledge”, and distill it into an AI skill that pre-audits submission to hopefully ease things along.
			Prestigious-Try-5372 (OP) reply to No-Aioli-4656: No one is begging you to use this. If you don't want to don't.
				DismissedFetus reply to Prestigious-Try-5372 (OP): I agree with other guy, just because something is free or "doesn't need to be used" doesn't make it above criticism.

Comment Tree 2:

Otherwise_Wave9374: This is a really practical "agent skill" idea. App review rejection messages are like 50% policy language and 50% guesswork. Suggestion: have the skill output a "what evidence to include" section (screenshots, demo creds, screen recording, exact menu path) because that often makes the difference on resubmission. If youre looking at packaging it as part of a bigger agent workflow library, https://www.agentixlabs.com/ might be a good place to see how others are structuring reusable agent skills.
	Prestigious-Try-5372 (OP) reply to Otherwise_Wave9374: Sure

## Post 9

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/rails
Title: Seeking Advice on Implementing User Roles and Permissions in Ruby on Rails
Post URL: https://www.reddit.com/r/rails/comments/1qq898w/seeking_advice_on_implementing_user_roles_and

Body:

I’m building a web app with Ruby on Rails as the backend, and I need to set up a solid user roles management system along with permissions. The app will have different user types like admins, moderators, regular users, and maybe guests or premium members. I want to control what each role can do, like accessing certain routes, editing content, or managing other users.

I’ve heard of gems like Devise for authentication, Rolify for role assignment, and Pundit or CanCanCan for authorization. But I’m looking for real-world suggestions on the best setup:

• What’s the most efficient way to define and manage roles? Should I use an enum in the User model or a separate Roles table?

• How do you handle permissions? Policy-based with Pundit, or ability-based with CanCanCan? Any pros/cons based on your experience?

• Any gotchas with scalability or security I should watch out for?

• Recommendations for testing this setup (e.g., with RSpec)?

• If you’ve integrated this with a frontend like React, how did you handle role checks on the client side?

Score: 15
Comment count: 19

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "Learning",
  "author": "BookkeeperAncient143",
  "final_url": "https://www.reddit.com/r/rails/comments/1qq898w/seeking_advice_on_implementing_user_roles_and/"
}
```

Loaded comment tree:

reported_comments: 19
loaded_comments: 19
included_comments: 19
top_level_comments: 14
max_comment_depth: 4

Comment Tree 1:

jasonswett: I suggest this approach: start by thinking about high-level technology-independent authorization principles, then work your way down to decisions about tools, efficiency, scalability, etc. If you're not already familiar, I suggest reading up on role-based access control (RBAC). In my opinion, RBAC gives a good mix of conceptual simplicity while also being flexible enough to handle pretty much any authorization scenario. Then, assuming you like RBAC, the question becomes: how should I implement RBAC in my Rails application? This eliminates a lot of detail decisions. Anytime you're unsure how to do a particular thing you can just refer to the RBAC literature to learn of "the RBAC way". (Not for every single decision of course, but a lot of decisions.) Regarding CanCanCan versus Pundit, I fin

...[truncated]
	fatalbaboon reply to jasonswett: Totally agree on Pundit being superior to CanCanCan. I suspect people favoring CanCanCan either did not grow to the levels where it's painful, or just never really looked at Pundit.
		jryan727 reply to fatalbaboon: Once I switched to Pundit I never looked back. You can easily express any authorization pattern with Pundit. "Can this user perform this action on this resource?" is the fundamental authorization question and is how Pundit is modeled.
			xkraty reply to jryan727: I find action policy ( by evil Martian I think? ) slightly better than pundit
				jryan727 reply to xkraty: I've never used it but will surely check it out thanks!
		sentrix_l reply to fatalbaboon: I use pundit everywhere. Scopes are OP

Comment Tree 2:

planetaska: One word: Pundit. You can use whatever authentication strategy you like, and Pundit will just work fine along with it. For a separate frontend, you do need to have a separate auth logic - that’s why Inertia is such a sweet deal.

Comment Tree 3:

djillusions24: I used to use CanCanCan and switched to Pundit, I much prefer pundit. Currently using it in quite a large multi tenant SaaS without issues.

Comment Tree 4:

tb5841: We use CanCanCan for an application with a vast number of users and a hugely complex permission system. It does everything you're asking, and it's fairly easy to use. ...But it does slow down queries a great deal, for us. It feels too late to change it now, butbwe do wish we had a more performant solution.

Comment Tree 5:

-Mart-: using Pundit, I can select what roles can access which controller actions, it's good for vast majority of cases, but for some special cases it's a bit less flexible, but no issue with some custom code added.

Comment Tree 6:

happypathonly: my two cents, don’t reach for pundit until if and when you really need it. Pundit is sooo much boilerplate for every single controller. Unless you have very complex auth logic it’s overkill, imo. The PORO policy pattern keeps things super simple and is more flexible.

Comment Tree 7:

TonsOfFun111: I'd suggest the [Rails authentication generator](https://guides.rubyonrails.org/security.html#authentication) for authentication you can learn more about authorization and [action\_policy](https://github.com/palkan/action_policy) for authorization. Learn more here https://actionpolicy.evilmartians.io/

Comment Tree 8:

neotorama: I just use this simple feature based authorization in multi-tenant app. # add to member t.jsonb "permissions", default: {}, null: false # helper method (works with controllers and views) def can?(member, permission) end I also like https://github.com/enjaku4/rabarber

Comment Tree 9:

Shy524: I have used rails 8 auth and pundit. Worked like a charm, maintenance and testing is pretty easy

Comment Tree 10:

Nemerie: I recommend against using Rolify unless you need to assign different roles in different scopes (for example, a Reddit user is just a user in one subreddit and a moderator in another). I worked on a project that used Rolify despite it not being the case there. I always had to think about joining roles when having a simple field in the users table would do all the work.

Comment Tree 11:

arpansac: We've been using devise for authentication, but for role-based access or authorization, we've created our own system. It's similar to Pandit but a little bit more flexible. We have grouped different actions together and defined collective permissions on different user roles. There is a separate table which defines all the user roles. So there are two types of differentiations: If the user is logged in or not If a user who is logged in has a specific permission or not For the first part, there is a basic thing which is to check if the user is authenticated, but for the second part, we are defining the permission for each action within the controller itself instead of creating a copy of it and putting the permissions there. That way we are able to save a little bit of headache in terms of ma

...[truncated]

Comment Tree 12:

InsideStorm9: On the project I work on there is devise (I'd choose rails authentication now) for authentication, this is independent of authorization. For the authorization we're migrating from one custom system similar to cancancan to ActionPolicy (similar to Pundit). The project has a hierarchy (Account, Folder, Project) where a user belongs to one account and can be given a role on any element from the hierarchy. Roles are inherited and can be locally overridden. So the role is stored in a join model (joining a user and an Account or a folder or a project). ActionPolicy is working well, is simpler to reason about than a big file of permissions for all the resources.

Comment Tree 13:

nflo88: I used pundit in various projects but I used action_policy in my last big project and it seems better than pundit to me.

Comment Tree 14:

farukca7: If it is multi tenant it is better you implement your own solution, none of those gems won’t work. Each company has different rules and approaches for authorizations.

## Post 10

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/androiddev
Title: How do you implement AI features into your app?
Post URL: https://www.reddit.com/r/androiddev/comments/1uf7mym/how_do_you_implement_ai_features_into_your_app

Body:

Hi,

Wondering what are the options if I want to create an AI features into in my app. I know about openAI api and other various API’s. The thing is I am a tad scared to use them because I hardly understand how they charge. I know a lot of stories where people used it wrongly and got huge bills for that.

Also, do we always need these powerful models? Can’t we use in some cases like qwen 8b or something like that running on a VPS?

Score: 0
Comment count: 25

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "",
  "author": "Inside-Conclusion435",
  "final_url": "https://www.reddit.com/r/androiddev/comments/1uf7mym/how_do_you_implement_ai_features_into_your_app/"
}
```

Loaded comment tree:

reported_comments: 25
loaded_comments: 25
included_comments: 25
top_level_comments: 5
max_comment_depth: 8

Comment Tree 1:

FunkyMuse: If i needed them, they're proxied through my own backend to avoid exposing the keys and everything goes through a backend which then scales on a server whether horz/vert
	Conexur reply to FunkyMuse: Also for cache use this is the best way.

Comment Tree 2:

pwhite13: It depends on what features you need. But I highly recommend starting with on-device AI first and see if that serves your need. Check out Gemini Nano APIs as a starting point.
	Conexur reply to pwhite13: In Android only for a few % of devices
	Inside-Conclusion435 (OP) reply to pwhite13: On device ai? So each user will have an ai running on their phone?
		VEHICOULE_ reply to Inside-Conclusion435 (OP): Yes you have Gemini nano for android and apple intelligence or whatever it's called for iOS, they are on device ai that you can use, but outside of very simple tasks it's not that good and very battery inneficient
			Inside-Conclusion435 (OP) reply to VEHICOULE_: Thanks good to know, I didn’t know about gemini nano
				pwhite13 reply to Inside-Conclusion435 (OP): It can do basic things like reading text in an image, for example
					Inside-Conclusion435 (OP) reply to pwhite13: Can it come up with a report and suggest ideas based on a set of data inputs?

Comment Tree 3:

simbolmina: I use local AI primarily on my app and remote LLMs as option. Depending on your use case, Gemini flash 2.5 or deepseek V4 flash can be very cheap.
	Inside-Conclusion435 (OP) reply to simbolmina: Can you elaborate on local ones? Is this app in play store? How does it work? Remote ones are via which provider?
		simbolmina reply to Inside-Conclusion435 (OP): Yes I use gamma 4 models on phone as local ai and it is simply completion API but far weaker and takes time. You can check iOS or android versions https://forgeapps.site/storycodex
			Inside-Conclusion435 (OP) reply to simbolmina: So your app has llm baked in? Surprised that the app size on app store is just little above 100mb
				simbolmina reply to Inside-Conclusion435 (OP): Yes backend itself is not big you need to download models after you installed the app. Gemma4 is 2.4/3.6gb. Voice models are 45-400mb.
					Inside-Conclusion435 (OP) reply to simbolmina: Oh so it does in the background user doesn’t even notice it
						simbolmina reply to Inside-Conclusion435 (OP): Aside from draining battery and heat, yes.
							Inside-Conclusion435 (OP) reply to simbolmina: Wow, heavy then in the end. Hmm, I wonder if it freezes or loads up slowly the app since so much going on behind the scenes
								simbolmina reply to Inside-Conclusion435 (OP): You can try.

Comment Tree 4:

Major_Chocolate2441: What language you using?
	Inside-Conclusion435 (OP) reply to Major_Chocolate2441: .Net
		Major_Chocolate2441 reply to Inside-Conclusion435 (OP): I know if I was to give this some thought and attention, I could find a solution.

Comment Tree 5:

amelech: What are you trying to do with AI? You can run Gemma 4 on phones
	Inside-Conclusion435 (OP) reply to amelech: Not a big deal. Analysis of user data/inputs. Like reports/summaries with suggestions, etc
		amelech reply to Inside-Conclusion435 (OP): Hmm ok I've found the on device models are ok for conversation but they are terrible with data.
			Inside-Conclusion435 (OP) reply to amelech: Good to know
