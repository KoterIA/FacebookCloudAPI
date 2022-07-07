from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    DOCUMENT = "document"
    TEMPLATE = "template"
    HSM = "hsm"


@dataclass
class MessageObject:
    message_type: MessageType
    to: str
    recipient_type: str | None = None
    hsm: dict | None = None
