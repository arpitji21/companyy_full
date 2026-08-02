from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    full_name: str
    role_id: str | None
    department_id: str | None
    is_active: bool
    is_email_verified: bool
    avatar_url: str | None
    last_login_at: datetime | None
    created_at: datetime


class UserUpdate(BaseModel):
    full_name: str | None = None
    avatar_url: str | None = None
    department_id: str | None = None
    role_id: str | None = None
    is_active: bool | None = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role_id: str | None = None
    department_id: str | None = None
