# A 55W GPU limit through standby and wake

[Home](../../README.md) · [Full case](case-55w.md) · [Installation](../../INSTALL.md)

One ROG G635LX / RTX 5090 Laptop recording contains 107 telemetry samples over 98.627 seconds. The first 57 samples show a 55W limit; the first sample after wake is 172.52W. This supports examining standby/wake behavior in this case.

The separate awake run stopped at a 104°C CPU reading. A configured 225W target did not establish a stable 225W workload result. These limits are part of the case, not omitted failures or a promised tuning gain.

## Inspect the same data

Download/extract the complete [release](https://github.com/yirancheng12-design/laptop-gpu-diagnostics/releases/latest), with Python 3.11+ installed. Double-click `Install.cmd`, then `Run.cmd`, or run `python tools/demo.py`. The standard-library tool reads the preserved archive without querying or changing your GPU.

For another machine, follow [the diagnostic workflow](diagnostic-workflow.md) and include timestamped telemetry, power/thermal conditions and excluded runs. A useful contribution is a comparable dataset or a correction, even if it shows a different result.

中文：这份发布导读围绕“55W 是否与待机有关”展示一台机器的原始记录，不把功耗上限、实际耗电与性能提升混为一谈。欢迎补充可复现的其他机型数据；请使用脱敏记录。
