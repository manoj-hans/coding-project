from datetime import datetime
from typing import List

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from calendly.db.models import Event
from fastapi import Depends

from calendly.db.dependencies import get_db_session

class EventDAO:
    """Data Access Object for Event model operations."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

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
