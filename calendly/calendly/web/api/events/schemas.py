from pydantic import BaseModel
from datetime import datetime


class EventCreateInputDTO(BaseModel):
    """DTO for creating a new event."""
    calendar_id: int
    title: str
    start_time: datetime
    end_time: datetime
    booked_by: str
    guests: str


class EventDTO(BaseModel):
    """DTO for returning event details."""
    id: int
    calendar_id: int
    title: str
    start_time: datetime
    end_time: datetime
    booked_by: str
    guests: str

    class Config:
        from_attributes = True
