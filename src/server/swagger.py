from flask import Blueprint, jsonify, render_template_string

from . import config

swagger_bp = Blueprint("swagger", __name__)

_SWAGGER_UI_HTML = """\
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>PythonWebServer API</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"/>
</head>
<body>
<div id="swagger-ui"></div>
<script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
<script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-standalone-preset.js"></script>
<script>
SwaggerUIBundle({
  url: "{{ spec_url }}",
  dom_id: "#swagger-ui",
  presets: [SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset],
  layout: "StandaloneLayout"
})
</script>
</body>
</html>
"""


def _build_spec() -> dict:
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "PythonWebServer API",
            "description": "Flask HTTPS Web Server with mTLS — 对应 SpringBoot2Demo 的 Python 实现",
            "version": "1.0.0",
        },
        "servers": [{"url": f"{config.SERVER_PROTOCOL}://localhost:{config.SERVER_PORT}"}],
        "paths": {
            "/health": {
                "get": {
                    "tags": ["System"],
                    "summary": "健康检查",
                    "description": "返回服务运行状态，始终在根路径，不受 CONTEXT_PATH 影响。",
                    "responses": {
                        "200": {
                            "description": "服务正常",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string", "example": "UP"},
                                            "timestamp": {"type": "string", "example": "1783321215118"},
                                        },
                                    }
                                }
                            },
                        }
                    },
                }
            },
            f"{config.CONTEXT_PATH}/demo/current": {
                "get": {
                    "tags": ["Demo"],
                    "summary": "获取当前 UTC 时间",
                    "description": "返回当前 UTC 时间的 zonedDateTime 字符串和时间戳（毫秒）。",
                    "responses": {
                        "200": {
                            "description": "成功返回当前时间",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "zonedDateTime": {
                                                "type": "string",
                                                "example": "2026-07-06 07:00:15.118021+00:00",
                                            },
                                            "timestamp": {"type": "string", "example": "1783321215118"},
                                        },
                                    }
                                }
                            },
                        }
                    },
                }
            },
        },
    }


@swagger_bp.route("/apispec_1.json")
def apispec():
    return jsonify(_build_spec())


@swagger_bp.route("/apidocs/")
def apidocs():
    return render_template_string(_SWAGGER_UI_HTML, spec_url="/apispec_1.json")
