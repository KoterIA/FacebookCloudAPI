from __future__ import annotations

from dataclasses import dataclass
from facebookcloudapi.api.dto.types.message_type import MessageType


@dataclass
class MessageObject:
    message_type: MessageType
    to: str
    recipient_type: str | None = None
    hsm: dict | None = None
