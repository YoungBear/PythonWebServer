# Poetry 依赖管理迁移设计

## 概述

将依赖管理从 pip + setuptools 迁移到 **Poetry 2.x**，实现依赖锁定与可复现构建。保留 PEP 621 `[project]` 元数据，poetry 完全接管开发工作流。

## 背景

- 当前：PEP 621 `pyproject.toml` + setuptools 后端，依赖精确固定（`==`），无锁文件
- 目标：`poetry.lock` 锁定全部依赖（含传递依赖），任何环境安装结果一致
- 约束：项目要求 Python >= 3.12；`run.py`、证书、`.env` 逻辑不受影响

## 方案决策

| 决策点 | 选择 |
|--------|------|
| 元数据格式 | PEP 621 `[project]`（poetry 2.x 原生支持，pip/uv 仍可安装） |
| 版本策略 | `^` 宽松约束（PEP 621 中等价于 `>=x,<y`）+ `poetry.lock` 锁定 |
| 工作流 | poetry 完全接管：`poetry install` / `poetry run` |
| 虚拟环境 | 项目内 `.venv`（`poetry.toml` 配置 `in-project = true`） |
| 构建后端 | `poetry-core>=2.0` |

## 代码变更

### `pyproject.toml`

- `[build-system]` 从 setuptools 换成 poetry-core
- `[project]` 保留 name/version/description/authors/requires-python
- `dependencies` 改为宽松约束：`flask>=3.1.3,<4`、`python-dotenv>=1.2.2,<2`、`waitress>=3.0.2,<4`
- 移除 `[project.optional-dependencies] dev`，pytest 移入 `[tool.poetry.group.dev.dependencies]`（`pytest = "^8.4.2"`）
- 新增 `[tool.poetry]`：`packages = [{ include = "server", from = "src" }]`（src-layout 声明）

### `poetry.toml`（新增，提交到仓库）

```toml
[virtualenvs]
in-project = true
```

### `poetry.lock`（新增，由 `poetry lock` 生成）

提交到仓库，实现可复现构建。

### `CLAUDE.md` / `README.md`

- 安装命令改为：

```bash
python3 -m pip install poetry   # 一次性
poetry install                  # 创建 .venv + 安装依赖
poetry run pytest tests/ -v
poetry run python run.py
```

- 项目结构章节补充 `poetry.toml`、`poetry.lock` 说明
- 依赖章节注明"由 poetry 管理，poetry.lock 锁定"

### 清理

- 本机卸载 pip 安装的 `PythonWebServer` egg（避免与 `.venv` 内安装冲突）
- `requirements.txt` 已在前序提交中删除，不恢复

## 影响范围

| 文件 | 变更 |
|------|------|
| `pyproject.toml` | 构建后端、依赖约束、dev group 改写 |
| `poetry.toml` | 新增（3 行） |
| `poetry.lock` | 新增（自动生成） |
| `CLAUDE.md` | 构建与运行、依赖章节 |
| `README.md` | 快速开始、项目结构章节（`.env` 配置章节不变） |

## 验证

1. `poetry lock` 成功生成 `poetry.lock`
2. `poetry install` 创建项目内 `.venv` 并完成安装
3. `poetry run pytest tests/ -v` — 25 个用例全部通过
4. `poetry run python run.py`（HTTP 模式）冒烟测试：`/health`、`/demo/current`、404 JSON、`/apidocs/` 符合预期

## 风险与注意

- 本机 PATH 上的 `pip` 属于 Python 3.9，安装 poetry 必须用 `python3 -m pip install poetry`
- `poetry install` 需访问 PyPI（首次下载依赖）
- 不改变任何运行时行为，TLS/mTLS、`.env` 加载、日志逻辑均不变
