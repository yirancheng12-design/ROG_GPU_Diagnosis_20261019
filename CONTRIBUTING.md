# Contributing and translation policy

## Preserve the evidence

Keep the original root-level reports, CSVs, and ZIPs unchanged. Their exact byte counts and SHA-256 values are recorded in [the manifest](evidence/manifest.json), anchored to source commit `0aeaf8c4f514c36b560d215670eb876be3b9b5d7`. Add corrected explanations or new evidence as separate, dated files. Do not rewrite old logs to agree with a newer conclusion.

Do not execute archived scripts to verify this repository. Verification is read-only and does not require administrator privileges, NVIDIA software, or access to the original laptop.

## English source mapping

| English edition | Chinese source |
| --- | --- |
| [GPU diagnosis](docs/en/gpu-diagnosis.md) | [Original diagnosis](ROG_G635LX_GPU诊断报告.html) |
| [Tuning and baseline](docs/en/tuning-report.md) | [Tuning HTML](ROG_G635LX_调校执行报告.html) and [baseline text](GPU调校基线与操作记录.txt), which contain substantially overlapping narratives |
| [225W retest](docs/en/power-225w-retest.md) | [Retest HTML](ROG_G635LX_225W复试结果.html), with an explicitly marked editorial chronology based on the packaged JSON records |
| [Evidence guide](docs/en/evidence-guide.md) | [Original overview](README_225W_整理说明.md), the two original CSV inventories, and ZIP member lists |

The English editions reorganize repeated material for readability. Preserve numerical values, timestamps, units, uncertainty, excluded runs, and the distinction between planned and executed work. Identify editorial additions. Do not present historical driver listings as currently recommended downloads.

Keep raw identifiers, hashes, source filenames, and paths unchanged, including Chinese filenames. Original CSV headers are already English; translating a path would break its relationship to the evidence. Screenshots, raw logs, machine-readable records, and archived copies of old reports remain in their original language. A translated interpretation must not replace them.

## Evidence claims

Distinguish these states explicitly: requested, accepted by an interface, read back, sustained under load, tested for performance, and restored with read-back evidence. A process exit code or a registry write alone proves none of the later states.

Document missing artifacts instead of fabricating a link or silently deleting a historical claim. References to files inside ZIPs should give the package and exact member path; they are not directly navigable GitHub file links. The generated [coverage report](docs/en/evidence-coverage.md) records archive members and absent references separately.

## Checks

For a new case, use the [diagnostic checklist](docs/en/diagnostic-workflow.md), [blank telemetry template](docs/en/telemetry-template.csv), and GitHub measurement issue form. The short [55W case](docs/en/case-55w.md) and [225W evidence case](docs/en/case-225w.md) are editorial introductions derived from the detailed English reports and packaged records; they are not new experiments.

`tools/summarize_telemetry.py` analyzes recorded CSVs only. Keep raw input data and the normalization method. Limit segments describe recorded samples, not continuously verified operation. The tool must not infer causes, FPS gains, or stable hardware settings.

Run from the repository root:

```console
python tools/verify_repository.py
python -m unittest discover -s tests -v
```

After a deliberate change to the coverage generator, refresh its output:

```console
python tools/verify_repository.py --write-coverage
```

That command only regenerates the coverage document. It does not update hashes or accept changed evidence. New evidence needs a separately reviewed manifest update with provenance. CI runs verification on pushes and pull requests.
