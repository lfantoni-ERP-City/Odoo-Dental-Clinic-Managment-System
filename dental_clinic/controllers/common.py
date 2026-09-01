import json
from datetime import date, datetime

from werkzeug.wrappers import Response


def _json_default(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    raise TypeError(f"{type(value).__name__} is not JSON serializable")


def json_response(payload, status=200):
    return Response(
        json.dumps(payload, default=_json_default),
        status=status,
        content_type="application/json; charset=utf-8",
        headers={"Cache-Control": "no-store"},
    )


def error_response(message, status=400, code="bad_request"):
    return json_response({"error": {"code": code, "message": message}}, status)
