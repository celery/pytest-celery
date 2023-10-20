from sphinx_celery import conf

globals().update(
    conf.build_config(
        "pytest_celery",
        __file__,
        project="Pytest Celery",
        version_dev="2.0",
        version_stable="1.0",
        canonical_url="https://docs.pytest-celery.dev",  # Update with your documentation URL
        webdomain="pytest-celery.dev",  # Update with your domain
        github_project="celery/pytest-celery",
        author="Tomer Nosrati",
        author_name="Tomer Nosrati",
        copyright="2023",
        publisher="Celery Project",
        # html_logo='images/logo.png',
        # html_favicon='images/favicon.ico',
        extra_extensions=[
            "sphinx_click",
            "sphinx.ext.napoleon",
            # ... other extensions ...
        ],
        extra_intersphinx_mapping={
            # ... other intersphinx mappings ...
        },
        apicheck_ignore_modules=[],
        linkcheck_ignore=[r"^http://localhost"],
    )
)

settings = {}
