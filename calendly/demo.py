import requests

BASE_URL = "http://127.0.0.1:8000/api"

def create_user(name, email):
    url = f"{BASE_URL}/user/users"
    payload = {"name": name, "email": email}
    response = requests.post(url, json=payload)
    return response.json()

def create_availability_schedule(user_id, name, schedules):
    url = f"{BASE_URL}/schedule/availability_schedules/"
    payload = {
        "name": name,
        "user_id": user_id,
        "schedules": schedules
    }
    response = requests.post(url, json=payload)
    return response.json()

def create_calendar(user_id, name, availability_schedule_ids):
    url = f"{BASE_URL}/calendar/calendars"
    payload = {
        "user_id": user_id,
        "name": name,
        "availability_schedule_ids": availability_schedule_ids
    }
    response = requests.post(url, json=payload)
    return response.json()

def get_calendar(calendar_id):
    url = f"{BASE_URL}/calendar/calendars/{calendar_id}"
    response = requests.get(url)
    return response.json()

def book_event(calendar_id, title, start_time, end_time, booked_by, guests):
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
    return response.json()

# Define users
user1 = create_user("UserA", "usera@example.com")
user2 = create_user("UserB", "userb@example.com")

# Define and create availability schedules with overlaps
schedule_a = create_availability_schedule(user1['id'], "Consultations A", [
    {"day_of_week": "Monday", "time_slots": [{"start_time": "09:00:00", "end_time": "11:00:00"}]},
    {"day_of_week": "Wednesday", "time_slots": [{"start_time": "10:00:00", "end_time": "12:00:00"}]}
])
schedule_b = create_availability_schedule(user2['id'], "Consultations B", [
    {"day_of_week": "Monday", "time_slots": [{"start_time": "10:00:00", "end_time": "12:00:00"}]},
    {"day_of_week": "Wednesday", "time_slots": [{"start_time": "11:00:00", "end_time": "13:00:00"}]}
])

import pdb;pdb.set_trace()

# Create calendars using these availability schedules
calendar_a = create_calendar(user1['id'], "Calendar A", [each['id'] for each in schedule_a])
calendar_b = create_calendar(user2['id'], "Calendar B", [each['id'] for each in schedule_b])

# Book an event on these calendars
event_a = book_event(calendar_a['id'], "Meeting A", "2024-06-24T10:00:00", "2024-06-24T11:00:00", "usera@example.com", "usera@example.com, userb@example.com")
event_b = book_event(calendar_b['id'], "Meeting B", "2024-06-24T11:00:00", "2024-06-24T12:00:00", "userb@example.com", "usera@example.com, userb@example.com")

# Attempt to rebook the same slot on Calendar A, expecting an error
try:
    book_event(calendar_a['id'], "Attempt Rebooking", "2024-06-24T10:30:00", "2024-06-24T11:30:00", "usera@example.com", "usera@example.com, userc@example.com")
except Exception as e:
    print("Failed to book:", e)

try:
    book_event(calendar_a['id'], "Attempt Rebooking", "2024-06-25T10:30:00", "2024-06-25T11:30:00", "usera@example.com", "usera@example.com, userc@example.com")
except Exception as e:
    print("Failed to book:", e)

# Output the results
print("User 1:", user1)
print("User 2:", user2)
print("Calendar A:", calendar_a)
print("Calendar B:", calendar_b)
print("Event A:", event_a)
print("Event B:", event_b)
