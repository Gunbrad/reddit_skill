# Search Occupancy Eval

Use after `reddit-search-occupancy` creates queries, runs SmartContent, downloads direction artifacts, selects three directions, and generates topic cards.

Threshold: 90/100.

## Hard Gates

Fail if any gate fails.

| Gate | Pass Standard |
| --- | --- |
| Query count | Exactly two queries per approved topic unless the user specified otherwise. |
| Query quality | Queries are long-tail, English, non-duplicative, and user-intent based. |
| API proof | Auth check, project/run IDs, polling result, and direction statuses are recorded. |
| Direction-level success | Selected directions all have successful map MD/JSON artifacts. |
| Three distinct directions | Exactly three selected directions, and each has a distinct intent/community/narrative use. |
| Topic cards generated | Each selected direction has the requested topic-card count and local MD download. |

## Weighted Rubric

| Criterion | Weight | Scoring Notes |
| --- | ---: | --- |
| Query specificity | 15 | Each query includes context + pain/category + Reddit-native vocabulary. |
| Query diversity | 15 | Two queries per topic probe different language or communities. |
| Search-result relevance | 15 | Downloaded results align with product personas and topic plan. |
| Map usability | 15 | Maps contain subreddit distribution, title patterns, content forms, narrative logic, semantic phrases, and reusable hooks. |
| Direction selection logic | 20 | Selected directions are mutually distinct and useful for topic-card generation. |
| Artifact completeness | 10 | All required local files exist and are named correctly. |
| Failure handling | 10 | Failed directions are documented and not used downstream. |

## Query Quality Checklist

Pass-worthy query:

- 4-10 meaningful terms.
- Contains a real user problem, stage, or comparison.
- Avoids generic marketing language.
- Avoids brand unless the topic is brand-aware.
- Likely returns Reddit discussions, not vendor pages.
- Does not duplicate another query's intent.

Examples of weak query patterns:

- `{product category} best`
- `{brand} review`
- `AI tool productivity`
- `how to use {feature}`
- Reordered duplicate phrases.

## Direction Selection Checklist

Selected directions should differ across at least two of:

- Persona.
- Stage of problem.
- Subreddit cluster.
- Emotional trigger.
- Content form.
- Product differentiator.
- Search phrase family.

If two directions overlap heavily, keep the one with better map richness and replace the other.

## Required Fixes By Failure Type

- Weak query: rewrite before API rerun.
- Failed map: drop direction or rerun with revised query.
- Too few successful directions: generate replacement queries and rerun.
- Duplicate directions: select another successful direction or rerun.
- Missing downloads: call the exact download endpoint and save locally.

## Pass Output

The eval report must list:

- Search query document path.
- SmartContent project ID and run ID.
- Successful directions.
- Dropped directions and reasons.
- Selected three directions.
- Topic card files handed to the next step.
