from typing import List, Optional, Tuple
from app.core.ports.graph_repository import GraphRepository
from app.core.ports.algorithm_service import AlgorithmService

"""
DetectCyclesUseCase is a class that represents a detect cycles use case.

Attributes:
    repository (GraphRepository): The graph repository.
    algorithm (AlgorithmService): The algorithm service.

Methods:
    execute(self, courses_override: Optional[List] = None) -> Tuple[bool, List[List[str]]]:
        Executes the detect cycles use case.
"""
class DetectCyclesUseCase:
    def __init__(self, repository: GraphRepository, algorithm: AlgorithmService):
        self.repository = repository
        self.algorithm = algorithm

    def execute(self, courses_override: Optional[List] = None) -> Tuple[bool, List[List[str]]]:
        courses = courses_override if courses_override is not None else self.repository.get_courses()
        return self.algorithm.detect_cycles(courses)
