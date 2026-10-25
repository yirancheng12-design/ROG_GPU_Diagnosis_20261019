# Evidence guide

[Repository home](../../README.md) · [Original Chinese overview](../../README_225W_整理说明.md) · [Reference coverage](evidence-coverage.md)

## Reading order

Read the [initial diagnosis](gpu-diagnosis.md), then the [tuning/baseline report](tuning-report.md), and finally the [225W chronology](power-225w-retest.md). Each describes a different phase. Statements such as "not attempted" or "restored" must be interpreted within that phase, not generalized across the day.

The original overview says the work involved software-level power/performance verification without BIOS writes. The preserved material also records software installation, attempted driver loading, and a registry override. The packaged result states no firmware flash. A ROM backup is not proof of a flash, and a software backup is not proof of recovery from every possible failure.

## Published packages

| Download | Members | Contents and boundary |
| --- | ---: | --- |
| [Tuning evidence](../../ROG_G635LX_调校证据.zip) | 48 | Initial settings, Cyberpunk baselines, standby/temperature stops, restoration records, and embedded copies of the original report/log |
| [Expanded GPU test evidence](../../GPU超频测试证据.zip) | 140 | Overlapping tuning records plus later FurMark/GPU-overclock test records; not a single controlled A/B dataset |
| [225W pre-restart evidence](../../225W新路线重启前证据_20261019.zip) | 40 | Later research, read-only probes, the 23:43 registry write/read-back, a registry export, a ROM backup, and historical scripts; no completed post-restart 225W load test established by these members |

Original ZIP bytes are unchanged. The [manifest](../../evidence/manifest.json) records every original root file's byte size and SHA-256, plus each ZIP member's path, uncompressed size, CRC32, and SHA-256. Member paths are evidence identifiers; download the named ZIP to inspect them. They are not ordinary GitHub links into an extracted directory.

Archived scripts, registry exports, ROMs, and raw shared-memory files are retained for provenance. Repository verification reads them as data and never executes or imports them into Windows. A backup cannot prevent or repair physical overvoltage, overcurrent, or thermal damage.

## Original CSV inventories

| Inventory | Header | Interpretation |
| --- | --- | --- |
| [Preparation / backup inventory](../../225W尝试准备_备份清单.csv) | `RelativePath, Bytes, SHA256` | Paths and hashes for a historical preparation backup. Some described artifacts are not included in the published repository. |
| [Unofficial-scheme review inventory](../../225W非官方方案核查证据清单.csv) | `File, Bytes, SHA256` | Names and hashes for a separate source-review collection. An inventory alone does not publish or authenticate the underlying files. |

`RelativePath` / `File` are exact historical identifiers, `Bytes` is the recorded byte count, and `SHA256` is the recorded digest. Their headers are already English. Path values, including Chinese filenames and Windows separators, are deliberately not translated. These source CSVs are preserved, not regenerated to describe a different archive.

## Evidence limitations

- The initial diagnosis references raw files not all present in the published packages. The verifier reports these absences rather than claiming complete coverage.
- Some historical HTML links point to files present only as ZIP members. Such a link will not work as an ordinary GitHub file link. The coverage document identifies the package instead.
- The original retest's later banner points to a missing execution report. The included pre-restart record cannot validate a later reboot, CPU stop, or completed restoration.
- Duplicate paths across ZIPs can represent different snapshots; inspect the package, timestamp, and hash together. A name such as `latest-checkpoint.json` does not establish chronological priority.
- The two original CSVs are inventories of historical collections, not a guarantee that those collections are present. The repository manifest separately inventories what is actually published.
- SHA-256 consistency and ZIP CRC checks establish integrity relative to the pinned repository snapshot. They do not prove sensor accuracy, authorship, safe hardware operation, or completeness of the original experiment.

## Reproduce the repository checks

From the repository root, with Python 3.11 or newer:

```console
python tools/verify_repository.py
python -m unittest discover -s tests -v
```

No network, package install, GPU query, administrator session, archive extraction, or hardware load is needed. CI runs the same commands on Linux and Windows. The checks validate maintained Markdown links, original-file hashes, archive member metadata/content, original CSV syntax, and whether the generated coverage document matches its inputs.

The historical HTML remains unchanged even where its links are incomplete. New English documents link to available packages and give exact member names rather than inventing extracted files.
