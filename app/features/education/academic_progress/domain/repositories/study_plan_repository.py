from abc import ABC, abstractmethod

from app.features.education.academic_progress.domain.models.entities.study_plan import StudyPlan


class StudyPlanRepository(ABC):

    @abstractmethod
    def save(self, plan: StudyPlan) -> StudyPlan:
        pass

    @abstractmethod
    async def get_by_id_with_all_relations(self, plan_id: str) -> StudyPlan | None:
        pass

    @abstractmethod
    def get_by_id(self, plan_id: int) -> StudyPlan | None:
        pass
