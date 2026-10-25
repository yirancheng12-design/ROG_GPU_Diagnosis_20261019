# 175W vs. 225W: what do the logs actually prove?

[Home](../../README.md) · [Detailed chronology](power-225w-retest.md) · [Evidence guide](evidence-guide.md)

**Finding:** the published material does not demonstrate a stable 225W workload result. The early API request was unsupported; a later registry write succeeded while live limits stayed at 175W. An appended post-restart claim points to a missing follow-up report. Those are three different evidence states.

## A request is only the first step

```mermaid
flowchart LR
    A[Target requested] --> B[Interface accepts change]
    B --> C[Live setting read back]
    C --> D[Actual draw measured under load]
    D --> E[Matched performance tests]
    E --> F[Restoration independently checked]
```

Each step needs its own evidence. Success at an earlier step does not establish the later steps. Even all of them together would describe tested conditions, not guarantee hardware lifetime.

| Published observation | Correct interpretation |
| --- | --- |
| A standard NVIDIA 225W request returned unsupported; exit code was 0 | The process exit code was not proof of a changed limit; the report's read-back stayed 175W |
| At 23:43, `RegistryReadbackMatches` was true | The registry value matched the write |
| The same JSON had `TargetMaxWatts: 225` and both `LiveCurrentStill175` / `LiveMaxStill175` true | Intended target and active limit differed; the live limit had not become 225W |
| `RestartRequired: true`, `StressTestStarted: false` | This was a pre-restart checkpoint, not a load-test result |
| A later HTML banner claimed a 225W limit and a CPU stop during a 175W baseline | A historical claim whose linked follow-up is absent; it still does not claim a completed 225W load test |

## Compare the right things

**Power draw** is an observed consumption value. **Power limit** is a control ceiling. **Performance** needs a workload result. **Stability** needs repeated checks within a defined test scope. Keep separate columns for all four.

The move from 175W to 225W is **28.6% more configured power**, not 28.6% more FPS. This repository has no matched, completed 175W/225W benchmark pair from which to calculate such a gain.

## Reproduce the evidence check

From a full clone, run:

```console
python tools/verify_repository.py
python -m unittest discover -s tests -v
```

The tests inspect the actual packaged pre-restart result and assert its target, live-limit flags, restart requirement, and lack of a started stress test. Integrity checks do not validate sensor accuracy, safe operation, or the missing follow-up.

The exact member is `power225-research-followup/apply-max225-20261019-234340-result.json` inside the [pre-restart ZIP](../../225W新路线重启前证据_20261019.zip). The [coverage audit](evidence-coverage.md) identifies missing references. No archived registry, driver, or ROM procedure needs to be executed to inspect this evidence.

## What would strengthen a future claim?

Publish timestamped post-restart live read-back, actual load telemetry, matched workload/settings, repeat results, exclusions, and restoration read-back. A missing stage should remain marked unknown rather than filled with an assumption. The [submission checklist](diagnostic-workflow.md) provides a reusable format.
