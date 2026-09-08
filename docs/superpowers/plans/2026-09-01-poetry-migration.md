# Poetry 依赖管理迁移实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将依赖管理从 pip + setuptools 迁移到 Poetry 2.x（PEP 621 + poetry-core + poetry.lock），实现可复现构建。

**Architecture:** 保留 PEP 621 `[project]` 元数据，构建后端换成 poetry-core；依赖改为宽松约束并由 poetry.lock 锁定全部依赖（含传递依赖）；poetry 完全接管开发工作流（`poetry install` / `poetry run`），虚拟环境建在项目内 `.venv`。

**Tech Stack:** Poetry 2.x（poetry-core>=2.0）、Python 3.12、pytest 8.4.2

## Global Constraints

- Python 版本要求 `>=3.12`；系统 `python3` 为 3.12.13
- PATH 上的 `pip` 属于 Python 3.9 —— 安装 poetry 必须用 `python3 -m pip install poetry`
- 本机已存在 pip 安装的 `PythonWebServer-1.0.0` egg，迁移后需卸载，避免与 `.venv` 内安装冲突
- 不改变任何运行时行为：`run.py`、`src/server/*`、`cert/`、`.env` 逻辑全部不动
- 测试基线：`tests/` 25 个用例必须全部通过
- `.venv/` 已在 `.gitignore` 覆盖，poetry.lock 必须提交
- 提交信息遵循仓库 conventional-commit 中文风格

---

### Task 1: 安装 Poetry 2.x

**Files:**
- 无文件变更（环境准备）

**Interfaces:**
- Produces: 本机可用的 `poetry` 命令（Python 3.12 环境下）

- [ ] **Step 1: 用 Python 3.12 的 pip 安装 poetry**

```bash
python3 -m pip install poetry
```

Expected: 输出以 `Successfully installed poetry-2.x` 结尾（版本需 >= 2.0）。

- [ ] **Step 2: 确认版本与解释器**

```bash
poetry --version && poetry debug info | grep -E '^Python'
```

Expected: `Poetry (version 2.x.x)`；Python 为 3.12.13。

- [ ] **Step 3: 运行 poetry 自带检查确认可用**

```bash
poetry --help > /dev/null && echo OK
```

Expected: `OK`

---

### Task 2: 重写 pyproject.toml

**Files:**
- Modify: `pyproject.toml`（整体重写）

**Interfaces:**
- Produces: poetry 可识别的 PEP 621 项目声明 + `[tool.poetry]` src-layout 包配置 + dev group 依赖

- [ ] **Step 1: 重写 pyproject.toml**

完整内容：

```toml
[build-system]
requires = ["poetry-core>=2.0"]
build-backend = "poetry.core.masonry.api"

[project]
name = "PythonWebServer"
version = "1.0.0"
description = "Flask HTTPS Web Server with mTLS — 对应 SpringBoot2Demo 的 Python 实现"
authors = [{ name = "YoungBear" }]
requires-python = ">=3.12"
dependencies = [
    "flask>=3.1.3,<4",
    "python-dotenv>=1.2.2,<2",
    "waitress>=3.0.2,<4",
]

[tool.poetry]
packages = [{ include = "server", from = "src" }]

[tool.poetry.group.dev.dependencies]
pytest = "^8.4.2"
```

注意：删除原 `[project.optional-dependencies] dev` 和全部 `[tool.setuptools.*]` 段；PEP 621 不支持 `^` 语法，`^3.1.3` 等价写成 `>=3.1.3,<4`。

- [ ] **Step 2: 验证 pyproject 语法与配置合法**

```bash
poetry check
```

Expected: `All set!`

- [ ] **Step 3: 暂不单独提交**（与 Task 4 的 poetry.lock 一起提交）

---

### Task 3: 新增 poetry.toml（项目内虚拟环境）

**Files:**
- Create: `poetry.toml`

**Interfaces:**
- Produces: 项目级 poetry 配置，使 `poetry install` 在项目内创建 `.venv`

- [ ] **Step 1: 创建 poetry.toml**

完整内容：

```toml
[virtualenvs]
in-project = true
```

- [ ] **Step 2: 验证配置被读取**

```bash
poetry config virtualenvs.in-project
```

Expected: `true`

- [ ] **Step 3: 暂不单独提交**（与 Task 4 一起提交）

---

### Task 4: 生成并提交 poetry.lock

**Files:**
- Create: `poetry.lock`（由 poetry 生成）
- Commit 包含: `pyproject.toml`、`poetry.toml`、`poetry.lock`

**Interfaces:**
- Consumes: Task 2 的 pyproject.toml、Task 3 的 poetry.toml
- Produces: `poetry.lock`（锁定 flask 3.1.3、python-dotenv 1.2.2、waitress 3.0.2、pytest 8.4.2 及全部传递依赖）

- [ ] **Step 1: 生成锁文件**

```bash
poetry lock
```

Expected: 输出 `Writing lock file`；生成 `poetry.lock`。锁文件中 flask 版本应为 3.1.3、waitress 3.0.2、python-dotenv 1.2.2、pytest 8.4.2。

- [ ] **Step 2: 复核锁文件中的直接依赖版本**

```bash
grep -A1 'name = "flask"' poetry.lock | head -2 && grep -A1 'name = "waitress"' poetry.lock | head -2
```

Expected: `version = "3.1.3"` 和 `version = "3.0.2"`

- [ ] **Step 3: 提交配置与锁文件**

```bash
git add pyproject.toml poetry.toml poetry.lock
git commit -m "build: 迁移依赖管理到 poetry（PEP 621 + poetry-core + poetry.lock）"
```

Expected: 提交成功，包含 3 个文件。

---

### Task 5: 安装依赖到项目内 .venv 并清理 pip egg

**Files:**
- 无仓库文件变更（`.venv/` 被 gitignore）

**Interfaces:**
- Consumes: Task 4 的 poetry.lock
- Produces: 可用的 `.venv` 环境（含 server 包 editable 安装与 pytest）

- [ ] **Step 1: 按锁文件安装**

```bash
poetry install
```

Expected: 输出 `Creating virtualenv PythonWebServer-... in /home/paas/learn/github/youngbear/PythonWebServer/.venv` 和 `Installing dependencies from lock file`。

- [ ] **Step 2: 确认 .venv 内 server 包安装成功**

```bash
poetry run python -c "import server; print(server.__file__)"
```

Expected: 输出路径位于 `.venv/` 内（如 `.../PythonWebServer/.venv/lib/python3.12/site-packages/server/__init__.py` 或指向 `src/server` 的 editable 路径）。

- [ ] **Step 3: 卸载系统 Python 里的旧 egg**

```bash
python3 -m pip uninstall -y PythonWebServer
```

Expected: `Successfully uninstalled PythonWebServer-1.0.0`。此步骤后系统 `python3` 不再能 import server（预期行为，一切走 poetry）。

- [ ] **Step 4: 确认系统 python3 已无法 import（预期）**

```bash
python3 -c "import server" 2>&1 | tail -1
```

Expected: `ModuleNotFoundError: No module named 'server'`

---

### Task 6: 验证测试与运行时行为不变

**Files:**
- 无仓库文件变更

**Interfaces:**
- Consumes: Task 5 的 .venv
- Produces: 迁移正确性的验证证据

- [ ] **Step 1: 运行完整测试套件**

```bash
poetry run pytest tests/ -v 2>&1 | tail -3
```

Expected: `25 passed`

- [ ] **Step 2: HTTP 模式冒烟测试**

```bash
SERVER_PROTOCOL=http SERVER_PORT=8899 poetry run python run.py > /tmp/pws_poetry_smoke.log 2>&1 & PID=$!; sleep 2; \
echo "== /health =="; curl -s http://127.0.0.1:8899/health; echo; \
echo "== /demo/current =="; curl -s http://127.0.0.1:8899/PythonWebServer/demo/current; echo; \
echo "== 404 =="; curl -s -w " [%{http_code}]" http://127.0.0.1:8899/nonexistent; echo; \
echo "== /apidocs/ =="; curl -s -o /dev/null -w "[%{http_code}] %{content_type}" http://127.0.0.1:8899/apidocs/; echo; \
kill $PID
```

Expected:
- `/health` → `{"status":"UP",...}`
- `/demo/current` → `{"timestamp":"...","zonedDateTime":"...+00:00"}`
- 404 → `{"error":"Not Found","status":404} [404]`
- `/apidocs/` → `[200] text/html; charset=utf-8`

---

### Task 7: 更新文档为 poetry 工作流

**Files:**
- Modify: `CLAUDE.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: Task 2-6 的实际命令与结果

- [ ] **Step 1: 更新 CLAUDE.md「构建与运行」章节**

将：

```bash
# 安装项目及依赖（dev extra 含 pytest）
python3 -m pip install -e ".[dev]"

# 运行测试
python3 -m pytest tests/ -v

# 运行应用（HTTPS 端口 8888，路径 /PythonWebServer/demo/current）
python run.py
```

替换为：

```bash
# 安装 poetry（一次性，注意用 python3 -m pip，PATH 上 pip 属于 Python 3.9）
python3 -m pip install poetry

# 安装依赖（在项目内创建 .venv，按 poetry.lock 安装）
poetry install

# 运行测试
poetry run pytest tests/ -v

# 运行应用（HTTPS 端口 8888，路径 /PythonWebServer/demo/current）
poetry run python run.py
```

- [ ] **Step 2: 更新 CLAUDE.md「包结构」与「依赖」**

将 `- pyproject.toml` 一行改为：

```
- `pyproject.toml` — 项目元数据（PEP 621）、依赖声明（poetry 管理）、poetry-core 构建配置
- `poetry.toml` — 项目级 poetry 配置（虚拟环境建在项目内 .venv）
- `poetry.lock` — 依赖锁文件（含传递依赖，保证可复现构建）
```

将「**依赖**: Flask 3.1.3, python-dotenv 1.2.2, waitress 3.0.2, pytest 8.4.2」改为：

```
**依赖**: 由 poetry 管理并锁定（poetry.lock）。直接依赖：Flask 3.1.3, python-dotenv 1.2.2, waitress 3.0.2；dev: pytest 8.4.2。
```

- [ ] **Step 3: 更新 README「快速开始」**

将：

```bash
# 安装项目及依赖（dev extra 含 pytest）
python3 -m pip install -e ".[dev]"

# 运行测试
python3 -m pytest tests/ -v

# 启动应用
python run.py
```

替换为：

```bash
# 安装 poetry（一次性）
python3 -m pip install poetry

# 安装依赖（自动创建 .venv，按 poetry.lock 安装）
poetry install

# 运行测试
poetry run pytest tests/ -v

# 启动应用
poetry run python run.py
```

- [ ] **Step 4: 更新 README「项目结构」**

将 `├── pyproject.toml` 一行替换为：

```
├── pyproject.toml                # 项目元数据 (PEP 621)、依赖声明与 poetry-core 构建配置
├── poetry.toml                   # poetry 配置 (虚拟环境建在项目内 .venv)
├── poetry.lock                   # 依赖锁文件 (含传递依赖，可复现构建)
```

- [ ] **Step 5: 提交文档**

```bash
git add CLAUDE.md README.md
git commit -m "docs: 更新安装说明与项目结构为 poetry 工作流"
```

Expected: 提交成功。

---

### Task 8: 最终验证与收尾

**Files:**
- 无仓库文件变更

- [ ] **Step 1: 全量复验**

```bash
poetry run pytest tests/ -v 2>&1 | tail -1 && git status --short && git log --oneline -5
```

Expected: `25 passed`；工作区干净；最近提交包含 poetry 迁移相关 2 个提交（build + docs）与设计文档提交。

- [ ] **Step 2: 向用户汇报**（是否 push 由用户决定）
