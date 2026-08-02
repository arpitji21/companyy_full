import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import (
    AlreadyExistsError,
    InactiveUserError,
    InvalidCredentialsError,
    InvalidTokenError,
    NotFoundError,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import EmailVerificationToken, PasswordResetToken, RefreshToken, User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest
from jose import JWTError


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)
        self.roles = RoleRepository(db)

    # ---- Registration -----------------------------------------------------
    def register(self, data: RegisterRequest) -> User:
        if self.users.get_by_email(data.email):
            raise AlreadyExistsError("A user with this email already exists.")

        role = self.roles.get_by_name(data.role_name) if data.role_name else None

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            role_id=role.id if role else None,
            department_id=data.department_id,
        )
        user = self.users.create(user)
        # New accounts start unverified; kick off the verification email in
        # the background so registration itself stays fast.
        self.request_email_verification(user)
        return user

    # ---- Login / tokens -----------------------------------------------------
    def login(self, email: str, password: str) -> tuple[str, str]:
        user = self.users.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Incorrect email or password.")
        if not user.is_active:
            raise InactiveUserError("This account has been deactivated.")

        user.last_login_at = datetime.now(timezone.utc)
        self.db.commit()

        return self._issue_token_pair(user)

    def _issue_token_pair(self, user: User) -> tuple[str, str]:
        role_name = user.role.name if user.role else None
        access = create_access_token(subject=user.id, role=role_name)
        refresh = create_refresh_token(subject=user.id)

        self.db.add(
            RefreshToken(
                user_id=user.id,
                token=refresh,
                expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            )
        )
        self.db.commit()
        return access, refresh

    def refresh_access_token(self, refresh_token: str) -> tuple[str, str]:
        stored = self.db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
        if not stored or stored.revoked or stored.expires_at < datetime.now(timezone.utc):
            raise InvalidTokenError("Refresh token is invalid, expired, or revoked.")

        try:
            payload = decode_token(refresh_token)
        except JWTError:
            raise InvalidTokenError("Refresh token is invalid or expired.")
        if payload.get("type") != "refresh":
            raise InvalidTokenError("Token is not a refresh token.")

        user = self.users.get(payload["sub"])
        if not user or not user.is_active:
            raise InvalidTokenError("User no longer exists or is inactive.")

        # Rotate: revoke the old refresh token and issue a brand new pair.
        stored.revoked = True
        self.db.commit()
        return self._issue_token_pair(user)

    def logout(self, refresh_token: str) -> None:
        stored = self.db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
        if stored:
            stored.revoked = True
            self.db.commit()

    # ---- Password reset -----------------------------------------------------
    def request_password_reset(self, email: str) -> str | None:
        """Returns the raw reset token (caller is responsible for emailing it)."""
        user = self.users.get_by_email(email)
        if not user:
            # Don't leak which emails exist — caller returns a generic message either way.
            return None

        token = secrets.token_urlsafe(32)
        self.db.add(
            PasswordResetToken(
                user_id=user.id,
                token=token,
                expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
            )
        )
        self.db.commit()

        from app.tasks import safe_delay
        from app.tasks.email import send_password_reset_email

        safe_delay(send_password_reset_email, user.email, user.full_name, token)
        return token

    def reset_password(self, token: str, new_password: str) -> None:
        record = self.db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()
        if not record or record.used or record.expires_at < datetime.now(timezone.utc):
            raise InvalidTokenError("Password reset token is invalid or expired.")

        user = self.users.get(record.user_id)
        if not user:
            raise NotFoundError("User not found.")

        user.hashed_password = hash_password(new_password)
        record.used = True
        self.db.commit()

    # ---- Email verification -----------------------------------------------------
    def request_email_verification(self, user: User) -> str:
        token = secrets.token_urlsafe(32)
        self.db.add(
            EmailVerificationToken(
                user_id=user.id,
                token=token,
                expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
            )
        )
        self.db.commit()

        from app.tasks import safe_delay
        from app.tasks.email import send_email_verification_email

        safe_delay(send_email_verification_email, user.email, user.full_name, token)
        return token

    def verify_email(self, token: str) -> None:
        record = self.db.query(EmailVerificationToken).filter(EmailVerificationToken.token == token).first()
        if not record or record.used or record.expires_at < datetime.now(timezone.utc):
            raise InvalidTokenError("Verification token is invalid or expired.")

        user = self.users.get(record.user_id)
        if not user:
            raise NotFoundError("User not found.")

        user.is_email_verified = True
        record.used = True
        self.db.commit()
