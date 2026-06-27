# Topic Planning Eval

Use after `reddit-topic-planning` creates or revises `02_topic_plan/topic_plan.md`.

Threshold: 85/100.

## Hard Gates

Fail if any gate fails.

| Gate | Pass Standard |
| --- | --- |
| Required fields | Every topic has content type, narrative, materials/research, brand exposure, target communities, search intent, reason, product facts, and risk notes. |
| Product-fit | Every topic is grounded in at least one verified or client-provided product fact. |
| Reddit-fit | Every topic is a discussion/story/question/teardown/troubleshooting angle, not a direct ad. |
| Distinctness | Topics are not minor rewrites of the same angle. |
| Feishu handoff | A Feishu doc exists, or creation is explicitly marked blocked with a reason. |

## Weighted Rubric

| Criterion | Weight | Scoring Notes |
| --- | ---: | --- |
| User pain specificity | 15 | Starts from a real situation, constraint, or frustration. |
| Narrative strength | 15 | Has a plausible story arc or discussion mechanism. |
| Search-intent value | 15 | Can naturally produce long-tail Reddit searches. |
| Brand exposure discipline | 15 | Brand mention is proportional, late, disclosed when needed, and removable without destroying topic value. |
| Material realism | 10 | Required visuals/data/research are available, ethical, or clearly requested from client. |
| Community targeting | 10 | Target communities match the user situation and topic type. |
| Portfolio coverage | 10 | Topic set covers multiple product differentiators and personas. |
| Risk handling | 10 | Flags promotional, fake-story, unsupported-claim, and subreddit-rule risks. |

## Topic Quality Signals

High-scoring topics usually:

- Can be summarized as "a real person in a real constraint asks or reports something".
- Include trade-offs instead of universal claims.
- Invite comments from people with experience.
- Let the product appear as one possible path, not the entire reason for the post.
- Have a natural reason to collect search data.

Low-scoring topics usually:

- Start with the product name.
- Depend on fake first-person experience.
- Need proof the client cannot provide.
- Could only live in an ad or launch community.
- Repeat the same pain with different wording.

## Required Fixes By Failure Type

- Too promotional: move the brand mention later and rebuild around the user's problem.
- Too vague: add concrete user situation, trigger, and target community.
- Missing materials: list required proof or change the post format to pure text.
- Duplicate topics: merge, drop, or separate by persona/search intent.
- Weak search intent: rewrite as a query-worthy pain or comparison.

## Pass Output

The eval report must list:

- Approved topics.
- Topics requiring client confirmation.
- Rejected topics and reasons.
- Feishu doc URL/token or blocker.
