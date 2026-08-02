from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MeetingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: str | None
    department_id: str | None
    organizer_id: str | None
    starts_at: datetime
    ends_at: datetime | None
    location: str | None
    status: str


class MeetingCreate(BaseModel):
    title: str
    description: str | None = None
    department_id: str | None = None
    organizer_id: str | None = None
    starts_at: datetime
    ends_at: datetime | None = None
    location: str | None = None
