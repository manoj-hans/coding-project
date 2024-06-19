from pydantic import BaseModel
from datetime import time
from typing import List


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


class TimeSlotDTO(BaseModel):
    """DTO for returned time slots within an availability schedule."""
    id: int
    availability_schedules_id: int
    start_time: time
    end_time: time


class AvailabilityScheduleDTO(BaseModel):
    """DTO for returned availability schedule."""
    id: int
    user_id: int
    day_of_week: int
    name: str
    time_slots: List[TimeSlotDTO]

    class Config:
        from_attributes = True

