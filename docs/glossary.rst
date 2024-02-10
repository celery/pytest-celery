.. _glossary:

Glossary
========

.. glossary::
    :sorted:

    tbd
        To be defined.

    container
        A container in the context of pytest-celery is a low level implementation of a Celery architecture
        component.

    node
        A node in the context of pytest-celery is a high level implementation of a Celery architecture
        component.

    component
        Celery architecture component that is defined using a container, a node, APIs & pytest fixtures.
        It is a collective name for all of the parts that compose a component, according to the pytest-celery
        design.

    vendor
        Independent built-in components provided by the plugin. Vendors can be used as-is,
        reconfigured, extended or overridden completely by the user.
