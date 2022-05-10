import pytest
from _pytest.fixtures import yield_fixture
from pytest_fixture_config import yield_requires_config
from pytest_virtualenv import CONFIG, VirtualEnv


@yield_fixture(scope="session")
@yield_requires_config(CONFIG, ["virtualenv_executable"])
def virtualenv():
    """Function-scoped virtualenv in a temporary workspace.
    Methods
    -------
    run()                : run a command using this virtualenv's shell environment
    run_with_coverage()  : run a command in this virtualenv, collecting coverage
    install_package()    : install a package in this virtualenv
    installed_packages() : return a dict of installed packages
    Attributes
    ----------
    virtualenv (`path.path`)    : Path to this virtualenv's base directory
    python (`path.path`)        : Path to this virtualenv's Python executable
    easy_install (`path.path`)  : Path to this virtualenv's easy_install executable
    .. also inherits all attributes from the `workspace` fixture
    """

    venv = VirtualEnv()
    yield venv
    venv.teardown()


@pytest.fixture(scope="session")
def plugin_virtualenv(virtualenv, pytestconfig):
    virtualenv.install_package(pytestconfig.rootpath, build_egg=True, installer="pip install")

    return virtualenv.run("python -c 'from sys import executable; print(executable)'", capture=True).strip()


@pytest.fixture(autouse=True)
def configure_pytester(plugin_virtualenv, pytester):
    pytester.plugins.append("celery")
    pytester._getpytestargs = lambda: (plugin_virtualenv, "-mpytest")
