from __future__ import annotations

import json
from copy import copy
from datetime import datetime
from typing import Dict, Any, Optional, Type, TypeVar


class Message:
    """
    Base class for Command, Query & Response
    """

    _REGISTER = {}

    def __init_subclass__(cls, **kwargs):
        Message._REGISTER[type(cls).__name__] = cls

    def __init__(
        self, payload: Dict[str, Any], headers: Optional[Dict[str, Any]] = None
    ):
        self.payload = payload
        self.headers = self.build_headers(headers or {})
        self.validate_payload()

    def validate_payload(self):
        pass

    def build_headers(self, base_headers: Dict[str, Any]) -> Dict[str, Any]:
        headers = copy(base_headers)
        if not "created_at" in headers:
            # Note: Command, Query and Response should never be persisted,
            #       created_at is mostly useful for logging purpose
            headers["created_at"] = datetime.now().timestamp()

        return headers

    def as_dict(self) -> Dict[str, Any]:
        return {
            "_type": type(type(self).__name__),
            "headers": self.headers,
            "payload": self.payload,
        }

    def serialize(self) -> str:
        return json.dumps(self.as_dict())

    @staticmethod
    def unserialize(message_json: str) -> Message:
        message_dict = json.loads(message_json)
        return Message._REGISTER[message_dict["_type"]](
            payload=message_dict["payload"], headers=message_dict["headers"]
        )

    def __repr__(self):
        return f"""
#####################
 {type(self).__name__}
#####################
headers: {self.headers}
payload: {self.payload}
        """

# for type hint purposes
MessageType = Type[TypeVar('MessageType', bound=Message)]
