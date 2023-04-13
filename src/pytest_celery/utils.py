from time import sleep
from typing import Any

import pytest


def resilient_getfixturevalue(request: pytest.FixtureRequest, max_tries: int = 5) -> Any:
    e = RuntimeError(f"Failed to get fixture value: '{request.param}'")
    tries = 1
    while tries <= max_tries:
        try:
            return request.getfixturevalue(request.param)
        except BaseException as pytest_error:
            if tries == max_tries:
                raise e from pytest_error
            tries += 1
            sleep(5)
