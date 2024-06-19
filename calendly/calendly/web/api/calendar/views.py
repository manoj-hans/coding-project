from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from calendly.db.dao.calendar_dao import CalendarDAO
from calendly.web.api.calendar.schemas import CalendarViewDTO, CalendarCreateInputDTO

router = APIRouter()


@router.post("/calendars/", response_model=CalendarViewDTO, status_code=201)
async def create_calendar(calendar_input: CalendarCreateInputDTO, dao: CalendarDAO = Depends()):
    calendar = await dao.create_calendar(
        user_id=calendar_input.user_id,
        name=calendar_input.name,
        availability_schedule_ids=calendar_input.availability_schedule_ids
    )
    if not calendar:
        raise HTTPException(status_code=400, detail="Failed to create calendar.")
    return calendar # TODO: returning calendar object directly for now. There is some problem to which why it is not alligning with CalendarViewDTO


@router.get("/calendars/{calendar_id}/", response_model=CalendarViewDTO)
async def view_calendar(calendar_id: int, dao: CalendarDAO = Depends()):
    calendar = await dao.get_calendar_by_id(calendar_id)
    if not calendar:
        raise HTTPException(status_code=404, detail="Calendar not found.")
    return calendar
