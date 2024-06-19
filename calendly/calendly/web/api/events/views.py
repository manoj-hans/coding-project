from fastapi import APIRouter, HTTPException, Depends
from typing import List

from calendly.db.dao.event_dao import EventDAO
from calendly.web.api.events.schemas import EventCreateInputDTO, EventDTO  # Assuming these are located in the schemas module
from calendly.db.dao.event_dao import EventDAO  # Assuming EventDAO is imported correctly

router = APIRouter()


@router.post("/events/", response_model=EventDTO, status_code=201)
async def book_event(event_input: EventCreateInputDTO, dao: EventDAO = Depends()) -> EventDTO:
    """
    Book (create) a new event in a calendar, ensuring no overlap with existing events.
    """
    available = await dao.is_time_slot_available(
        calendar_id=event_input.calendar_id,
        start_time=event_input.start_time,
        end_time=event_input.end_time
    )
    if not available:
        raise HTTPException(status_code=400, detail="Requested time slot is not available.")

    # Proceed to create the event since the time slot is available
    event = await dao.create_event(
        calendar_id=event_input.calendar_id,
        title=event_input.title,
        start_time=event_input.start_time,
        end_time=event_input.end_time,
        booked_by=event_input.booked_by,
        guests=event_input.guests
    )
    return event


@router.get("/events/{calendar_id}/", response_model=List[EventDTO])
async def get_events(calendar_id: int, event_dao: EventDAO = Depends()) -> List[EventDTO]:
    """
    Retrieve all events for a given calendar.

    :param calendar_id: ID of the calendar to retrieve events for.
    :param event_dao: DAO for event operations.
    :return: List of events associated with the calendar.
    """
    events = await event_dao.get_events_by_calendar(calendar_id)
    if not events:
        raise HTTPException(status_code=404, detail="No events found for this calendar.")

    return events
