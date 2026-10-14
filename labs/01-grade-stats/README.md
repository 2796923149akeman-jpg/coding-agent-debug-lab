# Coding Agent 纠错练习：成绩统计

把一个带有已知缺陷的小项目交给 AI，观察它如何阅读、运行测试、定位、修改和验证。建议练习时间 15～25 分钟。

**这是有意保留错误的教学起点。首次测试出现 `FAILED (errors=2)` 是正常现象。** 本项目用于课堂下载、修改和学习；只用 Python 标准库，无需安装第三方库，也不需要在项目中填写 API Key。

## 1. 下载并打开

- [直接下载 ZIP](https://github.com/2796923149akeman-jpg/coding-agent-debug-lab/archive/refs/heads/main.zip)，解压到一个新的文件夹。进入解压后的 `coding-agent-debug-lab-main/labs/01-grade-stats` 文件夹并打开终端，应能看到 `grade_stats.py`。
- 或者安装 Git 后执行：

```sh
git clone https://github.com/2796923149akeman-jpg/coding-agent-debug-lab.git
cd coding-agent-debug-lab/labs/01-grade-stats
```

ZIP 方式不需要 Git 或 GitHub 账号。[GitHub 官方下载说明](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives)。Python 可从 [Python 官网](https://www.python.org/downloads/) 获取；建议使用 Python 3.10 或更高版本。本次发布在 Python 3.13.9 上验证。

## 2. 亲手运行初始测试

```sh
python --version
python -m unittest -v
```

Windows 中若 `python` 不可用，可以把命令里的 `python` 替换为 `py`；macOS / Linux 常用 `python3`。如果显示 `Ran 0 tests`，通常是所在文件夹不对，先进入含 `test_grade_stats.py` 的目录。

初始状态应显示：共 3 项测试，1 项通过、2 项报错，最后一行为 `FAILED (errors=2)`。保存这次输出，再让 AI 修改。

## 3. 交给 AI 纠错

**能访问本地文件和终端的编程 Agent：** 将解压后的项目文件夹作为工作区，按 [分步提示词](docs/STUDENT_PROMPTS.md) 依次操作。只给它这份练习项目即可。

**普通聊天 AI：** 上传或粘贴 `grade_stats.py`、`test_grade_stats.py`、`data/scores.csv`，再附上测试报错。按同一份提示词提问；把它给出的修改保存到本地，然后自己运行命令，把真实输出发回去。不要把 AI 预测的输出当作实测结果。

先明确业务规则：空白或只有空格的成绩不计入平均分，但计入未填写人数；全部空白时 `average=None`；平均分保留两位小数。基础练习只修改 `grade_stats.py`，保留现有测试和示例数据。

## 4. 验收

```sh
python -m unittest -v
python grade_stats.py data/scores.csv
```

修复后必须满足：

| 检查 | 预期 |
| --- | --- |
| 原有三项测试 | `Ran 3 tests`，`OK` |
| 80、空白、90 | 平均分 `85.0`，未填写 `1` 人 |
| 全部空白（包含空格） | `average=None`，未填写人数正确 |
| 修改范围 | 未更改、删除或跳过现有测试，未硬编码示例答案 |

使用 Git 克隆的同学再运行 `git diff -- grade_stats.py test_grade_stats.py data/scores.csv` 检查差异。下载 ZIP 的同学，可用编辑器将修改后的文件与重新解压到另一个目录的原始文件对比。

复制 [练习记录模板](docs/EXPERIMENT_REPORT.md) 为 `my-report.md`，记录提示词、修改前后的真实输出、代码差异，以及你对结果的解释。无需向公共仓库上传自己的姓名或聊天记录。

## 5. 再做一遍 / 换一个 AI 对比

最简单的方式是重新下载并解压到**新目录**，保留上一次的结果；新开一次 AI 对话，避免旧答案影响对比。

Git 用户如需恢复：先保存自己的修改，再执行以下命令。它会丢弃这三个文件中尚未提交的修改，恢复到已发布的练习起点：

```sh
git restore --source=classroom-v2 -- grade_stats.py test_grade_stats.py data/scores.csv
python -m unittest -v
```

恢复后应再次出现 `FAILED (errors=2)`。

## 这个案例如何生成

阅读 [AI 辅助生成与复现说明](docs/AI_GENERATION.md)：包括教学设计、证据范围、可复制的生成提示词，以及如何验证一个新案例。提示词是本次整理的复现版本，不是原始对话逐字记录。

## 文件导航

| 文件 | 用途 |
| --- | --- |
| `grade_stats.py` | 等待修复的程序 |
| `test_grade_stats.py` | 原有三个验收测试 |
| `data/scores.csv` | 原材料中的教学示例数据 |
| `docs/STUDENT_PROMPTS.md` | 分步提示词与一次性提示词 |
| `docs/EXPERIMENT_REPORT.md` | 练习记录与评价标准 |
| `docs/AI_GENERATION.md` | AI 辅助出题流程、复现提示词与来源说明 |
| `docs/CLASSROOM_GUIDE.md` | 汇报后的课堂练习安排与讲解话术 |
| `provenance.json` | 三个原始案例文件的 SHA-256，用于核对来源 |

基础练习不涵盖任意文本成绩、缺少列或文件不存在等情况。完成后可另开一份副本，让 AI 为零分、只有表头、前后空格等边界情况补充测试，再讨论错误输入应该如何处理。三个测试通过只能证明这些测试覆盖的场景通过。
