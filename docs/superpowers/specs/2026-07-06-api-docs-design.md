# API 文档 (Swagger) 设计

## 概述

集成 Swagger/OpenAPI 3.0 文档，自动生成交互式 API 文档页面。使用 flasgger 库，通过 Flask 路由中的 docstring (YAML 格式) 描述 API 接口。

## 方案选择

| 方案 | 优点 | 缺点 | 结论 |
|------|------|------|------|
| flasgger | 轻量、docstring 驱动、社区活跃 | OpenAPI 3.0 支持需手动配置 | 采用 |
| flask-restx | 功能完整 | 侵入性强，需改造路由 | 不采用 |
| apispec | 灵活 | 需手写 schema，工作量大 | 不采用 |

## 配置

`server/__init__.py` 中 Swagger 配置：

- **title**: PythonWebServer API
- **openapi**: 3.0.3
- **specs_route**: `/apidocs/` (Swagger UI)
- **specs endpoint**: `/apispec_1.json` (OpenAPI JSON)
- **headers**: [] (禁用额外响应头，避免与自定义 error handler 冲突)

`_swagger_template` 通过 `servers` 字段指定服务器地址，格式为 `http://localhost:{SERVER_PORT}`。

## 代码变更

### `server/__init__.py`

- `Swagger(app, config=..., template=...)` 初始化
- `/health` 端点添加 OpenAPI docstring
- Swagger UI 和 spec 端点均在根路径，不受 CONTEXT_PATH 影响

### `server/routes.py`

- `/demo/current` 路由添加 OpenAPI docstring，包含请求/响应 schema 和示例

### `requirements.txt`

- 新增 `flasgger==0.9.7.1`

### `README.md` / `CLAUDE.md`

- 特性列表、API 表格、依赖说明同步更新

## 影响范围

| 文件 | 变更 |
|------|------|
| `requirements.txt` | +1 行 |
| `server/__init__.py` | +15 行（配置 + health docstring） |
| `server/routes.py` | +22 行（current docstring） |
| `README.md` | +4 行 |
| `CLAUDE.md` | +3 行 |

## 注意事项

- flasgger 的 `after_request` 钩子与 Flask 自定义 error handler 存在冲突，需在 config 中显式设置 `"headers": []` 避免 `TypeError`
- 新增端点不会随 `VERIFY_CLIENT_CERT` 或 `CONTEXT_PATH` 变化，始终可访问
- 新增 API 端点时，只需在路由函数的 docstring 中添加 OpenAPI 格式的描述即可自动出现在文档中
