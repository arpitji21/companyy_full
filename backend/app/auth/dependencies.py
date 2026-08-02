from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.exceptions import InactiveUserError, InvalidTokenError, PermissionDeniedError
from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/auth/login", auto_error=False)


def get_current_user(token: str | None = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    if not token:
        raise InvalidTokenError("Not authenticated.")

    try:
        payload = decode_token(token)
    except JWTError:
        raise InvalidTokenError("Could not validate credentials.")

    if payload.get("type") != "access":
        raise InvalidTokenError("Token is not an access token.")

    user = UserRepository(db).get(payload["sub"])
    if not user:
        raise InvalidTokenError("User not found.")
    return user


def get_current_active_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_active:
        raise InactiveUserError("This account has been deactivated.")
    return user


def require_roles(*allowed_roles: str):
    """Usage: `Depends(require_roles("CEO", "Admin"))` on any route."""

    def _checker(user: User = Depends(get_current_active_user)) -> User:
        if user.is_superuser:
            return user
        role_name = user.role.name if user.role else None
        if role_name not in allowed_roles:
            raise PermissionDeniedError(f"Requires one of roles: {', '.join(allowed_roles)}.")
        return user

    return _checker
