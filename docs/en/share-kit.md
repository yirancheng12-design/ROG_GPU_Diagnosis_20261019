# Share the findings, with enough context

[Home](../../README.md) · [55W case](case-55w.md) · [Growth measurement](growth-playbook.md)

The following are **unpublished drafts**, not testimonials or evidence of popularity. Edit them for your own voice and the destination's rules, disclose that you maintain the project, and link to the relevant case. No external messages or posts are sent by this repository.

## English technical-community draft

**Title:** A 55W GPU limit during Modern Standby: a G635LX telemetry case

I maintain a small open-source laptop GPU diagnosis project. In one G635LX / RTX 5090 Laptop recording, the first 57 of 107 samples showed a 55W limit. The next sample after wake was 172.52W; the limit fluctuated before approaching 175W. A separate awake run stopped after a 104°C CPU reading, so I am not presenting this as a successful tuning result.

The repository contains the original evidence, a short case study, and a Python standard-library analyzer that reads the CSV directly from a ZIP. It separates measured draw from the effective power limit and makes no automatic root-cause or FPS-gain claim.

Case and reproduction command: [55W case](https://github.com/yirancheng12-design/laptop-gpu-diagnostics/blob/main/docs/en/case-55w.md).

Has anyone recorded a comparable standby/wake power-limit transition on another laptop? Timestamped samples and the active OEM profile would be useful comparisons.

## 中文技术社区草稿

**标题：** ROG 显卡为什么出现 55W 上限？一次待机与唤醒日志对照

我整理并开源了一次 G635LX / RTX 5090 Laptop 的诊断记录：107 个采样中，最初 57 个的功耗上限为 55W；唤醒后的下一次采样为 172.52W，之后仍有波动，再接近 175W。另一次保持唤醒的测试因 CPU 104°C 读数而停止，所以这不是“调校成功”或“性能提升”的展示。

项目提供原始证据、时间线和只读 Python 分析工具，可以区分实际耗电与驱动功耗上限，不会自动修改电脑设置。

[查看中文入口与复现方法](https://github.com/yirancheng12-design/laptop-gpu-diagnostics/blob/main/README.zh-CN.md)。如果有其他机型的类似记录，欢迎补充环境、时间戳和数据，帮助判断哪些现象可以重复。

## Short link caption

> GPU power draw is not GPU power limit. This case follows a 55W limit through standby and wake, with the original CSV and a read-only analyzer. One machine, documented uncertainty, no claimed FPS gain.

## A short demonstration outline

1. Show the question and the [recorded-sample chart](../../assets/telemetry-preview.png).
2. Run `python tools/demo.py` from a full clone, showing actual terminal output.
3. Show the 55W timeline and explain why the invalid baseline is excluded.
4. Link the case, data, and issue form; invite a specific technical correction or comparison.

If recording a video, capture a real command run rather than fabricating terminal output. Present the CPU peak as a recorded sample, not a universal damage threshold.

## Before sharing

- Choose a community whose members actually encounter the problem; read its current rules first.
- Answer a relevant question with a useful explanation before adding a project link. Do not paste the same promotion into unrelated issues or discussions.
- Ask for comparison data or feedback rather than coordinated votes/stars.
- Hacker News currently prohibits generated or AI-edited posts and automated posting; these drafts are **not for HN**. Any HN submission must be independently written by the human author and follow the [HN guidelines](https://news.ycombinator.com/newsguidelines.html).
- Use `assets/telemetry-preview.png` as a repository-file image. Uploading it to GitHub's social-preview setting is a separate maintainer action; this file alone does not change that setting.
