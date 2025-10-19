from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set, Tuple
from app.core.entities.course import Course


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
