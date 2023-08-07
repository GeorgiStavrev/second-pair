import boto3
import json
import logging

logger = logging.getLogger(__name__)

ssm_client = boto3.client("ssm")

PARAMETER_FORMAT = "/second-pair/{env}/{name}"


def get_param(env: str, name: str, type: str = "string") -> str:
    try:
        param_full_name = PARAMETER_FORMAT.format(env=env, name=name)
        response = ssm_client.get_parameter(
            Name=param_full_name, WithDecryption=True)
        if type == "json":
            return json.loads(response["Parameter"]["Value"])
        return response["Parameter"]["Value"]
    except Exception:
        return None
