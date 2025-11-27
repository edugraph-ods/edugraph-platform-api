from app.features.education.academic_progress.domain.repositories.study_plan_repository import StudyPlanRepository

class GetStudentStudyPlanUseCase:

    def __init__(self, study_plan_repo: StudyPlanRepository):
        self.study_plan_repo = study_plan_repo

    async def execute(self, student_id: str):
        plan_list = await self.study_plan_repo.get_all_study_plan_by_student_id(student_id)

        if not plan_list:
            raise ValueError("Study plan not found")

        return plan_list
