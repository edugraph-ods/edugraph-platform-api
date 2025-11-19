from app.features.authentication.students.domain.repositories.student_repository import StudentRepository
from app.features.authentication.users.domain.repositories.user_repository import UserRepository


class GetStudentProfileUseCase:
    def __init__(self, student_repository: StudentRepository, user_repository: UserRepository):
        self.student_repository = student_repository
        self.user_repository = user_repository

    async def execute(self, user_id: str):
        print(user_id)
        student = await self.student_repository.get_student_by_user_id(user_id)
        print(student)
        if not student:
            raise ValueError("Student not found")

        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        return {
            "name": student.name,
            "email": user.email
        }
