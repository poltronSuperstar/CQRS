# Mock stuff
import pytest

from CQRS.dispatcher import Dispatcher
from CQRS.types.command import Command
from CQRS.types.interface import Interface, implements
from CQRS.types.middleware import middleware
from CQRS.types.middlewarebus import MiddlewareBus
from CQRS.types.response import Response


class IWatch(Interface):
    def greet(self, hello:str) -> None:...

@implements(IWatch)
class Watcher:
    def __init__(self):
        self.greetings = []

    def greet(self, hello:str) -> None:
        self.greetings.append(hello)

class SayHiCommand(Command):
    ...

class OtherCommand(Command):
    ...

def test_middleware():

    @middleware
    def m1(watcher:IWatch, command:SayHiCommand, next_:middleware ) -> Response:
        watcher.greet(f"{command.payload['content']}1")
        return next_(command)

    @middleware
    def m2(watcher:IWatch, command:SayHiCommand, next_:middleware = None ) -> Response:
        watcher.greet(f"{command.payload['content']}2")

        return Response(payload={'content':"Hi"})

    watcher = Watcher()


    middleware_bus = MiddlewareBus(SayHiCommand,
                                   m1(watcher),
                                   m2(watcher))
    response = middleware_bus(SayHiCommand(payload={"content":"Hello"}))

    assert isinstance(response, Response)
    assert response.payload['content'] == 'Hi'
    assert '_'.join(watcher.greetings) == 'Hello1_Hello2'


def test_dispatcher():
    @middleware
    def m1(watcher: IWatch, command: SayHiCommand, next_: middleware) -> Response:
        watcher.greet(f"{command.payload['content']}1")
        return next_(command)

    @middleware
    def m2(watcher: IWatch, command: SayHiCommand, next_: middleware = None) -> Response:
        watcher.greet(f"{command.payload['content']}2")

        return Response(payload={'content': "Hi"})

    watcher = Watcher()

    middleware_bus = MiddlewareBus(SayHiCommand,
                                   m1(watcher),
                                   m2(watcher))

    dispatcher = Dispatcher()

    dispatcher.register(middleware_bus)
    response = dispatcher.dispatch(SayHiCommand(payload={"content": "Hello"}))

    assert isinstance(response, Response)
    assert response.payload['content'] == 'Hi'
    assert '_'.join(watcher.greetings) == 'Hello1_Hello2'

    with pytest.raises(KeyError):
        dispatcher.dispatch(OtherCommand(payload={"a":'a'}))



