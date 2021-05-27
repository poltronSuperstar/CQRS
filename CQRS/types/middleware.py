"""
"""
from __future__ import annotations
from typing import Optional, Any, Callable

from CQRS.types.interface import Interface


class middleware:
    """
    Middleware decorator

    Postulate: a MiddleWare is a function with three arguments:
        * The Collaborator (type in prototype should ALWAYS be an interface)
        * A message subtyping Command or Query
        * next_ (Optional) the next middleware in the pipe


    Dependency Injection is done with Currying

    Usage:
    ```
    @middleware
    def log_time(logger:ILogger, command:Command, next_:Optionnal[middleware] = None):
        ...
    ```

    Not, a Command may either subclass Command/Query, or the base types
    (usefull in case of agnostic middleware as loggers)

    """
    def __init__(self, func:Callable[[...], ...]):
        self.func = func
        self._next_ = None

    def inject_collaborator(self, collaborator:Interface):
        self._collaborator = collaborator

    def inject_next(self, next_:middleware):
        self._next_ = next_

    def __call__(self, arg:Any):
        # TODO: Type hint with Union & Message
        if not hasattr(self,'_collaborator'):
            self._collaborator = arg
            return self

        return self.func(self._collaborator,
                         arg,
                         self._next_)