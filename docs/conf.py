from sphinx_celery import conf

config = conf.build_config(
    "pytest_celery",
    __file__,
    project="pytest_celery",
    version_dev="1.3",
    version_stable="1.2",
    canonical_url="https://pytest-celery.readthedocs.io/",
    webdomain="pytest-celery.readthedocs.io",
    github_project="celery/pytest-celery",
    author="Tomer Nosrati",
    author_name="Tomer Nosrati",
    copyright="2025",
    publisher="Celery Project",
    html_logo="images/celery_512.png",
    html_favicon="images/favicon.ico",
    html_prepend_sidebars=["sidebardonations.html"],
    extra_extensions=[
        "sphinx_click",
        "sphinx.ext.napoleon",
        "celery.contrib.sphinx",
        "sphinxcontrib.mermaid",
    ],
    apicheck_ignore_modules=[
        r"celery.contrib.*",
    ],
    linkcheck_ignore=[
        r"^http://localhost",
        r"^http://0.0.0.0",
        r"https://github\.com/Jc2k/pytest-docker-tools\?tab=readme-ov-file#images",
        r"https://github\.com/Jc2k/pytest-docker-tools\?tab=readme-ov-file#containers",
        r"https://github\.com/Jc2k/pytest-docker-tools\?tab=readme-ov-file#fixture-wrappers",
        r"https://github\.com/celery/celery/blob/main/requirements/test\.txt#L2",
        r"https://github\.com/celery/celery/blob/main/tox\.ini#L30",
        r"https://www\.opensource\.org/license/BSD-3-Clause",
        r"https://pypi\.org/project/pytest-celery/#history",
    ],
    autodoc_mock_imports=[],
)

del config["intersphinx_mapping"]["eventlet"]

globals().update(config)

settings = {}
ignored_settings = {}


def configcheck_project_settings():
    return set(settings)


def configcheck_should_ignore(setting):
    return setting in ignored_settings
