import requests

BASE_URL = "http://127.0.0.1:8000/api"


def create_user(name, email):
    print(f"Creating user with name: {name}")
    url = f"{BASE_URL}/user/users"
    payload = {"name": name, "email": email}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    user = response.json()
    print(f"User created: {user}")
    return user


def create_availability_schedule(user_id, name, schedules):
    print(f"Creating availability schedule for user ID {user_id}")
    url = f"{BASE_URL}/schedule/availability_schedules/"
    payload = {
        "name": name,
        "user_id": user_id,
        "schedules": schedules
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    schedule = response.json()
    print(f"Availability schedule created: {schedule}")
    return schedule


def create_calendar(user_id, name, availability_schedule_ids):
    print(f"Creating calendar '{name}' for user ID {user_id}")
    url = f"{BASE_URL}/calendar/calendars"
    payload = {
        "user_id": user_id,
        "name": name,
        "availability_schedule_ids": availability_schedule_ids
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    calendar = response.json()
    print(f"Calendar created: {calendar}")
    return calendar


def get_calendar(calendar_id):
    print(f"Fetching calendar with ID {calendar_id}")
    url = f"{BASE_URL}/calendar/calendars/{calendar_id}"
    response = requests.get(url)
    response.raise_for_status()
    calendar = response.json()
    print(f"Calendar fetched: {calendar}")
    return calendar


def book_event(calendar_id, title, start_time, end_time, booked_by, guests):
    print(
        f"Booking event '{title}' on calendar ID {calendar_id}, {start_time}-{end_time}")
    url = f"{BASE_URL}/event/events/"
    payload = {
        "calendar_id": calendar_id,
        "title": title,
        "start_time": start_time,
        "end_time": end_time,
        "booked_by": booked_by,
        "guests": guests
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    event = response.json()
    print(f"Event booked: {event}")
    return event


def compare_calendars(calendar_id1, calendar_id2):
    print(f"Comparing calendars {calendar_id1}, {calendar_id2}")
    url = f"{BASE_URL}/calendar/compare-calendars/{calendar_id1}/{calendar_id2}/"
    response = requests.get(url)
    response.raise_for_status()
    calendar = response.json()
    print(f"Common Slots: {calendar}")
    return calendar


# Define users
user1 = create_user("UserA", "usera@example.com")
print("\n")
user2 = create_user("UserB", "userb@example.com")
print("\n")
# Define and create availability schedules with overlaps
schedule_a = create_availability_schedule(user1['id'], "Consultations A", [
    {"day_of_week": "Monday",
     "time_slots": [{"start_time": "09:00:00", "end_time": "11:00:00"}]},
    {"day_of_week": "Wednesday",
     "time_slots": [{"start_time": "10:00:00", "end_time": "12:00:00"}]}
])
print("\n")
schedule_b = create_availability_schedule(user2['id'], "Consultations B", [
    {"day_of_week": "Monday",
     "time_slots": [{"start_time": "10:00:00", "end_time": "12:00:00"}]},
    {"day_of_week": "Wednesday",
     "time_slots": [{"start_time": "11:00:00", "end_time": "13:00:00"}]}
])

print("\n")
# Create calendars using these availability schedules
calendar_a = create_calendar(user1['id'], "Calendar A",
                             [each['id'] for each in schedule_a])
print("\n")
calendar_b = create_calendar(user2['id'], "Calendar B",
                             [each['id'] for each in schedule_b])
print("\n")

compare_calendars(calendar_a['id'], calendar_b['id'])
print("\n")

# Book initial events on each calendar
event_a = book_event(calendar_a['id'], "Meeting A", "2024-06-24T10:00:00",
                     "2024-06-24T11:00:00", "usera@example.com",
                     "usera@example.com, userb@example.com")
print("\n")
event_b = book_event(calendar_b['id'], "Meeting B", "2024-06-24T11:00:00",
                     "2024-06-24T12:00:00", "userb@example.com",
                     "usera@example.com, userb@example.com")

print("\n")
# Attempt to rebook the same slot on Calendar A, expecting an error
try:
    book_event(calendar_a['id'], "Attempt Rebooking", "2024-06-24T10:30:00",
               "2024-06-24T11:30:00", "usera@example.com",
               "usera@example.com, userc@example.com")
except Exception as e:
    print(f"Failed to book due to error: {e.response.text}")

print("\n")
try:
    book_event(calendar_a['id'], "Attempt Rebooking", "2024-06-25T10:30:00",
               "2024-06-25T11:30:00", "usera@example.com",
               "usera@example.com, userc@example.com")
except Exception as e:
    print(f"Failed to book due to error: {e.response.text}")
print("\n")

compare_calendars(calendar_a['id'], calendar_b['id'])
print("\n")
