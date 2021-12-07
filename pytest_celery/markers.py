from enum import Enum, auto


class MessageBroker(Enum):
    RabbitMQ = auto()
    Redis = auto()


class ResultBackend(Enum):
    RPC = auto()
    Redis = auto()
    MongoDB = auto()
