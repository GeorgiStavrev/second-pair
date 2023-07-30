from functools import wraps
from typing import Optional
from dateutil import parser
from datetime import datetime, timedelta

import flask
import boto3
from botocore.exceptions import ClientError

from config import ENV, CUSTOM_AUTH_HEADER, CUSTOM_AUTH_HEADER_PREFIX
from logger_factory import get_logger

from services import auth_service


TABLE_NAME_MAPPING = {
    "LOCAL": "test-second-pair-APIKeys",
    "TEST": "test-second-pair-APIKeys",
    "DEV": "test-second-pair-APIKeys",
    "PROD": "second-pair-APIKeys",
}

logger = get_logger(__name__)

dynamodb = boto3.resource("dynamodb")
api_keys_table = dynamodb.Table(
    TABLE_NAME_MAPPING[ENV.upper()]
)  # PK 'ACCESS_KEY_ID', SK 'SECRET_ACCESS_KEY'

BUFFER_SECONDS = 5


def _get_access_key(access_key_id: str) -> Optional[dict]:
    try:
        response = api_keys_table.get_item(
            Key={"ACCESS_KEY_ID": access_key_id})
        if "Item" in response:
            return response["Item"]
    except ClientError:
        logger.exception("Cannot get access key from database.")
    except Exception:
        logger.exception("Error getting access key.")


def _get_string_to_sign() -> str:
    method = flask.request.method
    dateHeaderValue = flask.request.headers.get("Date")
    date = None
    try:
        date = parser.isoparse(dateHeaderValue)
    except Exception:
        logger.exception("Unable to parse date header value.")
        return None

    date_now = datetime.utcnow()
    delta = timedelta(seconds=BUFFER_SECONDS)
    if date > (date_now + delta) or date < (date - delta):
        # Reject calls dated in the future or too old
        return None

    url = flask.request.url

    # Because ALB forwards https request to target group over http
    x_forwarded_proto = flask.request.headers.get("X-Forwarded-Proto")
    if x_forwarded_proto and url:
        url = url.replace("http://", f"{x_forwarded_proto}://")
    return f"{method}{dateHeaderValue}{url}"


# Authentication decorator
def requires_api_auth(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            if not authenticate_with_api_key():
                return flask.Response(
                    status=401, response="Unauthorized", content_type="text/plain"
                )
        except Exception:
            logger.exception("Request failed.")
            return flask.Response(status=500)

        flask.g.auth = "api"
        return f(*args, **kwargs)

    return decorator


def authenticate_with_api_key() -> bool:
    auth_comps = flask.request.headers.get(
        CUSTOM_AUTH_HEADER).split(CUSTOM_AUTH_HEADER_PREFIX)
    auth = auth_comps[1]
    access_key_id, client_signature = auth.split(":")
    access_key = _get_access_key(access_key_id)
    secret_key = access_key.get("SECRET_ACCESS_KEY", "")
    server_signature = auth_service.build_signature_for_string(
        _get_string_to_sign(), secret_key
    )
    if client_signature == server_signature:
        flask.g.client = access_key.get("Name", "Unknown")
        return True
    return False
