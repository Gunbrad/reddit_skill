# EVALS — Topic Card Optimization (Stage 5) — viral (爆帖) potential

Goal: pick cards with real breakout potential **without** sacrificing community fit or
nativeness. Score every stage-4-passed card. **Blocking** must pass.
Threshold: precondition gate passes AND viral total ≥ 80/100; chosen top-N = highest eligible.

The structure: (P) precondition guardrails (blocking gate), (V) viral-potential score,
(N) supplemental-note quality incl. the 选题 anchor.

---

## P. Precondition guardrails (blocking gate — fail any → card is INELIGIBLE for ranking)

A card may be scored for viral potential ONLY IF all of these hold:

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| P1 | Community-compliant | ✅ | target_subreddit allows this post type; viral angle won't break community rules |
| P2 | Not marketing/promo-heavy | ✅ | Brand at most a natural ≤1-2 capability mention; no feature dump / pitch |
| P3 | Not AI-flavored | ✅ | Idea isn't a checklist / 三段论 / generic listicle; carries a real, specific pain |
| P4 | Safe facts | ✅ | No reliance on unverified/"不可说" features or fabricated data to be interesting |

If P fails, the card cannot be chosen no matter how "viral" it looks — fix the angle or drop it.

---

## V. Viral-potential score (rank eligible cards; weighted 1-5 per dimension)

| Dimension | Weight | 5 = high | 1 = low |
|-----------|:---:|----------|---------|
| Hook strength | 20% | Title/opening creates curiosity, conflict, or counter-intuitive tension | Flat, predictable |
| Resonance breadth | 20% | Pain many readers share ("this is so me") → upvote/share urge | Niche / few relate |
| Discussion / controversy | 15% | Naturally splits opinion, invites debate / taking sides | Nobody argues |
| Story & specificity | 15% | Concrete scene, numbers, a turn/reveal — not vague | Generic abstraction |
| Title click-through | 15% | Matches the direction map's high-rank title structures/semantics | Ignores what ranks |
| Timeliness / trend | 10% | Rides a current trend or high-frequency search semantics | Stale |
| Low-effort participation | 5% | Easy for readers to reply/vote/share (a clear question or relatable take) | Hard to engage |

Compute weighted total per eligible card; rank. Chosen top-N = highest eligible while keeping
diversity (not N cards of the same subreddit + angle).

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| V1 | All passed cards scored | ✅ | Every stage-4-passed card has a viral weighted score in optimization.md |
| V2 | Top-N = highest eligible | ✅ | Chosen set matches the ranking among P-eligible cards; N per run_config/user |
| V3 | Diversity preserved | ✅ | No over-concentration on one subreddit + one angle |
| V4 | Rationale recorded | ⬜ | optimization.md says why each chosen card beats near-misses |
| V5 | Picks cite heat evidence | ✅ | Each TopN pick cites `occupancy_heat_evidence.json` (similar_posts / title_patterns / comment_triggers / skepticism_angles), not just a subjective hunch |

---

## N. Supplemental-note quality (per chosen card)

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| N1 | Viral-lift instruction | ✅ | Note targets the card's weakest viral dimension specifically, not "make it better" |
| N2 | 选题 anchor present | ✅ | Note includes the originating 选题 summary with the "参考、不必逐字一致、不要偏移该方向" framing |
| N3 | needs_extra_material handled | ✅ | If material needed, note instructs placeholder + no fabrication |
| N4 | Brand calibration | ⬜ | Steers brand to ≤1-2 capabilities + disclosure when relevant |
| N5 | Concise & API-ready | ⬜ | Short enough to pass verbatim as topic_supplemental_contexts value |
| N6 | length_multiplier justified | ⬜ | The chosen `length_multiplier` (user value, else situational per the UI map) is recorded in optimization.md with a one-line why; not blindly maxed for length |

---

## H. Handoff viral_intent (blocking — Stage 6 depends on it)

| # | Criterion | Blocking | Pass condition |
|---|-----------|:---:|----------------|
| H1 | viral_intent complete | ✅ | Each chosen post in `handoff_packet.json` has `core_hook`, `emotional_trigger`, `comment_engine`, and non-empty `must_preserve[]` |
| H2 | title pattern + comment types | ✅ | `title_pattern_to_preserve` + `expected_comment_types[]` present, derived from heat evidence |
| H3 | claim ids bound | ✅ | `allowed_claim_ids` / `forbidden_claim_ids` set from `global/product_fact_index.json` |
| H4 | subreddit risk noted | ⬜ | `subreddit_risk_note` present |

---

## Failure → action

- P1-P4 fail → card is ineligible; fix the angle to clear the gate or exclude it from top-N.
- V1/V2 fail → score the missing cards / re-pick to match the eligible ranking.
- V3 fail → swap a duplicate-angle pick for the next diverse high-scorer.
- N2 fail (no 选题 anchor) → add it before drafting; otherwise the draft drifts off-direction.
- N1 generic / N3 fail → rewrite the note (specific viral lift; placeholder, no fabrication).
- Record P/V/N verdicts in `run_manifest.md`.

## Reviewer prompt (MANDATORY evaluator worker - run BLIND; do not say it is the client's product)

Under isolated-worker execution, this reviewer must run as a separate evaluator worker. It is
not optional. If the runtime does not support subagents, emulate this with a fresh evaluation
session that receives only optimization.md, the chosen-card artifact, handoff_packet.json,
this EVALS.md, OUTPUT_SCHEMA.json, the heat evidence, and the minimal fact index.

"Read optimization.md and the chosen cards. (P) Does any chosen card read as an ad / AI
listicle / rely on unverified claims, or break its subreddit's rules? (V) For each chosen
card, is there a genuine reason it could blow up — a strong hook, a widely-shared pain, real
controversy — or is it just safe and forgettable? Is the chosen set the strongest eligible
set, and is it diverse? (N) Does each note give a specific viral-lift instruction AND include
the originating 选题 as参考-not-script guidance? List every violation."
