# Formatting Report

- Source: `05_posts/optimized_posts.md`
- Output: `06_formatted/formatted_posts.md`
- Final Feishu doc: `https://my.feishu.cn/docx/Mhuodv9IooWDCFxg1REcFjIInqc`

## Transformations

- Removed internal optimization metadata: Topic ID, target rationale, disclosure notes, image notes, risk notes, and claim-change logs.
- Converted each post to strict final structure: H1 post label, target subreddit paragraph, H2 `Title`, H2 `Body`, H2 `评论设计`.
- Skipped `素材` sections because none of the six selected posts require images or materials.
- Converted comment groups into anonymous `User X` labels with `<hr/>` separators.
- Removed OP-side promotional replies from raw draft comment material rather than carrying them forward.
- Highlighted brand terms with `<span background-color="light-yellow">...</span>`.

## Deleted / Weakened Content

- Deleted raw-draft references to unverified external security reports and leak counts.
- Deleted fake direct client incidents, fake screenshots, fake usage durations, and fake pricing details.
- Weakened product claims around RLS, GitHub sync, local handoff, and payment/webhook handling.
- Removed comments that sounded like product support, testimonial, or OP defense.

## QA Checks

- No `Tree`, `Standalone`, `Comment Trees`, `Metadata`, `Post Type`, `Flair`, or `Link Permissibility` strings remain.
- No H3/H4 headings or blockquote markers remain.
- No empty comment paragraphs remain.
- All brand mentions found by scan are highlighted.
- No image prompt or generated image is required for this selected set.

