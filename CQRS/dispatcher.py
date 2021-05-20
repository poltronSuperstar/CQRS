from typing import Dict

from CQRS.types.message import MessageType, Message
from CQRS.types.middlewarebus import MiddlewareBus
from CQRS.types.response import Response


class Dispatcher:
    def __init__(self):
        self.middleware_buses:Dict[MessageType, MiddlewareBus] = {}

    def register(self, middleware_bus:MiddlewareBus):
        assert not middleware_bus._listen_for in self.middleware_buses

        self.middleware_buses[middleware_bus._listen_for] = middleware_bus

    def dispatch(self, message:Message) -> Response:
        return self.middleware_buses[type(message)](message)