from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import AppException

class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, email: str, password: str) -> User:
        if await self.repo.get_by_email(email):
            raise AppException("Email already registered", 409)

        user = User(
            email=email,
            password_hash=hash_password(password),
        )
        return await self.repo.create(user)

    async def login(self, email: str, password: str) -> str:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise AppException("Invalid credentials", 401)

        return create_access_token(user.id)
