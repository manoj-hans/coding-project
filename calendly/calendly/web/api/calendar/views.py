from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from calendly.db.dao.calendar_dao import CalendarDAO
from calendly.web.api.calendar.schemas import CalendarViewDTO, CalendarCreateInputDTO

router = APIRouter()


@router.post("/calendars/", status_code=201)
async def create_calendar(calendar_input: CalendarCreateInputDTO, dao: CalendarDAO = Depends()):
    if not await dao.validate_availability_schedules_owner(calendar_input.user_id, calendar_input.availability_schedule_ids):
        raise HTTPException(status_code=400, detail="One or more availability schedules do not belong to the user.")

    calendar = await dao.create_calendar(
        user_id=calendar_input.user_id,
        name=calendar_input.name,
        availability_schedule_ids=calendar_input.availability_schedule_ids
    )
    if not calendar:
        raise HTTPException(status_code=400, detail="Failed to create calendar.")
    return calendar # TODO: returning calendar object directly for now. There is some problem to which why it is not alligning with CalendarViewDTO


@router.get("/calendars/{calendar_id}/")
async def view_calendar(calendar_id: int, dao: CalendarDAO = Depends()):
    calendar = await dao.get_calendar_by_id(calendar_id)
    if not calendar:
        raise HTTPException(status_code=404, detail="Calendar not found.")
    return calendar


@router.get("/compare-calendars/{calendar_id1}/{calendar_id2}/")
async def compare_calendars(calendar_id1: int, calendar_id2: int, dao: CalendarDAO = Depends()) -> List[dict]:
    today = datetime.now().date()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())

    # Fetch available slots for each calendar, considering booked events
    slots_calendar1 = await dao.get_available_slots(calendar_id1, start_of_day, end_of_day)
    slots_calendar2 = await dao.get_available_slots(calendar_id2, start_of_day, end_of_day)

    # Find common time slots
    common_slots = dao.find_common_slots(slots_calendar1, slots_calendar2)
    return common_slots
