from typing import Optional, List

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from calendly.db.models import AvailabilitySchedule, Calendar
from fastapi import Depends

from calendly.db.dependencies import get_db_session
from calendly.db.models.calendar import calendar_availability_association


class CalendarDAO:
    """Data Access Object for Calendar model operations."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_calendar(self, user_id: int, name: str, availability_schedule_ids: List[int]) -> Calendar:
        calendar = Calendar(user_id=user_id, name=name)
        self.session.add(calendar)
        await self.session.commit()
        # Associate availability schedules after committing the calendar to get its ID
        for schedule_id in availability_schedule_ids:
            assoc = calendar_availability_association.insert().values(
                calendar_id=calendar.id,
                availability_schedule_id=schedule_id
            )
            await self.session.execute(assoc)
        await self.session.commit()
        response = await self.get_calendar_by_id(calendar.id)
        return response

    async def get_calendar_by_id(self, calendar_id: int) -> Optional[Calendar]:
        result = await self.session.execute(
            select(Calendar).options(
                joinedload(Calendar.availability_schedules).joinedload(AvailabilitySchedule.time_slots)
            ).where(Calendar.id == calendar_id)
        )
        return result.scalars().first()
