from typing import Dict, List, Optional, Set

from app.features.education.domain.models.course import Course
from app.shared.infrastructure.algorithms.services.algorithm_service import AlgorithmService
from app.features.education.domain.repositories.graph_repository import GraphRepository

"""
RoutePlanner is a class that plans the minimum number of cycles for the given list of courses.

Args:
    repository (GraphRepository): The graph repository.
    algorithm_service (AlgorithmService): The algorithm service.
"""
class RoutePlanner:
    """
    RoutePlanner is a class that plans the minimum number of cycles for the given list of courses.

    Args:
        repository (GraphRepository): The graph repository.
        algorithm_service (AlgorithmService): The algorithm service.
    """
    def __init__(self, repository: GraphRepository, algorithm_service: AlgorithmService):
        self.repository = repository
        self.algorithm_service = algorithm_service

    """
    plan is a method that plans the minimum number of cycles for the given list of courses.

    Args:
        max_credits (int): The maximum number of credits.
        approved (Optional[Set[str]], optional): The set of approved courses. Defaults to None.
        target_codes (Optional[Set[str]], optional): The set of target courses. Defaults to None.
        failures (Optional[Dict[int, Set[str]]], optional): The set of failures. Defaults to None.
        courses_override (Optional[List[Course]], optional): The list of courses to override. Defaults to None.

    Returns:
        Dict: The plan of the minimum number of cycles.
    """
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
