from app.features.education.academic_progress.domain.repositories.study_plan_repository import StudyPlanRepository

class DeleteStudyPlanUseCase:

    def __init__(self, study_plan_repo: StudyPlanRepository):
        self.study_plan_repo = study_plan_repo

    async def execute(self, plan_id: str) -> None:
        deleted = await self.study_plan_repo.delete(plan_id)
        if not deleted:
            raise ValueError(f"Study plan with id {plan_id} not found")
