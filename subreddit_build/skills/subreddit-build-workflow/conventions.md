# conventions.md

## SmartContent API

- Base URL: `https://smartcontent.shifenglab.com`.
- Auth uses `planner_session` cookie from the environment only. Never hard-code or write it.
- Community builder APIs use `/api/projects/...`, not `/api/search-occupancy/...`.
- `GET /api/projects` is not a list endpoint; use `GET /api/workspace`.
- `status=succeeded` does not mean every subreddit succeeded; inspect `artifacts.community_urls.failed_subreddits`.
- This workflow does not补抓失败社区. Record failures and continue with successful subreddits.
- Download endpoints support `GET`; do not use `HEAD`.
- Round download keys are dynamic. Always call `/downloads` before `/download/{key}`.
- Use UTF-8 byte JSON for Chinese request bodies.

## Reddit Content

- Community fit beats product exposure.
- Brand exposure must be light, naturally framed, and tied to verified facts.
- The best Topic Cards preserve: a concrete situation, a clear emotional trigger, and an easy
  comment engine.
- Native rewrite should sound like a real user, not a polished content marketer.

## Feishu

- Topic Cards must be written to a Feishu topic doc before draft generation proceeds.
- Final posts must be written to a separate Feishu post doc.
- Created docs should be public-editable unless run_config explicitly says otherwise.
- Never paste API cookies, keys, run secrets, or hidden evaluation notes into Feishu.
