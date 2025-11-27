from abc import ABC, abstractmethod

from app.features.education.academic_progress.domain.models.entities.study_plan import StudyPlan


class StudyPlanRepository(ABC):

    @abstractmethod
    async def save(self, plan: StudyPlan) -> StudyPlan:
        pass

    @abstractmethod
    async def get_by_id_with_all_relations(self, plan_id: str) -> StudyPlan | None:
        pass

    @abstractmethod
    async def get_by_id(self, plan_id: str) -> StudyPlan | None:
        pass

    @abstractmethod
    async def delete(self, plan_id: str) -> bool:
        pass

    @abstractmethod
    async def get_all_study_plan_by_student_id(self, student_id: str) -> list[StudyPlan]:
        pass
