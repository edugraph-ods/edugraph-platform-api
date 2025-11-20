from dataclasses import dataclass

from app.features.education.courses.domain.models.course import Course
from app.features.education.courses.domain.value_objects.course_status import CourseStatus
from app.features.education.courses.domain.value_objects.cycle_credits import CycleCredits


@dataclass
class CourseProgress:
    course: Course
    current_cycle: CycleCredits
    status: CourseStatus = CourseStatus.NOT_STARTED

    def simulate_change_status(self, new_status: CourseStatus, approved_courses: set[str]):
        if new_status == CourseStatus.PASSED:
            if not self.course.prerequisites.all_met(approved_courses):
                missing = [pr for pr in self.course.prerequisites.course_ids if pr not in approved_courses]
                raise ValueError(f"Cannot mark as PASSED, missing prerequisites: {missing}")
        self.status = new_status
