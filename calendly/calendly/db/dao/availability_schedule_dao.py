from typing import List

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from calendly.db.models import AvailabilitySchedule, TimeSlot
from fastapi import Depends

from calendly.db.dependencies import get_db_session
from calendly.web.api.availability_schedules.schemas import AvailabilityScheduleInputDTO


class AvailabilityScheduleDAO:
    """Data Access Object for AvailabilitySchedule and TimeSlot model operations."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_availability_schedule(self,
                                           schedule_name: str,
                                           user_id: str,
                                           schedule_input: AvailabilityScheduleInputDTO) -> AvailabilitySchedule:
        availability_schedule = AvailabilitySchedule(
            user_id=user_id,
            day_of_week=schedule_input.day_of_week,
            name=schedule_name
        )
        self.session.add(availability_schedule)
        await self.session.commit()

        # Create associated time slots
        for slot in schedule_input.time_slots:
            time_slot = TimeSlot(
                availability_schedules_id=availability_schedule.id,
                start_time=slot.start_time,
                end_time=slot.end_time
            )
            self.session.add(time_slot)

        await self.session.commit()
        response = await self.list_availability_schedules_with_time_slots(user_id)
        return response


    async def list_availability_schedules_by_user(self, user_id: int) -> List[AvailabilitySchedule]:
        result = await self.session.execute(
            select(AvailabilitySchedule).where(AvailabilitySchedule.user_id == user_id)
        )
        return result.scalars().all()

    async def list_availability_schedules_with_time_slots(self, user_id: int) -> List[dict]:
        # Execute a query to fetch availability schedules and their associated time slots using a join
        result = await self.session.execute(
            select(AvailabilitySchedule)
            .options(joinedload(AvailabilitySchedule.time_slots))
            .where(AvailabilitySchedule.user_id == user_id)
        )
        availability_schedules = result.scalars().unique().all()

        # Transform the data into the desired format
        return [
            {
                "id": schedule.id,
                "user_id": schedule.user_id,
                "day_of_week": schedule.day_of_week,
                "name": schedule.name,
                "time_slots": [
                    {
                        "id": slot.id,
                        "availability_schedules_id": slot.availability_schedules_id,
                        "start_time": slot.start_time.isoformat(),
                        "end_time": slot.end_time.isoformat()
                    }
                    for slot in schedule.time_slots
                ]
            }
            for schedule in availability_schedules
        ]
