from datetime import datetime
from typing import Optional, List

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from calendly.db.models import AvailabilitySchedule, Calendar, Event, TimeSlot
from fastapi import Depends

from calendly.db.dependencies import get_db_session
from calendly.db.models.availabilityschedule import DayOfWeek
from calendly.db.models.calendar import calendar_availability_association


class CalendarDAO:
    """Data Access Object for Calendar model operations."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_calendar(self, user_id: int, name: str,
                              availability_schedule_ids: List[int]) -> Calendar:
        calendar = Calendar(user_id=user_id, name=name)
        self.session.add(calendar)
        try:
            await self.session.commit()
        except Exception as ex:
            # this will log details of the exception
            await self.session.rollback()
        # Associate availability schedules after committing the calendar to get its ID
        for schedule_id in availability_schedule_ids:
            assoc = calendar_availability_association.insert().values(
                calendar_id=calendar.id,
                availability_schedule_id=schedule_id
            )
            await self.session.execute(assoc)
        try:
            await self.session.commit()
        except Exception as ex:
            # this will log details of the exception
            await self.session.rollback()
        response = await self.get_calendar_by_id(calendar.id)
        return response

    async def get_calendar_by_id(self, calendar_id: int) -> Optional[Calendar]:
        result = await self.session.execute(
            select(Calendar).options(
                joinedload(Calendar.availability_schedules).joinedload(
                    AvailabilitySchedule.time_slots)
            ).where(Calendar.id == calendar_id)
        )
        return result.scalars().first()

    async def validate_availability_schedules_owner(self, user_id: int,
                                                    availability_schedule_ids: list):
        """Validate that all given availability schedule IDs belong to the specified user."""
        result = await self.session.execute(
            select(AvailabilitySchedule.id)
            .where(AvailabilitySchedule.id.in_(availability_schedule_ids))
            .where(AvailabilitySchedule.user_id == user_id)
        )
        valid_ids = {row for row in result.scalars().all()}
        print(valid_ids, type(valid_ids))
        return valid_ids == set(availability_schedule_ids)

    async def get_available_slots(self, calendar_id: int, start: datetime,
                                  end: datetime) -> List[tuple]:
        """Retrieve all available slots for a calendar within a specific day, excluding booked events."""
        day_of_week = start.weekday()  # 0=Monday, ..., 6=Sunday
        day_of_week = DayOfWeek((day_of_week + 1) % 7)
        availability_schedules = await self.session.execute(
            select(AvailabilitySchedule)
            .join(calendar_availability_association,
                  calendar_availability_association.c.availability_schedule_id == AvailabilitySchedule.id)
            .where(calendar_availability_association.c.calendar_id == calendar_id)
            .where(AvailabilitySchedule.day_of_week == day_of_week)
            # Filtering by day of the week
        )
        availability_schedules = availability_schedules.scalars().all()

        # Prepare a list to collect all time slots for the day
        availability_slots = []
        for schedule in availability_schedules:
            time_slots = await self.session.execute(
                select(TimeSlot.start_time, TimeSlot.end_time)
                .where(TimeSlot.availability_schedules_id == schedule.id)
            )
            availability_slots.extend(time_slots.fetchall())

        # Convert to list of tuples for easier handling
        availability_slots = [(slot.start_time, slot.end_time) for slot in
                              availability_slots]

        # Fetch events that block out time
        events = await self.session.execute(
            select(Event)
            .where(Event.calendar_id == calendar_id)
            # .where(Event.end_time >= start)
            # .where(Event.start_time <= end)
        )
        booked_slots = [(event.start_time, event.end_time) for event in
                        events.scalars().all()]

        # Subtract times blocked by events from available time slots
        available_slots = await self.subtract_booked_slots(availability_slots, booked_slots)

        return available_slots

    async def subtract_booked_slots(self, availability_slots, booked_slots):
        """Subtract booked event times from availability slots."""
        final_slots = []
        for avail_start, avail_end in availability_slots:
            current_slots = [(avail_start, avail_end)]
            for book_start, book_end in booked_slots:
                book_start = book_start.time()
                book_end = book_end.time()
                new_slots = []
                for start, end in current_slots:
                    print(f"current slots: {start}, {end}")
                    print(f"booked slots: {book_start}, {book_end}")
                    print(f"new slot: {new_slots}")
                    if book_start <= end and book_end >= start:
                        if start < book_start:
                            new_slots.append((start, book_start))
                        if end > book_end:
                            new_slots.append((book_end, end))
                    else:
                        new_slots.append((start, end))
                current_slots = new_slots
            final_slots.extend(current_slots)
        return final_slots

    async def find_common_slots(self, slots1: List[tuple], slots2: List[tuple]) -> List[
        dict]:
        """Find common available slots between two lists of time slots."""
        common_slots = []
        for start1, end1 in slots1:
            for start2, end2 in slots2:
                # Find overlap
                start_common = max(start1, start2)
                end_common = min(end1, end2)
                if start_common < end_common:  # There is an overlap
                    common_slots.append({"start": start_common, "end": end_common})
        return common_slots
