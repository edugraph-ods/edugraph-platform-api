from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set, Tuple
from app.features.education.domain.models.course import Course

"""
AlgorithmService is an abstract base class that defines the interface for algorithm services.

Methods:
    detect_cycles(self, courses: List[Course]) -> Tuple[bool, List[List[str]]]:
        Detects cycles in the given list of courses.
    topological_sort(self, courses: List[Course]) -> List[str]:
        Sorts the given list of courses topologically.
    plan_min_cycles(self, courses: List[Course], max_credits: int, approved: Optional[Set[str]] = None, target_codes: Optional[Set[str]] = None, failures: Optional[Dict[int, Set[str]]] = None, max_exact_courses: int = 18) -> Dict:
        Plans the minimum number of cycles for the given list of courses.
"""
class AlgorithmService(ABC):
    @abstractmethod
    def detect_cycles(self, courses: List[Course]) -> Tuple[bool, List[List[str]]]:
        pass

    @abstractmethod
    def topological_sort(self, courses: List[Course]) -> List[str]:
        pass

    @abstractmethod
    def plan_min_cycles(
        self,
        courses: List[Course],
        max_credits: int,
        approved: Optional[Set[str]] = None,
        target_codes: Optional[Set[str]] = None,
        failures: Optional[Dict[int, Set[str]]] = None,
        max_exact_courses: int = 18,
    ) -> Dict:
        pass
