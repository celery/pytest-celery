from sphinx_celery import conf

globals().update(
    conf.build_config(
        "pytest_celery",
        __file__,
        project="pytest_celery",
        version_dev="1.1",
        version_stable="1.0",
        canonical_url="https://pytest-celery.readthedocs.io/",
        webdomain="pytest-celery.readthedocs.io",
        github_project="celery/pytest-celery",
        author="Tomer Nosrati",
        author_name="Tomer Nosrati",
        copyright="2024",
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
        linkcheck_ignore=[r"^http://localhost"],
        autodoc_mock_imports=[],
    )
)

settings = {}
ignored_settings = {}


def configcheck_project_settings():
    return set(settings)


def configcheck_should_ignore(setting):
    return setting in ignored_settings
