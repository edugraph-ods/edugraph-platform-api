from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class CycleCredits:
    total_credits: int
    min_credits: int = 7

    def __post_init__(self):
        if self.total_credits < self.min_credits:
            raise ValueError(f"Total credits {self.total_credits} is less than the minimum required {self.min_credits}")

    @classmethod
    def from_courses(cls, courses: List):
        total = sum(course.credits for course in courses)
        return cls(total_credits=total)
