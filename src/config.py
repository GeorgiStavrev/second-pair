import os

from remote_config import get_param

ENV = os.getenv("ENV") or "PROD"  # <- set to ENV when running LOCALLY
APP_SECRET = get_param(ENV, "APP_SECRET") or "You should set an app secret"
ROUTE_PREFIX = "/api"
JWT_SECRET = get_param(ENV, "JWT_SECRET")
JWT_ALGO = "HS256"
CUSTOM_AUTH_HEADER = "X-AUTH"
CUSTOM_AUTH_HEADER_PREFIX = "Moment "


class Config:
    SESSION_COOKIE_NAME = "__session"
    CORS_EXPOSE_HEADERS = [CUSTOM_AUTH_HEADER]
    CORS_ALLOW_HEADERS = "*"
    CORS_SUPPORTS_CREDENTIALS = True
    API_TITLE = "second-pair Service API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_RAPIDOC_PATH = "/rapidoc"
    OPENAPI_RAPIDOC_URL = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"
    API_SPEC_OPTIONS = {
        "security": [{"bearerAuth": []}],
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        },
    }
