# ROG G635LX GPU Diagnosis

An evidence archive documenting GPU power limits, stability observations, and tuning attempts on an ASUS ROG Strix SCAR 16 G635LX with an RTX 5090 Laptop GPU.

**Recorded on October 19, 2026.** All test times use Asia/Shanghai (UTC+8). These are historical measurements from one machine, not a statement about its current state or a tuning profile for other laptops.

## Start here

| English document | Contents |
| --- | --- |
| [GPU diagnosis](docs/en/gpu-diagnosis.md) | Hardware, the recorded 175W limit, telemetry, stability events, and testing methodology |
| [Tuning and baseline report](docs/en/tuning-report.md) | Cyberpunk 2077 runs, standby interference, CPU temperature stops, and restoration checks |
| [225W retest and chronology](docs/en/power-225w-retest.md) | Failed driver/API attempts, the later registry experiment, and missing follow-up evidence |
| [Evidence guide](docs/en/evidence-guide.md) | Downloads, archive contents, CSV interpretation, and evidence limitations |
| [Evidence coverage](docs/en/evidence-coverage.md) | Generated audit of references in the original HTML reports |
| [Contributing](CONTRIBUTING.md) | How to add evidence, update translations, and run checks |

## What the records establish

- The initial diagnosis recorded a **175W** current and maximum GPU power limit, consistent with the specification cited in that report: **150W + 25W Dynamic Boost**.
- The initial passive trace contains **85 samples**. It is not a sustained-load benchmark.
- A Cyberpunk baseline was affected by Modern Standby and a **55W** limit. A subsequent awake run stopped after a **104°C** CPU reading; no completed tuned Cyberpunk A/B result was obtained in that phase.
- The early 225W retest failed to load its experimental driver (Windows error **577**). A later standard NVIDIA API request also left the read-back limit at **175W**.
- A packaged **23:43** record documents a registry override write, with live current/maximum limits still at **175W**, a restart required, and no stress test started.
- The retest HTML contains an appended claim that a later restart enabled a 225W driver limit, followed by a CPU-temperature stop at a 175W baseline. Its linked follow-up report is absent. Treat that as an **unverified later report**, not evidence of sustained 225W or a completed restoration.

There is no demonstrated stable 225W performance result in the published evidence. A configuration target, a successful registry write, an exit code of zero, and measured sustained power are different outcomes.

## Repository layout

```text
README.md                  English entry point
docs/en/                   Edited English editions and evidence guide
evidence/manifest.json     Original-file hashes and ZIP member inventory
tools/verify_repository.py  Read-only integrity and documentation checks
tests/                     Verifier regression tests
.github/workflows/         Automated verification
*.html, *.txt, *.csv, *.zip Original Chinese reports and evidence, unchanged
```

The English editions translate and reorganize the readable reports. Original filenames, CSV path fields, binary data, screenshots, and logs are retained as evidence identifiers. Text embedded in historical screenshots and raw machine output is not relabeled or translated. Read the [translation policy](CONTRIBUTING.md) for the source mapping and treatment of later annotations.

## Verify the archive

Python 3.11 or newer is sufficient; no third-party packages or GPU tools are required. From the repository root:

```console
python tools/verify_repository.py
python -m unittest discover -s tests -v
```

The verifier checks original-file SHA-256 values, ZIP CRCs and member inventory, local links in maintained Markdown, and the generated evidence-coverage report. It reads archives without extracting or executing their contents. It makes no hardware changes and does not establish the truth of a sensor reading or the completeness of a historical experiment.

## Original Chinese material

The [original overview](README_225W_整理说明.md), [diagnosis](ROG_G635LX_GPU诊断报告.html), [tuning report](ROG_G635LX_调校执行报告.html), [baseline log](GPU调校基线与操作记录.txt), and [225W retest](ROG_G635LX_225W复试结果.html) are preserved byte for byte. Download HTML files to view their original layouts; GitHub normally displays their source.

This repository documents past experiments. It does not provide a validated over-spec power profile or instructions to run the scripts, registry exports, or ROM files inside the evidence packages. The original records describe no firmware flashing, but they do describe software changes, an experimental driver-load attempt, and a later registry override. The blanket phrase "software only" should not be read as "nothing changed" or "all changes were proven reversible."
