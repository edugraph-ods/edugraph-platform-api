import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


def _generate_object_id() -> str:
    return uuid.uuid4().hex[:24]

@dataclass
class University:
    name: str
    acronym: str

    id: str = field(default_factory=_generate_object_id)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(cls, name: str, acronym: str):
        return cls(
            name=name,
            acronym=acronym,
        )
