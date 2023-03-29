from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AuthReply(_message.Message):
    __slots__ = ["can_view"]
    CAN_VIEW_FIELD_NUMBER: _ClassVar[int]
    can_view: bool
    def __init__(self, can_view: bool = ...) -> None: ...

class AuthRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...
