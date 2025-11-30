from typing import List

class Prerequisites:
    def __init__(self, course_ids: List[str]):
        self.course_ids = course_ids

    def all_met(self, approved_courses: set[str]) -> bool:
        return all(pr in approved_courses for pr in self.course_ids)
