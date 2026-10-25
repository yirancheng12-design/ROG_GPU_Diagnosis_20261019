# Tuning execution, baseline measurements, and restoration

[Repository home](../../README.md) · [Chinese HTML](../../ROG_G635LX_调校执行报告.html) · [Chinese baseline log](../../GPU调校基线与操作记录.txt)

**October 19, 2026 · Windows hardware session · ASUS G635LX / ROG Strix SCAR 16.** Times are Asia/Shanghai (UTC+8). This edition combines the substantially overlapping HTML and baseline-text narratives. It describes that testing phase, not every subsequent experiment in the larger ZIP archive.

## Result

Installation, backups, monitoring, and restoration checks were completed. **No additional undervolt or overclock was applied in this phase.** At the original clocks, both monitored baseline rounds produced instantaneous **104°C CPU readings**. The second round exceeded the tightened **100°C** stop guard; testing ended and original settings were restored. GPU temperature peaked at **76°C**, with no observed GPU thermal-protection trigger. The available thermal evidence did not support delivering a tuning profile labeled stable.

The official **175W** limit remained. The original **+50MHz core / +100MHz memory** offsets were restored; no custom curve or startup auto-application was enabled. These offsets predated this session and must not be described as a newly achieved overclock.

The owner confirmed an original rectangular **380W (20V DC / 19A)** adapter, a stand/cooling base, unobstructed airflow, restoration of an earlier overclock, and prior game stability. These statements were not treated as new stability-test results.

## Hardware and original settings

| Item | Recorded state |
| --- | --- |
| Device | ASUS G635LX; RTX 5090 Laptop GPU 24GB; Core Ultra 9 275HX; 32GB RAM |
| Versions | BIOS G635LX.338; VBIOS `98.03.5c.00.6f`; NVIDIA 616.92; Windows 11 Home Chinese edition, build 26200 |
| Mode | Existing Armoury Crate Turbo and Ultimate discrete-GPU mode; Windows Turbo plan retained |
| Original offsets | Official Afterburner SDK read-back: core +50MHz, memory +100MHz; custom V/F curve off, nodes not locked |
| Power | AC checked during the test; final battery discharge rate 0 and remaining capacity 87,092mWh |
| Tool | MSI Afterburner 4.6.6 / build 16757, installed under the owner's `D:\msi\MSI Afterburner` directory |

The source reports that the installer hash matched the Microsoft WinGet manifest and the installer/program MSI signatures were valid. The adapter rating was owner-confirmed; software did not establish a 225W GPU capability from it. Afterburner exposed **127 V/F nodes**. A zero UI offset, idle consumption, NVML default-limit field, or unsupported SDK field was not treated as sustained TGP.

## Cyberpunk 2077 measurements

Game **2.31**, built-in benchmark, **2560×1600**, DLSS **Quality / Transformer**, high textures, path tracing and ray reconstruction on, frame generation off. The raw conventional Ray Tracing field was `false` while Path Tracing was `true`; this is not a pure rasterization benchmark.

| Run | Performance | Power / temperature | Validity |
| --- | --- | --- | --- |
| 19:28 preliminary baseline; temporary 240 FPS cap | Mean **36.0848 FPS**; 1% low **32.279 FPS**; **64.21s / 2,317 frames** | Stable-load GPU mean **165.62W / 2104.71MHz**; peak **74°C**; no continuous CPU record | Useful as a preliminary GPU observation, not whole-system thermal or long-term stability proof |
| 20:12 automated baseline; temporary 120 FPS cap | Mean **29.6961 FPS**; 1% low **8.9895 FPS**; **68.90s / 2,046 frames** | GPU limit was **55W** during part of the run, returning to about 175W after wake; CPU peak **104°C**, GPU peak **74°C** | **Excluded from performance comparison:** standby disturbed the conditions |
| 20:15 awake baseline; temporary 120 FPS cap | Incomplete; no valid score | Effective limit **169.85–175W**, no repeat 55W episode; GPU peak **76°C**, CPU again **104°C** | Temperature stop and automatic restoration; no further tuning runs in this phase |

There was no completed post-tuning result in this phase, so a measurable undervolt/overclock gain was **not established**. Baselines under different conditions are not a before/after A/B test. Removing standby interference is not an overclocking gain.

The recorded 1% low is the reciprocal of the mean frame time of the slowest 1% of frames, with the frame count rounded upward. It is not the game's displayed minimum FPS. GPU telemetry was sampled about once per second, permitting only approximate alignment with frame-level data. Native results, frame times, and samples were preserved where available in the packages.

## Finding 1: the 55W interval coincided with Modern Standby

| Time | Event / observation |
| --- | --- |
| 20:09:30 | Kernel-Power 506: entered Modern Standby after Idle Timeout |
| 20:12:06–20:12:58 | Effective GPU limit 55W; load clocks approximately 577–667MHz |
| 20:12:58 | Kernel-Power 507: keyboard input caused wake |
| 20:12:59 | Next sample limit 172.52W, then approaching 175W |

This temporal match strongly supports standby involvement. It does not fully identify the internal driver/firmware mechanism. The next run used Windows `SetThreadExecutionState` to request system/display wakefulness only during the test; it did not rewrite the permanent power plan. The request was released at completion. That run did not repeat the 55W limit.

## Finding 2: insufficient verified CPU thermal margin

The 104°C readings occurred at **20:13:22.567** and **20:16:56.502**. At the second observation, GPU readings were **76°C / 170.78W** and CPU package power was approximately **44.86W**. Power and temperature sampling were not strictly synchronized: second-level power data cannot exclude shorter turbo spikes or establish a cooler fault.

The source cites **105°C** as Intel's maximum operating temperature for the 275HX. A 104°C reading alone does not establish damage or sustained thermal throttling. Stopping was a conservative decision aligned with the owner's stability priority. CPU thermal-throttling flags were not independently recorded, and no continuous GPU voltage trace was available.

After stopping, 15 light-load samples showed CPU package **62–97°C**, mean **71.87°C**, mean CPU power **11.23W**, and GPU **50°C**. This was not continuous operation at 104°C. Independent checks of package/core peaks, throttling flags, and fan speed were still needed.

## Operations and restoration

| Operation | Purpose / observed effect | Restoration or final status |
| --- | --- | --- |
| Install Afterburner 4.6.6 | Owner-authorized installation; read the official SDK, reducing repeated mouse interaction | Installation retained. Uninstalling it, and RTSS separately if installed, was optional rather than necessary for restoring settings |
| Back up configuration, 127-node curve, and shared memory | Preserve +50/+100 offsets, curve-off state, and original game configuration | Original records under member prefix `tuning/afterburner-original/`. Raw binaries are evidence, not VBIOS or universal flash/recovery images |
| Reapply original offsets through the official SDK | Validate restoration, including after the stop; no extra candidate voltage/clock was submitted | Core +50, memory +100; all 127 offsets matched, **0 differences**; curve off, lock index 0 |
| Temporarily disable frame generation and cap FPS | Measure rendered performance and limit unbounded menu rendering; no save loaded or game progress changed | Entire `UserSettings.json` restored after each round; SHA-256 matched the backup; original frame-generation/cap settings returned |
| Monitor thermal, power, and event state | Check GPU protection, CPU, AC, telemetry validity, and related System errors; stop the session's game after the second 104°C reading | Test processes closed; no residual monitoring or wake request; original power plan retained |
| Temporarily inhibit standby | Isolate the standby issue; awake run retained 169.85–175W but failed the CPU guard | Request released in `finally`; display/sleep timeouts were not rewritten |

The source's final check found the game closed, the game configuration hash unchanged, and **0 new GPU / Display / WHEA events** in the **19:45–20:20** query window. Startup auto-apply, constant voltage, and unlocked voltage control were not enabled. BIOS, VBIOS, driver, and hardware protections were not changed in this phase.

Original game-settings SHA-256:

```text
FDE88E654A0EF4A58D308371CC68B0AC5BF759267BEEC2675D7C2F40F76E8C76
```

Backup member: `tuning/Cyberpunk-UserSettings-before.json`. The recorded target was `%LOCALAPPDATA%\CD Projekt Red\Cyberpunk 2077\UserSettings.json`. The source says it was already restored, so no repeated copy was needed. These are historical identifiers, not repository-relative executable instructions.

## Further options and their limits

| Priority | Proposed action | Benefit boundary / trade-off | Restoration |
| --- | --- | --- | --- |
| 1 | Cross-check CPU thermals and fans | Determine whether peaks represent a core hotspot, turbo transient, or measurement difference. Airflow was already owner-confirmed clear. No FPS promise. If independent tools repeatedly confirm readings near the cited maximum, the source recommends ASUS evaluation of fans/contact/firmware rather than disassembly of liquid-metal cooling | Exit read-only monitoring; no hardware change |
| 2 | Evaluate CPU/GPU allocation within official Armoury ranges | Smaller CPU turbo budgets might smooth GPU-bound games, but CPU-bound games can lose performance. Not executed; no universal "45W / 65W is stable" claim | Save the current configuration, then restore Turbo and verify +50/+100 |
| 3 | Evaluate a GPU V/F curve after thermal conditions pass | Aim for efficiency/frequency within 175W, preserving dynamic clocks and the original memory setting. Gain may be zero; overly low voltage/high clocks can cause artifacts or resets. No validated voltage point was delivered | Restore the backed-up curve/offsets; verify curve off, +50/+100, no startup auto-apply. Afterburner's default Reset may mean 0/0, not this session's baseline |
| 4 | Assess memory tuning and CPU undervolting separately | Not tested; memory errors can reduce performance without an immediate crash. CPU support/protection policy was unverified; no firmware/protection bypass was proposed | Save and restore each original setting separately; do not combine variables |
| 225W | No official delivered solution | Cited G635LX specification remains 150W + 25W, up to 175W. A 380W adapter does not establish 225W sustained GPU capability | Retain the official limit |

Before resumed tuning: remove standby interference, establish trusted thermal/fan monitoring, and complete repeat runs at the original settings. Then use at least three matched before/after runs recording frame time, power, clocks, and temperatures, followed by longer load and light/heavy transitions. Short-term passes do not prove absolute long-term stability.

## Evidence and source references

The [tuning ZIP](../../ROG_G635LX_调校证据.zip) contains this phase's records. The [larger GPU test ZIP](../../GPU超频测试证据.zip) also contains later GPU-only tests, so its full contents must not be described as the same no-additional-tuning phase.

| Evidence | Member path in the tuning ZIP |
| --- | --- |
| Restoration verification | `tuning/restore-verification.json` |
| Initial control and curve | `tuning/afterburner-original/control-initial.json` |
| Final control | `tuning/final-control.json` |
| Preliminary native result | `tuning/benchmark_2026-10-19_19-28-16/summary.json` |
| Preliminary GPU telemetry summary | `tuning/baseline-summary.json` |
| Excluded automated baseline | `tuning/baseline-auto-1/analysis.json` |
| Standby/wake events | `tuning/baseline-auto-1/standby-events.json` |
| Automated run samples | `tuning/baseline-auto-1/telemetry.csv` |
| Awake-run stop/session | `tuning/baseline-awake-1/session.json` |
| Awake-run samples | `tuning/baseline-awake-1/telemetry.csv` |
| Restoration read-back | `tuning/baseline-awake-1/gpu-restore.json` |
| Post-stop observation | `tuning/post-stop-idle.csv` |

The control interface was documented in the installed SDK's `MACMSharedMemory.h`, `MAHMSharedMemory.h`, and official examples. This phase used standard clock/curve restoration through shared memory, not register, I²C, firmware-write, or protection-bypass interfaces.

Historical references from the source: [ASUS specifications](https://rog.asus.com/laptops/rog-strix/rog-strix-scar-16-2025/spec/), [Intel 275HX specifications](https://www.intel.com/content/www/us/en/products/sku/242293/intel-core-ultra-9-processor-275hx-36m-cache-up-to-5-40-ghz/specifications.html), [Microsoft SetThreadExecutionState](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setthreadexecutionstate), and [MSI's tuning guide](https://www.msi.com/blog/msi-afterburner-overclocking-undervolting-guide).

Restoration statements were based on read-back or file hashes. Planned tuning was not presented as executed work, and performance claims were limited to recorded results.
