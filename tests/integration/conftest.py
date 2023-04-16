from typing import Type

import pytest

from pytest_celery.api.setup import CeleryTestSetup


class IntegrationSetup(CeleryTestSetup):
    def ready(self, *args: tuple, **kwargs: dict) -> bool:
        kwargs["ping"] = True
        return super().ready(*args, **kwargs)


@pytest.fixture
def celery_setup_cls() -> Type[CeleryTestSetup]:
    return IntegrationSetup
