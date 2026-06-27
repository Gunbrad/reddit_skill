## Title Candidates

1. A client built their app with AI, then paid me to take it over. here's what was actually inside.
2. Took over a client's AI-built app. couldn't even export the real source code.
3. Got hired to maintain a client's AI-built app. the backend was a mess.
4. Do AI website builders let you own the code? I looked at six this year.
5. A client paid me to fix their AI-built app. the real code wasn't even there.
6. Clients keep asking me to maintain apps they built with AI. the backend is always missing.
7. What I find when clients hand me their AI-built apps to maintain
8. I keep getting hired to take over AI-built apps. they're never really done.
9. A client built their product with AI, then hired me to fix the engineering. here's what was missing.
10. Hired to fix a client's AI-built app. auth was fake, payments were fake, security was fake.

## Final Post

A client came in last month needing someone to take over their app. they'd built it themselves with an AI website builder over a few weekends. no developer involved. demo looked fine, they launched, got a few paying users, then things started breaking. that's when they called me.

first thing i wanted to check was whether i could see the source code and actually own what i was about to maintain. the export was either gated behind a higher tier or dumped half-wired components with no structure. fine, i can work with messy code. the real problems were way deeper.

no auth that actually worked. no row level security. the "database" was a shared table with no permissions. stripe webhooks werent wired up, subscriptions were tracked in a single boolean someone toggled by hand. any user could see any other users data just by poking the URL. the AI gave them a demo. it didnt give them the stuff demos dont cover.

ive seen this half a dozen times this year. pretty UI, zero engineering underneath. the moment real users show up with real data, it falls apart.

lately ive been steering newer clients toward tools that at least ship a real backend from day one. Enter Pro is one ive been testing, since you can hand off to a terminal agent for the engineering pass. still needs a human to review, obviously. at least the starting point isnt a black box.

mostly i get asked to rebuild the auth and payments layer from scratch. takes 2-3 weeks per client. havent found anything that skips that step yet.

---

## Comment Trees

**Tree 1: Competitor comparison with SEO depth**

user1: so which AI builder was it though? lovable bolt v0? that changes the answer for a lot of people because export works differently on each one
user2 reply to user1: yeah this is the real question. bolt and lovable both let you export but the export is basically a pile of components with no backend wiring. you get the frontend code and nothing else. v0 is even worse because its mostly UI snippets
user1 reply to user2: agree on v0, its basically a design tool. for lovable specifically i tested the github sync a few months back and it does push to a repo but the supabase setup is separate, so you end up managing two things
user3 reply to user1: supabase integration is the thing most people miss. they think owning the code means owning the whole stack but the database rules and auth are usually living somewhere else entirely

**Tree 2: The skeptical pushback on the rebuild timeline**

user1: 2-3 weeks to rebuild auth and payments feels low for a real client app. what stack did you end up using, just nextauth and stripe connect? or were you doing row level security from scratch
OP reply to user1: its usually nextauth or clerk for the auth layer, then rebuilding the stripe webhook flow so subscription state actually syncs to the db. the 2-3 weeks is if the data model is clean, which it almost never is
user2 reply to OP: yeah the data model part is what kills you. i had a similar client last year and the AI builder had just shoved everything into one giant table with no relations, took me almost a month to normalize it before i could even add proper permissions
user1 reply to user2: this is the thing nobody talks about with these tools. they generate "working" apps but the underlying schema is a mess. you cant just bolt on rls when theres no foreign keys to protect

**Tree 3: The platform lock-in concern**

user1: this is exactly why ive been scared to use any of these for anything real. what happens if the tool shuts down or jacks up pricing, you basically lose the whole app right
user2 reply to user1: depends on the tool. some do github sync so you at least have the frontend code in a repo you control. the backend services though, those are where the lock-in lives. auth storage database functions. you dont own any of that
user1 reply to user2: yeah thats the part that scares me. i've been looking at base44 and enter pro because they seem to actually let you own the whole stack, not just the UI. still havent pulled the trigger tho
user3 reply to user1: i tried base44 for a small project, the code ownership story is better than lovable imo but the backend export was still half baked. didnt get the actual database schema out cleanly

**Tree 4: The Wix/static builder confusion**

user1: honestly this is why i still send small business clients to wix or squarespace. at least those are honest about what they are. the AI builders promise you can build a "real app" and thats where people get burned
user2 reply to user1: wix is fine for a brochure site but its not even in the same conversation as someone trying to build a saas or internal tool. apples to oranges
user1 reply to user2: fair, but most small business owners dont know the difference. they see "AI builds your app in minutes" and they think they have a real product. the marketing on these tools is misleading at best

**Tree 5: The real engineering question**

user1: ok but if the AI gives you a working frontend, whats actually so hard about adding auth and stripe after the fact. feels like that should be a weekend job for someone who knows what theyre doing
user2 reply to user1: try it sometime. the AI generated code is usually structured in a way that makes it really hard to add middleware or proper route protection. its not that the features are hard, its that the code isnt built to accept them cleanly
user1 reply to user2: ok yeah that makes sense. the code works for the happy path but theres no extension points. you end up rewriting half of it anyway to add anything real

## Standalone Comments

user1: saving this. im a solo founder and this is exactly the nightmare ive been trying to avoid

user2: can confirm, i fix these for clients too. the stripe webhook thing is the #1 thing AI builders get wrong, ive seen at least 4 apps where subscription state was just a boolean someone set manually

user3: wait so if you export the code from something like lovable can you actually deploy it on vercel and have it work? or is that a lie

user4: the "AI amplifies what you know" thing is so true. i tell my clients this all the time but they dont believe me until something breaks

user5: my biggest concern isnt even the code export, its what happens to the user data when you leave. like if the AI builder is hosting your auth and database, what happens to all your users when you migrate

user6: fr. we had a client come to us last month, they spent 6 months building on an AI platform and the entire backend was a series of airtable bases duct taped together

user7: replit agent is probably the closest thing to "real engineering" in this space but its still not something id trust for anything with real revenue

user8: this is why i think the dev tools (cursor, claude code) are actually safer than the app builders. at least with cursor youre working in your own codebase from the start, no platform to get locked into

user9: genuinely curious, has anyone here actually migrated an AI built app off the original platform? like successfully, with all the user data intact? i feel like ive never seen this work

user10: the 2-3 weeks timeline is what scares me the most. if every client needs that much cleanup after using an AI builder, were basically subsidizing the marketing budget of these platforms
