from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.features.education.academic_progress.domain.models.entities.study_plan import StudyPlan
from app.features.education.academic_progress.domain.repositories.study_plan_repository import StudyPlanRepository
from app.features.education.academic_progress.infrastructure.persistence.sql_alchemist.models import \
    StudyPlanCoursePrerequisiteModel
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

    async def save(self, plan: StudyPlan) -> StudyPlan:
        model = StudyPlanModel(
            id=plan.id,
            name=plan.name,
            max_credits=plan.max_credits,
            student_id=plan.student_id,
            career_id=plan.career_id,
        )

        for cycle in plan.cycles:
            cycle_model = StudyPlanCycleModel(
                id=cycle.id,
                cycle_number=cycle.cycle_number,
                study_plan_id=model.id
            )

            for course in cycle.courses:
                course_model = StudyPlanCourseModel(
                    id=course.id,
                    course_id=course.course_id,
                    name=course.name,
                    credits=course.credits,
                    status=course.status,
                    cycle_id=cycle_model.id
                )

                for prereq in course.prerequisites:
                    prereq_model = StudyPlanCoursePrerequisiteModel(
                        id=prereq.id,
                        study_plan_course_id=course_model.id,
                        prerequisite_course_code=prereq.id,
                    )
                    course_model.prerequisites.append(prereq_model)

                cycle_model.courses.append(course_model)

            model.cycles.append(cycle_model)

        await self.create(model)
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

    async def get_by_id(self, plan_id: int) -> StudyPlan | None:
        stmt = select(StudyPlanModel).where(StudyPlanModel.id == plan_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            return self._to_domain(model)
        return None

    async def delete(self, plan_id: str) -> bool:
        stmt = select(StudyPlanModel).where(StudyPlanModel.id == plan_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return False

        await self.session.delete(model)
        await self.session.commit()
        return True

    async def get_all_study_plan_by_student_id(self, student_id: str) -> list[StudyPlan]:
        stmt = select(StudyPlanModel).where(StudyPlanModel.student_id == student_id)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]



