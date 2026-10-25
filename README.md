# make-knowledge-cards

[![CI](https://github.com/128zh/article-to-knowledge-cards/actions/workflows/ci.yml/badge.svg)](https://github.com/128zh/article-to-knowledge-cards/actions/workflows/ci.yml)
[![Release](https://github.com/128zh/article-to-knowledge-cards/actions/workflows/release.yml/badge.svg)](https://github.com/128zh/article-to-knowledge-cards/actions/workflows/release.yml)

一个把文章 / 笔记自动整理成「知识卡片」的 Agent Skill。它按 Agent Skills 开放标准编写，同时提供 Claude Code 的 `SKILL.md` 和 OpenAI/Codex 的 `agents/openai.yaml` 两套入口，方便在支持 Skill 的智能体工具中使用。

## 解决什么问题

读长文容易「看过就忘」。这个 Skill 把一篇原文压缩成 5～8 张便于复习的知识卡片，每张只讲一个知识点，帮你：

- 快速抓住一篇文章**真正重要的知识**，而不是复述全文；
- 把知识变成「标题 + 核心知识 + 简明解释 + 例子/自测」的结构，方便日后自测复习；
- 避免记一堆无关细节、重复内容或原文没有的信息。

## 主要功能

- **输入**：用户直接粘贴的文章文本，或本地 Markdown（`.md`）/ 纯文本（`.txt`）文件的路径。
- **输出**：5～8 张知识卡片，每张包含：
  - **标题**：这张卡要讲的知识点；
  - **核心知识**：一句话点出该知识点；
  - **简明解释**：1～3 句大白话讲清楚；
  - **例子 / 自测**：一个具体例子，或一个可自问自答的小问题。
- **质量约束**（写进 SKILL.md，智能体会遵守）：
  - 一张卡片只讲一个知识点；
  - 只提取真正重要的知识，去重；
  - 不编造原文没有的信息；
  - 信息不足时不硬凑 5～8 张，按实际数量输出并说明。

**暂不支持**：网页抓取（URL）、PDF、Anki 导入/导出、图形界面。

## 安装方法

本 Skill 无需安装依赖，只需把 `skills/make-knowledge-cards` 目录放到你的智能体工具的 skills 目录下即可：

- 本项目内：已位于 `skills/make-knowledge-cards`。
- Claude Code：放到项目 `.claude/skills/` 或用户级 `~/.claude/skills/`。
- Codex / OpenAI Agents：放到 `~/.codex/skills/`（或对应 `skills/` 目录）。

目录结构：

```
skills/make-knowledge-cards/
├── SKILL.md            # 核心说明（触发条件 + 生成规则 + 卡片模板）
└── agents/
    └── openai.yaml     # OpenAI/Codex 界面元数据
```

## 使用方法

把文章粘贴给智能体，或给出本地 `.md` / `.txt` 文件路径，然后让它生成知识卡片。例如：

```
把下面这篇文章做成知识卡片：
<粘贴正文>
```

或：

```
把 examples/article-1-sleep.md 做成知识卡片
```

也可以直接说：`生成知识卡片` / `做学习卡片` / `拆解这篇文章`。

## 输入输出示例

**输入**（粘贴文本）：

> 光合作用是植物、藻类和部分细菌利用光能，把二氧化碳和水转化成有机物并释放氧气的过程，主要发生在叶绿体中。影响光合作用速率的主要因素有光照强度、二氧化碳浓度和温度。

**输出**：

### 卡片 1：光合作用的定义
**核心知识**：光合作用是利用光能把二氧化碳和水转化为有机物并释放氧气的过程。
**简明解释**：植物、藻类和部分细菌在叶绿体里完成这一过程，把无机物变成有机物，同时放出氧气。
**例子 / 自测**：试着分别指出光合作用的原料和产物各是什么？

### 卡片 2：影响光合作用速率的因素
**核心知识**：光照强度、二氧化碳浓度和温度是影响光合作用速率的主要因素。
**简明解释**：这三者任何一项不足或过量，都可能限制反应速率，成为「瓶颈」。
**例子 / 自测**：阴天光照弱时，光合速率为什么下降？

更多完整示例见 [examples/](examples/)：科学科普（睡眠与记忆）、技术（Git 分支）、方法论（费曼学习法），以及一个「信息不足、只出 2 张卡」的边界案例。

## 验证

用结构校验脚本检查 SKILL.md 是否符合规范：

```
python quick_validate.py skills/make-knowledge-cards
# 输出：Skill is valid!
```

校验规则与官方 Agent Skills 的 `quick_validate.py` 一致：检查 frontmatter 是否存在、键是否合法、`name` 是否为小写连字符、`description` 是否含尖括号或超长等。

## 开发与测试

本项目带有一组自动化测试和代码质量检查，依赖声明在 `requirements-dev.txt`。

```bash
# 创建虚拟环境并安装开发依赖
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

# 运行测试
pytest

# 代码质量检查（lint + 格式）
ruff check .
ruff format --check .
```

测试覆盖：

- `tests/test_validate.py`：校验脚本 `quick_validate.py` 的各类合法 / 非法 frontmatter 用例；
- `tests/test_examples.py`：检查 `examples/` 中每篇原文都有对应卡片，且卡片遵循「标题 + 核心知识 + 简明解释 + 例子 / 自测」模板、数量在 1～8 张之间。

## CI / CD

- **CI**（`.github/workflows/ci.yml`）：在每次 Pull Request 和推送到 `main` 时触发，依次运行 Ruff 代码质量扫描、Skill 结构校验，并在 Python 3.10 / 3.11 / 3.12 上跑 pytest。
- **CD**（`.github/workflows/release.yml`）：推送 `v*` 标签（如 `v1.0.0`）时，把 `skills/make-knowledge-cards` 打包成 zip 并发布为 GitHub Release，附带自动生成的更新说明。

```
git tag v1.0.0
git push origin v1.0.0
```
