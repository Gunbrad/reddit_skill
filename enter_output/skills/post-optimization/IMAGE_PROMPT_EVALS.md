# EVALS — Image Prompt (de-AI) for Stage 6

Scores an image prompt AND its generated output so the picture does NOT look AI-made or like
an ad. Run per image. Two classes share a common de-AI core, then each adds a class-specific
rubric:

- **实体类 (Physical)** — a real-world candid photo (desk in front of a monitor, phone held
  over a laptop, a notebook, a person's hands on a keyboard).
- **虚拟类 (Virtual)** — a software UI / app screenshot / dashboard, OR anime / illustration.

**Classify first**, then score: Common core + the matching class rubric.
**Threshold (both classes): all blocking ✅ pass AND total ≥ 85/100** (same bar as the stage-6
de-AI text rubric). Score the prompt before generating, and re-score the output after.

---

## Common core (applies to BOTH classes) — 40 pts

| # | Criterion | Blocking | Weight | Pass condition |
|---|-----------|:---:|:---:|----------------|
| G1 | Not an ad composition | ✅ | 10 | No hero/studio/poster framing, no centered "product beauty shot", no marketing gloss |
| G2 | No logo / text overlay / watermark | ✅ | 8 | No brand logo, no headline text baked on, no stock-style watermark or border |
| G3 | Anchored to the post's real scenario | ✅ | 8 | Prompt names the body's concrete situation, not a generic pretty image |
| G4 | Imperfection required, not optional | ✅ | 8 | Prompt explicitly asks for some mess/asymmetry/uneven light; bans "perfect/clean/pristine/4k ultra" |
| G5 | Traceable record | ⬜ | 3 | prompt + class + scenario-change reason saved in prompts.md, bound to the post |
| G6 | Aspect/context sane | ⬜ | 3 | Framing/aspect fits where it's posted (not a billboard banner for a Reddit selfie context) |

---

## A. 实体类 (Physical / candid photo) — 60 pts

| # | Criterion | Blocking | Weight | Pass condition |
|---|-----------|:---:|:---:|----------------|
| P1 | Natural light, real room | ✅ | 12 | Home/office ambient light, uneven exposure; NOT studio/softbox/rim lighting |
| P2 | Casual amateur framing | ✅ | 12 | Slight tilt, off-center, natural depth of field; not a product-photography tripod shot |
| P3 | Lived-in detail | ✅ | 10 | Clutter / cables / dust / smudges / reflections / used surfaces present |
| P4 | No CGI / plastic sheen | ✅ | 10 | No hyper-real sharpness, no waxy 3D render look, no impossible symmetry |
| P5 | Correct anatomy if people/hands | ✅ | 8 | Right finger count & proportion; no melted hands/faces; or no people at all |
| P6 | Real device/screen behavior | ⬜ | 4 | If a screen is shown, it has glare/moire/off-angle, not a pasted-in clean UI |
| P7 | Phone-camera realism | ⬜ | 4 | Mild grain/compression/auto-HDR feel beats clinical clarity |

### Failure → action (实体类)
- P1/P2 fail → rewrite prompt: name a room, a light source, a casual angle; drop "studio/clean".
- P3 fail → add concrete clutter from the body (e.g. "coffee mug, tangled charger, sticky notes").
- P4/P5 fail → regenerate; if only hands/text are broken, use the image2 **edits** endpoint to
  repair that region instead of re-rolling the whole image.

---

## B. 虚拟类 (Virtual / UI screenshot, anime, illustration) — 60 pts

Score the relevant sub-block (UI **or** anime/illustration); ignore the other.

### B-UI (software page / screenshot)

| # | Criterion | Blocking | Weight | Pass condition |
|---|-----------|:---:|:---:|----------------|
| V1 | Believable real UI | ✅ | 12 | Real-looking controls, sane information density, plausible layout; NOT "fake futuristic glowing UI" |
| V2 | No garbled / placeholder text | ✅ | 12 | No lorem-gibberish, no warped glyphs; visible text is real and semantically correct |
| V3 | Possible data, not magic | ✅ | 8 | Charts/numbers are plausible; no impossible graphs or nonsense metrics |
| V4 | Capture realism | ⬜ | 6 | Browser chrome / OS bar / cursor / real resolution; looks captured, not designed |
| V5 | Matches product boundary | ⬜ | 4 | If it implies the client's product, only verified capabilities are shown (per product_brief) |

### B-Anime / Illustration

| # | Criterion | Blocking | Weight | Pass condition |
|---|-----------|:---:|:---:|----------------|
| V6 | Consistent coherent style | ✅ | 12 | One coherent art style; no melted limbs, extra fingers, broken perspective |
| V7 | No classic AI tells | ✅ | 12 | No mushy background, no uncanny symmetric face, no garbled in-image text |
| V8 | Topic-fit subject | ✅ | 8 | Subject matches the post's context; not defaulting to "cyberpunk neon" model bias |
| V9 | Text only if correct | ⬜ | 6 | In-image text appears only if legible & correct (else omit it); fix via edits endpoint |
| V10 | Multi-image consistency | ⬜ | 4 | If a post uses several images, style/character stays consistent across them |

### Failure → action (虚拟类)
- V1 fail → rewrite to a mundane real interface; ban "futuristic/glowing/holographic/sci-fi UI".
- V2/V9 garbled text → regenerate or use the image2 **edits** endpoint to correct exact strings.
- V6/V7 fail → regenerate with a tighter style anchor; repair local distortions via edits.
- Record the chosen sub-block + verdict in prompts.md.

---

## Decision flow

1. Classify the image: 实体类 or 虚拟类 (and for 虚拟类, UI vs anime/illustration).
2. Score the PROMPT: Common core + class rubric. If any blocking fails or total < 85, rewrite
   the prompt before spending an API call.
3. Generate, then RE-score the OUTPUT on the same rubric. If a blocking AI tell appears
   (warped hands, garbled UI text, plastic sheen, fake UI), fix the prompt or repair the
   region with the image2 edits endpoint, and re-score.
4. Only a passing image goes into the image Feishu doc. Record the per-image verdict in
   prompts.md and the manifest.

## Reviewer prompt (optional subagent — run BLIND, do NOT tell it this is a client's product)

"You're a sharp-eyed Reddit user. Look at this image. Does it look like a real person snapped
it / a real screenshot, or like an AI-generated / ad image? Call out specific tells: studio
lighting, too-perfect framing, plastic CGI sheen, warped hands, garbled or fake UI text,
impossible charts, logos or text overlays, default 'cyberpunk neon' look. Would this get
called out as AI or an ad in the target subreddit? List every tell."
