# Reddit Raw Posts

Generated at: 2026-06-26T16:33:57.982964+00:00
Total posts: 9

## Post 1

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/softwarearchitecture
Title: Designing security and audit boundaries for a privacy-sensitive data portability app
Post URL: https://www.reddit.com/r/softwarearchitecture/comments/1u528sh/designing_security_and_audit_boundaries_for_a

Body:

I’m working on the high-level design and architecture of a browser app that I am developing to fill the vacuum of a similar app that is closing up shop on July 1. The app consists of a web client front end, a REST API service on the backend, and Azure as the scalable data store and API service hosting.

I am one of the users of the app that is shutting down, so while I have a solid understanding and black-box design, I grossly underestimated the scale. I was led to believe that the subscriber base came in at 100K subscribers, and that the concurrency was below 5K. I have since learned that in fact there are 500K subscribers and concurrency of 10-15K users at any time.

Given these new scaling assumptions and the privacy-sensitive data, I need to rethink scalability and security. In addition, I need to consider that 500K users / 10-15K concurrent users may be the low end. I don’t want to have to come back to the drawing board and do another redesign. I am currently working through the architecture for this system and would appreciate feedback on the user/security model before implementation gets too far along.

The system started as a data-preservation use case: users, such as myself, need to export their data before the service closes down for good. That was actually the easy part. The harder design problem is that the data is sensitive, may not always map cleanly to one individual owner, and needs to be able to address different communities with different rules around consent, shared access, privacy, support roles, and auditability.

The thing I want to avoid is building a simple “user logs in, admin manages everything” model that works for an early prototype but becomes the wrong foundation later.

The main architecture questions I’m wrestling with are:

I am leaning

...[truncated]

Score: 5
Comment count: 4

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "Discussion/Advice",
  "author": "Sharky_J_Yellowfish",
  "final_url": "https://www.reddit.com/r/softwarearchitecture/comments/1u528sh/designing_security_and_audit_boundaries_for_a/"
}
```

Loaded comment tree:

reported_comments: 4
loaded_comments: 4
included_comments: 4
top_level_comments: 1
max_comment_depth: 3

Comment Tree 1:

bartekus: Solid post, you’re asking these in the right order (before implementation locks them in). Two reframes first, then the per-question stuff. Your scale worry is pointed at the wrong axis. 500K subscribers with 10-15K concurrent isn’t a hard scaling problem. That’s a stateless API behind Azure with connection pooling, read replicas, and caching. Standard stuff. The decisions that are actually expensive to reverse aren’t throughput, they’re your ownership model, your authz model, and how consent and audit relate to the PII. You’re anxious about the cheap-to-fix axis. The one scaling decision worth nailing now is your partition key (tenant vs data-subject), because that one hurts to change later. You’re collapsing five different boundaries into one “System.” That’s the real trap. They have diff

...[truncated]
	Sharky_J_Yellowfish (OP) reply to bartekus: Thanks for taking the time to respond with so much detail. This is exactly the kind of answer I was hoping for as I continue turning the design work into schema and API boundaries. I like the way you framed the expensive-to-reverse decisions: ownership model, authorization model, consent model, audit model, and partition key. I think I got tunnel vision over scale only because I underestimated the size of the user base. Your post helped shake out my narrow view. I am incorporating the separation between tenancy/isolation, resource ownership, authorization, consent, and audit into my next design and planning pass. I need to be especially careful about user trust with this project because it works closely with private exported data. I don't want account/System membership or consent to become

...[truncated]
		bartekus reply to Sharky_J_Yellowfish (OP): Glad it was useful, and your playback is spot on, so I’ll just add two guardrails for the schema pass. One: treat ReBAC as the relationship layer, not the whole authz story. It’s tempting once you stand up OpenFGA to model everything as tuples, including consent. Resist that. Ownership, sharing, and delegation are relationships; consent state and purpose-of-use stay as policy inputs to the decision. Time-bounded consent encoded as relationship tuples gets ugly fast. Two: the five separations are conceptual boundaries, not five services you build on day one. Put the seams in the schema and behind the single decision point now, but keep the deployment a monolith until something actually forces a split. Model the seams, defer the splits. As a solo build against a July 1 vacuum, that’s the dif

...[truncated]
			Sharky_J_Yellowfish (OP) reply to bartekus: Thanks again for the architecture advice. I wanted to circle back with where the design landed, because your point about separating ownership, authorization, consent/visibility, audit, and partitioning was the thing that finally made the model click. The current spine is now: Account -> Membership -> System -> Authorization -> System-scoped data Account is the login/security principal. System is the protected data namespace. Membership is the account-to-system access grant. Roles attach to that membership. The API resolves the current account, resolves active membership, resolves the current system, then checks authorization before returning system data. A few things were deliberately kept separate: Privacy bucket data from the app being sunset on July 1 is preserved as source/import data.

...[truncated]

## Post 2

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/vibecoding
Title: I built an open-source client portal. Here's the stack and how I built it.
Post URL: https://www.reddit.com/r/vibecoding/comments/1s11drg/i_built_an_opensource_client_portal_heres_the

Body:

I run a small agency and needed a client portal. Everything I found was either a feature buried in a bloated CRM or a SaaS I couldn't white-label. So I built my own.

What it does:

• Centralized workspace for files, tasks, messages, and invoices per client

• White-label ready, runs on your domain with your branding

• Multi-tenant so you can manage multiple clients from one instance

• Self-hostable via Docker Compose

How I built it:

• Backend: NestJS with Prisma as the ORM, PostgreSQL for the database

• Frontend: Next.js with Tailwind

• Auth: Better Auth for session management

• Deployment: Docker Compose for self-hosting, with plans to get listed in Unraid Community Apps

• AI tooling: Used Claude Code heavily throughout development for scaffolding modules, writing Prisma schemas, and iterating on API endpoints. Most of the core feature buildout was paired with Claude rather than written fully by hand.

The biggest challenge was designing multi-tenancy cleanly so each client gets an isolated workspace without overcomplicating the data model. Prisma made this easier than expected with relational filtering at the query level. It's still early but functional and I'm building it in public. Actively adding features based on what users request.

Landing page: https://atrium.vibralabs.co

GitHub: https://github.com/Vibra-Labs/Atrium

Happy to go deeper on any part of the stack or process.

Score: 3
Comment count: 2

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "https://atrium.vibralabs.co/",
  "flair": "",
  "author": "bartsimpsonnn",
  "final_url": "https://www.reddit.com/r/vibecoding/comments/1s11drg/i_built_an_opensource_client_portal_heres_the/"
}
```

Loaded comment tree:

reported_comments: 2
loaded_comments: 2
included_comments: 2
top_level_comments: 1
max_comment_depth: 1

Comment Tree 1:

Excellent_Sweet_8480: This is really solid, the multi-tenancy problem is honestly one of those things that sounds simple until you're actually in it. Curious how you handled tenant isolation at the query level with Prisma, like are you scoping everything through a clientId on every query or did you go with something like row-level security on the postgres side? Also the white-label angle is smart, that was always the thing that killed SaaS options for agency work. Most of them let you slap a logo on it and call it a day but you're still sending clients to someone else's domain.
	bartsimpsonnn (OP) reply to Excellent_Sweet_8480: Thanks! For tenant isolation we scope everything through organizationId at the application level, every query filters by the org from the authenticated session. We went with Prisma scoping over Postgres RLS mainly for simplicity and portability, since the app is meant to be self-hosted and we didn't want to require specific Postgres configs. The auth layer (Better Auth with organizations plugin) handles org membership and role enforcement, then NestJS guards make sure you can only touch data within your org. And yeah, the white-label piece was a big motivator. Agencies shouldn't have to send clients to a generic-looking portal. Right now you can customize colors, logo, and favicon per org and we're working on branded login pages with custom slugs (/login/your-agency) so clients never see a

...[truncated]

## Post 3

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/dotnet
Title: IdentityServer/OAuth: Added New Client but Custom Role Claims Not Appearing in Access Token
Post URL: https://www.reddit.com/r/dotnet/comments/1to7b1e/identityserveroauth_added_new_client_but_custom

Body:

I'm working on an existing system that was configured before I joined the project, and I'm trying to introduce a new client application.

Current setup:

Angular web client

IdentityServer

Resource/API server

OAuth/OIDC authentication flow

Configuration stored in SQL database

We recently added a new client (admin-client) for system-level administrators.

What I've done so far:

Added the new client entry in the IdentityServer database

Added the required Identity Resources / API Resources / Claims mappings

Added role-related claims for the admin users

When I generate an access token, I only see a role claim with the type:

http://schemas.microsoft.com/ws/2008/06/identity/claims/role

is it normal?

I expected to receive additional role claims as well, but they are not appearing in the token payload.

On the Resource Server side, my authorization policy checks for multiple possible role claim types:

role
roles
http://schemas.microsoft.com/ws/2008/06/identity/claims/role

Is this ideal way? I am not sure about what will be the proper way of implementing whole flow so

My questions:

When adding a completely new client to an existing IdentityServer setup, what are the minimal database changes required?

Which tables/entries typically need to be updated (Clients, ClientScopes, ApiScopes, ApiResources, IdentityResources, Claim mappings, etc.)?

Is there anything special required to ensure role claims are emitted into the access token?

Does anyone have an example of a multi-client IdentityServer setup where a new client was added through SQL configuration?

if anyone did this kind of setup them please share the knowledge or example configurations you have.

Score: 2
Comment count: 6

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "http://schemas.microsoft.com/ws/2008/06/identity/claims/role",
  "flair": "Question",
  "author": "rpsilver36",
  "final_url": "https://www.reddit.com/r/dotnet/comments/1to7b1e/identityserveroauth_added_new_client_but_custom/"
}
```

Loaded comment tree:

reported_comments: 6
loaded_comments: 4
included_comments: 4
top_level_comments: 3
max_comment_depth: 1

Comment Tree 1:

Coda17: Don't add stuff directly to the database, use the IdentityServer API to add clients. But generally, clients don't have roles, users do. Your authZ policy shouldn't be checking all the possible claim names, it should be transforming the incoming claims to how you want them represented on the resource server side
	zaibuf reply to Coda17: But generally, clients don't have roles, users do. We use roles for some api to api calls. This was built before my time, I think it makes more sense to use scopes. In our system we have a custom schema with a few tables to manage roles which joins in on clientId.

Comment Tree 2:

TNest2: You configure the claims that should appear in the ID-token separately from the claims that should go into the access tokens. See my blog post here: https://nestenius.se/net/identityserver-identityresource-vs-apiresource-vs-apiscope/ I do have a lot of blog posts about IdentityServer. See this page https://learn.microsoft.com/en-us/aspnet/core/security/authentication/claims You need to set this flag, to prevent the AddOpenIDConnect from renaming your clams into the legacy default Microsoft claim names: options.MapInboundClaims = false;

Comment Tree 3:

AutoModerator: Thanks for your post rpsilver36. Please note that we don't allow spam, and we ask that you follow the rules available in the sidebar. We have a lot of commonly asked questions so if this post gets removed, please do a search and see if it's already been asked. I am a bot, and this action was performed automatically. Please contact the moderators of this subreddit if you have any questions or concerns.

## Post 4

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/Supabase
Title: I migrated auth away from Supabase but kept the database. Here's what I learned.
Post URL: https://www.reddit.com/r/Supabase/comments/1san78h/i_migrated_auth_away_from_supabase_but_kept_the

Body:

I've been using Supabase as my main database for about a year now and I'm not going anywhere. RLS, Postgres functions, the dashboard, all great. But I recently ripped out Supabase auth and moved to Clerk and wanted to share why, and what the migration actually looked like, since I couldn't find many posts from people who partially migrated away.

The reason wasn't that Supabase auth is bad. It worked fine for a while. The problem was I'm building a multi-tenant app and needed organization-level features: inviting team members, role management per org, and a prebuilt UI for user profiles and org switching. Supabase auth handles individual users well but the organization layer doesn't exist. I was building so much custom logic on top that it stopped feeling like I was using a managed auth service.

Clerk gave me organizations, invitations, role-based access, and prebuilt components out of the box. The admin-side auth UI that would've taken me weeks to build was done in a day.

The migration itself was 44 files changed. The main gotchas:

Supabase auth user IDs are UUIDs. Clerk user IDs are strings like user_abc123. If you have any foreign keys referencing auth.users or columns typed as UUID for user IDs, you need to migrate those to TEXT. I had to write a migration just for that column type change.

RLS policies that referenced auth.uid() all broke. I replaced them with policies that check a custom claim from the Clerk JWT. You have to set up a custom JWT template in Clerk that includes the Supabase tenant ID, then configure Supabase to verify Clerk's JWT. Not hard but not obvious either.

The session flow changed completely. With Supabase auth the client SDK handles sessions automatically. With Clerk you need to get the token from Clerk and pass it to your Supabase clien

...[truncated]

Score: 85
Comment count: 32

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "tips",
  "author": "FinanceSenior9771",
  "final_url": "https://www.reddit.com/r/Supabase/comments/1san78h/i_migrated_auth_away_from_supabase_but_kept_the/"
}
```

Loaded comment tree:

reported_comments: 32
loaded_comments: 32
included_comments: 30
top_level_comments: 15
max_comment_depth: 2

Comment Tree 1:

ivasilov: Great breakdown, thank you for sharing. We do officially support Clerk as an auth provider, have you looked at https://supabase.com/docs/guides/auth/third-party/clerk? I don't know enough about your migration, but it might've been easier using the Third-Party Auth as a step?
	FinanceSenior9771 (OP) reply to ivasilov: oh nice, i didn't know about the official third-party auth guide for clerk. i set up the JWT integration manually so this would've saved some time. the custom JWT template and RLS policy rewrite was the bulk of the work so if this guide covers that path it's definitely the way to go for anyone doing the same migration. thanks for sharing it.

Comment Tree 2:

ashkanahmadi: Thanks for sharing. Why not use something like Neon if you wanted the database without the auth part?
	FinanceSenior9771 (OP) reply to ashkanahmadi: fair question. honestly by the time i decided to move auth out, everything else on supabase was already working well. RLS policies were set up, migrations were in place, the dashboard is great for debugging. moving to neon would've meant migrating the database too for no real benefit. supabase without supabase auth is basically a managed postgres with a nice UI and RLS built in, which is exactly what i need. if i were starting fresh today i'd still probably pick supabase for the database layer.
		ashkanahmadi reply to FinanceSenior9771 (OP): Makes sense 👍
		alfrednutile reply to FinanceSenior9771 (OP): Great share. It also for me would bring storage to the table and events system so I can integrate into other tools. I wonder if websockets (Realtime) still work if you are not using its sessions?

Comment Tree 3:

CandidChameleon: Interesting post! I actually did the same migration, but in the opposite direction. This was before I had real users so it was straightforward, though -- not too painful. I wanted the clerk org structure, SSO, and invites, but ultimately decided: maintaining all the hooks and a separate copy of my tables was annoying the maintenance of an additional service wasn't worth it I needed the built-in second layer security from RLS Admittedly, SSO was a pain in the ass. The org structure thing wasn't too bad, though -- what made it so tough on your end?
	FinanceSenior9771 (OP) reply to CandidChameleon: The org structure itself wasn't the hard part, it was everything around it. i needed each tenant to map to a clerk org, then store the supabase tenant ID in the org's metadata so the backend could resolve which tenant a request belongs to. then invitations, role management per org, an org switcher in the UI, and making sure RLS policies respected the org-level tenant ID instead of just the user ID. Supabase auth gives you users but the "this user belongs to this organization and has this role within it" layer doesn't exist. i was building a custom orgs table, a memberships table, invitation logic, and UI for all of it. at that point i was maintaining more auth code than product code. Your reasons for going back make sense though. if you need tight RLS integration and don't want to maintain

...[truncated]

Comment Tree 4:

mrdingopingo: I'm building a MVP with multi tenant support and for now everything's working fine
	FinanceSenior9771 (OP) reply to mrdingopingo: nice, are you using supabase auth for the multi-tenant part? if so just make sure your RLS policies are airtight early on. the biggest pain point for us was retrofitting tenant isolation after the fact. way easier to set it up correctly from the start than to migrate later.

Comment Tree 5:

drewhackworth: I’m building an app right now with Supabase + Clerk and one of the biggest things I did to being with was abstract everything in tables to match clerk so if I do move to different auth in the future it’s an easy repoint. Users, org memberships, and roles are all abstracted into tables and for now Clerk is the source of Truth but the internal tables are updated based on that. RLS rows and permissions are based on the tables associated org id and not the clerk org id and I have db functions to match, it’s a little more complex on the front end and slightly more resource intensive, but more forwards compatible should I switch. One of the biggest reasons I went with Clerk vs something else is I had planned on rolling out Clerk Billing as well but it’s been a fucking nightmare with zero help fr

...[truncated]
	FinanceSenior9771 (OP) reply to drewhackworth: The abstraction layer is smart. we didn't do that and it made the migration more painful than it needed to be. having your own internal tables that mirror clerk means you could swap to auth0 or anything else without touching your RLS policies. wish i'd thought of that upfront. the clerk billing thing is interesting, we skipped that entirely and went with razorpay directly since stripe isn't available in india. sounds like building billing yourself might be the better move regardless. at least you own the integration and aren't debugging someone else's stripe connection.

Comment Tree 6:

midlifematt: Even as a single tenant app, Supabase Auth is too buggy. Have spent too much time building workarounds. Thanks for sharing your experience though.
	FinanceSenior9771 (OP) reply to midlifematt: yeah i didn't want to trash supabase auth in the post because it did work for my initial use case but i definitely ran into some rough edges too. clerk has been noticeably smoother on the auth side. hope the migration goes easy if you end up switching.

Comment Tree 7:

ParfaitDeli: Great advice! Thanks. I am starting to build a platform for customer needing to add producers of courses that can have own users. Would clerk be a good fit ?
	FinanceSenior9771 (OP) reply to ParfaitDeli: yeah clerk would work well for that. the organizations feature maps naturally to your use case - each producer would be an org, their users would be org members, and you can assign roles (admin, viewer, etc.) per org out of the box. the invitation flow and org switcher come prebuilt too so you're not building that from scratch. free tier is generous enough to validate the idea before paying anything.
		ParfaitDeli reply to FinanceSenior9771 (OP): Thank you! Sounds like what we need.

Comment Tree 8:

AlternativeInitial93: This is a really solid breakdown — especially the part about how deeply auth is baked into Supabase. A lot of people underestimate that until they try to swap it out. The UUID → string migration and the RLS rewrite are probably the biggest “hidden costs” here. Once you lose auth.uid(), you’re basically responsible for recreating that trust layer yourself, which changes how you think about security entirely. I’ve seen a similar pattern where teams start with Supabase auth, then outgrow it once multi-tenant + org-level permissions become core. At that point, tools like Clerk or Auth0 start making more sense because they treat orgs as first-class citizens instead of something you bolt on. Your point about “Supabase becoming just Postgres” is spot on too — not a bad thing, but definitely a min

...[truncated]
	FinanceSenior9771 (OP) reply to AlternativeInitial93: JWT claims. clerk lets you set up a custom JWT template where i include the supabase tenant ID from the org's metadata. on every request the backend passes that token to the supabase client and the RLS policies check the tenant_id claim from the JWT instead of auth.uid(). so every query is automatically scoped to the tenant without doing joins against a memberships table in the policy. the tradeoff is you're trusting the JWT entirely for tenant scoping. with supabase auth, auth.uid() was verified server-side by supabase itself. with clerk JWTs, supabase is just verifying the signature and reading the claims. functionally the same security but it feels different because you're managing that trust boundary yourself instead of supabase handling it internally. it works well in practice. the ma

...[truncated]
	parasight reply to AlternativeInitial93: slop

Comment Tree 9:

jondonessa: Thanks for sharing. I have been wondering the supabase without its own auth system. Could you explain the migration process a little more, for example did you experience any downtime or other issue
	FinanceSenior9771 (OP) reply to jondonessa: no downtime but i did it in a single cutover since we were still early with few users. wouldn't recommend that approach if you have a lot of active sessions. the rough process was: set up clerk, configure the custom JWT template with the supabase tenant ID as a claim, update the supabase client to use the clerk token instead of supabase auth session, rewrite all RLS policies to check the JWT claim instead of auth.uid(), migrate the owner_user_id column from UUID to TEXT since clerk IDs are strings, then update every protected route on the backend to use clerk's middleware instead of supabase's gotrue helpers. the frontend was actually the easier part. clerk's react components (SignIn, SignUp, UserButton) are drop-in and look good out of the box. the backend was where most of the 44 file ch

...[truncated]

Comment Tree 10:

cryptomuc: Thanks for sharing. How did it work with passwords? Had all users to reset the passwords? Because if i understood it correntlcy, they are hashed with a salt that supabase cloud doesn't hand out. True/False?
	FinanceSenior9771 (OP) reply to cryptomuc: you're right, you can't migrate the password hashes from supabase to another provider. in my case i did the migration early enough that i only had a handful of users so i just created new accounts in clerk and had them set new passwords. not a real problem at my scale. if you have a lot of existing users you'd probably need to force a password reset for everyone or set up a transition period where both auth systems are active and you migrate users as they log in. neither option is great which is why doing this migration earlier is better than later.

Comment Tree 11:

leetgoat_dot_io: fire post thank you

Comment Tree 12:

arianebx: I moved away from supa auth for a better auth worker on cloudflare — so i really treat supabase as a hosted postgres (I dont use the built in deno edge function stuff either - i use cloudflare workers) I wanted modularity and avoiding vendor lock-in I have a rbac model for my users which is entirely not tied to auth, and this makes auth in general “just” be auth — because i really didnt want to have to find myself painted in a corner if i wanted to swap auth providers/framework It took a little bit of fiddling to get better auth on the edge to work well with the user table (in supabase as a regular table), but once i figured it out , it s been great
	FinanceSenior9771 (OP) reply to arianebx: yeah that's basically where i landed too. supabase as hosted postgres with a nice dashboard and RLS. the RBAC model decoupled from auth is the right call, wish i'd done that from the start. would've made the whole migration way less painful since the permission logic wouldn't have been tangled up with the auth provider. do you notice a speed difference doing auth on cloudflare workers vs a regular server? i've been curious about edge auth but haven't tried it.
		arianebx reply to FinanceSenior9771 (OP): yes, (though i have hyperdrive in front of the db which made better auth on the edge to supa go from 'truly noticeably long' to 'acceptable) but yes - compared to auth done within the same instance, there is a difference. it won't 'feel' too terrible to users. I just happen to know that it could be faster... still, really, worth it. Better auth drives 2 tables in its schema, and everything else belong to my app and the bff. I dont have to manage a ton of complex RLS because the bff is the only thing making calls to the DB. And if i wanted to move from supabase to a vps of a regular postgres tomorrow, it would be a very light operation (as God intended it)

Comment Tree 13:

R9dmT9g9t: Thanks for sharing, I actually tried a reverse migration from firebase to supabase and it didnt go so well. After realising I was losing the multitenant stuff and that my custom golang api gateway was far superior to GoTrue. I reverted back. I dont like vendor lockin like this and even though it could be argued that firebase is Google lockin in a way, the microservices/modular aspect of firebase it actually makes it easier and doesnt break stuff if I decide to use some features of firebase while keeping others. I can far easier replicate and simulate my local dev environment with production which leads to a far cleaner/smoother CI/CD pipeline, which also doesnt break if I decide to bolt and unbolt services and features. Making it more enterprise ready and on top of this firebase is cheaper

...[truncated]

Comment Tree 14:

raghavyuva: Thank you for sharing your insights. I encountered a similar scenario in my own work. My objective was to enable users to self-host my open source project with PostgreSQL. However, I aimed to avoid the use of Supabase as a highly restricted database, which led me to bypass its authentication features.

## Post 5

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/Intune
Title: Problem signing into client machines. Cloudonly machines.
Post URL: https://www.reddit.com/r/Intune/comments/1u3wt2e/problem_signing_into_client_machines_cloudonly

Body:

Problem Overview

Multiple users are experiencing issues when attempting to log in to their computers. The error message presented is:

"The sign-in method you're trying to use isn't allowed. For more information, contact your network administrator."

This occurs even though:

The password is correct (incorrect passwords produce the expected error message)

Login via browser (office.com) works as intended

Scope (company size 100-800 devices)

Initially reported for approximately 5–10 users

Later indications suggest the number may be 10-30 users

Affected users are located across different offices and networks, indicating it is unlikely to be a network-related issue.

Users has diffrent roles and computer models. New users old and old users.

Troubleshooting Performed
Verifications

User accounts work correctly via the web, suggesting no issue with the accounts themselves

AD synchronization appears to be functioning as expected

The issue affects users and devices randomly

Affected users are able to sign into other machines.

This error is not hitting any of our CA policies

Technical Observations

Device exports suggest that no groups are assigned rights to log in locally

Potential impact from local logon policies (e.g., "AllowLocalLogOn")

The security baseline indicates that local logon should be allowed for users and administrators

LAPS produces the same "prohibited" error

Local admin access has the same error.

Even though no policys has been changed in the past two weeks we've gone through them all, nothing indicates that the users shouldn't be able to sign in.

If a user writes the wrong password it says wrong password, when typing the correct one it says "The sign-in method you're trying to use isn't allowed. For more information, contact your network admi

...[truncated]

Score: 5
Comment count: 13

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "Windows Management",
  "author": "Luke_-_Starkiller",
  "final_url": "https://www.reddit.com/r/Intune/comments/1u3wt2e/problem_signing_into_client_machines_cloudonly/"
}
```

Loaded comment tree:

reported_comments: 13
loaded_comments: 13
included_comments: 13
top_level_comments: 7
max_comment_depth: 2

Comment Tree 1:

intuneisfun: I've dealt with this before, but it was self-inflicted by accident during testing and rollout of CIS policies. I can tell you with 100% sureness that the reason for the error is because of the local security policy on the device itself. On an affected device, open the Local Security Policy app and dig into Security Settings > Local Policies > User Rights Assignment. Then, look for the policies named "Allow log on locally" and "Deny log on locally". Look at the users or user groups listed in each setting. I guarantee that the users getting the error message are either not in a group that's allowed, or they're in a group that's denied. The question/issue then, is finding out where that setting is getting pushed from. I know you said cloud only, so that should be just Intune, SCCM (if co-mana

...[truncated]
	Luke_-_Starkiller (OP) reply to intuneisfun: Yeah im leaning towards this aswell, our IT partner has had 3 different people go through all the intunes policies and they can't find anything. If i look throguh the policy list, last one was changed 2026-06-01 so that's 11 days ago, and the problem started at around 09.00am today. Not saying it isn't but if it is a policy why today, why not any other day from the 1st to today. We have tried to gain access to one of the machines but we are unable to get remote access to them. All the affected users has been on the remote offices. But just before closing today 2 users reported the issue at the HQ so i will look into it on monday. I suspect the "Allow log on locally" and "Deny log on locally"aswell. Yeah the computers are cloud only, so they don't get any GPOs from the local AD, we only hav

...[truncated]
		intuneisfun reply to Luke_-_Starkiller (OP): Yeah to resolve it on some of mine, I had to use our remote access tool. Couldn't log in, but I could run a command shell on them with SYSTEM level access which was essential. If you don't have something like that, it could be tricky. Maybe a LAPS account could get in though, because it is likely in a different local user group (Administrators vs Users). Ran some powershell commands to export the security config (secedit.exe), modified it on another computer, then imported it back so the user could log in and get the "fixed" policy from Intune. I doubt it was something Microsoft pushed otherwise all the forums would be on fire.. but if you want to DM to review anything when you have more access next week feel free to shoot over a message or comment back!

Comment Tree 2:

mnjimn: We’ve had this intermittently lately as well, sometimes you wait a few minutes or restart a couple times and it resolves itself. Other times we remote in, login with LAPS creds then switch user to the affected user.
	Luke_-_Starkiller (OP) reply to mnjimn: The problem is that reboot doesn't work and we get the same error trying to sign in with the LAPS account.

Comment Tree 3:

Extension-Term-743: Pretty wild that it's spreading throughout the day like that - almost sounds like some kind of auth token or certificate issue propagating across your environment. The fact that LAPS is throwing the same error is particularly telling since that should bypass most user-level restrictions Have you checked if there's any certificate expiration happening today or recent changes to your tenant's token signing certs? Sometimes these auth failures can cascade when devices can't properly validate against Azure AD even though the web auth still works through different pathways
	Luke_-_Starkiller (OP) reply to Extension-Term-743: good point, looked into it and all certs looked fine. It's happeningn on machines that are deployed just 3-4 days ago. So that should also rule out the cert thing.

Comment Tree 4:

Pacers31Colts18: Check your User Rights policies. Access From the Network, Allow Local Logon, Deny Access From Network specifically.
	Luke_-_Starkiller (OP) reply to Pacers31Colts18: Yeah we havn't had access to any machines, but this will be the first.

Comment Tree 5:

TeramindTeam: check if u have any conditional access policies blocking legacy auth or enforcing specific signin methods for those users. sometimes a recent change there can trigger that error message even if the creds are fine. its a common headache when stuff just stops working suddenly
	Luke_-_Starkiller (OP) reply to TeramindTeam: Yeah we've been trhough the CA policies multiple times, nothing there. Nothing in the logs regarding the devices hitting CAs. and if it was a CA would it not hit all devices not 10-20 out of several hundred.

Comment Tree 6:

Avean: I've had this issue before but it was self-inflicted by trying to block a custom entra id group by adding them to Guests and then Deny local logon for Guests only. But for some reason this would evolve into blocking ALL users on the actual device. Whats worse is that the policy is sticky, so resolution was to push a policy for User Rights: Allow Local Log On: *S-1-5-32-544, *S-1-5-32-545 Which basicly is Administrators and Users. Can take up towards 1 hour for the policy to take effect but it works if you are ever have this issue. If even this doesnt work, you may have SeDenyInteractiveLogonRight set as well. This is basiscly a powershell script to reset the security database if all fails. $Path = "C:\Windows\Temp\fix-logon-rights.inf" $Db = "C:\Windows\Temp\fix-logon-rights.sdb" $Log = "C

...[truncated]

Comment Tree 7:

EntraGlobalAdmin: There is only one way to find out. Please upload your SYSTEM and SECURITY event logs of any affected machine to an LMM. If you need to extract them, use WinPE to open the event log, use the Bitlocker key from Entra to unlock the drive, then store the events in a CSV file and upload them to your LMM.

## Post 6

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/nocode
Title: Ideas on The Best No Code platform to build a Client Portal with 2,000+ records & payment processing?
Post URL: https://www.reddit.com/r/nocode/comments/1cgtidi/ideas_on_the_best_no_code_platform_to_build_a

Body:

Looking to build a college tennis recruiting portal that helps recruits track interactions with coaches & has a bunch of preloaded stats/information on thousands of schools. Any ideas on what I can use to accomplish this?

Score: 9
Comment count: 36

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "Question",
  "author": "krymany11",
  "final_url": "https://www.reddit.com/r/nocode/comments/1cgtidi/ideas_on_the_best_no_code_platform_to_build_a/"
}
```

Loaded comment tree:

reported_comments: 36
loaded_comments: 32
included_comments: 30
top_level_comments: 18
max_comment_depth: 6

Comment Tree 1:

Travel-craze: I ran into a similar challenge when I set up a membership portal for 800+ student athletes earlier this year. After testing Glide and Bubble, I settled on Softr once their Native Database rolled out. The database handles a few thousand rows without the lag I used to see in Airtable and the security part is automatically in the actual app. that with Make for updating records made it super easy for class sign ups/ payment tracking.

Comment Tree 2:

UK363: Bubble.io is a great fit. You're probably not going to use any backend flows so you won't be spending a lot on cost. Whether you want a separate backend/database like Xano or Supabase is your choice but if there's no complex database operations and no need for scheduled flows or stuff like that and you your records are not going over 10 thousands you're probably great with only bubble. Apart from a web app, you can even have a PWA or wrap it into a native mobile app and it'll still perform good. Can suggest and advice more if you got some specific features and functionalities, feel free to DM me.
	krymany11 (OP) reply to UK363: Will do. Thanks
		UK363 reply to krymany11 (OP): You’re welcome!
			krymany11 (OP) reply to UK363: Any other platform suggestions besides Bubble?
				UK363 reply to krymany11 (OP): Give WebFlow a try. I’ve been hearing about Adalo but haven’t built or seen it’s potential. Btw, why not bubble? Any specific reason?
					damonous reply to UK363: I wouldn't suggest WebFlow for this. I find it difficult to build out web apps with it. It's better as a website builder. Maybe take a look at WeWeb or FlutterFlow (if mobile only)
						UK363 reply to damonous: Ah yes I meant to suggest WebFlow lol it’s just that I get all mixed up in WebFlow, Web, and one other lol
				Nocode4life reply to krymany11 (OP): Depends on how many users you want. If this is more about building the app, and less about having thousands of users, then Softr could be a great, easy to learn option... But if your app is meant to have thousands of users, it wouldn't work well... Bubble would, but again, big learning curve.
	Nocode4life reply to UK363: Yes, it could be. Will just take too long for a beginner to do all of this IMO.
		UK363 reply to Nocode4life: For a beginner yes maybe. But if you’re a fast learner i think a month is enough anyway with low code.

Comment Tree 3:

kiterdave0: Do this in Knack, half day max. Start here: https://www.knack.com/r/knack-signup-link

Comment Tree 4:

[deleted]: Has anyone used Ninox Database before? I pretty much have this built in there, but no way offer it as a product to a potential customer.
	krymany11 (OP) reply to [deleted]: Has anyone used Ninox Database before? I pretty much have this built in there, but no way offer it as a product to a potential customer.

Comment Tree 5:

bubble__man: Bubble is great for this! I have a few samples of similar apps with the features you mentioned that Ive mafde. happy to show you their functioning to help you make the decision. Feel free to dm

Comment Tree 6:

helium66: Would give a look at Appfarm.io too!

Comment Tree 7:

[deleted]: Thanks. Unfortunately need more than 2,000 records and the next price point is too steep atm
	krymany11 (OP) reply to [deleted]: Thanks. Unfortunately need more than 2,000 records and the next price point is too steep atm
		NolocoHQ reply to krymany11 (OP): For what it's worth, you can get started with a 30-day trial of any of our larger plans if you want to see how it would work for more than 2,000 records

Comment Tree 8:

Blaze-tech: Blaze.tech can do this. We have a lot of customers with client portals with payment processing. Happy to help if interested. All the best with your project!
	krymany11 (OP) reply to Blaze-tech: Thanks. $400 per month wow

Comment Tree 9:

[deleted]: I agree with you here. Softr is really good for Client Portals!
	Warm_Archer5250 reply to [deleted]: I agree with you here. Softr is really good for Client Portals!

Comment Tree 10:

techsin101: what does this do? Recruits.. you mean recruiters.. why does preloaded information matter?

Comment Tree 11:

Public_Flounder6419: Hey if your using SalesForce, Titan is probably your best bet, drop me a message and I can tell you more

Comment Tree 12:

jessicalacy10: If you're trying to build a client style web app that handles a ton of records and payments, Knack is honestly one of the best places to start. It's built for data heavy stuff, you can create custom databases, use portals and dashboards without touching code. It handles big datasets smoothly, lets you set up different user roles and connects easily with payment options like stripe and paypal. It's great if you want something that feels like a real app (not just a pretty website ) and you can get your MVP live pretty fast without messing around with backend setup. Bubble is great if you need tons of flexibility or complex workflows, but it can slow down with big data sets. For what you're describing, lots of records and payments features, Knack really hits the sweet spot between power and s

...[truncated]

Comment Tree 13:

Warm_Archer5250: Have you looked into Softr? It's pretty solid for client portals with that many records. The user management is built-in which saves tons of headache, and it handles payment processing through Stripe integration. What's your timeline looking like for getting this up and running?

Comment Tree 14:

Coffee-tea3004: I’ve been using MGX as an AI dev team on top to vibe-code the portal logic, let deep research map out competing products and race mode generate a few dashboard layouts to pick from.

Comment Tree 15:

Separate-Web-1398: For a site with 2000+ records and payments, you have a few good options. Softr is one of the most powerful if you need a clean client portal. It can handle large datasets, user accounts, roles, payments, and now has its own databases (or you can still use Airtable if you want). If you need a mobile app-like experience, Glide can also be a good option, but be aware of their record limits. I’m curious as to which features are most important to you: tracking, school database, or payments?

Comment Tree 16:

EntropicMonkeys: For a portal with thousands of records plus payment processing, you’re going to want something that’s good with data, handles user accounts cleanly, and won’t choke once you get past a few hundred rows. A few solid options: Softr is probably the easiest way to build a polished client portal without touching code. Works well with Airtable and external DBs, handles user accounts, roles, payments, and can display large datasets with filters. Good for this kind of research and tracking portal. WeWeb w/ Xano as db is more flexible and more scalable if you expect this to get big. WeWeb for the front end, Xano as the backend/database. More setup than Softr, but better long-term if you need custom logic or advanced filtering. Bubble can do everything, but it’s slower to build and has a steeper lea

...[truncated]

## Post 7

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/vibecoding
Title: How are you adding security to your vibe coded apps?
Post URL: https://www.reddit.com/r/vibecoding/comments/1r4d79n/how_are_you_adding_security_to_your_vibe_coded

Body:

Hey guys, just wanted to know how are you adding security to your vibe coded apps since we know vibe coded apps are vulnerable with very less security to it? Let me know if you use any tools or tips

Edit: guys I'm a full stack developer. Currently most of the AIs seem to miss out the edge cases, like for example with handling concurrent transactions etc. I use such tools to fasten up my work and handle such issues manually

Score: 41
Comment count: 60

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "",
  "author": "Anonymous03275",
  "final_url": "https://www.reddit.com/r/vibecoding/comments/1r4d79n/how_are_you_adding_security_to_your_vibe_coded/"
}
```

Loaded comment tree:

reported_comments: 60
loaded_comments: 50
included_comments: 30
top_level_comments: 37
max_comment_depth: 2

Comment Tree 1:

Horror_Brother67: "be secure, make no mistakes. Thank you"
	Stibi reply to Horror_Brother67: This but unironically
	StevenSafakDotCom reply to Horror_Brother67: 🤣🤣🤣🤣🤣
	Better-Prompt3628 reply to Horror_Brother67: You forgot the "please" part 🤣

Comment Tree 2:

Any-Main-3866: I treat all AI generated auth, validation, and RBAC as drafts. I rewrite or review anything that touches authentication, roles, payments, and similar areas. I also add server side validation to check again. I use proven auth providers like Supabase Auth, Firebase, and I add rate limiting and basic logging early in the app.

Comment Tree 3:

sreekanth850: Some things that i implemented. Tenant-Specific Signing Keys (Asymmetric): Each tenant has its own RSA-2048 signing key for JWT token generation, ensuring cryptographic isolation where tokens issued for one tenant cannot be validated using another tenant's public key Authentication Architecture: OpenIddict OAuth 2.0/OIDC Server with custom tenant-specific signing keys that rotate the key pair every 7 days. this is for signing keys not JWT itself. Access token + refresh token. With access token expiring at 15 minutes. Authorization and Permission system: 3 layer permissions with Role user and Openiddict Client to make API permission granular. Key Management Security: Encrypted private key storage with master encryption key stored at Infisical. Middleware Security Pipeline Order: Use Authent

...[truncated]
	614c49457a reply to sreekanth850: Not sure why this was downvoted, great content.
		sreekanth850 reply to 614c49457a: May be vibecoders doesn't understand this. Forget to say that it has zero cloud dependency. I deploy it using a systemd with dns level load balancing (Entire dta plane is statless and ephemeral). App is mainly into WebSocket infra for collaboration. We had separate control plan for token issue and data plane for WebSocket implemented using hocupocus and fastify.

Comment Tree 4:

Existing_Bird_9090: 'Make it non-hackable' /s

Comment Tree 5:

MediumRedMetallic: If you’re using version control, run your app through Claude’s Security Review GitHub Actions on your pull requests. It will generate extensive feedback on OWASP top 10 vulnerabilities, recommend corrections and show you things your app does well. You can make additional commits with fixes to trigger review scopes down to just the new commits. If you’re not using version control, set it up. It’s 20252026. Development without version control is asking for pain.
	tidoo420 reply to MediumRedMetallic: Bro its 2026 dafaq is wrong with you
	BusEquivalent9605 reply to MediumRedMetallic: (empty comment)

Comment Tree 6:

farhadnawab: this is a real concern as we move faster with ai. the best way i’ve found is to not "vibe" the security parts. use battle-tested infra like supabase or clerk for auth/db rules so you aren't building those from scratch. also, once you have a feature working, specifically ask the ai: "act as a senior security engineer and find vulnerabilities in this specific code block." it’s much better at finding holes than it is at proactively writing secure code on the first try.

Comment Tree 7:

[deleted]: "make this shit secure" x10

Comment Tree 8:

working_beyond_2021: Hi, so I use built in checks in a lot of the vibe coding tools (like Lovable, Replit, etc.) - additionally I check for API keys, row level security of the database and have a risk check: What would happen if someone accesses some kind of data? What kind of data is that? Maybe it should be encrypted and in an even more secure area (dedicated database that has a dedicated connection). Hope that helps!

Comment Tree 9:

Nisam_robot: Not much needed if u use already made software and implement it right way Sec headers rate limiting sanitization dos prevention etc.. should be as your standard when building apps or websites if you dont do basics its on you it is expected of you to do basic sec stuff when going into production so nobody should even mention this to you but alot of noobs dont know it and don't implement basics into apps when vibecoding bcs ai won't do it by default for you of course
	[deleted] reply to Nisam_robot: Your mom did. And you now...
		Nisam_robot reply to [deleted]: Your mom did. And you now...

Comment Tree 10:

completelypositive: Lol

Comment Tree 11:

Adventurous_Till4661: You don't add security, you design it in from the start. If you aren't designing with security in the service as a first class concern then you're doing it wrong, however you create the code.

Comment Tree 12:

wally659: It's not really responsible or realistic to attempt to make vibe coded tech "secure". Or idk, maybe you've got a different definition of vibe coding. But to me, if you don't know exactly what's making it secure, it's not. And if you know exactly what's making it secure, it's not vibe coded because you have to fully understand and probably manually author those parts of the code.

Comment Tree 13:

EnvironmentalLayer72: Create a checklist/safety protocol you can follow -rate limits -row level security -CAPTCHA on auth + forms -serves-side validation -gitignore -JWT with short expiry + refresh tokens -At-rest encryption -logging -env vars set -CORS restriction -dependency audit -CSRF protection And there is a lot more. All depend on what you doing/need

Comment Tree 14:

Difficult-Two-8279: Claude is this ready for production?

Comment Tree 15:

JW9K: Check for vulnerabilities, no em dashes.

Comment Tree 16:

EliHusky: Build a roadmap of what security will look like on your platform (yeah you’re gonna have to put time into this) then go step by step with ChatGPT and see if it can find researchers/businesses that already did that specific step and build a thorough action plan with references/repo links. Then build it with Claude, and have ChatGPT double check and look for bugs. GPT and Claude have very different ways of analyzing scripts, it almost like they trained GPT to debug Claude’s work. then all that is left is paying $5k for an ethical hacker and then another $40k for a team to rebuild your entire system. Good luck!

Comment Tree 17:

Inside_Session101: Claude > find me security loopholes bugs errors etc, I am sure you cant , I challenge you to find me a single and I will buy another month of claude subscription.

Comment Tree 18:

ef4: I can’t overemphasize how screwed you are if you think of security as something that can be “added”. It’s not a feature, it’s a property that needs to be maintained by every single piece of the system.

Comment Tree 19:

Terrible_Tangelo6064: Yo Claude make secure gooder

Comment Tree 20:

TriggerHydrant: Come on Claude, make this very securely secure pls! In all fairness: I have a bunch of methods and I mostly follow what other experiences devs do and let Claude explain to me why they do that and how we can implement it.

Comment Tree 21:

oh_jaimito: I used Claude Opus 4.5 a few months ago for a big project. An auto enthusiast "social network". Nuxt, capacitor, convex, R2, clerk. The app is deployed, but I never shared it. I knew it wasn't ready. Then had the idea of using Codex and Gemini (both CLI) to fully audit the code base and each wrote a report to audit-by-gemini/codex.md. Gemini report was over 800 lines. Codex was about 150. Both covered critical issues, but Gemini was extremely detailed, even mentioning filenames and line numbers. Codex would just say what function. Both did well with explaining their reasoning. Still on 4.5 I gave Claude Code the audit markdowns. It went through and made all the fixes. While I like Gemini for its massive context usage, it is slow. Opus 4.6 dropped. New Codex version dropped. I repeated the

...[truncated]

## Post 8

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/AZURE
Title: Front Door or Application Gateway?
Post URL: https://www.reddit.com/r/AZURE/comments/1tq10w6/front_door_or_application_gateway

Body:

Hello!

We have some internal applications that are hosted in an Azure App Service Environment (Isolated SKU, no public access) and our user base accesses them by connecting to a VPN hosted on a Fortinet firewall (using FortiClient).

I wonder whether now is the time to move away from the VPN and make these apps available (securely) by using either Azure Front Door or Application Gateway. I would want them to only be accessible to users that authenticate in Entra ID (with MFA, of course, presumably enforced using Conditional Access Policies).

Has anybody else done this, and can you offer any practical advice or thoughts on which you used and how successful it was? Any gotchas or regrets? Or any different solutions entirely?

Thanks in advance :)

Score: 25
Comment count: 31

Media:

```json
{
  "post_type": "text",
  "media_urls": [],
  "outbound_url": "",
  "flair": "Discussion",
  "author": "dai_webb",
  "final_url": "https://www.reddit.com/r/AZURE/comments/1tq10w6/front_door_or_application_gateway/"
}
```

Loaded comment tree:

reported_comments: 31
loaded_comments: 29
included_comments: 29
top_level_comments: 16
max_comment_depth: 3

Comment Tree 1:

jdanton14: Microsoft MVP
	dai_webb (OP) reply to jdanton14: Systems Administrator
		-Akos- reply to dai_webb (OP): Cloud Architect
			Snowy32 reply to -Akos-: DevOps Engineer

Comment Tree 2:

rschoneman: If they’re web apps why not use azure app proxy? Most Entra license tiers include it free.
	techb00mer reply to rschoneman: Was going to suggest this as well. It’s pretty darn good at doing exactly what OP is after.
	wubalubadubdub55 reply to rschoneman: That sounds like Cloudflare tunnels. Is that correct?
		rschoneman reply to wubalubadubdub55: Yes similar. No client needed though.

Comment Tree 3:

jba1224a: Cloud Administrator

Comment Tree 4:

AdmRL_: But... why? Yeah you can do it, but why would you? Are you planning on being a remote-only business with BYOD? That might be an argument for it as VPN may not be supported by every OS and every version, so shifting from a client requirement to clientless has clear and obvious benefits. But otherwise there's literally no reason to. VPN + corp device + private link setup is the least friction most hands off access pattern. App gw adds non-trivial admin overheads, backend pool monitoring, WAF config and a load of other stuff, if your apps are novel code then you're going to have to do testing to ensure they're secure over the internet. Same story for Front Door. Plus if you're already using a fortinent FW and that's your only ingress point, you're now introducing a second ingress point so dou

...[truncated]
	NUTTA_BUSTAH reply to AdmRL_: Thousand times this. I like analogies, and the first thing that came to my mind is that OP now has a safe in their office with the code known only by select personnel, and is wondering if they should move the safe outside to the street.
		gyarbij reply to NUTTA_BUSTAH: Cybersecurity Architect

Comment Tree 5:

mat-ferland: I wouldn’t frame Front Door/App Gateway as the VPN replacement. Put Entra Private Access/ZTNA in the access lane first, then use AppGW/Front Door for routing and WAF where the app exposure model actually needs it.

Comment Tree 6:

Altan013: Enable private access only on the App Service and put an AppGw in front. For authentication you could use the built-in authentication options of an App Service that can utilize OpenID. Or Entra App Proxy.

Comment Tree 7:

Over_Function_1884: I’d separate publishing from authentication. Front Door/App Gateway can protect and route HTTP traffic, but they don’t magically replace the identity layer. If the goal is VPN-less access with Entra ID + MFA, I’d first look at Entra App Proxy / Private Access or app-level Entra auth. Use Front Door Premium + Private Link if you need global edge/WAF/private origin. Use App Gateway if this is mostly regional/internal and you want more VNet-level control. Biggest gotchas: DNS, headers, health probes, private endpoints, and blocking any direct origin bypass.

Comment Tree 8:

hardcorepr4wn: If your UX is ‘I have internet’ then this is a valid question.And I work in a regulated industry. You should provide authentication, and verify access up front. Either can do this. What fits your need? FD adds global resolution, which is niche, so probably Appgw.

Comment Tree 9:

SkybertNO: I mostly lean towards Frontdoor due to the certificate handling. It handles all that and issues them itself, AG needs it from a KV or similar
	kolbasz_ reply to SkybertNO: But if you manage your own certificates, fd still needs it from a kv, no?
		joelby37 reply to kolbasz_: AFD can automatically provision Azure-managed certificates too.
			kolbasz_ reply to joelby37: Sure but what if you want to manage via your own auth. That’s all. Just both options are available, sure the one simplifies life.
	Rodri-in-the-Green reply to SkybertNO: This.

Comment Tree 10:

skiitifyoucan: The question is what are you accomplishing , or trying to accomplish by doing this? I would say leave it alone. Don't make something simple that already works more complicated than it needs to be. Unless you are leaving out some detail for why it should be publicly accessible... or needs a waf in front even though it is internal only?

Comment Tree 11:

bigscankin: IMO I would leave the current solution as it is, and introduce conditional access policies to protect your app with MFA (This would require Entra P2 licensing) Front door and App Gateway are layer 7 load balancers, in your current use case I don’t actually think you need any of the functionality which they provide. If however you were looking to make the application multi-region, wanted to take advantage of CDN capabilities or wanted SSL offloading then Frontdoor is your answer. If you were looking for a single region and wanted to load balance across multiple instances, then App Gateway. I think introducing a layer of complexity to a fairly simple application is just going to add maintenance overhead and increase your Azure spend for no real benefit to the end user or the system.

Comment Tree 12:

moccolfc: Cloud Architect

Comment Tree 13:

Potential_Mix_519: You can use Global Secure Access (which is a per-user license) or an Azure web proxy. I added the Azure Proxy web app to my user Office portal. When the user authenticated in the portal (https://outlook.cloud.microsoft/), they were required to complete MFA, which was enforced using Conditional Access policies and then have then access to internal app.

Comment Tree 14:

Guywithacamera8: Front Door is global and allows you to go multiregion later.

Comment Tree 15:

rexthod: Whitelist IPs if you know the sources of the people that need to access and and a extra layer, add a app registration Linked to the group of users that can login and config the easy auth callback to the app registration to add the MFA

Comment Tree 16:

Nusuthoid: Sounds like a good plan. Granted, you are exposing your apps to public Internet, but if you do region-specific or CIDR based IP filtering, you can massively reduce number of IPs that can access your apps. As you already said, you have to pay special attention to identity-based protection. I'd certainly go with WAF to further protect workloads from SQL injection and other types of attacks that OWASP detects. It takes a bit of time to iron out exemptions and custom rules, but after that you should be golden. Exposing apps over L7 load balancer with WAF is a standard way to do app publishing, and it can even be good for limited audience, as is your scenario. Decision between AFD and AppGW will largely rely on amount of traffic you expect and specific differences between resources that better

...[truncated]
	dai_webb (OP) reply to Nusuthoid: Systems Administrator

## Post 9

Below is the detailed Reddit post content and the currently loaded comment tree.
Subreddit: r/devsecops
Title: RedAccess scanned 380,000 publicly accessible vibe-coded apps and found 2,000+ leaking corporate data with no auth — how are you handling this in your org?
Post URL: https://www.reddit.com/r/devsecops/comments/1trq4mb/redaccess_scanned_380000_publicly_accessible

Body:

RedAccess just published the Shadow Builders report (covered by WIRED, THN, VentureBeat this week), and the numbers are genuinely harder to dismiss than I expected.

**What they found:**
- 380,000 publicly accessible web assets across major vibe-coding platforms (Lovable, Bolt, Cursor etc)
- ~5,000 appeared to be built for corporate use
- 2,000+ of those were exposing sensitive data — clinical trial records, financial data, shipping manifests, customer PII — to anyone with the URL
- No credentials required. Passive scan only.

**The structural problem they're flagging:**

This isn't old Shadow IT (buying Trello on a corporate card). These apps are custom-built, directly integrated with CRM/ERP/BI production systems, and published externally. They don't exist in any CMDB, don't show up in vuln scanners, and the employees building them don't know they're creating a security surface. CVE-2025-48757 documented Supabase RLS being skipped in Lovable-generated apps — 170+ production systems affected.

**My question for the community:**

How are your orgs actually handling vibe-coded app governance? I'm seeing a few approaches floated — browser-layer DLP, mandatory pre-deployment checklists, procurement gating — but nothing that feels like consensus yet.

Also curious if anyone's run a passive scan of their own org's public web footprint specifically looking for AI platform subdomains. RedAccess did it at scale; you can probably do a rough version with shodan or similar.

I previously covered the Megalodon GitHub Actions supply chain attack — same underlying pattern of developer tooling moving faster than security governance — here if you want background on the CI/CD layer angle: https://www.techgines.com/post/megalodon-github-actions-supply-chain-attack-safedep-2026

Full writ

...[truncated]

Score: 5
Comment count: 1

Media:

```json
{
  "post_type": "multi_media",
  "media_urls": [],
  "outbound_url": "https://www.techgines.com/post/megalodon-github-actions-supply-chain-attack-safedep-2026",
  "flair": "",
  "author": "Expert_Sort7434",
  "final_url": "https://www.reddit.com/r/devsecops/comments/1trq4mb/redaccess_scanned_380000_publicly_accessible/"
}
```

Loaded comment tree:

No loaded comment content available.
