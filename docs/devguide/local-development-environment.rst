.. _local-development-environment:

===============================
 Local Development Environment
===============================

:Release: |version|
:Date: |today|

.. contents::
    :local:
    :depth: 2

Cloning the Repository
======================

Clone the repository from GitHub: https://github.com/celery/pytest-celery

**Https**::

    https://github.com/celery/pytest-celery.git

**SSH**::

    git@github.com:celery/pytest-celery.git

**GitHub CLI**::

    gh repo clone celery/pytest-celery

Using Poetry
============

The plugin uses `Poetry <https://python-poetry.org/>`_ for dependency management.

To install the development dependencies, run the following command in your desired virtual environment::

    poetry install -E "all" --with test,dev,ci,docs

.. tip::

    During development of the dependencies themselves, you can use the following snippet for easy cleanup & reinstallation of the dependencies::

        pip uninstall pytest-celery celery -y && pip freeze | cut -d "@" -f1 | xargs pip uninstall -y;\
        pip install -U pip ipython;\
        poetry install -E "all" --with test,dev,ci,docs

Debugging with VSCode
=====================

Create a ``.vscode`` directory with the following ``launch.json`` file that can be used to for debugging.

.. note::

    Take note of ``"justMyCode": false``

.. code-block:: json

    {
        // Use IntelliSense to learn about possible attributes.
        // Hover to view descriptions of existing attributes.
        // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Debug Tests",
                "type": "python",
                "request": "launch",
                "program": "${file}",
                "purpose": [
                    "debug-test",
                ],
                "console": "integratedTerminal",
                "justMyCode": false,
                "presentation": {
                    "hidden": true
                },
                // Disable cov to allow breakpoints when launched from VS Code Python
                "env": {
                    "PYTHONUNBUFFERED": "1",
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "PYTEST_ADDOPTS": "--no-cov --exitfirst"
                },
                "stopOnEntry": false,
                "showReturnValue": true,
                "redirectOutput": true
            }
        ]
    }
