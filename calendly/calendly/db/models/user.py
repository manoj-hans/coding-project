from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship, Mapped
from sqlalchemy.sql.schema import ForeignKey

from calendly.db.base import Base

from calendly.db.models.calendar import Calendar


class User(Base):
    """Model for user profiles."""

    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String(length=200))
    email: Mapped[str] = Column(String(length=200), unique=True, index=True)

    # Relationship to calendars
    calendars: Mapped[list[Calendar]] = relationship("Calendar", back_populates="user")

    # Relationship to Availability Schedule
    availability_schedules = relationship("AvailabilitySchedule", back_populates="user")
