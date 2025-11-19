from dataclasses import dataclass, field
import uuid
from datetime import datetime, timezone


def _generate_object_id() -> str:
    return uuid.uuid4().hex[:24]


@dataclass
class Student:
    name: str
    user_id: str
    university_id: str

    id: str = field(default_factory=_generate_object_id)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(cls, name: str, user_id: str, university_id: str):
        return cls(
            name=name,
            user_id=user_id,
            university_id=university_id,
        )
