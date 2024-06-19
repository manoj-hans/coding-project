from datetime import datetime
from typing import List

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from calendly.db.models import Event, AvailabilitySchedule
from fastapi import Depends

from calendly.db.dependencies import get_db_session
from calendly.db.models.availabilityschedule import DayOfWeek
from calendly.db.models.calendar import calendar_availability_association


class EventDAO:
    """Data Access Object for Event model operations."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def is_time_slot_available(self, calendar_id: int, start_time: datetime,
                                     end_time: datetime) -> bool:
        """Check if the time slot is available for booking an event by loading data and processing in Python."""

        # Fetch all events for the calendar
        events = await self.session.execute(
            select(Event)
            .where(Event.calendar_id == calendar_id)
            .where(
                ((Event.start_time < end_time) & (Event.end_time > start_time))
            )
        )
        events = events.scalars().all()
        if events:
            return False  # Found overlapping events

        # Fetch the availability schedules linked to this calendar
        availability_schedules = await self.session.execute(
            select(AvailabilitySchedule)
            .join(calendar_availability_association,
                  calendar_availability_association.c.availability_schedule_id == AvailabilitySchedule.id)
            .where(calendar_availability_association.c.calendar_id == calendar_id)
        )
        availability_schedules = availability_schedules.scalars().all()

        # Check day of the week against availability schedules
        day_of_week = start_time.weekday()  # 0=Monday, ..., 6=Sunday
        day_of_week = DayOfWeek((day_of_week + 1) % 7)
        # Verify against each schedule
        for schedule in availability_schedules:
            if schedule.day_of_week == day_of_week:
                time_slots = schedule.time_slots
                for slot in time_slots:
                    if slot.start_time <= start_time.time() and slot.end_time >= end_time.time():
                        return True  # Found a valid time slot

        return False  # No valid time slot or day found

    async def create_event(self, calendar_id: int, title: str, start_time: datetime, end_time: datetime, booked_by: str, guests: str) -> Event:
        event = Event(calendar_id=calendar_id, title=title, start_time=start_time, end_time=end_time, booked_by=booked_by, guests=guests)
        self.session.add(event)
        await self.session.commit()
        return event

    async def get_events_by_calendar(self, calendar_id: int) -> List[Event]:
        result = await self.session.execute(
            select(Event).where(Event.calendar_id == calendar_id)
        )
        return result.scalars().all()
