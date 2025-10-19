from typing import Dict, List, Optional, Set

from app.core.entities.course import Course
from app.core.ports.algorithm_service import AlgorithmService
from app.core.ports.graph_repository import GraphRepository


class RoutePlanner:
    def __init__(self, repository: GraphRepository, algorithm_service: AlgorithmService):
        self.repository = repository
        self.algorithm_service = algorithm_service

    def plan(
        self,
        max_credits: int,
        approved: Optional[Set[str]] = None,
        target_codes: Optional[Set[str]] = None,
        failures: Optional[Dict[int, Set[str]]] = None,
        courses_override: Optional[List[Course]] = None,
    ) -> Dict:
        courses = courses_override if courses_override is not None else self.repository.get_courses()
        return self.algorithm_service.plan_min_cycles(
            courses=courses,
            max_credits=max_credits,
            approved=approved,
            target_codes=target_codes,
            failures=failures,
        )
