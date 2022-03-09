from abc import ABCMeta


class Node(metaclass=ABCMeta):
    """
    A node is always instantiated by a MessageBroker (in the future, also by a ResultBackend).
    The node instance provides a vhost, a URL at which to access the MessageBroker.
    """
    pass
