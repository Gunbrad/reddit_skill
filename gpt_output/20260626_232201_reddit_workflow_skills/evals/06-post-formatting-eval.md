# Post Formatting Eval

Use after `reddit-post-formatting` creates `06_formatted/formatted_posts.md` and updates the Feishu document when available.

Threshold: 95/100.

## Hard Gates

Fail if any gate fails.

| Gate | Pass Standard |
| --- | --- |
| Heading structure | Each post uses H1 for post label and only H2 sections: `Title`, `素材` if needed, `Body`, `评论设计`. |
| Metadata removed | No final-only clutter such as post type, flair, link permissibility, internal scoring, or generation notes remains. |
| Materials preserved | Image/material blocks are preserved and not accidentally deleted. |
| Comment labels cleaned | No `Tree`, `Comment Trees`, `Standalone`, or similar labels remain. |
| Username anonymized | All usernames are converted to `User X` or `User X replies to User Y`. |
| OP promotional replies removed | OP/brand-side replies that explain or defend the product are deleted. |
| Brand highlighting | All brand variants are highlighted, and unrelated substrings are not highlighted. |

## Weighted Rubric

| Criterion | Weight | Scoring Notes |
| --- | ---: | --- |
| Structural compliance | 25 | Correct heading levels and section order across all posts. |
| Comment formatting | 20 | Replies, separators, blockquote removal, empty comment paragraphs, and thread readability are correct. |
| Content preservation | 15 | Approved title/body/material meaning remains intact. |
| Brand highlighting accuracy | 15 | All variants highlighted; no false positives. |
| OP and ad-risk cleanup | 10 | Promotional OP replies and support-like comments removed. |
| Local and Feishu parity | 10 | Feishu document matches local formatted output or discrepancy is documented. |
| Formatting report quality | 5 | Lists changes, deletions, and unresolved issues. |

## Formatting Checklist

For every post:

- H1 exists.
- Target subreddit line is a paragraph.
- H2 `Title` exists.
- H2 `素材` exists only when material exists.
- H2 `Body` exists.
- H2 `评论设计` exists.
- No H3/H4 headings.
- No metadata block.
- No blockquote markers in comments.
- No empty paragraphs inside comments.
- Separators between comment threads are preserved.
- User numbering is internally consistent.
- Brand variants are highlighted.

## Required Fixes By Failure Type

- Extra headings: convert to paragraphs or delete labels.
- Missing material block: restore from optimized post artifact.
- Username leak: replace with `User X` format.
- False brand highlight: remove span from unrelated text.
- Missing brand highlight: apply span to all exact variants.
- OP promotional reply remains: delete only the OP reply, preserve other thread comments.

## Pass Output

The eval report must list:

- Local formatted file path.
- Feishu document URL/token or blocker.
- Deleted comments and reasons.
- Brand terms checked.
- Any remaining manual QA notes.
