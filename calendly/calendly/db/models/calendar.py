from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship, Mapped
from sqlalchemy.sql.schema import ForeignKey, Table

from calendly.db.base import Base


# I have chose to kept primary key False on this.
# Because we need to handle it in code that new availability id
# can only be mapped to calendar id if previous one has been expired.
calendar_availability_association = Table(
    'calendar_availability_association',
    Base.metadata,
    Column('calendar_id', Integer, ForeignKey('calendars.id', ondelete="CASCADE"),
           primary_key=False, unique=True),
    Column('availability_schedule_id', Integer,
           ForeignKey('availability_schedules.id', ondelete="CASCADE"),
           primary_key=False),
    Column('expires_on', DateTime, nullable=True)
    # Optional field to control the association's validity
)


class Calendar(Base):
    """Model for calendars owned by users."""
    __tablename__ = "calendars"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"),
                                  index=True)
    name: Mapped[str] = Column(String(length=200))
    event_slot_minutes: Mapped[int] = Column(Integer, default=30)

    # Relationship to user
    user: Mapped["User"] = relationship("User", back_populates="calendars")

    # Many-to-many relationship to Availabilities
    availability_schedules = relationship(
        "AvailabilitySchedule",
        secondary=calendar_availability_association,
        back_populates="calendars")
    # Relationship to events

    events: Mapped[list["Event"]] = relationship("Event", back_populates="calendar")
