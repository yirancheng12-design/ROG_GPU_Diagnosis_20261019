# GPU power and performance diagnosis

[Repository home](../../README.md) · [Chinese source](../../ROG_G635LX_GPU诊断报告.html)

**Device:** ROG Strix SCAR 16 G635LX / RTX 5090 Laptop GPU 24GB. **Diagnosis:** October 19, 2026, Asia/Shanghai (UTC+8). **Final check for this phase:** 18:53:41.

This English edition covers the initial diagnostic phase. Later testing is documented in the [tuning report](tuning-report.md) and [225W chronology](power-225w-retest.md); statements about work not attempted here apply to this phase only.

## Conclusion and scope

The recorded OEM design and driver-enforced GPU ceiling were **175W**. A 225W target exceeds the cited specification; no official configuration path meeting the requested long-term stability goal was verified on this machine. Turbo and discrete-GPU output were already enabled. Existing GPU timeout records took priority over adding another 50W.

This phase did not flash BIOS/VBIOS, increase power, temperature, voltage, or clock targets, or disable protections. It completed hardware/version identification, data preservation, specification and update research, mode/tuning checks, approximately 90 seconds of passive sampling, stability-log review, and an optimization/restoration assessment. Sustained full-load TGP, controlled before/after FPS or scores, and long-term stability were not established. Stress testing stopped at the existing-timeout condition; desktop readings were not substituted for benchmark results.

225W is **28.6% more power** than 175W. That is not a measured performance gain.

## 1. Hardware, versions, and original state

| Item | Recorded result | Interpretation |
| --- | --- | --- |
| Platform | ASUSTeK ROG Strix SCAR 16 G635LX_G635LX | SMBIOS and Armoury Crate agreed on the 16-inch platform. The readable SMBIOS did not establish a sales-SKU or regional suffix. |
| GPU | RTX 5090 Laptop GPU; 24GB GDDR7; 10,496 CUDA cores | NVIDIA App and nvidia-smi; 24,463 MiB visible. The roughly 4GB Win32_VideoController AdapterRAM field does not represent the actual VRAM capacity. |
| VBIOS | `98.03.5c.00.6f` | Cross-checked in NVIDIA App and nvidia-smi. This phase did not back up or flash a ROM, or establish that it was the factory-original ROM. |
| System BIOS | `G635LX.338`; SMBIOS date 2026-06-04 | An internal BIOS date can differ from a download-package publication date. |
| NVIDIA driver | Game Ready 616.92 / Windows 32.0.16.1692 | NVIDIA App release date 2026-09-09; Windows file date 2026-09-04. These are different date fields. |
| CPU / RAM / OS | Core Ultra 9 275HX, 24 cores / 24 threads; 32GB; Windows 11 Home, Chinese edition, 10.0.26200 | Windows CIM and NVIDIA App. |
| Adapter | Original 380W rectangular connector, 20V DC / 19A | Confirmed by the owner, not read from the label by software. AC was online; no charging/discharging was recorded during sampling. |
| Performance mode | Turbo in Armoury Crate and Windows | Checked before and after the component installation; the power-plan GUID was preserved. |
| Display path | Discrete GPU; internal display on RTX 5090; 2560×1600 / 240Hz / G-SYNC | Armoury Crate and NVIDIA agreed. Advanced Optimus reporting "No" in fixed discrete mode does not establish absence of the hardware feature. |
| Dynamic Boost | Enabled; manual editor allowed 25W | This confirms availability/configuration range, not an extra 25W of desktop consumption. |
| NVIDIA automatic tuning | Off; NVIDIA tuning offset +0MHz | This is the NVIDIA App's additional offset, not proof that all ASUS or third-party offsets are zero. |
| Platform drivers | NVIDIA Platform Controllers and Framework; ASUS System Control Interface v3: Status OK, error 0 | Successful enumeration does not exclude software defects elsewhere in the stack. |
| PCIe | Current Gen 5 ×8; GPU capability maximum ×16 | A read-only snapshot, not a bandwidth test or sufficient evidence of a fault. |

The original report cites [ASUS G635 specifications](https://rog.asus.com/laptops/rog-strix/rog-strix-scar-16-2025/spec/). Its referenced `system-inventory.json`, initial NVIDIA snapshots, and UI text are discussed in the [coverage audit](evidence-coverage.md); a reference does not guarantee that the file is published.

## 2. Evidence for the 175W limit

| Evidence | Recorded value | Meaning |
| --- | --- | --- |
| ASUS specification cited in the source | 150W + 25W Dynamic Boost = 175W | The dynamic allowance is already included; it must not be counted twice. |
| Initial nvidia-smi | Current 175W; maximum 175W; requested N/A | The exposed driver/firmware range ended at 175W. N/A means unavailable, not zero. |
| NVIDIA system details | Maximum graphics power 175W; Dynamic Boost enabled | Agrees with the specification and lower-level readout. |
| Armoury Crate home | Turbo; Max TGP 175W | The machine was not merely restricted by Silent mode. |
| Manual editor, not applied | TGP up to 150W; Dynamic Boost up to 25W; temperature target 87°C | Viewing the range did not apply a new profile or change Turbo mode. |

The 175W ceiling reflects the OEM power policy implemented through the NVIDIA driver/platform-firmware chain. Software telemetry cannot uniquely assign every watt to VBIOS, EC, or a driver component. This phase performed no firmware reverse engineering or forced power-limit writes.

Why a particular game does not reach 175W is a separate question. It requires synchronized workload data for utilization, CPU/GPU power, temperature, clocks, and limiting flags. Full-load reproduction was not performed in this phase, so a game-specific bottleneck was not established.

| Possible constraint | Observation | Limit of the conclusion |
| --- | --- | --- |
| GPU power cap | Multiple sources agreed on 175W; SW Power Cap was inactive in light load | An inactive flag at light load says nothing about full-load capping. |
| Dynamic Boost / CPU competition | Effective limit was 175W in 84 of 85 samples and 172.59W once | A single adjustment does not identify CPU competition, dynamic policy, or a service update as its cause. Continuous CPU/full-load data were missing. |
| Thermals | GPU 54–56°C; SW/HW Thermal Slowdown inactive | No throttling in this window; memory, hotspot, VRM, and full-load thermal margin were not tested. |
| Whole-system power | Owner-confirmed 380W adapter; AC online; battery discharge 0; HW Power Brake inactive | No light-load indication of power braking or battery supplementation. Wall power, ripple, connector temperature, and combined CPU/GPU load were not measured. |
| Software stability | Repeated historical 0x141 and nvlddmkm errors; automatic tuning currently off | Investigate this independently of the official 175W ceiling. |

The **95W Default Power Limit** field is not proof of a current 95W restriction and is not the ASUS 150W base TGP. Interpret current/maximum values alongside the platform's dynamic-power definition. The reported **14,101MHz** memory clock is that sensor's convention, not a newly calculated effective data rate; NVIDIA details reported **28.00Gbps**.

The sampled `Reliability` flag was Active; other collected power, thermal, external-power, and board-limit flags were Not Active. The local nvidia-smi help describes Reliability as a frequency constraint for expected device lifetime. It is not a damage diagnosis and was not bypassed. Initial cumulative SW Power Capping and SW Thermal Slowdown counters were both **539,916,314μs** and did not increase in the later snapshot. Cumulative counters without event temperatures/times do not prove overheating in this session.

A transient peak or a software field displaying 225W would not prove sustained 225W, VRM headroom, or long-term stability.

## 3. Measurements and validity

Passive trace: **18:39:02–18:40:32**, 85 samples, approximately 1.06 seconds apart. The existing AC/Turbo/discrete-GPU environment and applications remained. No game or stress workload was launched. Armoury component installation/UI rendering and background applications could contribute load. This was neither a clean idle baseline nor a thermally settled game benchmark. Ambient temperature and placement were not independently verified.

| Metric | Mean | Minimum–maximum |
| --- | ---: | ---: |
| GPU Average Power Draw (W) | 62.99 | 62.24–65.85 |
| GPU instantaneous power (W) | 63.00 | 61.88–66.42 |
| GPU core temperature (°C) | 54.44 | 54.00–56.00 |
| GPU core clock (MHz) | 2393.74 | 2362.00–2505.00 |
| Memory clock, driver convention (MHz) | 14101.00 | 14101.00–14101.00 |
| GPU utilization (%) | 15.62 | 15.00–30.00 |
| Effective power limit (W) | 174.97 | 172.59–175.00 |

Battery RemainingCapacity stayed at **87,092mWh**, discharge rate 0, AC online. A separate NVIDIA performance-page snapshot showed GPU **46W / 51°C / 2047MHz / 9%** and CPU **9.786W / 66°C / 6%**. Their approximately **55.8W** sum is neither wall power nor a full-load CPU/GPU budget; sensor updates were not guaranteed synchronous.

The manual editor showed CPU PL1 **140W**, PL2 **175W**, and GPU offsets **+50MHz core / +100MHz memory**. Those were unapplied manual settings, not measured active Turbo CPU limits. Adding CPU PL2 to GPU TGP does not establish sustainable total power. Turbo displayed ROG Boost O.C.; a historical `UserOC` label alone cannot identify extra user overclocking.

There was no controlled hardware-parameter A/B change in this phase. Armoury auto-updated, so software conditions also differed. FPS, 1% low, and scores were **not measured**, rather than zero. Sustained 175W and 225W were not tested. No newly filtered GPU/WHEA/unexpected-shutdown event was found through **18:53:41**, but that short window does not invalidate historical timeouts or certify stability.

## 4. Stability evidence

The available preceding seven-day logs contained **7 nvlddmkm event 153 entries** on October 16–17 and **21 application 0x141 report entries**, referencing **8 distinct WATCHDOG filenames**. Queuing/archiving can duplicate entries: neither count is an exact count of independent crashes.

| Local time | Evidence | Interpretation |
| --- | --- | --- |
| Oct 16, 12:26–13:36 and around 21:33; Oct 17, around 15:54 and 23:58 | LiveKernelEvent 141; bucket includes `nvlddmkm.sys_Blackwell_UserOC` | A display engine did not respond in time. This live-dump code does not automatically mean a blue screen. Clock, driver, game, display-path, and hardware causes were not distinguished; dumps were not debugged. |
| Oct 16, 12:28–12:29 | 0x193 graphics-kernel live-dump entries | Relevant to display-stack investigation; not separately decoded or attributed. |
| Oct 18, 10:32 startup | Kernel-Power 41 and EventLog 6008, referring to an unexpected shutdown at 00:16:38 | Event 41 alone does not prove an inadequate adapter or a shared cause with earlier GPU timeouts. |
| Oct 18, 10:32 | Informational WHEA-Logger 3 | Preserved as recorded, not classified as a confirmed uncorrectable CPU/GPU hardware failure. |
| Oct 17, 01:06 | ArmouryCrate.UserSessionHelper.exe 6.5.10.0 application exception | A historical control-software exception, not proof that it caused the GPU timeout. |

See the [Microsoft 0x141 definition](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/bug-check-0x141---video-engine-timeout-detected) cited by the source. Only event text/XML and referenced paths were exported; WATCHDOG kernel dumps were not successfully opened/debugged or uploaded in this phase. The owner had confirmed the adapter but had not supplied corresponding symptom descriptions. Automatic tuning being off does not mean a current extra overclock was found and fixed.

## 5. 225W feasibility and historical update research

The source found no official G635LX 225W certification. A 380W adapter rating does not establish the GPU branch, VRM, connectors, memory, or cooling capacity for another 50W. The cited [ASUS 2025 launch material](https://press.asus.com/news/press-releases/asus-rog-2025-gaming-laptop-lineup/) describes up to **240W system-level** thermal capability, not 240W exclusively for this GPU or a measurement on this laptop.

The observed official UI/driver configuration ended at 175W. This does not prove every unofficial experiment physically impossible. A reversible software target also does not make possible hardware damage reversible. This phase tried no unofficial over-spec tool, cross-model VBIOS, shunt modification, or protection bypass. Existing timeouts and unmeasured VRM/hotspot/combined-load behavior did not support the requested long-term stability goal. More power does not scale linearly to FPS.

The following are **listings recorded on October 19**, not independently refreshed download recommendations:

| Item | Source report's finding | Action/status |
| --- | --- | --- |
| BIOS | Installed 338; listed 340. Windows package date 2026-10-16; EZ Flash date 2026-08-12; general performance wording | Not run or flashed. No explicit 225W or local 0x141 fix was established. SKU support, power, backups, and encryption-recovery preparation would be needed before a separately authorized update; downgrade availability was not guaranteed. [Recorded ASUS page](https://www.asus.com/jp/supportonly/g635lx/helpdesk_bios/) |
| ASUS OEM NVIDIA driver | US page listed 32.0.15.9191 / 591.91, dated 2026-02-26; installed 616.92 | A compatibility comparison candidate, not automatically more stable because it is older. Applicability and region require checking. Not installed. [Recorded ASUS page](https://www.asus.com/us/supportonly/g635lx/helpdesk_download/) |
| NVIDIA driver | Report listed Game Ready 617.42, dated 2026-10-06 | Not installed; no promised timeout fix or power increase. A matching version number on another product's package is insufficient. [Recorded NVIDIA entry](https://www.nvidia.cn/drivers/details/280171/) |
| Armoury components | Service 6.5.14.0 before launch, 6.7.6.0 afterward; ROG Live Service 3.7.6.0 appeared | Opening the existing app triggered its installer without a manual update-button click. Turbo/175W remained. This was a real software change, not a demonstrated performance improvement. Exact rollback was not performed or guaranteed. |

## 6. Optimization options recorded for future evaluation

Baseline: Turbo, discrete output, original 380W adapter. With no controlled game data, the source did not assign unsupported percentage gains. Stability and frame-time improvements must not be presented as an average-FPS increase.

| Priority | Proposed action and expected boundary | Trade-off, restoration, and phase status |
| --- | --- | --- |
| 1 | Retain the already enabled official performance path | Repeating Turbo/discrete/adapter selection adds no demonstrated gain. Discrete idle power and fan noise remain; no change was needed. |
| 2 | Establish a stable baseline without additional tuning; audit tools, offsets, and game settings | Save settings before single-variable changes. A zero-additional-offset comparison might reduce peak scores. Do not infer active offsets from an unapplied editor or a UserOC tag. Only NVIDIA automatic tuning was checked; other settings were not changed. |
| 3 | Compare one appropriate official driver in the same failure scenario | FPS could improve, stay flat, or fall. Preserve the existing installer/settings for reinstallation. No force-cleaning or TDR-timeout masking was performed; candidates were researched only. |
| 4 | Reduce unwanted background GPU activity one item at a time | Benefit depends on actual contention. Closing recording/remote tools can interrupt needed work; GameViewer and other existing programs were not terminated. Restarting the feature restores it. |
| 5 | Verify airflow and official fan behavior when logs show thermal limitation | Without throttling, FPS benefit may be near zero. Higher fan speeds add noise. No fan-curve change or disassembly occurred; liquid-metal/cooling service belongs with qualified personnel. |
| 6 | Adjust official CPU/GPU budgets only if logs establish competition | GPU already sustaining 175W gains no extra TGP. Excessive CPU limits can worsen 1% low. Record PL1/PL2/fans and restore Turbo; no adjustment was made. |
| 7 | Evaluate voltage/frequency efficiency at the same power after stability is established | Results vary by unit/workload; crashes, computation errors, and memory errors are possible. No fixed internet voltage/clock profile or extra overclock was applied in this phase. |
| 8 | Adjust per-game expensive effects or DLSS settings | Image quality, latency, and artifacts trade off against performance. Separate generated/displayed FPS from base rendering FPS. No game setting was changed in this phase. |
| Excluded in this phase | Raise GPU power to 225W | Exceeds the verified official ceiling; long-term stability and recoverability were not established. No over-spec write was performed during this phase. |

## 7. Proposed controlled test procedure

This is a future procedure, not a completed experiment. If 0x141 persists at original clocks with an appropriate official driver, the report prioritizes ASUS analysis of logs and necessary dumps over performance exploration.

1. Fix the adapter, placement/cooling, software versions, display mode, battery state, and background processes; record ambient temperature. Finish component installation before testing. Preserve needed remote sessions.
2. Fix the game version, resolution, graphics, ray tracing, and DLSS. Disable frame generation for hardware-performance comparison. Cyberpunk's built-in benchmark or a fixed 3DMark version/preset can be used; report Graphics Score separately from total score. FrameView was available but not launched in this phase.
3. Begin with a short reproduction, extending only with controlled temperatures and no errors. After warm-up, run the same scene at least three times and report the median. Change one variable, repeat, then restore A and retest to check drift.
4. Record GPU average/peak/sustained power, effective limit, clocks, temperature, utilization, and limiting flags; CPU package power/temperature; battery supplementation; FPS, 1% low, frame times, and scores. Mark unavailable memory/hotspot/VRM temperatures as unavailable rather than substituting core temperature.
5. The original proposed conservative stop examples were GPU core **≥85°C for about 10 seconds**, CPU **≥95°C for about 30 seconds**, thermal throttling, abnormal external power braking, AC loss, or abnormal sustained battery discharge. These were early-stop criteria, not manufacturer damage limits. Artifacts, resets, black screens, computation errors, or unusual odor called for immediate stopping. Later test phases used different, explicitly recorded CPU guards.
6. Stop the workload and restore the single changed setting plus the recorded original profile. Preserve before/after logs. Any score difference must exceed natural repeat variation without worse 1% low or errors. Longer real-use testing still establishes stability only for tested conditions, not lifetime reliability.

## 8. Operation audit and end-of-phase state

CIM, nvidia-smi, powercfg, device checks, and event reads were read-only. Logs were not cleared. The existing Armoury app auto-installed updated components; the installer was not forcibly interrupted or rolled back. The manual editor was viewed without applying, saving, or editing sliders, then exited. The passive sampler ended without a resident task. NVIDIA performance/system pages were viewed without changing tuning. Web research did not run driver or BIOS installers.

At **18:53:41**, Windows remained on Turbo; current/maximum GPU limits were 175W; BIOS 338, VBIOS `98.03.5c.00.6f`, and driver 616.92 were unchanged; AC was online and the battery was not discharging. The final GPU snapshot was **53°C / 47.54W**. No hardware-tuning change from this phase needed rollback. Armoury auto-update prevents describing the entire system as unchanged. Evidence files are not a disk image, firmware backup, or system restore point.

## 9. Screenshots, original records, and references

The Chinese HTML contains embedded screenshots of the unapplied 150W + 25W manual configuration and NVIDIA tuning off / +0MHz with light-load CPU/GPU values. These screenshots retain their original labels.

The source describes initial NVIDIA text/XML, inventories, telemetry/statistics, events/XML, stability records, screenshots, update research, operation records, and a final state. It says those records were not sent to ASUS/NVIDIA or another third party during that phase. **Publication note:** the files present in this public repository are now publicly accessible; that historical statement is not a privacy claim about this repository.

Named review targets include `nvidia-smi-initial.txt`, `passive-telemetry.csv`, `application-stability-events.json`, `stability-event-summary.csv`, `nvidia-system-details-ui.txt`, `action-record.json`, and `final-state.json`. Use the [evidence guide](evidence-guide.md) and [coverage audit](evidence-coverage.md) to distinguish published members from absent references. Minute-based report filenames and log counts do not directly count failures.

The source also cites [ASUS Armoury Crate modes](https://rog.asus.com/support/faq/1043747/) and [NVIDIA control-panel documentation](https://www.nvidia.com/content/Control-Panel-Help/vLatest/en-gb/mergedProjects/nv3dENG/Manage_3D_Settings_%28reference%29.htm). The precise flag interpretation was based on local `nvidia-query-help.txt`; differences between official material and telemetry were retained rather than replaced with marketing figures.

**End-of-phase judgment:** keep the official 175W ceiling and investigate stability first. No measured performance gain or safe 225W operating point was established. Controlled full-load and failure-reproduction work remained deferred.
