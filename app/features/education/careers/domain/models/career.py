import uuid
from dataclasses import dataclass, field


def _generate_object_id() -> str:
    return uuid.uuid4().hex[:24]
@dataclass
class Career:
    name: str
    program: str
    university_id: str

    id: str = field(default_factory=_generate_object_id)

    @classmethod
    def create(cls, name: str, program: str, university_id: str):
        return cls(
            name=name,
            program=program,
            university_id=university_id,
        )