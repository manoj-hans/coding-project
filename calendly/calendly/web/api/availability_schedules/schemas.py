import enum

from pydantic import BaseModel, field_validator
from datetime import time, datetime
from typing import List


from calendly.db.models.availabilityschedule import DayOfWeek


class TimeSlotInputDTO(BaseModel):
    """DTO for creating new time slots."""
    start_time: time
    end_time: time


class AvailabilityScheduleInputDTO(BaseModel):
    """DTO for creating a new availability schedule."""
    day_of_week: str  # Assuming you use integers to represent days (0=Sunday, 1=Monday, etc.)
    time_slots: List[TimeSlotInputDTO]


class AvailabilityScheduleListInputDTO(BaseModel):
    """DTO for creating a list of availability schedules."""
    name: str
    user_id: int
    schedules: List[AvailabilityScheduleInputDTO]


class DayOfWeek(enum.Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 0


class TimeSlotDTO(BaseModel):
    id: int
    availability_schedules_id: int
    start_time: time
    end_time: time

    @field_validator('start_time', 'end_time')
    def parse_time(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, '%H:%M:%S').time()
        return value


class AvailabilityScheduleDTO(BaseModel):
    id: int
    user_id: int
    day_of_week: DayOfWeek
    name: str
    time_slots: List[TimeSlotDTO]

    class Config:
        from_attributes = True

    @field_validator('day_of_week')
    def convert_day_of_week(cls, value):
        if isinstance(value, int):
            return DayOfWeek(value)
        return value

