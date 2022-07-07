from __future__ import annotations
from datetime import date
from typing import List
from dataclasses import dataclass
from facebookcloudapi.api.dto.inherited import (
    ActionObject, BodyObject, FooterObject, HeaderObject
)
from facebookcloudapi.api.dto.types import InteractiveType

from facebookcloudapi.utils import clean_dict


@dataclass
class LocationObject:
    """
    From: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/messages#interactive-object
    """
    longitude: str
    latitude: str
    name: str = None
    address: str = None

    def to_dict(self):
        d = clean_dict(self.__dict__)
        return d
