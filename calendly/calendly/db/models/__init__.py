"""calendly models."""
import pkgutil
from pathlib import Path


def load_all_models() -> None:
    """Load all models from this folder."""
    package_dir = Path(__file__).resolve().parent
    modules = pkgutil.walk_packages(
        path=[str(package_dir)],
        prefix="calendly.db.models.",
    )
    for module in modules:
        __import__(module.name)  # noqa: WPS421

from calendly.db.models.user import User
from calendly.db.models.calendar import Calendar
from calendly.db.models.event import Event
from calendly.db.models.timeslot import TimeSlot
from calendly.db.models.availabilityschedule import AvailabilitySchedule
