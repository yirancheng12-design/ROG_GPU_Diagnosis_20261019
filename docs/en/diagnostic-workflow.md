# A reproducible workflow for laptop GPU diagnosis

[Home](../../README.md) · [55W case](case-55w.md) · [175W/225W evidence case](case-225w.md)

Use this checklist to turn an observation into an inspectable case. The original G635LX data are an example, not a universal profile or a required benchmark result.

## 1. Define one question

Choose a specific symptom: a reduced power limit, low draw despite high utilization, unexpected clock drops, a temperature stop, or a driver timeout. Record when it occurs and what changed. Keep expected behavior separate from what you actually measured.

## 2. Capture the environment

- [ ] Laptop model and GPU/VRAM, including whether it is a Laptop GPU.
- [ ] OS, BIOS, VBIOS, GPU driver, and control-software versions.
- [ ] AC/battery state and adapter rating; mark owner-confirmed ratings separately from telemetry.
- [ ] Active OEM profile, display/GPU mode, and any existing offsets or custom curves.
- [ ] Ambient/cooling conditions, background workloads, and event-log timezone.
- [ ] Workload version, resolution, preset, DLSS/ray-tracing/frame-generation state, and FPS cap.

Preserve the original settings before any deliberate experiment. This workflow and the repository's scripts do not change them.

## 3. Collect time-aligned measurements

Start with existing/read-only data. Use the [blank CSV template](telemetry-template.csv) when normalizing samples from your own monitoring tool:

| Column | Meaning | Unit / missing data |
| --- | --- | --- |
| `timestamp` | Sample time | ISO 8601 recommended; include a consistent UTC offset. Historical `YYYY/MM/DD HH:MM:SS.sss` is also accepted |
| `power_W` | Measured GPU draw | Watts; blank or `N/A` if unavailable |
| `limit_W` | Effective GPU power limit | Watts; not actual draw |
| `gpu_C` | GPU core temperature | Degrees Celsius; not hotspot, memory, or VRM temperature |
| `core_MHz` | Reported GPU core clock | MHz |
| `util_percent` | GPU utilization | Percent |
| `cpu_C` | Recorded CPU sensor temperature | Degrees Celsius; identify package/core sensor in case notes |

The template has only headers, with no fabricated measurements. Keep samples strictly chronological and use one timezone convention throughout a file. All columns are required; unavailable values are blank or `N/A`, not zero. Extra source columns are accepted but not interpreted. Retain the original file separately and document conversion or resampling.

Correlate telemetry with standby/wake, AC changes, driver events, and workload start/stop times. Do not derive causation from one coincident sample or silently interpolate gaps.

## 4. Summarize without changing the machine

Python 3.11+, no external dependencies, from the repository root:

```console
python tools/summarize_telemetry.py --csv my-telemetry.csv
```

`my-telemetry.csv` is your own populated file, not shipped data. For the published example:

```console
python tools/summarize_telemetry.py --zip "ROG_G635LX_调校证据.zip" --member "tuning/baseline-auto-1/telemetry.csv"
```

The tool prints JSON sample counts, first/last timestamps, sample-span seconds, per-metric minimum/maximum/mean and available counts, and segments of equal recorded `limit_W`. Segment endpoints are sample timestamps, not proof of uninterrupted operation. It rejects malformed/non-finite numbers, missing columns, empty data, and non-increasing/inconsistent-timezone timestamps. It does not infer FPS, a root cause, thermal safety, or stability.

## 5. Separate observations from comparisons

- [ ] Identify the workload interval rather than treating the whole recording as loaded operation.
- [ ] Preserve invalid, interrupted, standby-affected, or thermally stopped runs; label and exclude them from inappropriate comparisons.
- [ ] For a planned A/B comparison, fix the workload/settings, change one variable, and record at least three completed runs per condition when conditions permit.
- [ ] Report spread and median, not only the best result. Separate rendered from generated/displayed FPS and explain the 1% low method.
- [ ] Document conservative stop conditions before deliberate testing; a sample maximum is not a manufacturer damage threshold.
- [ ] Verify restoration against the recorded original state, not an assumed generic default.

The analyzer does not select workload windows or certify a benchmark. The [original testing proposal](gpu-diagnosis.md) and [temperature-stopped case](tuning-report.md) explain why these distinctions matter.

## 6. Publish a useful case

1. **Question and result:** what happened, on which machine, and what remains unknown.
2. **Conditions:** hardware, software, workload, timestamps/timezone, and configuration.
3. **Evidence:** compact table/timeline, raw filenames, and hashes.
4. **Interpretation:** supported findings, alternatives, excluded runs, and missing records.
5. **Reproduction and restoration:** read-only inspection steps and verified original-state checks.

Open a [measurement issue](https://github.com/yirancheng12-design/laptop-gpu-diagnostics/issues/new?template=measurement.yml) or follow the [contribution guide](../../CONTRIBUTING.md). Share relevant sanitized excerpts rather than credentials, serial numbers, or unrelated personal data. Failed and inconclusive experiments are welcome when their limits are clear.
