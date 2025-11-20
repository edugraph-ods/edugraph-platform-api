from abc import ABC, abstractmethod

from app.features.education.courses.domain.models.course_prerrequisite import CoursePrerequisite

class CoursePrerequisiteRepository(ABC):

    @abstractmethod
    async def save(self, course_prerequisite: CoursePrerequisite) -> CoursePrerequisite:
        pass