from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from .schemas import AvailabilityScheduleListInputDTO, AvailabilityScheduleDTO  # Import your DTOs
from calendly.db.dao.availability_schedule_dao import AvailabilityScheduleDAO

router = APIRouter()


@router.post("/availability_schedules/", response_model=List[AvailabilityScheduleDTO], status_code=status.HTTP_201_CREATED)
async def create_availability_schedules(
    schedules_input: AvailabilityScheduleListInputDTO,
    schedule_dao: AvailabilityScheduleDAO = Depends()
) -> List[AvailabilityScheduleDTO]:
    """
    Creates multiple availability schedules along with associated time slots in the database.

    :param schedules_input: DTO containing data to create new availability schedules and time slots.
    :param schedule_dao: DAO for handling the database operations for availability schedules.
    """
    for schedule_input in schedules_input.schedules:
        availability_schedule = await schedule_dao.create_availability_schedule(schedules_input.name, schedules_input.user_id, schedule_input)

    return availability_schedule


@router.get("/availability_schedules/{user_id}", response_model=List[AvailabilityScheduleDTO])
async def get_availability_schedules_with_time_slots(
    user_id: int,
    dao: AvailabilityScheduleDAO = Depends(AvailabilityScheduleDAO)
) -> List[AvailabilityScheduleDTO]:
    """
    Retrieve all availability schedules along with their time slots for a given user.

    :param user_id: The ID of the user whose schedules are to be retrieved.
    :param dao: The data access object for handling availability schedules.
    :return: A list of availability schedules with time slots.
    """
    try:
        availability_schedules = await dao.list_availability_schedules_with_time_slots(user_id)
        return availability_schedules
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
