"""Manage event registrations and persist event data as JSON."""

import json
import secrets
from datetime import date
from pathlib import Path

events = {}


def create_event(event_name, venue, capacity=50, guests=None):
    """Create an event and return its details."""
    guest_list = [] if guests is None else list(guests)
    events[event_name] = {
        "venue": venue,
        "capacity": capacity,
        "guests": guest_list,
    }
    return events[event_name]


def register_guest(event_name, guest):
    """Register a guest if the event has available capacity."""
    event = events.get(event_name)
    if event is None:
        print("No such event:", event_name)
        return False
    if len(event["guests"]) >= event["capacity"]:
        print(event_name, "is full, cannot add", guest)
        return False
    event["guests"].append(guest)
    return True


def seats_left(event_name):
    """Return the number of seats remaining at an event."""
    event = events[event_name]
    return event["capacity"] - len(event["guests"])


def event_status(event_date):
    """Return whether an event is upcoming or completed."""
    if event_date >= date.today():
        return "Upcoming"
    return "Completed"


def guest_report(event_name, sort_order):
    """Return a comma-separated guest list in the requested order."""
    descending = sort_order.lower() in {
        "desc", "descending", "reverse"
    }
    names = sorted(
        events[event_name]["guests"],
        reverse=descending,
    )
    return ", ".join(names)


def save_events(file_name="events.json"):
    """Save all events to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(events, file, indent=2)


def load_events(file_name="events.json"):
    """Load events from a JSON file."""
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)


def print_badges(event_name):
    """Display the contents of an event's badge file safely."""
    if not event_name or any(
        not (character.isalnum() or character in " _-")
        for character in event_name
    ):
        raise ValueError("Event name contains unsupported characters.")

    badge_file = Path(f"badges_{event_name}.txt")

    if not badge_file.is_file():
        raise FileNotFoundError(
            f"Badge file not found: {badge_file.name}"
        )

    print(badge_file.read_text(encoding="utf-8"))


def main():
    """Run the event manager demonstration."""
    create_event("Tech Meetup", "Hall A", 3)
    create_event("Alumni Dinner", "Rooftop", 2)
    register_guest("Tech Meetup", "Asha")
    register_guest("Tech Meetup", "Ravi")
    register_guest("Alumni Dinner", "Meena")
    register_guest("Workshop", "Kiran")
    left = seats_left("Tech Meetup")
    print("Seats left at Tech Meetup:", left)
    print("Seats left at Alumni Dinner:", seats_left("Alumni Dinner"))
    print("Tech Meetup guests:", guest_report("Tech Meetup", "name"))
    print("Tech Meetup is", event_status(date(2099, 1, 15)))
    print("Alumni Dinner is", event_status(date(2020, 5, 1)))
    winner = secrets.choice(events["Tech Meetup"]["guests"])
    print("Lucky draw winner:", winner)
    save_events()
    restored = load_events()  # Reload to confirm the save worked
    print("Events restored from file:", len(restored))
    print("Venues:", [event["venue"] for event in restored.values()])


main()
