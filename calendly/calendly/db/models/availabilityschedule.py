from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship, Mapped
from sqlalchemy.sql.schema import ForeignKey

from calendly.db.base import Base

from calendly.db.models.calendar import calendar_availability_association

import enum
from sqlalchemy import Column, Integer, Enum

class DayOfWeek(enum.Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 0

# Usage in SQLAlchemy Model
class AvailabilitySchedule(Base):
    """Model for storing a reusable weekly schedule tied to a specific user and day of the week."""
    __tablename__ = "availability_schedules"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), index=True)  # Link to the User model
    day_of_week: Mapped[DayOfWeek] = Column(Enum(DayOfWeek))
    name: Mapped[str] = Column(String(length=200))  # Descriptive name for the schedule

    # Relationship to User
    user: Mapped["User"] = relationship("User", back_populates="availability_schedules")

    # Relationship to Calendars
    calendars: Mapped[list["Calendar"]] = relationship(
        "Calendar",
        secondary=calendar_availability_association,
        back_populates="availability_schedules")

    # Relationship to TimeSlots
    time_slots: Mapped[list["TimeSlot"]] = relationship("TimeSlot", back_populates="availability_schedules", cascade="all, delete-orphan", lazy="selectin")
