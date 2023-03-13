from pytest_docker_tools import build
from pytest_docker_tools import container
from unit.docker.api import UnitTestContainer

unit_tests_image = build(
    path="tests/unit/docker",
    tag="localhost/pytest-celery/tests/unit:latest",
)


unit_tests_container = container(image="{unit_tests_image.id}", wrapper_class=UnitTestContainer)
