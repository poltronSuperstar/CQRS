from typing import Callable
import inspect

from CQRS.utils.functional import verify, getattr

class InterfaceImplementationError(Exception):
    pass

class Interface:
    """
    Simple interface mechanism in Python.

    Usage:
        *Creating an interface*
        ```python
        class ILogger(Interface):
            def log(self, content:str) -> None: ...
        ```

        *Implementing an interface*
        ```python
        @implements(ILogger)
        class MyLogger:
            def log(self, content:str) -> None:
                # Do log stuff here
        ```

    """
    @classmethod
    def _check_implements(cls, instance):
        for interface_method in cls._public_methods(cls):
            instance_metod = getattr(instance, interface_method.__name__, None)

            if instance_metod is None\
                or instance_metod.__annotations__ != interface_method.__annotations__:
                raise InterfaceImplementationError(
                    f"{instance.__name__} must implement {inspect.getsource(interface_method)}"
                )

    def _public_methods(cls):
        predicate = verify(
            inspect.isfunction,
            lambda m: hasattr(m, '__name__') and not m.__name__.startswith('_')
        )

        return filter(
            predicate,
            map(
                getattr(cls),
                dir(cls)
            )
        )





# Note & TODO: type hint with "type" fells awkard. Should be generics whenever
#              I have a grasp on how to generic in Python
def implements(interface:Interface) -> Callable[[type], type]:
    def _decorator(cls:type) -> type:
        interface._check_implements(cls)
        setattr(cls, '__implements', interface)

        return cls

    return _decorator

__all__ = [
    'Interface',
    'InterfaceImplementationError',
    'implements',
]