## Title Candidates

1. How are you handling AI coding agents that want to deploy to your clusters?
2. Letting Claude Code push to prod from the terminal, how are you scoping its permissions?
3. AI coding agent + kubectl from the terminal, what does your audit trail actually look like?
4. How do you stop an AI coding agent from going full shadow IT on your K8s cluster?
5. Terminal-driven AI deployments on K8s, what does the permission boundary look like for you?
6. Running 3 AI agents from the terminal, here's how I keep them from owning the kubeconfig
7. Letting an AI coding agent deploy from my terminal for 2 months, here's what scared me
8. AI agent deploying from the terminal, how are you handling the RBAC gap?
9. Stop giving your AI agent the kubeconfig, what actually worked for you?
10. Anyone else scared to give their local AI agent deployment access?

## Final Post

curious how other folks in this sub are handling this one.

we let our devs use Claude Code and Cursor in the terminal to write code, and the code itself is fine. the part that keeps me up at night is what happens when the agent wants to push it somewhere.

right now the agent basically has three paths:

1. **gets handed a kubeconfig** and runs `kubectl apply` like a CI pipeline would. no way to tell in the audit logs if that rollout was triggered by a human or by an agent. same broad RBAC either way.

2. **bypasses the cluster entirely** and deploys to Vercel or Railway because its just easier. now you have shadow IT inside a K8s-first org, and good luck explaining to security why prod is split across three runtimes. we've already had one team drift this way.

3. **files a ticket** and waits for the platform team. at which point the "AI speed advantage" is gone.

K8s RBAC really wasnt designed with "this action was initiated by an agent on behalf of user X" in mind. there's no native way to tag it, most admission controllers don't have policies for it, and the audit trail cant distinguish agent from human. that's the part that keeps biting us.

things we've tried or looked at:

- **scoped service accounts per agent session** with short-lived tokens. works in theory, but provisioning and revoking is annoying and we ended up writing custom tooling for it.
- **OPA/Gatekeeper policies** that tag agent-initiated requests differently. possible, but it means custom admission webhooks, and maintaining those isnt free.
- **GitOps (ArgoCD/Flux) with PR-based approval.** agent pushes manifests, a human reviews the PR, ArgoCD syncs. cleanest story, but the "who opened this PR and should it auto-merge" question just shifts to the git layer.
- **an API layer in front of the cluster** that handles auth, RBAC, and audit, and only exposes specific commands to the local agent. Enter CLI does roughly this, it only exposes `build` / `edit` / `publish` / `domain` style commands so Claude Code never gets raw cluster creds. less to wire up than the custom OPA route.

for teams not already on ArgoCD, the API layer route seems like the path of least resistance. for teams deep in GitOps, the PR review pattern is probably the right answer.

anyone running the scoped-service-account thing in prod, or is it really just GitOps and a prayer for most of you.

(disclosure: I work on Enter, so yeah, biased toward that last option.)

---

## Comment Trees

**Tree 1: The GitOps Purist**

old_k8s_hand: GitOps with PR review. its the only one that scales. once you have 10+ devs and their agents all pushing manifests, you need that git layer as the source of truth and a human eyeball on the diff.

devops_dan reply to old_k8s_hand: agreed but the PR review bottleneck just moves. we tried this and our platform team became the merge queue. ended up writing custom auto-merge policies per agent which felt worse than the original problem lol

enter_dev reply to devops_dan: did you scope the auto-merge policies per agent identity, or per repo? curious because we ran into the same merge queue issue and the GitOps-with-approval answer kept breaking down at scale

**Tree 2: The Skeptical Cluster Defender**

paranoid_sre: tbh none of this matters if the agent can still read your secrets. ive seen too many agents dump entire env files into prompts. api layer in front of the cluster is cute but if Claude Code can read your .env it owns you regardless

cli_lover reply to paranoid_sre: this is why i ran everything through dev containers for a while. contained the blast radius. devcontainer-mcp was a lifesaver until the team refused to onboard lol

enter_dev reply to cli_lover: yeah container isolation helps on the host side. on the deploy side we tried to keep it tight by only letting the agent hit build/publish endpoints rather than raw infra commands. still doesnt solve every leak path but narrows it

**Tree 3: The OPA Nerd**

policy_nerd: OPA/Gatekeeper route is underrated but you have to commit to maintaining the rego. one of our teams wrote a nice admission webhook that tags requests with an `agent-id` label and forces extra policy checks. broke in 3 months because nobody owned the rego

senior_platform_eng reply to policy_nerd: this is the part nobody talks about with OPA. the day-2 cost is brutal. we ended up ripping ours out and going with a thin api layer because we didnt have the bandwidth to babysit admission webhooks

**Tree 4: The Enterprise Contrarian**

enterprise_dave: for big orgs this whole thread is kind of academic. your CISO is going to demand an audit log that clearly labels agent vs human, period. half of these approaches cant actually produce that on demand

enter_dev reply to enterprise_dave: yeah fair, the audit log separation is the hardest part. we tried to thread that by having the api layer emit its own structured events with agent identity baked in. not perfect but its queryable

**Tree 5: The Solo Builder**

solo_builder_fr: coming from a 1 person company perspective, the kubeconfig path is honestly fine for me. i am the only human and the only agent. the moment i hire a second person tho this whole thread becomes my problem

enter_dev reply to solo_builder_fr: yeah solo is the easy mode. the problem compounds fast tho, like 3 devs with 3 agents pushing in parallel is where the permission model starts creaking

## Standalone Comments

cant believe this is still such a mess in 2026

we ended up on argocd + a strict pr template that requires the agent to fill in its own session id in the manifest. not perfect but at least its queryable later

lol at "GitOps and a prayer" real

the real question is what happens when the agent wants to deploy a database migration. that is the path that scares me

saved this, exactly what we are dealing with right now

curious if anyone has tried binding this to SPIFFE/SPIRE identities for the agent. feels like the right primitive but the integration story with most build platforms is nonexistent

honestly the shadow IT path is what ive seen most often. devs just go to vercel because the platform team is slow and then security has a meltdown 6 months later

fr the scoped service account thing sounds nice in a doc but the revocation story is a nightmare in practice. we tried and ended up with zombie tokens

how does Enter CLI handle rollback specifically. like if the agent publishes a bad build is there a one-liner to roll back or is it full redeploy
