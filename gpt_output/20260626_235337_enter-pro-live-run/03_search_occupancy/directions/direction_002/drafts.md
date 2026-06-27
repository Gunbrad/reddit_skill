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
