from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.core.exceptions import AppException

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise AppException("User not found", 404)
        return user