from abc import ABCMeta


class Node(metaclass=ABCMeta):

    def __init__(self):
        pass

    def get_message_broker(self, type):
        pass
