from fastapi.routing import APIRouter

from calendly.web.api import user, availability_schedules, calendar

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(availability_schedules.router, prefix="/schedule", tags=["schedule"])
api_router.include_router(calendar.router, prefix="/calendar", tags=["calendar"])
