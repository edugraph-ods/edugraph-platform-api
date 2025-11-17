from dataclasses import dataclass, field
from typing import List, Optional

"""
Course is a dataclass that represents a curriculum course node in the graph.

Args:
    code (str): Unique course code.
    name (str): Course name.
    credits (int): Course credits.
    cycle (int): Academic cycle/semester number.
    university (Optional[str]): University name.
    career (Optional[str]): Career/major.
    program (Optional[str]): Program name/track.
    prerequisites (List[str]): List of prerequisite course codes.

Returns:
    Course: The Course instance.
"""
@dataclass
class Course:
    code: str
    name: str
    credits: int
    cycle: int
    university: Optional[str] = None
    career: Optional[str] = None
    program: Optional[str] = None
    prerequisites: List[str] = field(default_factory=list)
