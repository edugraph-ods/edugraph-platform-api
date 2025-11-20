from itertools import combinations
from functools import lru_cache
from typing import List

from app.features.education.academic_progress.domain.models.entities.academic_progress import CourseProgress
from app.features.education.academic_progress.domain.models.value_objects.course_status import CourseStatus


class AcademicProgressUseCase:
    def __init__(self, course_progress_list: List[CourseProgress], max_credits: int):
        self.courses = course_progress_list
        self.max_credits = max_credits
        self.index_map = {cp.course.id: i for i, cp in enumerate(course_progress_list)}

    def compute_min_cycles(self) -> int | None:
        n = len(self.courses)
        initial_mask = 0
        courses_to_take = []

        for i, cp in enumerate(self.courses):
            if cp.status == CourseStatus.PASSED:
                initial_mask |= (1 << i)
            else:
                courses_to_take.append(i)

        def prereqs_met(mask, idx):
            return all(mask & (1 << self.index_map[pr]) for pr in self.courses[idx].course.prerequisites.course_ids)

        @lru_cache(None)
        def dp(mask):
            if mask == (1 << n) - 1:
                return 0

            available_courses = [
                i for i in courses_to_take
                if not (mask & (1 << i)) and prereqs_met(mask, i)
            ]

            if not available_courses:
                return float('inf')

            best = float('inf')
            for r in range(1, len(available_courses) + 1):
                for subset in combinations(available_courses, r):
                    total_credits = sum(self.courses[i].course.credits for i in subset)
                    if total_credits <= self.max_credits:
                        new_mask = mask
                        for i in subset:
                            new_mask |= (1 << i)
                        best = min(best, 1 + dp(new_mask))
            return best

        min_cycles = dp(initial_mask)
        return min_cycles if min_cycles != float('inf') else None

    def update_course_availability(self):
        approved_courses = {cp.course.id for cp in self.courses if cp.status == CourseStatus.PASSED}
        for cp in self.courses:
            if cp.status not in [CourseStatus.PASSED, CourseStatus.FAILED]:
                if not cp.course.prerequisites.all_met(approved_courses):
                    cp.status = CourseStatus.NOT_STARTED
        return self.courses
