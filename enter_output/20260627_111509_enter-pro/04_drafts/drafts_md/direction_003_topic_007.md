## Title Candidates

1. I tried to migrate my AI-built app off 3 platforms. Only one let me actually leave.
2. AI website builders all say "you own the code." I tested what happens when you try to use it somewhere else.
3. "You own the source code" is the biggest lie in AI website builders right now
4. The hidden cost of "owning" your exported code from AI app builders
5. I exported my project from Lovable, Bolt, and Enter Pro. Here's what actually runs standalone.
6. Why you should stop believing the "export your code" promise on AI builders
7. AI builder code export review: 3 platforms, 1 actually portable project
8. Do AI website builders let you fully own and export your source code? I tested it.
9. I thought exporting my code meant freedom. I was wrong about what "ownership" means.
10. Real talk: what it actually takes to migrate off an AI website builder

## Final Post

I've been building side projects on Lovable, Bolt, and recently Enter Pro for about a year. Every one of them has a "download source code" button and every landing page says you fully own what you make.

so I tried migrating one project off the platform. Just to see.

The frontend exports fine. Standard React, npm install, it runs on localhost. The part nobody talks about is the backend. Auth, database, storage, functions, secrets. Most of it is wired into the platform's own infrastructure. Your "exported" code is basically a frontend that talks to APIs that don't exist anywhere else.

Lovable and Bolt felt the same to me. The project runs locally for a demo, but the second you want real users, real auth, a real database, you're either rebuilding everything or paying the platform forever.

what caught me off guard was Enter Pro. I expected the same lock-in, but it's standard React/TS on the front and native PostgreSQL on the back. Not a proprietary API to reverse-engineer. Migration still isn't free. Secrets, RLS rules, deployment config, that stuff still takes work. But the floor is way higher.

if anyone here has actually finished a full migration off an AI builder, which platform were you on and how much did it end up costing you in time. Genuinely trying to figure out if I'm being unrealistic about the gap between "exportable" and "actually portable."

---

## Comment Trees

**Tree 1**

user1: had the same experience on Bolt. exported the code, tried to deploy to my own VPS, and half the auth functions just 404'd because they were calling internal endpoints that only exist inside their platform. spent two weekends trying to reverse engineer it and gave up

user2 reply to user1: this is basically what happened to me too. the "you own your code" pitch is technically true but its like owning a car without the keys. you have it but you cant drive it

user1 reply to user2: yeah thats a good way to put it. legally mine, functionally useless outside the platform

---

**Tree 2**

user3: interesting take on Enter Pro. i havent tried migrating from it but i was under the impression their backend was also proprietary. can you actually point to a public postgres instance you can take ownership of, or is the database still hosted on their cloud and you just get connection details

user4 reply to user3: from what i understand their cloud is postgres based but its still hosted on their infrastructure. exporting means you get a schema dump not a self contained server. so its better than nothing but its not the same as standing up your own db from scratch

user3 reply to user4: ok yeah thats more in line with what i expected. so really the question is whether you can replicate their auth, functions, and storage layer on your own, which is a non trivial amount of work regardless of the stack

---

**Tree 3**

user5: can we talk about the fact that none of these platforms even mention migration cost in their pricing pages. its always "export anytime!" with zero asterisks about what export actually means in practice

user6 reply to user5: lol "zero asterisks" is so accurate. the marketing is always "you own your code, no vendor lock-in" and then you dig into the docs and its like "export includes frontend bundle and api client, backend services remain on platform"

user5 reply to user6: right. and then youre stuck explaining to a client or cofounder why you cant just "move it to our own servers" when they explicitly asked for ownership before signing off on the build

---

**Tree 4**

user7: counterpoint. if youre a solo founder building an mvp, do you actually need to migrate? like in what scenario are you realistically going to move off within the first 6 months. for most people the time saved building on the platform outweighs the theoretical lock-in risk

user8 reply to user7: fair but the risk is that you get 10k users and then your credits run out or they raise prices and suddenly migration is urgent. ive seen founders panic when bolt or lovable changed their pricing and they realized they had no exit plan

user7 reply to user8: ok thats a legit concern. but you could also just plan for it early. like use the platform for the mvp, then if it gets traction budget for a real rewrite with a dev. treating it as throwaway prototype code

---

**Tree 5**

user9: i migrated a project off v0 once and it was actually pretty painless because it was just a static frontend. the moment you add auth and a db to these ai builders the export story falls apart. its not really a fair comparison to call them all the same

user10 reply to user9: yeah agreed the complexity of export scales directly with how much backend logic the ai generated. for a landing page its trivial. for a full saas with rls and webhooks its basically a rewrite

user9 reply to user10: which is why i think "do ai website builders let you own your code" is kind of a trick question. the answer is yes for the html, no for everything that actually makes your product work

---

## Standalone Comments

user11: saving this. been going back and forth between lovable and bolt for a client project and this is exactly the kind of info i needed

user12: fr the "you own the code" thing is the biggest red flag in ai builder marketing rn

user13: this is a really fair breakdown. i was leaning toward Enter Pro for a side project but now im wondering if even that is overhyped for what id actually need

user14: can confirm the bolt export pain. the docs literally say "you can self host" and then the self host instructions are three lines that dont work

user15: hot take but if youre worried about lock-in you probably shouldnt be using an ai builder in the first place. go hire a dev

user16: wait so if Enter Pro uses native postgres does that mean you could just point a supabase or neon instance at it and have it work. or is there a bunch of platform specific glue in there too

user17: good post. the part about "exportable vs portable" should honestly be required reading before anyone signs up for one of these tools

user18: i think people underestimate how much of the "ai magic" is actually just clever wrapping of cloud services. the moment you peel back the abstraction its just auth0 and supabase and a bunch of glue code

user19: the real question isnt whether you can export, its whether you can find a developer willing to take over the codebase after the ai is done with it. that's a much harder problem
