from enum import Enum

class CourseStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    PASSED = "PASSED"
    FAILED = "FAILED"
