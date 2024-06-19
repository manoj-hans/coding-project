from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship, Mapped
from sqlalchemy.sql.schema import ForeignKey

from calendly.db.base import Base


class Event(Base):
    """Model for events on calendars."""

    __tablename__ = "events"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    calendar_id: Mapped[int] = Column(Integer,
                                      ForeignKey('calendars.id', ondelete="CASCADE"),
                                      index=True)
    title: Mapped[str] = Column(String(length=200))
    start_time: Mapped[datetime] = Column(DateTime, index=True)
    end_time: Mapped[datetime] = Column(DateTime, index=True)
    booked_by: Mapped[str] = Column(String(length=200))
    guests: Mapped[str] = Column(String(length=200))  # For now we are expecting
    # emails addresses concatenated by strings

    # Relationship to calendar
    calendar: Mapped["Calendar"] = relationship("Calendar", back_populates="events")
