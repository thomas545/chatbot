import os
from typing import Any
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv(override=True)


def get_environ(
    key: str,
    value_type: Any = str,
    default: Any = None,
    raise_on_not_found: bool = True,
):

    secret = os.environ.get(key)
    if secret is None and default is None and raise_on_not_found:
        raise HTTPException(404, f"Secret value not exits for key: {key}")

    if secret is None:
        secret = default

    if secret is not None:
        return value_type(secret)

    return secret
