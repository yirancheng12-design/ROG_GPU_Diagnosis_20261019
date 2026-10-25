# Measure discovery before optimizing for stars

[Home](../../README.md) · [Sharing drafts](share-kit.md) · [Release checklist](release-notes.md)

The practical sequence is **useful result → qualified visitors → successful use → feedback and voluntary stars**. This is a working hypothesis for this project, not a guarantee of growth or a claim about GitHub's ranking algorithm.

## First cycle

| Action | Deliverable | What to observe |
| --- | --- | --- |
| Show an inspectable result | Sample-based preview chart and `python tools/demo.py` | Can a new reader explain the finding without reading the full archive? |
| Lower the starting cost | English/Chinese entry points, one demo command, no runtime dependencies | Can another person reproduce the output from a clean download? |
| Share one useful case | Human-reviewed post in a relevant community, with original data and owner disclosure | Which referring source brings relevant questions or visitors? |
| Invite another machine | Structured measurement issue, with conditions and exclusions | Does a new case add evidence rather than another unsupported performance claim? |
| Package a coherent version | Reviewed release notes, a tag/release only after verification | Do readers understand what is shipped, how to run it, and what remains unknown? |

Focus one experiment at a time. Avoid changing the title, lead image, demo, and distribution channel simultaneously if you want to understand the response.

## Record only observed metrics

The [blank growth log](growth-log.csv) has no fabricated starting values. Enter dated observations manually:

- `snapshot_date`: date/time and timezone of the observation.
- `stars_total`: current total, not a projected goal.
- `views_14d`, `unique_visitors_14d`, `clones_14d`: the values GitHub reports for its rolling traffic window, or blank when unavailable.
- `channel` and `content_url`: the actual source of a published post, or blank if it was not posted.
- `change_notes`: what was changed or learned; do not claim causation from one coincident increase.

GitHub traffic covers a rolling window. Do not sum overlapping 14-day totals or treat differences between them as daily visitors. Traffic and referral sections update on different schedules; a zero/delayed count is not proof that nobody opened a link. New stars divided by visitors is at most a rough aggregate, not attribution of individual visitors or a reliable cross-project comparison. See [GitHub's traffic documentation](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository).

## Decide what to improve next

| Observed pattern | Next experiment |
| --- | --- |
| Little recorded traffic after allowing for update delay | Share one relevant case with context; review the title, description, and accurate topics |
| Visitors arrive but cannot run the demo | Fix setup friction and clarify expected output before adding more promotion |
| People use it but ask the same question repeatedly | Turn that question into a short guide with evidence and a visible entry point |
| Other laptop owners contribute comparable samples | Add a carefully sourced case index and compare matched conditions |
| A particular post attracts unrelated traffic | Narrow its claim and target audience rather than chasing the raw view count |

Repository topics and social-preview images support discovery/presentation, but they do not guarantee traffic or stars. [Topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics) should describe actual content. [Social previews](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview) require a separate Settings upload; the supplied 1280×640 PNG is a ready asset, not an automatically applied setting.

## Keep the project worth returning to

Publish real improvements and new evidence, respond to useful issues, credit contributors, and preserve reproducible inputs. Add a brief optional Star invitation after demonstrating value. No paid stars, star exchanges, mass unsolicited messages, or fabricated popularity are part of this plan. No recurring automation or external posting is enabled by these files.
