# 笔记本 GPU 功耗与稳定性诊断

[English](README.md) · [原始中文资料说明](README_225W_整理说明.md)

通过真实日志，区分功耗上限、实际耗电、性能成绩与稳定性。首个案例来自 **ASUS ROG G635LX / RTX 5090 Laptop GPU**，记录日期为 **2026 年 10 月 19 日，UTC+8**。

## 先看你遇到的问题

| 问题 | 阅读入口 |
| --- | --- |
| 显卡功耗上限为什么降到 55W？ | [待机与唤醒时间线（英文）](docs/en/case-55w.md) |
| 设置了 225W，就代表运行在 225W 吗？ | [175W/225W 证据判断（英文）](docs/en/case-225w.md) |
| 怎样记录自己的电脑问题？ | [检查清单与空白数据模板（英文）](docs/en/diagnostic-workflow.md) |
| 想核对完整原始记录？ | [中文诊断报告](ROG_G635LX_GPU诊断报告.html) / [调校报告](ROG_G635LX_调校执行报告.html) / [复试记录](ROG_G635LX_225W复试结果.html) |

## 三个发现

- 55W 上限与新式待机时段重合，唤醒后的下一次采样回到 172.52W，之后仍有波动，再接近 175W。时间对应关系支持待机参与，但不能推断所有低功耗问题都是这个原因。
- 排除待机干扰后的测试仍因 CPU 104°C 读数触发停测，不能作为成功调校的成绩。
- 225W 注册表目标写入成功时，实时上限仍为 175W。原报告顶部另有后续声明，但其链接指向的后续报告未发布，因此没有可交付的稳定 225W 负载结果。

## 一条命令看实际数据

下载或克隆完整仓库，在仓库根目录使用 Python 3.11 或更新版本：

```console
python tools/demo.py
```

演示直接读取现有证据包，显示 107 个样本、98.627 秒采样跨度、最初 57 个 55W 样本等结果。无需安装第三方依赖、管理员权限或 NVIDIA 工具，不查询或修改本机 GPU。

完整分析与检查：

```console
python tools/summarize_telemetry.py --zip "ROG_G635LX_调校证据.zip" --member "tuning/baseline-auto-1/telemetry.csv"
python tools/verify_repository.py
python -m unittest discover -s tests -v
```

## 参与

欢迎提交其他机型的可复现案例、修正解释或补充缺失证据。使用 [案例表单](https://github.com/yirancheng12-design/ROG_GPU_Diagnosis_20261019/issues/new?template=measurement.yml)，记录环境、数据、排除的轮次和未知部分。原始 10 个文件与 228 个 ZIP 成员保持不变。

如果这些方法对你有帮助，可以点 Star，方便以后找到项目；也欢迎直接提交有效反馈。

原创代码与文档采用 [MIT License](LICENSE)。证据包中的第三方内容保留其原有权利和许可。此项目不提供通用超规格调校配置，也不把短时测试作为长期稳定性保证。
