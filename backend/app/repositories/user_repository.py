from sqlalchemy import select

from app.models.user import Role, User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email))

    def list_by_role_names(self, role_names: list[str]) -> list[User]:
        """Active users holding any of the given roles (e.g. ["CEO", "Admin"]).
        Used to fan out notifications to whoever should see them, without the
        caller needing to know how roles are stored."""
        if not role_names:
            return []
        stmt = (
            select(User)
            .join(Role, User.role_id == Role.id)
            .where(Role.name.in_(role_names), User.is_active.is_(True))
        )
        return list(self.db.scalars(stmt).all())
