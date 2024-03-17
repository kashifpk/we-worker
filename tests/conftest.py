import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def tests_init():
    """This only gets executed once."""

    print("Initializing tests")
    old_environment = os.environ.get("ENVIRONMENT", None)
    os.environ["ENVIRONMENT"] = "testing"

    yield None

    if old_environment is None:
        del os.environ["ENVIRONMENT"]
    else:
        os.environ["ENVIRONMENT"] = old_environment
