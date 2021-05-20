from typing import Callable, Dict

import pytest

from CQRS.types.interface import (
    Interface,
    InterfaceImplementationError,
    implements,
)


def test_simple_implements():
    class IFoo(Interface):
        def hello(self): ...

    @implements(IFoo)
    class MyFoo:
        def hello(self):
            pass

def test_simple_exception():
    class IFoo(Interface):
        def hello(self): ...

    with pytest.raises(InterfaceImplementationError):
        @implements(IFoo)
        class Bar:
            def hi(self):
                pass

    with pytest.raises(InterfaceImplementationError):
        @implements(IFoo)
        class Bar:
            def hello(self, name:str):
                pass

def test_typed_prototype():
    class IFoo(Interface):
        def hello(self, name:str): ...

    @implements(IFoo)
    class MyFoo:
        def hello(self, name:str):
            pass

    with pytest.raises(InterfaceImplementationError):
        @implements(IFoo)
        class Bar:
            def hello(self, name:int):
                pass

    with pytest.raises(InterfaceImplementationError):
        @implements(IFoo)
        class Bar:
            def hello(self, first_name:str):
                pass
    with pytest.raises(InterfaceImplementationError):
        @implements(IFoo)
        class Bar:
            def hello(self, name:str) -> float:
                pass

def test_complexe_typed_prototype():
    class IFoo(Interface):
        def hello(self, name:Callable[[int], Dict[str,str]]) -> Dict[str,str]: ...

    @implements(IFoo)
    class MyFoo:
        def hello(self, name:Callable[[int], Dict[str,str]]) -> Dict[str,str]:
            pass

    with pytest.raises(InterfaceImplementationError):
        @implements(IFoo)
        class Bar:
            def hello(self, name: Callable[[int], Dict[str, str]]) -> Dict[str, int]:
                pass

    with pytest.raises(InterfaceImplementationError):
        @implements(IFoo)
        class Bar:
            def hello(self, name: Callable[[int], Dict[float, str]]) -> Dict[str, str]:
                pass

