from datetime import time

from sqlalchemy import Time, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, declarative_base
from sqlalchemy.sql.schema import ForeignKey

from calendly.db.base import Base


class TimeSlot(Base):
    """Model for individual time slots within a day's availability."""
    __tablename__ = "time_slots"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    availability_schedules_id: Mapped[int] = Column(Integer, ForeignKey('availability_schedules.id',
                                                              ondelete="CASCADE"), index=True)
    start_time: Mapped[time] = Column(Time)
    end_time: Mapped[time] = Column(Time)

    # Relationship to Availability
    availability_schedules = relationship("AvailabilitySchedule", back_populates="time_slots")
