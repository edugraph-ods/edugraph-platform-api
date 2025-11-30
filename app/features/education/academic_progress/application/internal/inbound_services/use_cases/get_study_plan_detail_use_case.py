from app.features.education.academic_progress.domain.repositories.study_plan_repository import StudyPlanRepository

class GetStudyPlanDetailUseCase:

    def __init__(self, study_plan_repo: StudyPlanRepository):
        self.study_plan_repo = study_plan_repo

    async def execute(self, plan_id: str):
        plan_model = await self.study_plan_repo.get_by_id_with_all_relations(plan_id)
        if not plan_model:
            raise ValueError("Study plan not found")
        return plan_model