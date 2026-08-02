from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NotificationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    type: str
    title: str
    body: str | None
    link: str | None
    is_read: bool
    reference_type: str | None = None
    reference_id: str | None = None
    created_at: datetime


class NotificationCreate(BaseModel):
    user_id: str
    type: str
    title: str
    body: str | None = None
    link: str | None = None
