from app.features.education.academic_progress.domain.repositories.study_plan_repository import StudyPlanRepository

class GetStudyPlanUseCase:

    def __init__(self, study_plan_repo: StudyPlanRepository):
        self.study_plan_repo = study_plan_repo

    async def execute(self, plan_id: str, student_id: str):
        plan = await self.study_plan_repo.get_by_id_with_all_relations(plan_id)

        if not plan:
            raise ValueError("Study plan not found")

        if plan.student_id != student_id:
            raise PermissionError("You do not own this study plan")

        return plan
