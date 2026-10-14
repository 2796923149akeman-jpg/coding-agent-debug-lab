# Coding Agent 课堂实操：从修 Bug 到完成文件整理任务

同一个仓库，两个独立练习。先用成绩统计体验“读取 → 测试 → 修复 → 验收”，再用照片整理体验“理解需求 → 编写程序 → 实际运行 → 自检 → 迭代”。

| 练习 | 内容 | 建议时间 | 依赖 |
| --- | --- | --- | --- |
| [01 成绩统计](labs/01-grade-stats/README.md) | 修复空白成绩处理，保留原有三个测试 | 15～20 分钟 | Python 标准库 |
| [02 照片整理](labs/02-photo-organizer/README.md) | 将 205 个混杂文件分类归档，识别重复，保留完整记录 | 30～50 分钟 | Python + Pillow |

## 下载与开始

1. [下载两个案例的固定课堂版本 ZIP](https://github.com/2796923149akeman-jpg/coding-agent-debug-lab/archive/refs/tags/classroom-v2.zip)，解压到新文件夹；无需 GitHub 账号或 Git。
2. 选择一个 `labs` 子目录，在该目录打开终端和 AI 工作区，先阅读它的 README。
3. 根据该案例的提示词操作，保留实际运行输出和修改记录。

也可使用 Git：

```sh
git clone https://github.com/2796923149akeman-jpg/coding-agent-debug-lab.git
cd coding-agent-debug-lab
```

**不要在仓库根目录直接运行成绩测试。** 应先进入 `labs/01-grade-stats`。照片素材必须先运行 `prepare.py` 初始化，不能把 ZIP 本身交给整理程序当作输入。

推荐 Python 3.10+。Windows 可以用 `py` 替代 `python`，macOS / Linux 可以用 `python3`。照片练习安装依赖需要联网，素材初始化和本地运行不需要联网。AI 工具的账号与网络要求由各自服务决定。

## 给汇报者和同学

- [两人汇报的实操安排](docs/CLASSROOM_GUIDE.md)：45 分钟与课后练习两种安排。
- [两套提示词入口](docs/STUDENT_PROMPTS.md)：先复现再修改，不把预测输出当实测。
- [练习记录模板](docs/EXPERIMENT_REPORT.md)：记录真实命令、结果、差异和人工判断。
- [AI 辅助生成与来源](docs/AI_GENERATION.md)：说明哪些是已有材料，哪些是本次整理。
- [文件规范与版本说明](docs/REPOSITORY_STRUCTURE.md)。

公开内容为学生版，不含照片整理参考程序、答案索引或正确归档结果。成绩练习故意保留错误：初始 3 个测试中 2 个报错是正常状态。照片数据是程序生成的教学素材，视频是用于分类练习的占位文件，不代表可播放的视频。

## 原成绩案例的旧链接

原仓库地址保持不变。[`classroom-v1` 的旧版 ZIP](https://github.com/2796923149akeman-jpg/coding-agent-debug-lab/archive/refs/tags/classroom-v1.zip) 仍可下载，内部仍是原来的单案例目录；新资料统一使用 `classroom-v2`。
