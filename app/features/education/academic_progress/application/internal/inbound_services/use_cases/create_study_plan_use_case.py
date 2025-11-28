from app.features.education.academic_progress.domain.models.entities.study_plan import StudyPlan
from app.features.education.academic_progress.domain.models.entities.study_plan_course import StudyPlanCourse
from app.features.education.academic_progress.domain.models.entities.study_plan_course_prerequisite import \
    StudyPlanCoursePrerequisite
from app.features.education.academic_progress.domain.models.entities.study_plan_cycle import StudyPlanCycle
from app.features.education.academic_progress.domain.repositories.study_plan_repository import StudyPlanRepository
from app.features.education.courses.domain.repositories.course_repository import CourseRepository


class CreateStudyPlanUseCase:

    def __init__(
            self,
            study_plan_repo: StudyPlanRepository,
            course_repo: CourseRepository
    ):
        self.study_plan_repo = study_plan_repo
        self.course_repo = course_repo

    async def execute(self, payload, student_id):
        plan = StudyPlan(
            name=payload.name,
            max_credits=payload.max_credits,
            career_id=payload.career_id,
            student_id=student_id,
            cycles=[]
        )

        for c in payload.cycles:
            cycle = StudyPlanCycle(
                cycle_number=c.cycle_number,
                study_plan_id=plan.id
            )

            for course_item in c.courses:

                course = await self.course_repo.get_by_id(course_item.course_id)
                if not course:
                    raise ValueError(f"Course {course_item.course_id} not found")

                plan_course = StudyPlanCourse(
                    course_id=course.id,
                    name=course.name,
                    credits=course.credits,
                    status=course_item.status,
                    prerequisites=[]
                )

                for prereq_id in course_item.prerequisites:
                    prereq = StudyPlanCoursePrerequisite(
                        prerequisite_course_id=prereq_id
                    )
                    plan_course.prerequisites.append(prereq)

                cycle.courses.append(plan_course)

            plan.cycles.append(cycle)

        saved = await self.study_plan_repo.save(plan)
        return saved