# 同学上手指南：下载后一步一步做

这份指南可以独立使用，不需要其他资料。建议按“成绩统计纠错 → 照片整理”的顺序，在自己的副本中操作。每一步先看实际输出，再发下一段提示词。

## 1. 下载、解压，找到主文件夹

点击 [下载当前完整实操包 ZIP](https://github.com/2796923149akeman-jpg/coding-agent-debug-lab/archive/refs/heads/main.zip)，将 ZIP 完整解压到一个新文件夹。不要直接在压缩包预览窗口里运行文件。

打开解压后的 `coding-agent-debug-lab-main`，应能看到：

```text
README.md
docs/
labs/
  01-grade-stats/
  02-photo-organizer/
```

如果外面还有一层同名文件夹，请继续打开，直到看到 `labs`。两个案例都已包含在这份下载中。

## 2. 检查 Python 和终端

建议使用 Python 3.10 或更高版本。没有安装时可从 [Python 官网](https://www.python.org/downloads/) 获取。

Windows：在资源管理器中进入上面的主文件夹，在地址栏输入 `powershell` 并回车，即可在该目录打开终端。macOS / Linux：使用终端进入解压后的主文件夹。

```sh
python --version
```

能显示 Python 3.x 版本后继续。Windows 如果找不到 `python`，试试 `py --version`，后面的 `python` 也相应替换为 `py`；macOS / Linux 可试 `python3`。都不可用时先完成安装并重新打开终端。

## 3. 选择怎样使用 AI

**有文件和终端访问能力的编程 Agent：** 在工具中打开当前案例文件夹作为项目或工作区，让它只处理这个案例。具体入口名称因工具而异，以它能读到该目录中的文件为准。先让它说明当前目录和主要文件，确认没有打开错项目。

**只能对话的 AI：** 由你上传文件或粘贴代码、执行它给出的命令，再把真实输出发回去。它没有执行能力时，不应把预测结果写成“我已经运行成功”。照片案例包含二进制素材，适合让它提供检查脚本，由你在本地运行并回传输出。

不要把整个磁盘当作工作区。两个案例分别打开；从第一个切到第二个时，建议新开一次对话。

## 4. 实操一：成绩统计纠错

在主文件夹的终端执行：

```sh
cd labs/01-grade-stats
python -m unittest -v
```

此时应能看到 `grade_stats.py`、`test_grade_stats.py` 和 `data`。预期输出是 `Ran 3 tests` 和 `FAILED (errors=2)`：一项通过、两项因空白成绩报错，这是练习起点。

把 `labs/01-grade-stats` 作为 AI 工作区，打开 [成绩案例提示词](../labs/01-grade-stats/docs/STUDENT_PROMPTS.md)，依次发送：

1. 先读文件，解释项目和测试方式，不修改。
2. 运行测试，依据报错定位原因，不修改。
3. 只修复 `grade_stats.py`，保持测试和示例数据不变，重新运行。
4. 展示差异，用 80、空白、90 手算解释结果。

AI 修改后，在本地终端执行：

```sh
python -m unittest -v
python grade_stats.py data/scores.csv
```

应为三项测试全部通过，程序输出平均分 `85.0`、未填写 `1` 人。还要确认全部空白时返回 `average=None`，且测试没有被删除、跳过或改预期。

**这一例要理解：** 测试先把问题变成可观察的失败，Agent 根据失败修改代码，再用同一套测试检查修复。只看它给出的代码，无法确认这一步是否完成。

## 5. 实操二：照片整理

如果终端仍在成绩案例目录，执行：

```sh
cd ../02-photo-organizer
python -m pip install -r requirements.txt
python prepare.py
```

如果重新打开终端，请先在主文件夹进入 `labs/02-photo-organizer`。安装 Pillow 需要联网；素材就在下载包内，不需另找图片。若系统不允许向当前 Python 安装包，可创建虚拟环境，或使用已配置好依赖的 Python 环境。

`prepare.py` 应生成 `input/`，里面有 205 个文件，并恢复它们的统一修改时间。不要手动修改这些文件，也不要把 `data/photos.zip` 直接当作待整理目录。

将 AI 工作区切换到 `labs/02-photo-organizer`，新开对话。打开 [照片案例提示词](../labs/02-photo-organizer/PROMPTS.md)，依次让它：

1. 阅读任务、观察真实输入，说明数据特点和验收标准。
2. 创建 `organize.py`，按年月整理，保留全部副本，输出逐文件清单。
3. 实际运行整理程序和自检，根据失败改进自己的程序。
4. 展示结果，解释日期来源、完全重复与近重复的区别。

`organize.py` 最初不存在是正常的，它就是这一段由 AI 编写的任务产物。与 AI 约定接口后执行：

```sh
python organize.py input output reports
python self_check.py input output
python prepare.py --check
```

正常情况下，整理后的文件在 `output/`，清单等报告在 `reports/`。自检应为 C1～C4 全部 PASS，输入核对也应 PASS。发生失败时，将命令与完整输出发给 AI，只修改整理程序；不要修改自检或素材来制造通过。

再次运行若目标目录已有结果，保留上一轮，使用新的结果目录，例如：

```sh
python organize.py input output-round2 reports-round2
python self_check.py input output-round2
python prepare.py --check
```

最后还要查看清单、抽查年月和重复报告。**205 进、205 出并不等于日期归档正确。** 自检覆盖不到的内容，由你依据 [验收目标](../labs/02-photo-organizer/EXPECTED_RESULTS.md) 进一步检查。

**这一例要理解：** Agent 的任务包括把自然语言要求落实到程序、处理实际数据、从运行反馈中发现遗漏。代码能跑完，只代表执行结束，不代表满足全部需求。

## 6. 两个案例结束后，留下自己的证据

复制 [记录模板](EXPERIMENT_REPORT.md)，分别记录两个案例的操作：提示词、真实命令、修改前后输出、关键代码差异和你的解释。

回答三个问题：AI 使用了哪些工具？哪条真实反馈促成了修改？哪些结论最后仍需要人判断？能用两个案例回答这些问题，就抓住了本次 Coding Agent 实操的重点。

## 常见卡点

| 现象 | 怎么处理 |
| --- | --- |
| 成绩测试显示 `Ran 0 tests` | 进入包含 `test_grade_stats.py` 的目录再执行 |
| 找不到 `grade_stats.py` / `prepare.py` | 检查终端所在案例；两个案例命令不能在同一目录混用 |
| 提示 `No module named PIL` | 在照片案例目录用同一个 Python 执行 `python -m pip install -r requirements.txt` |
| 找不到 `organize.py` | 先让 AI 创建并保存该文件，再运行 |
| 提示 `input` 内容或修改时间变化 | 保留当前结果，重新下载到新目录初始化，不把被修改的输入当基准 |
| 结果目录已存在 | 使用新的输出与报告目录，并在自检时指向同一个输出目录 |
| AI 说成功，却没有运行输出 | 让它实际执行；不能执行时，由你运行并回传输出 |
| ZIP 下载后 `git diff` 不能运行 | ZIP 没有 Git 历史，用编辑器对照另一份全新解压的副本 |

再次练习时，解压到新目录并新开 AI 对话，保留上一次的结果。
