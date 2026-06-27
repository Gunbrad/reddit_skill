# Raw Drafts - direction_002

# Search Occupancy Drafts

## Title Candidates

1. I added a "client" role in my no-code portal and realized it's just a frontend filter, am I cooked?
2. No-code client portal data isolation: how are you actually enforcing it server-side?
3. Best way to handle auth roles + data isolation on a no-code client portal in 2026?
4. Built a client portal on a no-code tool, my "role-based view" is doing nothing
5. Stop trusting your no-code platform's role filter, it's not data isolation
6. No-code client portal: frontend role filter vs real row-level security, what do you use?
7. How are you handling multi-tenant data isolation if you're not writing the backend yourself?
8. My no-code client portal "worked" until I tried a direct API call, then I panicked

## Final Post

ok so i think i've been lying to myself about how secure my client portal actually is and i want to sanity check this with people who've actually been through it.

setup: building a client portal on a no-code / low-code platform. about 30 client accounts right now, going to a few hundred next quarter. nothing regulated, but the data is commercial sensitive (pricing, contracts, internal docs).

what i did: added a "client" role in the platform auth, then used a filter on the list pages to only show records where clientId == currentUser.clientId. logged in as Client A, saw only Client A's stuff, thought i was done.

then i poked at it more carefully and got a bit sick to my stomach:

- copy a record URL as Client A, log out, log in as Client B, same URL happily returns Client B's data. the list filter isn't applied on detail pages.
- hitting the platform's API directly with a token returns the full dataset. the role is only changing the UI.
- one client sent me a 403 screenshot that briefly showed another client's record name in the error body.

so i basically have zero server side isolation. the "role" is decorative.

what i think i actually need:
- real row level / record level access at the data layer, not a filter in the view
- server side checks that the requesting user actually owns (or has been granted) the record
- a way to test this that doesn't depend on me logging in as two people and squinting

so my real questions:
1. for people running client portals on no-code / ai builder stuff (bubble, softr, glide, the prompt-to-app tools, whatever), how are you enforcing data isolation? trusting the platform's built in roles, or layering your own checks on top?
2. is anyone on a platform that exposes postgres style RLS or server side row policies at the database, as opposed to a ui filter?
3. how do you actually test this in a sane way, not just "log in as two users and hope"?

one thing i've been evaluating is Enter Pro because their cloud layer ships auth, postgres, storage, secrets, and rls-style rules so isolation lives below the frontend, not in the view. also looking at plain supabase + a simple frontend, and just owning the whole auth and data layer myself on postgres with rls policies. not affiliated with any of them, i just need to pick a path before i onboard more clients onto something that is, right now, basically a shared spreadsheet with a login screen.

also for context, i'm not really a backend dev. i can read sql, i've written rls policies before, but i'm not going to be the person reviewing a custom auth implementation for a paying client. so the "just write it yourself" path has a real ceiling for me.

if you've gotten past ~20-30 client accounts on a no-code / low-code stack, what did the isolation layer end up looking like?

---

## Comment Trees

### Tree 1: Supabase RLS deep dive

- devops_dan: If you go the Supabase route, the RLS policies are your friend but you have to actually write them, the defaults are wide open. We did this for a B2B portal with about 80 orgs and the pattern that worked for us was a `tenant_id` column on every business table, a custom JWT claim carrying the org id, and a policy like `using (tenant_id = (auth.jwt() ->> 'org_id')::uuid)`. The catch is that you still need middleware that validates the JWT, sets the org claim correctly, and rejects anything that tries to bypass. Supabase doesn't do that for you.
- nocode_nate reply to devops_dan: wait so you had to add the org_id into the jwt yourself? how did you do that, supabase hook or a separate auth server
- devops_dan reply to nocode_nate: We used a supabase auth hook to inject the claim on sign in. It's not super well documented but it's there. You have to write a function that reads the user's org membership and stamps it into the token payload. Took us a couple of tries to get the timing right because the hook fires before the session is fully set up in some cases.
- small_agency_sam reply to devops_dan: this is basically what we ended up doing but with clerk instead of supabase auth, and rls policies on the postgres side. the auth provider change is annoying but the policies themselves were straightforward once we stopped overthinking it

### Tree 2: Skeptical pushback

- mvp_max: Real talk, if you're handling client contracts and pricing on a no-code platform you're one config mistake away from a breach. The role filter thing is the symptom, the disease is that you don't own the data layer. I would not be comfortable telling a client "your data is safe" while running their portal through some third-party builder that I can't audit.
- indie_iris reply to mvp_max: yeah but the alternative is a 6 month build or hiring a backend dev, most solo founders cant afford that
- mvp_max reply to indie_iris: sure, budget is real, but the compromise is that you owe it to your clients to at least know what the isolation model is. "the platform handles it" is not an answer you can give a paying customer during a security review. Even if the answer is "we use postgres rls through Enter Cloud / Supabase / whatever", you should be able to say the actual words and point to the actual policies.

### Tree 3: Bubble-specific experience

- bubble_pete: We had exactly this happen on Bubble. The privacy rules look like they're doing something but if you miss one rule on one field, or if the rule references a thing the client doesn't have access to, it just returns empty instead of 403. Which sounds fine until a client realizes they can guess record IDs and see blank records that shouldn't exist for them at all. We moved off Bubble for any client data app after that.
- nocode_nate reply to bubble_pete: so bubble privacy rules arent rls? i thought they were the same thing
- bubble_pete reply to nocode_nate: They're enforced server side at least, so they're closer to rls than a frontend filter, but the failure mode is "return nothing" which is its own kind of data leak. RLS on postgres will hard reject the query and you can log it.

### Tree 4: How to test isolation (OP appears here)

- test_first: For testing, two things. One, hit the API directly with curl/Postman using a token from Client A, try to fetch a record that belongs to Client B. If it comes back, you have no isolation. Two, write a small script that loops through every endpoint with a Client A token and asserts the response set is exactly what Client A is supposed to see. Run it in CI. We caught two regressions this way that nobody noticed in the UI for weeks.
- OP reply to test_first: yeah the direct api call is what scared me, i just had a feeling and tried it with one of my own test accounts and it returned everything. i had assumed the role was being applied to the query, it definitely was not. For the script approach, do you run it as a separate test suite or hook it into your deploy pipeline? Im trying to figure out how heavy to make this since im the only dev
- test_first reply to OP: We run it on every PR against a staging env with seed data. Takes about 4 minutes to run. Definitely overkill for 30 clients, but it has saved us twice so i dont care.

### Tree 5: Audit logging is the next problem

- sec_steve: Once you fix the isolation thing, the next thing that's going to bite you is audit logging. Specifically, who accessed which client's record, and when. RLS stops the cross-tenant read but it doesn't tell you that Client A's user with email X looked at invoice Y at 3am. If any of these clients ever ask you for a SOC 2 or even just "show me who in your team looked at my data", you need that trail. A lot of the no-code platforms don't expose audit logs at all, or they only show you app-level events not data-level access.
- nocode_nate reply to sec_steve: is this what supabase logs give you or do you need something else on top
- sec_steve reply to nocode_nate: Supabase has some logging but you have to wire it up. There's no "log every read" out of the box. We ended up adding a trigger on the sensitive tables that writes to an audit table on every SELECT. Painful but it works.

## Standalone Comments

- ind_builder_22: saved this, im literally in the same boat with a softr portal
- ai_native_andy: fr, the "role" in most no-code tools is just a tag on the user record, it doesn't filter anything server side unless the platform explicitly does rls or equivalent
- agency_owner_jen: have you looked at clerk + supabase. thats the stack we settled on and rls has been solid for 6 months, no leaks yet
- mvp_max: how big are these client records though, 30 accounts you could probably just own the whole stack for like 2k in dev cost and be done
- bubble_pete: this is why i stopped using bubble for anything with client data, the privacy rules gave me false confidence for a year
- nocode_nate: is the goal to eventually sell this portal as a product or is it internal to your agency? changes the calculus a lot
- devops_dan: vibe coded portals are a nightmare for this btw, the ai has zero concept of rls unless you literally ask "add row level security for tenant isolation" and even then it usually gets the policy wrong
- firebase_fan: firebase auth rules can do this but its not rls, its more like middleware that runs before the query, which is fine but you have to think about rule ordering carefully
- small_agency_sam: the 403 thing is a classic, error messages shouldnt leak record names. usually a sign the api is returning the row before checking permissions
- indie_iris: just a heads up, enter pro is fine but the stack is locked to react/vite/typescript. if you ever need python or go or anything else you have to leave the platform and own it yourself. not a dealbreaker just something to know going in

---

## Title Candidates

- How are you adding auth roles + data isolation to a vibe-coded client portal?
- No-code client portal with real auth, roles, and tenant isolation — how are you actually doing it?
- AI built my client portal UI. Now auth + RBAC + data isolation is on me. What are you using?
- Vibe-coded a client portal. How do you secure it before real clients sign in?
- Best way to add auth roles + data isolation to a vibe-coded client portal?
- AI builder client portal: how do you enforce auth + tenant data isolation without rewriting everything?
- How are you patching auth + data isolation on a vibe-coded client portal before launch?
- I shipped an AI-built client portal UI and the auth/roles/isolation is half-baked. What worked for you?

## Final Post

alright, gotta vent and also actually ask for help.

i'm non-dev (product/ops background) and i used an AI builder to scaffold a client portal for my small agency. the UI looked genuinely good out of the box. login screens, dashboards, client lists, all of it. i was pumped for like 2 days.

then i started poking around at what the AI actually shipped under the hood and... yeah.

auth is basically a stub. there's no real role separation between my internal team and the actual clients. and data isolation is the part that actually scares me, because every client's records look like they're sitting in the same table with maybe a `client_id` column, but i don't see any row-level checks actually being enforced. some queries filter by org, some don't. the AI was super inconsistent about it.

so before i let a real client anywhere near this thing i need to fix:

- real auth. signup, login, session, password reset, the boring stuff
- roles (admin vs client vs staff) enforced server-side, not just hidden behind disabled buttons in the UI
- data isolation so client A literally cannot see client B's stuff, even if someone fat-fingers a query
- some kind of audit log because these are paying customers and i'd like to know who clicked what

read that redaccess report about 2,000+ vibe-coded apps leaking corporate data with zero auth on the URL. that's basically my nightmare scenario and it's half the reason i stopped sending the demo link to clients.

i'm looking at a few things right now. one of them is enter pro because it bundles auth + postgres + something RLS-ish, has a plan mode that lays out the isolation model before any code is written, and the code panel means i can actually see and export what was generated. not married to it, just one of maybe 3 options on my shortlist, and the "plan first + see the code" part is what caught my eye.

for anyone who has shipped a client portal with vibe coding or an AI builder, what did you actually bolt on for auth + roles + isolation? did you stay on the same platform, layer supabase / clerk / auth0 on top, or just rip the whole thing out and rebuild in a real framework? and more specifically, what looked fine in a tutorial but fell apart the second a real client logged in.

---

## Comment Trees

Comment Tree 1:
jpmckinney: Genuinely curious, when you say "RLS-ish" for enter pro, are you actually getting row level security at the postgres layer or is it app-level filtering with a `org_id` column? because if its the second one thats a single bad query away from a leak. postgres RLS with proper policies is the only thing that makes me sleep at night for multi-tenant data.
casualmobileuser23 reply to jpmckinney: from what i tested its postgres RLS not just app filtering. the policies are defined per table and you can see them in the code panel. not saying its magic but its not the same as scoping in a where clause
devthrowaway42 reply to jpmckinney: yeah the "app-level filtering" pattern is exactly how i burned myself on a supabase project. wrote one query wrong and client A saw client B's invoices. never again

Comment Tree 2:
saaskevin: check out lovable if you havent. i know its another AI builder but their backend auth + rls is actually decent for client portals. enter pro sounds newer tho, whats the pricing like for something with like 30 clients
enter_fan92 reply to saaskevin: lovable is solid yeah, used it for a couple things. enter pro has a credits system, you pay as you build and for the cloud stuff. i think their paid plans are listed on the site. both have tradeoffs, lovable is more UI-first imo, enter pro feels more "infra included"
saaskevin reply to enter_fan92: ok thanks, ill check the credits thing. yeah lovable is great until you need real backend stuff and end up wiring supabase anyway

Comment Tree 3:
fullstackdev_nyc: not to be that guy but auth + roles + data isolation in 2026 should not require you to read a report and panic. every AI builder should ship with this stuff working out of the box and they all still dont. its genuinely embarrassing
tinydevops reply to fullstackdev_nyc: hard agree. the redaccess report was wild tho, 2000+ apps just open on the internet. some of those were definitely "i built this in a weekend" and never went back to lock it down
fullstackdev_nyc reply to tinydevops: exactly. the gap between "AI built me a demo" and "this is safe to give to a client" is the whole game and nobody talks about it

Comment Tree 4:
nocode_veteran: i went down the supabase + clerk + stripe rabbit hole for a client portal last year. ended up being more work than just hiring a dev to build it properly. has anyone actually shipped a no-code client portal that handles auth + roles + isolation + payments in one go without it falling apart at like 50 users?
saaskevin reply to nocode_veteran: base44 is probably closest to what you want but payments are still on you. for 50 users tho honestly a real stack might be faster than fighting the tools

Comment Tree 5:
mharchitect: for anyone reading this later, the practical checklist before you let clients log into an AI-built portal: server-side session validation on every route, explicit role checks in the API not just the UI, RLS policies on every tenant-scoped table, audit log for sensitive reads, rate limiting on auth endpoints, and rotate any secrets the AI generated for you. if your builder cant do all of that its not ready
casualmobileuser23 reply to mharchitect: this is the checklist i wish i had 3 months ago lol. saved

## Standalone Comments

- fr i was looking for this exact thread
- can confirm the redaccess report, it was a wake up call for my team
- the "AI built the UI in 2 hours and i spent 2 weeks on auth" pipeline is so real
- wait enter pro is new to me, how does it compare to replit agent for client portals
- im on bolt and basically gave up on the built-in auth, wired up supabase manually
- "session enforced server-side not just hidden behind UI buttons" should be tattooed on every AI builder founders forehead
- is there a builder that actually does RBAC + multi-tenant + audit log without you writing policies from scratch? seems like a gap
- my biggest fear is one of my clients forwards the url to someone and they see everyones invoices. RLS or bust
- you should also check what your AI builder does with secrets, a lot of them hardcode API keys in the frontend bundle which is terrifying
- this is the right question to ask. most people just ship the pretty UI and pray
- clerk has been the easiest auth drop-in for me but its another vendor to pay for
- anyone tested enter pros plan mode for something like a 5-role RBAC setup? curious how it handles the policy design
- the moment a client asks for an audit log is the moment every AI builders shortcuts show



# Raw Drafts - direction_003

# Search Occupancy Drafts

## Title Candidates

1. AI app builder code export developer handoff: the checklist I run every time
2. Got handed a Lovable/Bolt/base44 project from a non-tech founder? Read this first
3. Code export isn't enough: 8 things I check on every AI-generated web app before pricing the job
4. The handoff from AI app builder to developer is still completely broken
5. Your founder just DMed you their AI-built app. The 8-point intake checklist.
6. I keep getting handed half-finished AI app builder projects. Here's what breaks first.
7. AI app builder developer handoff in 2026: what to verify before you say yes
8. Best AI app builder for clean code export and handoff? It's not about the tool.
9. AI app builder code export vs real developer handoff: the gap nobody closes
10. 8 things I verify on every AI-generated app before I quote the handoff

## Final Post

A non-tech friend DMed me again last week. "Built this thing on [AI builder], can you take it from here?"

I get this request roughly once a month now. The pattern is always the same. Before I touch anything, I run it through this checklist.

**1. Can I actually run it locally?**

If the answer is "I don't know, I built it in a browser," that's already a red flag. I want a `git clone`, an install command, a dev script, and a working `localhost` within 10 minutes. No black box. No "just click deploy in the dashboard."

**2. What's the auth story?**

Who can sign up. Who can sign in. Password reset, email verification, social login, the works. Can a user see another user's data if they guess a UUID? I don't care if it's Firebase, Supabase, Clerk, or a custom JWT setup. I need a clear model. "Anyone with the link can log in" is not auth.

**3. Is there a database, and is there RLS?**

most browser-based AI builders happily spin up a Postgres for you and then forget to write the row-level security rules. I open the data tables, create two test users, and try to read user A's records as user B. If it works, the app is already leaking.

**4. Where are the secrets?**

Open the deployed bundle. Search for `sk_`, `key=`, `AIza`, `Bearer`. Anything in client code is a leak waiting to happen. A friend of mine got hit with a £1,000+ bill because a Google AI key sat in a public GitHub repo. don't be that friend.

**5. What's the deploy story?**

Is it one-click. Do I have a custom domain. Can I reproduce the deploy from a clean machine. Staging vs prod split? "It works on my builder's subdomain" is not production.

**6. Stripe / payments, and is it actually wired up?**

If theres a paywall, I check: does checkout actually create a subscription, does the webhook update the user record, does the feature gate flip when payment fails. I've seen "subscriptions" that are basically a static "Pro" button.

**7. Do I own the code?**

Full file tree visible. Export to GitHub. Can I fork and walk away. If the answer to any of these is no, I tell the founder upfront: you're locked in, and that has a cost.

**8. What happens when something breaks?**

Can I read the error. Are there logs. Is there a way to rewind. If the only way to "debug" is to re-prompt the AI and hope, I charge extra for that.

---

**What a clean handoff actually looks like**

the times handoffs have gone smoothly, its been because the AI builder produced something a dev could actually grab. React/Vite/TypeScript/Tailwind is the usual stack. I can see the full file tree in a code panel, export to GitHub, and clone locally. Auth, Postgres, storage, secrets, and RLS are already wired as part of the platform's backend, not five different SaaS accounts I have to reconcile. And if I want to keep working in my own environment, theres a local terminal agent that lets me read, edit, test, and rewind the same project on my machine without losing context.

Enter Pro is one example of that shape. Browser builder plus an actual cloud backend plus a local terminal handoff, not just a UI generator. Full disclosure: I work with them, so I'm biased, but the checklist above is what I run against any AI-built app regardless of vendor. Their stack is React/Vite/TypeScript/Tailwind, code panel with export and GitHub sync, built-in Auth/Postgres/Storage/Functions/Secrets/RLS, and a local terminal agent for handoff. I still verify every item by hand because "the platform says it does X" and "X actually works" are different sentences.

---

The cost of the handoff isn't the code. It's the unstated assumptions. "Users can only see their own data" is an assumption. "Secrets aren't in the bundle" is an assumption. "Deploy is reproducible" is an assumption. Every one of those can be true, but the founder has to know theyre assumptions, and the builder has to make them auditable.

If you're a dev getting handed one of these, run the checklist, send the founder the list of what's missing, and price accordingly. Not their fault the tooling hid it from them. but its your time on the line.

---

## Comment Trees

**Tree 1: The RLS deep-dive**

user1 (The PC User): RLS point is underrated. most non-tech founders have no idea their supabase tables are basically wide open by default. I've seen "internal CRM" type apps where any logged in user can SELECT * from the customers table. nobody checks until a customer finds a URL parameter and pokes around.

user2 reply to user1 (The Casual Mobile User): same. its always the "well they need to be logged in" defense that kills me. logged in is not authenticated for that specific row

user3 reply to user2 (The Rushed Typist): yeah but to be fair most of the AI builders now have a "turn on RLS" toggle in the table editor. problem is its off by default and theres no warning. founder just clicks create table and moves on

user1 reply to user3: 100%. and even when RLS is on the policies are usually "auth.role() = 'authenticated'" with no per-row check. technically on, functionally useless for multi tenant apps

user4 reply to user1 (The Casual Mobile User): this is why i tell founders to write out one sentence per table: "user X can do Y to row Z if condition W." if they cant fill that in the table probably shouldnt exist

---

**Tree 2: The competing tooling objection**

user5 (The PC User): Honest question, why not just tell the founder to scrap the AI builder and rebuild in Next.js + Supabase + Clerk + Stripe directly? you'd have cleaner code, real RLS, no platform tax. a few extra weeks upfront saves a lot of handoff pain

user6 reply to user5 (The Rushed Typist): because most of these founders cant "just" do that. thats the whole point. they dont know what nextjs is. the AI builder got them 80% there in a weekend. a real stack would take them 6 months or a dev they cant afford

user5 reply to user6: fair. i was thinking from the dev's side where id rather inherit a clean next project than a custom internal framework with a one click deploy button. but yeah for a solo non technical founder the AI route is probably the only realistic one

user7 reply to user5 (The Casual Mobile User): also half these AI builders export to nextjs or react anyway. the code isnt magic. its just a v0 or lovable project with extra steps in front of it. what changes is who owns the deploy pipeline and the db

---

**Tree 3: The API key disaster story**

user8 (The Rushed Typist): section 4 hit hard. client of mine last year had an openai key sitting in a netlify preview deploy. some bot found it and racked up about $400 in a weekend before they noticed. now i do a "search for sk- in the built bundle" as step 0 on every handoff

user9 reply to user8 (The Casual Mobile User): $400 is honestly lucky. the ai key stories i hear are usually 4 figures. google especially because their billing dashboard takes forever to alert

user8 reply to user9: yeah google was the one that got my friend in the original post. took them like 3 weeks and a stack of proof to actually refund it. first response was a template email saying no evidence of unauthorized use lol

user10 reply to user8 (The PC User): Pro tip: rotate your keys every 30 days anyway. even if the key is currently safe, assume it will leak and make the blast radius small. also check your builder's "env var" UI, half of them push client env vars to the bundle by default and the user has no idea

---

**Tree 4: The local terminal handoff skepticism**

user11 (The PC User): The "local terminal agent" mention is interesting but i'm skeptical. in my experience the moment a non tech founder's project is in a folder on a real devs machine, the project forks. the founder never goes back to the browser builder and the two versions drift. how does Enter Pro actually keep them in sync, is there a real git round trip or is it "export to zip and pray"

user12 reply to user11 (The Rushed Typist): good q. from what ive seen the github sync is one way reliable. you can push from the browser to github, you can pull from github back into the builder. but the "local terminal agent" part is more for the dev to keep working locally while the founder stays in the browser. its not really a two way live sync, more like a handoff boundary

user11 reply to user12: ok that makes more sense. so its not "edit in both at once and it merges." its "hand off to dev, dev does the hard stuff, dev pushes back, founder sees updates." thats actually a reasonable model for this market

OP reply to user11: yeah seconding user12. local terminal side is for me to do real work without fighting a browser editor. browser side stays as the source of truth for the founder. github is the bridge. no live merge magic, just a clean push/pull. i wouldnt frame it as "sync" to a client without caveats.

---

**Tree 5: The "is this just a checklist for Lovable" pushback**

user13 (The Casual Mobile User): am i missing something or is this whole post just "use Enter Pro because it does the backend." feels like a sponsored checklist. what about bolt.new or base44 which also have postgres and auth built in

user14 reply to user13 (The PC User): op literally said they work with Enter Pro in the disclosure line. read the post. also Bolt and Base44 are not the same product category, Bolt is closer to a StackBlitz wrapper, Base44 is more of a workflow tool. different tradeoffs. op is not saying "only use this," they're saying "here's what to check, and by the way one tool that does check these boxes is X"

user13 reply to user14: ok fair, i did skip the disclosure line on mobile. still dont love the framing but the checklist itself is solid. saving it for the next time a founder slacks me a base44 link

OP reply to user13: yeah fair criticism on the framing. the checklist is the part i actually use on every handoff regardless of what built it. the Enter Pro mention is because its the closest thing ive seen to "browser builder that doesnt lie about the backend." but bolt, base44, lovable, v0 all have their place. it just depends which checkboxes the founder needs filled.

---

## Standalone Comments

saved this. sending to a friend who just spent 2 weeks in lovable and is about to ping a dev for "small tweaks"

the RLS one is the one i never see non-tech founders think about. thanks for spelling it out

fr the "can i run it locally in 10 min" test is the single biggest time saver. if i cant clone and npm install without 6 environment variables and a youtube tutorial, im not touching it

section 6 (stripe) is where i see the most "it works in the demo" delusion. "i have subscriptions" yeah bro you have a button

honest question for the op, how do you price these handoffs? flat fee, hourly, or "depends on what breaks when i open the bundle" because ive been lowballing myself on these

this is good but id add a step 0: "does the founder actually have a paying customer or a waitlist, or are they pre revenue with a landing page." changes whether the handoff is even worth doing

not gonna lie i came in expecting another "10x developer with AI" hype post. this is actually a useful checklist. upvoted

the api key in the bundle thing is so common it should be in every AI builder onboarding flow as a warning popup. someone at google or openai should be paying for that banner slot

can confirm step 4 from personal experience. £300 in a weekend because i left a key in a vercel env that got mirrored to the client bundle. wouldve been £3000 if i hadnt caught it on a sunday morning randomly checking the dashboard

---

## Title Candidates

1. The handoff between AI app builders and a developer is completely broken
2. Can an AI app builder actually survive a developer handoff in 2026?
3. Has anyone found an AI app builder that exports clean code for dev handoff?
4. I tested 5 AI app builders for code export and developer handoff. here's what worked
5. The AI app builder to developer handoff is the real bottleneck. anyone solving it?
6. Got stuck on AI app builder code export? AMA on dev handoff workflows
7. Stop using AI app builders that don't let you export code. my breakdown
8. AI app builder code export: the developer handoff trap nobody talks about

## Final Post

running a split setup with my co-founder. she does UI flows and simple logic in a browser AI builder. when auth, stripe webhooks, db rules or weird edge cases come up thats me.

problem is I either rewrite the whole thing or fight an export that clearly wasnt designed to be touched. tried a few options. Enter Pro came up because the browser side has a code panel + github sync, and Enter Code is a local terminal agent that picks up the same project. trialing it on a side project for a couple weeks. if the code panel shows real source not some minified blob and github sync works both ways thats already half the battle.

has anyone kept a browser + local split going past the prototype phase or is it always "demo works then I rewrite everything"

---

## Comment Trees

**Tree 1: The Skeptical Validator (Competitor Defense)**

user1: how is this any different from lovable? they have github sync too and the code export is at least readable. feels like youre shilling

user2 reply to user1: lovable is fine for ui but the second you need real backend logic (rls, webhooks, functions) youre bolting on supabase manually. thats where the handoff falls apart for me

user3 reply to user2: this. the lovable + supabase combo is basically two products pretending to be one. at least with enter the cloud stuff is in the same workspace so when the dev opens the code panel everything is there

user1 reply to user3: fair, i havent tried enter. is the code actually production quality or is it "works on the happy path" code

user3 reply to user1: honestly mixed. plan mode helps because you see what its going to build before it builds it. but you still need to review for security stuff. nobody is replacing a dev here

**Tree 2: The Deep Dive (SEO Smuggling on Code Export)**

user4: for anyone who cares about the actual export quality. i tested 4 builders last month for code export specifically. bolt gave me a vite project but no backend. v0 was component-only. base44 was basically a black box. enter pro was the only one that exported a full project tree with the auth + db schema included, not just the frontend react

user5 reply to user4: wait so it includes the postgres schema on export? thats huge. most builders just give you the ui and tell you to figure out data

user4 reply to user5: yeah i was surprised too. its not magic though, you still need to set up your own db if you migrate out. exportable doesnt mean zero migration. took me a weekend to move one project to my own infra

user6 reply to user4: this is the answer ive been looking for. thank you. do you know if it works with turborepo or is it strictly single app

user4 reply to user6: single react app from what i saw. not a monorepo. enter code lets you work in a local repo but its the same project not multiple packages

**Tree 3: The Real World Handoff**

user7: ive been on both sides of this handoff and honestly the biggest issue isnt the tool. its that the non tech person builds something the dev cant run. no readme, no seed data, no env file example. you open it locally and its just... blank

user8 reply to user7: yep. and then they say "it worked on my screen" and youre stuck

user7 reply to user8: enter code at least lets the dev rewind changes and see what got modified. saved me once when my cofounder pushed an update that broke the auth flow. i just rolled it back and fixed it in the terminal

user9 reply to user7: does the rewind actually work well or is it like ctrl z in google docs where you lose context

user7 reply to user9: its better than that. shows diffs. but dont expect git-level granularity, its session based

**Tree 4: The Stripe Webhook Tangent**

user10: curious how this handles stripe. thats always where my handoffs die. the non tech person adds a checkout button in the browser builder, i need to wire up the webhook + subscription state + feature gate on my end. usually the builder has no idea what the webhook payload even looks like

user11 reply to user10: enter pro has stripe docs in the resource layer. didnt use it end to end yet so cant confirm the webhook reliability. plan was to test it this weekend with test mode keys

user10 reply to user11: let us know. ill prob do the same. if it actually handles the full subscription state sync without me writing glue code ill switch

OP reply to user10: same boat, havent gotten to the stripe piece yet. my cofounder added the button but i need to verify the webhook flow + access gate logic before we charge anyone. will report back

**Tree 5: The "Just Use a Real Framework" Take**

user12: hot take. if you have a dev on the team just use next.js + cursor. skip the whole browser builder entirely. all these "handoff" workflows exist because people are trying to avoid the thing that actually works

user13 reply to user12: this works if the dev has time to build the ui too. in our case the cofounder moves faster in the browser tool than i do in code. shes not learning react. im not building her screens. the split is a feature not a bug

user12 reply to user13: ok thats a legit reason. but youre one api change away from being stuck maintaining a vite app you didnt write

user13 reply to user12: thats exactly why i use enter code. when it gets weird i just open it locally and treat it like a normal repo. not locked in

## Standalone Comments

user14: saved this, im in the exact same spot. non tech cofounder loves the browser builders, i hate every export ive ever opened

user15: the "code panel" thing is the differentiator for me. most builders hide the code behind a paywall or dont show it at all. if i cant see the files i cant hand it off

user16: can confirm the github sync works both ways on enter. pushed a fix from my local vscode, cofounder kept editing in browser, no merge conflicts yet. small project though so grain of salt

user17: is this basically replit agent but with a browser first workflow? replit has been my go to for the "non tech person builds, dev takes over locally" thing

user18: not the same. replit locks you into their ide. enter code is just a terminal agent, you can use whatever editor. and enter pro is separate from enter code which keeps things cleaner imo

user19: the real question is pricing. none of these tools are cheap once you actually ship something. whats the credits situation look like for a small team

user20: hot take but the handoff problem isnt technical its communication. no tool fixes "my cofounder cant explain what she wants." ive tried 3 builders. same problem every time

user21: op are you on the free tier or paid for enter. wondering if the github sync is gated

OP reply to user21: paid, github sync is included. free tier might be limited im not 100% sure, check the pricing page its listed

user22: 3 months in on a similar setup. the browser builder is great for mvp. the moment you have real users the dev takes over completely and the browser tool gets used for prototyping only. which is fine, just be honest about what stage youre using it for

user23: lol everyone here is acting like code export is the holy grail. most of the code these tools spit out is still mid. you will rewrite half of it

user24: true but rewriting half is better than rewriting all. thats the whole point of having a code panel + source access in the first place



# Raw Drafts - direction_006

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



