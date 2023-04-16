from time import sleep
from typing import Any
from typing import List
from typing import Union

import pytest
from kombu.utils.objects import cached_property  # noqa
from pytest_lazyfixture import lazy_fixture

from pytest_celery import defaults


def resilient_getfixturevalue(
    request: pytest.FixtureRequest,
    max_tries: int = defaults.DEFAULT_MAX_RETRIES,
) -> Any:
    e = RuntimeError(f"Failed to get fixture value: '{request.param}'")
    tries = 1
    while tries <= max_tries:
        try:
            return request.getfixturevalue(request.param)
        except BaseException as pytest_error:
            if tries == max_tries:
                raise e from pytest_error
            sleep(5 * tries)
            tries += 1


def resilient_lazy_fixture(
    names: Union[str, List[str]],
    max_tries: int = defaults.DEFAULT_MAX_RETRIES,
) -> Any:
    e = RuntimeError(f"Failed to get fixture value: '{names}'")
    tries = 1
    while tries <= max_tries:
        try:
            return lazy_fixture(names)
        # TODO: Replace BaseException with docker IP4Address exception etc.
        # that happens due to running too many parallel containers at the same time.
        except BaseException as pytest_error:
            if tries == max_tries:
                raise e from pytest_error
            sleep(5 * tries)
            tries += 1
