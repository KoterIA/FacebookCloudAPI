from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TemplateObject:
    namespace: str
    name: str
    language: str
    components: list | None
