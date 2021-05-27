import json
from collections import defaultdict
from datetime import datetime
from functools import wraps
from typing import Any, Dict, TypeVar, Callable

from typeguard import check_type

T = TypeVar('T', bound='ValueObject')

def identity(value):
    return value

def truisme(*a, **k):
    return True


class ValidationError(Exception):
    """

    """

class ValueObjectSerializerRegistry(defaultdict):
    pass

class ValueObject:
    _REGISTRY = ValueObjectSerializerRegistry(truisme)



    class Field:
        def __init__(self,
                     optionnal:bool=False,
                     coerce:Callable=identity,
                     validation=truisme):
            self.optionnal = optionnal
            self.coerce = coerce
            self.validation = validation

        def __call__(self, value):
            if self.optionnal or value is None:
                raise ValidationError(f"{type(self)} cannot be None")

    def __init_subclass__(cls, **kwargs):

        ValueObject._REGISTRY[cls.__qualname__] = cls
        assert '_type' in kwargs
        cls._type = kwargs['_type']

    def coerce(self, value:Any) -> Any:
        return value

    def validate(self, value:Any) -> None:
        """

        :param value:
        :return:
        :raises: ValidationError
        """
        check_type('value', value, self._type)



    def __init__(self, value:Any):
        self.validate(value)
        self._is_struct = hasattr(self._type,'_name') \
                          and self._type._name in ['List', 'Dict']
        self._set_value(value)

    def _set_value(self, value:Any) -> None:

        self.value = self.coerce(self._cast(value))

        if not self._is_struct:
            return

        for field, field_type in self.__annotations__.items():
            field_value = value.get(field)
            check_type(field, field_value, field_type)
            setattr(self, field, field_value)

    def _cast(self, value:Any) -> Any:
        if isinstance(value,(int, float, str, bytes, bool)):
            return self._type(value)

        return value


    def serialize_dict(self) -> Dict[str,Any]:
        return {
            "_type":type(self).__qualname__,
            "value": self.value
        }

    def serialize_json(self) -> str:
        return json.dumps(self.serialize_dict())


    @staticmethod
    def deserialize_dict(vo:Dict[str, Any]) -> T:
        return ValueObject._REGISTRY[vo['_type']](vo['value'])

    @staticmethod
    def deserialize(vo):
        if isinstance(vo, dict) and '_type' in vo:
            return ValueObject.deserialize_dict(vo)

        return vo


    @staticmethod
    def deserialize_json(vo_str:str) -> T:
        return ValueObject.deserialize_dict(json.loads(vo_str))

    @classmethod
    def autowrap(cls, func:Callable) -> Callable:
        """
        Wraps litterals into ValueObject based on annotations
        :param func:
        :return:
        """
        @wraps(func)
        def _decorator(*args, **kwargs):
            for name, wrapper_type in func.__annotations__.items():
                provided_value = kwargs.get(name)

                if provided_value is None:
                    raise Exception(f"You should use kwargs for {name}, lol")

                if isinstance(wrapper_type, str) \
                        and hasattr(args[0], wrapper_type) \
                        and issubclass(getattr(args[0], wrapper_type), cls):
                    wrapper_type = getattr(args[0], wrapper_type) # type: ValueObject

                if issubclass(wrapper_type, cls) \
                        and isinstance(provided_value, wrapper_type._type):
                    kwargs['name'] = wrapper_type(kwargs['name'])

            return func(*args, **kwargs)

        return _decorator


    @property
    def _type_name(self) -> str:
        try:
            return self._type.__name__
        except AttributeError:
            return str(self._type).replace('typing.','')

    def __repr__(self):

        return f"{type(self).__qualname__}({json.dumps(self.value)}) : {self._type_name}"

    def __eq__(self, other):
        return self._type == other._type and self.value == other.value

