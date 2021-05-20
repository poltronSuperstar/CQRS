from typing import List, Type

from toolz import sliding_window, first

from CQRS.types.message import Message, MessageType
from CQRS.types.middleware import middleware


class MiddlewareBus:
    def __init__(self,
                 listen_for:MessageType,
                 *middlewares:List[middleware]):
        self._listen_for = listen_for
        self.middlewares = list(middlewares)
        self.prepare_pipe()

    def prepare_pipe(self):
        print('__________')
        print('__________')
        print('__________')
        print('__________')
        for a, b in sliding_window(2, self.middlewares):
            print(f"injecting {b} in {a}")
            a.inject_next(b)
        print('__________')
        print('__________')
        print('__________')

    def __call__(self, message):
        return first(self.middlewares)(message)
