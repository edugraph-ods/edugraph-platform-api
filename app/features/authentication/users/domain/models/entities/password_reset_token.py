from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


def _generate_object_id() -> str:
    return uuid.uuid4().hex[:24]


@dataclass
class PasswordResetToken:
    user_id: str
    token_hash: str
    expires_at: datetime
    used: bool = False
    id: str = field(default_factory=_generate_object_id)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    used_at: Optional[datetime] = None

    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at
