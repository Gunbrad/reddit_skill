# Eval Report: Post Formatting

- Artifact: `06_formatted/formatted_posts.md`
- Evaluated At: 2026-06-27T01:11:00+08:00
- Result: PASS
- Score: 97/100

## Hard Gates

| Gate | Result | Evidence | Required Fix |
| --- | --- | --- | --- |
| Heading structure | PASS | Each post uses `<h1>` plus only `<h2>Title</h2>`, `<h2>Body</h2>`, and `<h2>评论设计</h2>`. No material sections were needed. | None. |
| Metadata removed | PASS | Internal scoring, risk notes, post type, flair, and link metadata are absent from final formatted file. | None. |
| Materials preserved | PASS | No selected post requires images/materials; no material block was dropped. | None. |
| Comment labels cleaned | PASS | `rg` check found no `Tree`, `Standalone`, `Comment Trees`, or similar labels. | None. |
| Username anonymized | PASS | Comments use `User X` and `User X replies to User Y`. | None. |
| OP promotional replies removed | PASS | No OP promotional/support replies remain. | None. |
| Brand highlighting | PASS | `Enter Pro`, `Enter Cloud`, and `Enter Code` are all wrapped in `<span background-color="light-yellow">...</span>` and no unrelated substrings were highlighted. | None. |

## Weighted Rubric

| Criterion | Weight | Score | Evidence | Required Fix |
| --- | ---: | ---: | --- | --- |
| Structural compliance | 25 | 25 | Local file follows required H1/H2 structure across six posts. | None. |
| Comment formatting | 20 | 19 | Comment threads use bold user labels and `<hr/>` separators; no blockquotes or empty comment paragraphs. | None. |
| Content preservation | 15 | 14 | Approved optimized post meaning is preserved while internal fields are removed. | None. |
| Brand highlighting accuracy | 15 | 15 | Manual scan confirms all brand terms highlighted. | None. |
| OP and ad-risk cleanup | 10 | 10 | Final comments avoid OP product defense. | None. |
| Local and Feishu parity | 10 | 9 | Final Feishu doc was created directly from `06_formatted/formatted_posts.md`; no local-vs-cloud divergence expected. | Optional visual review in Feishu UI. |
| Formatting report quality | 5 | 5 | `06_formatted/formatting_report.md` records transformations and checks. | None. |

## Revision Log

- Attempt 1: Converted optimized posts into strict final format, removed metadata, normalized comments, and highlighted brand terms.
- Attempt 2: Ran local checks for forbidden labels, extra headings, empty comment paragraphs, and brand highlighting; no fixes needed after scan.

## Handoff Notes

- Final formatted local file: `06_formatted/formatted_posts.md`
- Formatting report: `06_formatted/formatting_report.md`
- Final Feishu document: `https://my.feishu.cn/docx/Mhuodv9IooWDCFxg1REcFjIInqc`
- Brand terms checked: `Enter Pro`, `Enter Cloud`, `Enter Code`, lowercase variants.
- Blockers: none.

