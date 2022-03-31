from pytest_celery.nodes import Node


class RedisNode(Node):
    @property
    def should_create_vhost(self) -> bool:
        return True

    def destroy_vhost(self):
        pass

    def create_vhost(self):
        pass
