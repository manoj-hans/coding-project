from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, time

from calendly.web.api.availability_schedules.schemas import AvailabilityScheduleDTO


class CalendarCreateInputDTO(BaseModel):
    """DTO for creating a new calendar."""
    user_id: int
    name: str
    availability_schedule_ids: List[int]  # List of availability schedule IDs to associate with the calendar


class CalendarViewDTO(BaseModel):
    """DTO for viewing a calendar with its availabilities."""
    id: int
    user_id: int
    name: str
    event_slot_minutes: int
    availability_schedules: List[AvailabilityScheduleDTO]  # Detailed availability schedules associated with the calendar

    class Config:
        from_attributes = True
