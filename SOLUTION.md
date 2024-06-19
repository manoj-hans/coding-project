
## Calendly System Design

Calendly is crafted to provide a flexible and dynamic scheduling solution for users. Each user can create multiple calendars, tailored to different needs. These calendars are linked to availability schedules through a one-to-many relationship, enhancing scheduling flexibility.

Each availability schedule is specific to a day and is directly associated with a user, defining when they are available. As events are booked, availability dynamically adjusts, ensuring the system remains up-to-date with the user's commitments.

### Assumptions
- **User Ownership**: Each calendar and schedule is owned individually, with no cross-user access unless shared.
- **Dynamic Availability**: Availability adjusts in real-time as events are booked, preventing any double bookings.
- **Unified Time Management**: Times are managed in a unified time zone within the backend, with conversions handled at the application level for user interactions.
- **Privacy and Security**: Users maintain control over their calendars and events, with robust security measures in place to protect user data.

## Known Limitations and Declarations

### Calendar Comparison
- **Date for Comparison**: The "Compare Calendars" feature currently compares the calendars of both demo users specifically for June 24, 2024 (Monday). This is intended for demonstration purposes and showcases the system's ability to identify overlapping available slots between two users.

### Availability Schedules
- **Configurability**: The Availability Schedule, or simply "Schedule," should be regarded as a configurable entity that can be replicated across multiple calendars. This design allows each calendar to have its unique event management but follows predefined availability patterns set in the schedules. This setup enables versatile yet consistent scheduling capabilities across different user calendars.

### Calendar Expiry and Meeting Slots
- **Handling Incompleteness**: Fields such as calendar expiry and specific meeting slots exist within the database schema but are not fully implemented or handled in the current system version. Future updates will aim to address these aspects to enhance functionality and user experience.

### Timezone Management
- **Current Implementation**: All time-related data are currently stored in UTC. Although the system is capable of supporting timezone specifications at the calendar or user level, this functionality is not yet implemented. Users should be aware that all displayed times are in UTC, and any conversions to local times must be manually handled outside the system.

### Docker Persistance
- **Current Implementation**: Although docker is running but there is some problem due to which commit is not happening on the db.

- These declarations are intended to acknowledge the system's current limitations and provide transparency about its capabilities and areas for future development.


## Models

### User

- **Description**: Represents system users.
- **Fields**:
  - `id`: Unique identifier for the user.
  - `name`: Name of the user.
  - `email`: Email address of the user.

### AvailabilitySchedule

- **Description**: Defines the availability of a user over various days of the week. Understand this part of the system as schedule configuration, which can be reused with multiple calendars.
- **Fields**:
  - `id`: Unique identifier for the availability schedule.
  - `user_id`: References the user to which the availability pertains.
  - `name`: Descriptive name for the schedule.
  - `time_slots`: Collection of time slots specifying start and end times for availability on the specified day.

### TimeSlot

- **Description**: Specific periods during which a user is available within their Availability Schedule.
- **Fields**:
  - `id`: Unique identifier for the time slot.
  - `availability_schedule_id`: Links back to the `AvailabilitySchedule`.
  - `start_time`: Start time of the availability.
  - `end_time`: End time of the availability.

### Calendar

- **Description**: Represents a calendar that can be used to manage and book events. Each calendar can be associated with multiple availability schedules.
- **Fields**:
  - `id`: Unique identifier for the calendar.
  - `user_id`: Owner of the calendar.
  - `name`: Name of the calendar.

### CalendarAvailabilityAssociation

- **Description**: Manages the many-to-many relationship between `Calendar` and `AvailabilitySchedule`. This association table allows a calendar to include multiple availability schedules and vice versa.
- **Fields**:
  - `calendar_id`: Foreign key to the `Calendar` table.
  - `availability_schedule_id`: Foreign key to the `AvailabilitySchedule` table.
  - `expires_on`: Optional datetime field to specify when the schedule ceases to be active in the calendar.

### Event

- **Description**: Represents a specific appointment or meeting scheduled on a calendar.
- **Fields**:
  - `id`: Unique identifier for the event.
  - `calendar_id`: References the calendar where the event is booked.
  - `title`: Title of the event.
  - `start_time`: Start time of the event.
  - `end_time`: End time of the event.
  - `booked_by`: Email of the user who booked the event.
  - `guests`: Comma-separated emails of guests attending the event.

## API Endpoints

### User Management

- **POST /api/user/users**
  - **Description**: Create a new user.
  - **Payload**: `{"name": "string", "email": "string"}`
  - **Returns**: User details with unique ID.

### Availability Schedules

- **POST /api/schedule/availability_schedules/**
  - **Description**: Create availability schedules for a user.
  - **Payload**: Detailed JSON including user ID, name of the schedule, and detailed time slots.
  - **Returns**: Details of the created availability schedule.

### Calendar Manager

- **POST /api/calendar/calendars**
  - **Description**: Create a calendar using specified availability schedules.
  - **Payload**: JSON specifying the user ID, calendar name, and IDs of availability schedules.
  - **Returns**: Details of the created calendar.

- **GET /api/calendar/calendars/{calendar_id}**
  - **Description**: Retrieve details of a specific calendar.
  - **Returns**: Calendar details including all linked availability schedules and events.

### Event Scheduling

- **POST /api/event/events/**
  - **Description**: Book an event on a calendar.
  - **Payload**: JSON specifying calendar ID, event title, start and end times, booked by, and guests.
  - **Returns**: Details of the booked event.

- **GET /api/calendar/calendars/{calendar_id}/events**
  - **Description**: Retrieve all events scheduled on a specific calendar.
  - **Returns**: List of events on the specified calendar.

### Error Handling

- All endpoints include error handling to manage situations like non-existent IDs, invalid data inputs, and permission errors.

## Demo Scipt is included in calendly sub directory. Follow the ReadMe file inside for setup.

