# HTTP 模式支持设计

## 概述

新增 `SERVER_PROTOCOL` 配置项，控制服务使用 HTTP 还是 HTTPS，默认 HTTPS 保持向后兼容。

## 配置

`.env` 新增：

```
SERVER_PROTOCOL=https   # http 或 https，默认 https
```

## 代码变更

### `app.py`

- `create_ssl_context()` 保持不变，仅在 HTTPS 时调用
- 启动分支：读 `SERVER_PROTOCOL` 环境变量，`http` 时 `app.run(host="0.0.0.0", port=8888, debug=False)`，`https` 时走原有 SSL 路径
- 未知值时打印警告并 fallback 到 https

### `.env`

- 新增 `SERVER_PROTOCOL=https`

### `README.md`

- 配置表增加 `SERVER_PROTOCOL` 说明

## 影响范围

| 文件 | 变更 |
|------|------|
| `app.py` | 启动逻辑，约 10 行 |
| `.env` | 新增 1 行 |
| `README.md` | 配置表新增 1 行 |

## 向后兼容

- 不配置 `SERVER_PROTOCOL` 时默认 `https`，行为与当前完全一致
- `VERIFY_CLIENT_CERT` 仍在 HTTPS 模式下生效，HTTP 模式下忽略
