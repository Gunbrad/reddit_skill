# Post Optimization Eval

Use after `reddit-post-optimization` rewrites raw drafts, creates/updates the Feishu post document, recommends communities, and handles image prompts/assets.

Threshold: 90/100.

## Hard Gates

Fail if any gate fails.

| Gate | Pass Standard |
| --- | --- |
| Product truth | Every product claim is supported by the product brief or weakened/removed. |
| No fake experience | No fabricated user story, revenue, review, benchmark, screenshot, or customer outcome. |
| Reddit-native purpose | Each post has a discussion/story/question value beyond product exposure. |
| Target communities | Each post lists at least three target subreddits with rationale and risk. |
| Disclosure handled | Promotional relationship or product involvement is disclosed when needed. |
| Image audit | Every image-needed post has an audited prompt; unreasonable prompts are rewritten or rejected. |
| Local asset saving | Image prompts and generated image metadata/files are saved locally, or generation is explicitly blocked. |

## Weighted Rubric

| Criterion | Weight | Scoring Notes |
| --- | ---: | --- |
| Factual accuracy | 15 | Claims match fact bank, boundaries, and unverified list. |
| Native Reddit voice | 20 | Reads like a plausible Reddit user: specific, imperfect, conversational, not polished marketing. |
| Anti-AI language cleanup | 15 | Removes essay structure, generic transitions, overbalanced framing, and feature-dump cadence. |
| Community fit | 10 | Target subreddits match topic, tone, rules, and audience maturity. |
| Brand integration | 10 | Brand mention is proportional, honest, and late enough to avoid ad smell. |
| Comment design | 10 | Comments include skepticism, technical pushback, user experience, and natural short replies. |
| Image prompt quality | 10 | Prompt is realistic, useful, non-ad-like, and aligned with verified facts. |
| Handoff completeness | 10 | Feishu doc, local files, image assets, claim changes, and blockers are recorded. |

## Native Reddit Voice Diagnostic

Flag and revise when a post contains:

- Grand opening lines: "I've been thinking a lot about..."
- Corporate abstractions: "streamline", "seamless", "robust", "unlock productivity".
- Over-neat paragraph logic: problem, solution, benefits, conclusion.
- Too many balanced caveats in a row.
- Unnatural "as someone who..." authority setup.
- Feature list replacing lived detail.
- Comments that sound like product FAQ or support replies.
- Excessive slang that feels pasted on.

Prefer:

- Specific time costs, setup friction, mistakes, or uncertainty.
- Short uneven sentences mixed with longer explanation.
- Real trade-offs: lock-in, migration, setup time, pricing uncertainty, support risk.
- User questions that invite experienced replies.
- Light self-correction when a claim is uncertain.
- Technical details only where the community would care.

## Product Fact Diagnostic

For every product mention, classify:

- `verified-safe`: keep.
- `verified-but-risky`: keep only with narrower wording.
- `client-provided`: keep if disclosure/context supports it.
- `needs-confirmation`: remove or turn into a question.
- `forbidden`: remove.

Examples of required weakening:

- "handles payments end to end" -> "helps with payment state/webhook setup if that is verified".
- "no lock-in" -> "code export/GitHub sync exists; migration still has trade-offs".
- "production-ready" -> "closer to a real app than a demo, but still needs review".

## Comment Design Diagnostic

A good comment section contains at least three of:

- Skeptical validator accusing or questioning promotion.
- Technical correction or implementation detail.
- Competitor comparison.
- Personal anecdote.
- Short agreement/disagreement.
- Follow-up question that surfaces buying objections.
- Correction that weakens an overclaim.

Delete or rewrite comments that:

- Defend the product from the brand perspective.
- Repeat the same product benefit.
- Sound like a testimonial.
- Use formal essay language.
- Include fake user claims.

## Image Prompt Diagnostic

An image prompt passes when:

- The scene would plausibly exist in a Reddit post.
- The image helps explain the post, not decorate it.
- UI, product, or device details are verified.
- It avoids glossy ad composition.
- It avoids fake charts, fake reviews, fake dashboards, and fake logos.
- It includes negative constraints.

If image2 API is available, generated assets must include:

- Prompt file.
- Image file.
- Metadata JSON with prompt, model/API identifier if known, timestamp, dimensions, and source post ID.

If image2 API is not available:

- Save the final prompt.
- Mark `image_generation_blocked`.
- Do not claim the image was generated.

## Required Fixes By Failure Type

- AI-like post: rewrite with specific incidents, shorter lines, concrete friction, and less symmetry.
- Hard ad: reduce brand mention, add skepticism, and move product detail later.
- Unsupported claim: remove or weaken.
- Weak target communities: replace with communities matching the search map and post format.
- Bad image scene: rewrite prompt around a realistic screenshot, setup photo, diagram, or simple comparison.
- Comments too polished: delete the worst comments and add shorter, messier, more specific replies.

## Pass Output

The eval report must list:

- Per-post score.
- Removed or weakened product claims.
- Final target subreddits.
- Image assets/prompts and generation status.
- Feishu doc URL/token or blocker.
- Remaining client questions.
