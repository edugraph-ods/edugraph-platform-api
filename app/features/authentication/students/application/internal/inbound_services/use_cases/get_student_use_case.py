from app.features.authentication.students.domain.repositories.student_repository import StudentRepository
from app.features.authentication.users.domain.repositories.user_repository import UserRepository
from app.features.education.universities.domain.repositories.university_repository import UniversityRepository


class GetStudentProfileUseCase:
    def __init__(self, student_repository: StudentRepository, user_repository: UserRepository, university_repository: UniversityRepository):
        self.student_repository = student_repository
        self.user_repository = user_repository
        self.university_repository = university_repository

    async def execute(self, user_id: str):
        print(user_id)
        student = await self.student_repository.get_student_by_user_id(user_id)
        print(student)
        if not student:
            raise ValueError("Student not found")

        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        university = await self.university_repository.find_by_id(student.university_id)
        if not university:
            raise ValueError("University not found")

        return {
            "id": student.id,
            "name": student.name,
            "email": user.email,
            "university": university.name,
            "university_id": university.id,
        }
