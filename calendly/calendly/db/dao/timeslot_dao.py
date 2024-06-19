from datetime import time
from typing import List

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from calendly.db.models import TimeSlot
from fastapi import Depends

from calendly.db.dependencies import get_db_session


class TimeSlotDAO:
    """Data Access Object for TimeSlot model operations."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_time_slot(self, availability_schedule_id: int, start_time: time, end_time: time) -> TimeSlot:
        time_slot = TimeSlot(availability_schedule_id=availability_schedule_id, start_time=start_time, end_time=end_time)
        self.session.add(time_slot)
        await self.session.commit()
        return time_slot

    async def list_time_slots_for_schedule(self, availability_schedule_id: int) -> List[TimeSlot]:
        result = await self.session.execute(
            select(TimeSlot).where(TimeSlot.availability_schedule_id == availability_schedule_id)
        )
        return result.scalars().all()
