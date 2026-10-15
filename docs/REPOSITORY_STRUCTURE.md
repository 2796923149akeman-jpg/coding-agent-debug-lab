# 文件规范与目录用途

```text
README.md                       总入口
docs/                           上手指南、概念说明、提示词与记录模板
pyproject.toml                  静态检查与格式配置
.editorconfig                   编辑器编码、缩进和换行约定
requirements-dev.txt            可选的规范检查工具依赖
labs/
  01-grade-stats/                成绩案例：程序、测试、CSV 与独立说明
  02-photo-organizer/            照片案例：任务、初始化、自检、依赖与工具测试
    data/photos.zip             原始素材资产
    data/manifest.json          内容校验与修改时间
    input/                      初始化生成，Git 忽略
    output/                     学生结果，Git 忽略
    reports/                    学生报告，Git 忽略
```

- 目录和工具文件使用小写英文、连字符或下划线；面向同学的文字为中文。
- Python、Markdown、JSON、依赖文件使用 UTF-8；通过 `.gitattributes` 统一文本换行为 LF。
- 原始照片文件名与字节保持不变，含刻意设置的 `.DS_Store`、`Thumbs.db`、`desktop.ini`；它们只封装在素材 ZIP 内，不能按日常清理规则删掉。
- 根目录不堆放重复 ZIP、执行输出、缓存或答案成品。实操下载使用 README 中指向当前主分支的 ZIP 链接。
- `.gitignore` 忽略虚拟环境、缓存、练习输出和本地记录。只提交代码、必要素材、依赖声明与说明。
- 全部操作说明以当前双案例目录为准；先做成绩统计，再做照片整理。

Python 代码使用 4 空格缩进、清晰命名和必要注释，异常应明确报错。可选的格式检查命令为 `python -m ruff check .` 和 `python -m ruff format --check .`，先安装 `requirements-dev.txt` 中的工具即可。

本仓库只提供实操所需的代码起点、素材、工具和说明，不提供正确代码或答案成品。需要重做时解压到新目录，保留上次结果。
