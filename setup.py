import os
from setuptools import setup, find_packages

requirements = [
    "celery>= 5.2.0",
    "pytest>=6.2.5",
    "testcontainers[redis]>=3.4.2",
    "APScheduler~=3.8.1",
]

test_dependencies = {
    "test": [
        "pytest>=6.2.5",
        "pytest-cov~=3.0.0",
        "pytest-xdist>=2.4.0",
        "mocket[speedups]~=3.10.4",
        "Faker~=11.3.0",
        "pyfakefs~=4.5.4",
        "testcontainers~=3.4.2",
        "docker-py~=1.10.6",
        "pytest-subtests~=0.6.0"
    ]
}

docs_dependencies = {
    "docs": [
        "Sphinx~=4.3.1"
    ]
}

extras = {**test_dependencies, **docs_dependencies}

entry_points = {"pytest11": ["celery = pytest_celery.plugin"]}

setup(
    name="pytest-celery",
    version="1.0.0a1",
    author="Thomas Grainger",
    author_email="pytest-celery@graingert.co.uk",
    description="Pytest plugin for Celery.",
    license="BSD",
    url="https://github.com/celery/pytest-celery",
    packages=find_packages('.', exclude=['tests*', 'examples*']),
    classifiers=["License :: OSI Approved :: BSD License"],
    python_requires=">= 3.7,<4.0",
    install_requires=requirements,
    extras_require=extras,
    entry_points=entry_points,
)
