"""
Functional Programming stuffs
"""
from operator import and_
from typing import Callable, Any

from toolz.curried import juxt, reduce, compose, curry


def verify(*conditions) -> Callable[[Any], bool]:
    return compose(
        reduce(and_),
        juxt(*conditions)
    )

getattr = curry(getattr)

