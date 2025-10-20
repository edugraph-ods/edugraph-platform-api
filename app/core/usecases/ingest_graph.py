from typing import Iterable, Optional
from app.core.entities.course import Course
from app.core.ports.parser import Parser
from app.core.ports.graph_repository import GraphRepository

"""
IngestGraphUseCase is a class that represents an ingest graph use case.

Attributes:
    parser (Parser): The parser.
    repository (GraphRepository): The graph repository.

Methods:
    execute(self, source_path: str, university: Optional[str] = None, career: Optional[str] = None, program: Optional[str] = None) -> Iterable[Course]:
        Executes the ingest graph use case.
"""
class IngestGraphUseCase:
    def __init__(self, parser: Parser, repository: GraphRepository):
        self.parser = parser
        self.repository = repository

    def execute(
        self,
        source_path: str,
        university: Optional[str] = None,
        career: Optional[str] = None,
        program: Optional[str] = None,
    ) -> Iterable[Course]:
        courses = list(
            self.parser.load_courses(
                source_path=source_path, university=university, career=career, program=program
            )
        )
        self.repository.set_courses(courses)
        return courses
