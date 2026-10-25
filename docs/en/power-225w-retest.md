# 225W retest and evidence chronology

[Repository home](../../README.md) · [Chinese source](../../ROG_G635LX_225W复试结果.html)

**Device:** ASUS G635LX / RTX 5090 Laptop, NVIDIA 616.92. **Date:** October 19, 2026, Asia/Shanghai (UTC+8).

## Editorial note: read the phases separately

The original HTML combines an early failed retest with a later appended banner. The banner says a **225W driver limit** subsequently took effect, a **175W baseline** hit **102°C CPU**, no 225W load test occurred, and an override was removed with a normal restart in progress. Its linked later report is absent from this repository. That is a historical reported claim, not independently verified completion of the later phase.

The packaged pre-restart JSON provides a narrower, directly inspectable fact: at **23:43:42**, an override was written and read back, but **live current and maximum limits remained 175W**, **a restart was required**, and **no stress test had started**. It cannot prove the banner's later post-restart, temperature, or restoration claims.

| Phase | Available account / record | What can be concluded |
| --- | --- | --- |
| 22:37 driver retest | HTML narrative; raw probe files referenced but absent | Reported failure to load the experimental driver; no power IOCTL or load test in that attempt |
| 22:45 standard API | HTML narrative; referenced request/read-back JSON absent | Reported unsupported request, with 175W read back; exit code 0 was not success |
| 23:43 registry experiment | Result and plan JSON present inside the pre-restart ZIP | Write/read-back succeeded; both live limits still 175W, restart pending, no stress test |
| Later banner | Banner present; linked follow-up HTML missing | A reported 225W limit/CPU-stop/restoration sequence, without the linked supporting follow-up; no demonstrated sustained 225W |

This chronology is an editorial addition based on the preserved sources. No new power changes or hardware tests were run to produce the English edition.

## Early retest: driver-load failure

The source says the first reboot did not select startup option 7; the owner then entered Advanced Startup again and replied that it was done. Windows reported a boot time of **22:32:48**. The actual menu key was not observed, so the reply alone was not proof that security policy changed.

At **22:37:48–49**, the experimental driver again failed with Windows error **577**. The temporary service was deleted. No power IOCTL, high-load test, or firmware modification occurred in this attempt. This proves only the reported load failure under that software/security configuration, not hardware support for or against 225W.

| Operation | Intended result | Reported outcome / cleanup |
| --- | --- | --- |
| Advanced Startup | Owner selects a one-boot signature-check option | Reboot completed; observed policy still rejected the test-signed driver. No persistent TESTSIGNING or integrity-disable setting was established |
| Check old driver | Confirm the pinned Nvpwr.sys hash | Hash matched the recorded file; that did not establish Microsoft trust or safety. No certificate import/trust-store change |
| Create/load demand-start service | Test loading only, without power calls | Service creation succeeded; start failed with 577. CodeIntegrity event 3004 named Nvpwr.sys. Stop reported not started; delete succeeded; no experimental service remained in the subsequent enumeration |
| Read GPU policy | Check settings before/after | Current and maximum remained 175W. There was no power write to roll back, so this was not a verified rollback from 225W |
| Query display/WHEA/crash events | Look for new errors in the probe interval | None matching the filter were reported. No FPS/score was produced; short idle checks do not prove long-term stability |

## Standard NVIDIA API request at 22:45

At **22:45**, the source records submission of the standard NVIDIA power-limit request for 225W in response to the owner's request to write and stress-test. The interface returned **"Changing power management limit is not supported in current scope"**. Immediate and final read-back stayed at **175W**. **Exit code 0 did not mean the requested setting took effect.**

The following 175W restoration request also returned unsupported. Since actual state never changed, the attempt did not verify restoration from an over-spec state. No stress test began because 225W had not taken effect. Before the request, GPU utilization was **2%** and temperature **49°C**; no experimental driver was loaded for this standard-API attempt.

The original report also records an earlier unsupported **180W** request with a 175W read-back.

## Reported code-integrity state

At **22:39:37**, the read-only `NtQuerySystemInformation(SystemCodeIntegrityInformation)` query reportedly returned **0xF405**. The source interpreted it as kernel code-integrity enforcement on, test signing not accepted, and HVCI kernel enforcement/strict mode enabled. Secure Boot remained on. It cites [Microsoft API documentation](https://learn.microsoft.com/en-us/windows/win32/api/winternl/nf-winternl-ntquerysysteminformation).

Event 3004 said Windows could not verify the file under current integrity/trust rules and mentioned a missing corresponding file hash. This does not independently classify the file as malware or separate the contributions of Secure Boot, HVCI, and the signature chain. The old driver remained blocked after that reboot. The source records no further disabling of Secure Boot/memory integrity or import of its test certificate.

## Later pre-restart experiment: packaged evidence

Download the [pre-restart evidence ZIP](../../225W新路线重启前证据_20261019.zip). Exact members:

- `power225-research-followup/apply-max225-20261019-234340-plan.json`
- `power225-research-followup/apply-max225-20261019-234340-result.json`
- `power225-research-followup/apply-max225-20261019-234340-live-power.txt`
- `power225-research-followup/latest-checkpoint.json`
- `power225-research-followup/latest-power-state.txt`

The result JSON records `Success: true` and `RegistryReadbackMatches: true`, alongside `TargetMaxWatts: 225`, `LiveCurrentStill175: true`, `LiveMaxStill175: true`, `RestartRequired: true`, `RuntimeCurrentAbove175Requested: false`, `StressTestStarted: false`, and `FirmwareFlashed: false`.

The plan identifies a registry override and `FirmwareWrite: false`. This is a real configuration write even though it is not a firmware flash. The archive includes a registry backup, a ROM backup, and a restoration script as historical evidence. Their presence does not prove that restoration ran or that physical damage would be reversible. They are not a portable profile or instructions for another device.

The file named `latest-checkpoint.json` is timestamped **23:33**, earlier than the **23:43** write. Its filename must not be treated as proof that it captures the newest state. The corresponding earlier power snapshot reports 175W current/maximum, GPU **53°C**, and approximately **47W**. Only timestamped records for the same phase should be compared.

## Performance and restoration limits

The source cites the model's official **150W + 25W Dynamic Boost = 175W** specification. It says a 380W adapter does not establish sustained 225W GPU capability. The early load failure neither measured 225W nor established sustained operation, FPS benefit, or reliable rollback.

It also mentions earlier CPU peaks of **101–104°C** and a separate short GPU test with approximately **0.89%** mean gain from an extra **+30MHz core**, later restored. That claim does not establish a stable 225W profile or a completed tuned Cyberpunk comparison. The larger GPU-test archive contains separate overclock-test records; keep the workload/phase distinction.

At the end of the **early retest**, the report says the GPU limit remained 175W, no experimental services/autostart entries remained, Afterburner curves were unchanged, and no benchmark or Afterburner session was launched in that retest. It recommended a normal reboot to clear any one-boot startup option, citing [Microsoft test-signing documentation](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/test-signing). This is a historical restoration account, not a fresh inspection of the current machine.

The original banner describes a **later** override removal with reboot in progress. Without the missing follow-up and post-reboot read-back, this edition does not mark that later restoration as verified complete.

## Missing source artifacts

The original links to a later execution report, an unofficial-scheme review, configuration/retest ZIPs, driver-load probes, integrity events, and GPU-error query files that are not all published. The exact references and whether they are found inside existing archives are listed in the [coverage audit](evidence-coverage.md). Archived backup inventories may describe omitted packages; an inventory row is not proof that its file is available here.

**Repository-level conclusion:** there is no published completed, stable 225W workload result. The early failed requests, the later pre-restart write, and the banner's unsupported follow-up must remain distinct.
