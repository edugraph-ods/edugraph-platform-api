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

        approved = set(
            i for i, cp in enumerate(self.courses)
            if cp.status == CourseStatus.PASSED
        )

        def prereqs_met_idx(idx: int) -> bool:
            prereq_ids = self.courses[idx].course.prerequisites.course_ids
            return all(self.index_map.get(pr) in approved for pr in prereq_ids)

        def select_courses_knapsack(available_indices: List[int]) -> List[int]:
            C = self.max_credits
            dp = [(-1, 0, None) for _ in range(C + 1)]
            dp[0] = (0, 0, None)
            parent = [[False for _ in range(len(available_indices))] for _ in range(C + 1)]

            for j, idx in enumerate(available_indices):
                w = self.courses[idx].course.credits
                for c in range(C, w - 1, -1):
                    if dp[c - w][0] != -1:
                        cand_credits = dp[c - w][0] + w
                        cand_count = dp[c - w][1] + 1
                        best_credits, best_count, _ = dp[c]
                        if cand_credits > best_credits or (cand_credits == best_credits and cand_count > best_count):
                            dp[c] = (cand_credits, cand_count, j)
                            parent[c] = parent[c - w].copy()
                            parent[c][j] = True

            best_c = max(range(C + 1), key=lambda c: (dp[c][0], dp[c][1]))
            chosen = []
            choose_mask = parent[best_c]
            for j, take in enumerate(choose_mask):
                if take:
                    chosen.append(available_indices[j])
            return chosen

        cycles = 0
        if n == 0:
            return 0

        min_cycle = min(cp.course.cycle for cp in self.courses)
        max_cycle = max(cp.course.cycle for cp in self.courses)
        current_cycle = min_cycle

        while len(approved) < n:
            available = [
                i for i in range(n)
                if i not in approved and self.courses[i].course.cycle <= current_cycle and prereqs_met_idx(i)
            ]

            if available:
                chosen = select_courses_knapsack(available)
                if not chosen:
                    return None
                for i in chosen:
                    approved.add(i)
            else:
                if current_cycle >= max_cycle:
                    return None
            cycles += 1
            if current_cycle < max_cycle:
                current_cycle += 1

        return cycles

    def update_course_availability(self):
        approved_courses = {cp.course.id for cp in self.courses if cp.status == CourseStatus.PASSED}
        for cp in self.courses:
            if cp.status not in [CourseStatus.PASSED, CourseStatus.FAILED]:
                if not cp.course.prerequisites.all_met(approved_courses):
                    cp.status = CourseStatus.NOT_STARTED
        return self.courses
