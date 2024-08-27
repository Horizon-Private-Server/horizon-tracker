from pathlib import Path
import json
import copy
from typing import Dict, Any

from app.utils.aws import get_secrets


def read_environment_variables() -> Dict[str, Any]:
    """
    Scans for 'env.json' and pulls in environment details from that file. If 'env.json' is not found,
    this function raises an AssertionError. The environment file requires 2 named keys 'environment',
    which is the name of the environment (the AWS Secrets Manager name) and 'region' which is the AWS
    Region name where the secrets are located.

    If the 'environment' value ends with 'dev', this function will ignore the AWS region and secret name
    and load variables locally. In this case, the variables will come from the JSON file itself. Otherwise,
    this function reaches out to AWS Secrets Manager and attempts to fetch the value. This also requires
    AWS credentials to be set up along with the appropriate Secrets Manager configuration.

    :return: A dictionary containing the requested credentials.
    """

    assert "env.json" in [path.name for path in Path().iterdir()], "env.json not found in root folder."

    with open("env.json") as stream:
        environment: Dict[str, Any] = json.load(stream)

    assert "environment" in environment, "Variable 'environment' not found in env.json."
    assert "region" in environment, "Variable 'region' not found in env.json."

    environment_name: str = environment["environment"]
    region_name: str = environment["region"]

    if environment_name.lower().endswith("dev"):
        credentials: Dict[str, Any] = copy.deepcopy(environment)
        del credentials["environment"]
        del credentials["region"]
        return credentials
    else:
        return get_secrets(region_name=region_name, secret=environment_name)
