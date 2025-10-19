from typing import Dict, List, Optional, Set
from app.core.ports.graph_repository import GraphRepository
from app.core.ports.algorithm_service import AlgorithmService


class PlanRouteUseCase:
    def __init__(self, repository: GraphRepository, algorithm: AlgorithmService):
        self.repository = repository
        self.algorithm = algorithm

    def execute(
        self,
        max_credits: int,
        approved: Optional[Set[str]] = None,
        target_codes: Optional[Set[str]] = None,
        failures: Optional[Dict[int, Set[str]]] = None,
        courses_override: Optional[List] = None,
    ) -> Dict:
        courses = courses_override if courses_override is not None else self.repository.get_courses()
        return self.algorithm.plan_min_cycles(
            courses=courses,
            max_credits=max_credits,
            approved=approved,
            target_codes=target_codes,
            failures=failures,
        )
