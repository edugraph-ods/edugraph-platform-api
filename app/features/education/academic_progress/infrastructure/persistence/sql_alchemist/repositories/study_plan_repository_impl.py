from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.features.education.academic_progress.domain.models.entities.study_plan import StudyPlan
from app.features.education.academic_progress.domain.repositories.study_plan_repository import StudyPlanRepository
from app.features.education.academic_progress.infrastructure.persistence.sql_alchemist.models.study_plan_course_model import \
    StudyPlanCourseModel
from app.features.education.academic_progress.infrastructure.persistence.sql_alchemist.models.study_plan_cycle_model import \
    StudyPlanCycleModel
from app.features.education.academic_progress.infrastructure.persistence.sql_alchemist.models.study_plan_model import \
    StudyPlanModel
from app.features.shared.infrastructure.persistence.sql_alchemist.repositories.base_repository import BaseRepository


class StudyPlanRepositoryImpl(StudyPlanRepository, BaseRepository):

    def __init__(self, db_session):
        BaseRepository.__init__(self, db_session, None)
        self.db = db_session

    def _to_domain(self, model) -> StudyPlan:
        return StudyPlan(
            id=model.id,
            name=model.name,
            max_credits=model.max_credits,
            student_id=model.student_id,
            career_id=model.career_id,
        )

    def save(self, plan: StudyPlan) -> StudyPlan:
        model = StudyPlanModel(
            id=plan.id,
            name=plan.name,
            max_credits=plan.max_credits,
            student_id=plan.student_id,
            career_id=plan.career_id,
        )
        self.create(model)
        return plan

    async def get_by_id_with_all_relations(self, plan_id: str):
        stmt = (
            select(StudyPlanModel)
            .where(StudyPlanModel.id == plan_id)
            .options(
                selectinload(StudyPlanModel.cycles)
                .selectinload(StudyPlanCycleModel.courses)
                .selectinload(StudyPlanCourseModel.prerequisites)
            )
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_id(self, plan_id: int) -> StudyPlan | None:
        pass

