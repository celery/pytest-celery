from abc import ABCMeta, abstractmethod


class Node(metaclass=ABCMeta):
    """
    A node is always instantiated by a MessageBroker (in the future, also by a ResultBackend).
    The node instance provides a vhost, a URL at which to access the MessageBroker.
    """
    def __init__(self, entity):
        self.entity = entity  # MessageBroker or ResultBackend

    @abstractmethod
    def start(self) -> str:
        """Spin up a container (or reuse if already exists), returning the vhost for the entity"""
        pass

    @abstractmethod
    def stop(self):
        pass

    def __enter__(self) -> str:
        """"""
        return self.entity.start()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """"""
        self.entity.stop()
