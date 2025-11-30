from abc import ABC, abstractmethod

from app.features.education.courses.domain.models.entities.course_prerrequisite import CoursePrerequisite

class CoursePrerequisiteRepository(ABC):

    @abstractmethod
    async def save(self, course_prerequisite: CoursePrerequisite) -> CoursePrerequisite:
        pass

    @abstractmethod
    async def find_by_course_and_prerequisite(self, course_id: str, prerequisite_id: str) -> CoursePrerequisite | None:
        pass