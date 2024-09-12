# Automating adding events to Google Calendar

# Importing Modules / Packages
import os
import csv
import datetime as dt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import CALENDAR_NAME, CSV_FILE

# Scopes required for API access
SCOPES = ["https://www.googleapis.com/auth/calendar"]


# Function to retrieve the calendar ID for a given calendar name.
def get_calendar_id(service, CALENDAR_NAME):
    # Getting the list of existing calendars'
    calendars = service.calendarList().list().execute().get("items", [])

    # Find the calendar with the specified name
    for calendar in calendars:
        if calendar["summary"] == CALENDAR_NAME:
            return calendar["id"]

    # If the calendar with specified name is not found, return None
    return None


# Check if a new event conflicts with any existing events.
def check_event_conflict(service, calendar_id, new_event):
    now = dt.datetime.now().isoformat() + "Z"
    event_result = service.events().list(calendarId=calendar_id, timeMin=now, maxResults=10, singleEvents=True,
                                         orderBy="startTime").execute()
    existing_events = event_result.get("items", [])

    conflicting_events = []
    for existing_event in existing_events:
        existing_start = existing_event["start"].get("dateTime", existing_event["start"].get("date"))
        existing_end = existing_event["end"].get("dateTime", existing_event["end"].get("date"))

        if new_event["start"]["dateTime"] < existing_end and new_event["end"]["dateTime"] > existing_start:
            conflicting_events.append(existing_event)

    return conflicting_events


# Function to add a manual event
def add_manual_event(service, calendar_id):
    # Gathering event information
    manual_event_summary = input('Name:\n')
    manual_event_date = input('Date (YYYY-MM-DD):\n')
    manual_event_start = input('Start time (HH:MM:SS):\n')
    manual_event_end = input('End time (HH:MM:SS):\n')
    manual_event_location = input('Location:\n')
    manual_event_description = input('Description:\n')

    event = {
        "summary": manual_event_summary,
        "location": manual_event_location,
        "description": manual_event_description,
        "start": {
            "dateTime": manual_event_date + "T" + manual_event_start,
            "timeZone": "Europe/Oslo"
        },
        "end": {
            "dateTime": manual_event_date + "T" + manual_event_end,
            "timeZone": "Europe/Oslo"
        }

    }

    # Check if the new event conflicts with existing event
    conflicting_events = check_event_conflict(service, calendar_id, event)
    if conflicting_events:
        print('This event conflicts with the following events:')
        for conflicting_event in conflicting_events:
            print(conflicting_event["summary"])

        choice = input("Do you want to continue? (Y/N)").upper()
        if choice == "N":
            print('Event not added.')
            return

    # Adding the event
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f"Event created {event.get('htmlLink')}")


# Function to read events from CSV
def read_events_from_csv(csv_file_path):
    events = []
    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            events.append({
                'summary': row['summary'],
                'description': row['description'],
                'start': {
                    'dateTime': row['start_datetime'],
                    'timeZone': row['start_timezone']
                },
                'end': {
                    'dateTime': row['end_datetime'],
                    'timeZone': row['end_timezone']
                }
            })
        return events


# Function to get calendar events from CSV file
def import_events_from_csv(service, calendar_id, csv_file_path):
    events = read_events_from_csv(csv_file_path)
    events_created_count = 0

    for event in events:
        # Check if the new event conflicts with existing events
        conflicting_events = check_event_conflict(service, calendar_id, event)
        if conflicting_events:
            print(f"\nEvent '{event['summary']}' conflicts with existing event(s):")
            for conflicting_event in conflicting_events:
                start_date = conflicting_event['start'].get('dateTime', conflicting_event['start'].get('date'))
                print(f"{conflicting_event['summary']}, {start_date}")
            choice = input("Do you want to continue and add this event? (Y/N): ").strip().upper()
            if choice != "Y":
                print(f"Event '{event['summary']}' not added.")
                continue

        # Attempting to add each event
        try:
            event = service.events().insert(calendarId=calendar_id, body=event).execute()
            events_created_count += 1
            print(f"Event created {event.get('htmlLink')}")
        except Exception as e:
            print(f"Failed to create event: {e}")

    print(f"\nSuccessfully added {events_created_count} events.")


def export_events_to_csv(calendar_id, credentials_file, csv_file):
    pass


# Function to print upcoming events
def print_upcoming_events(service, calendar_id, calendar_name):
    now = dt.datetime.now().isoformat() + "Z"

    # Retrieve upcoming events from the specified calendar
    event_result = service.events().list(calendarId=calendar_id, timeMin=now, maxResults=10, singleEvents=True,
                                         orderBy="startTime").execute()
    events = event_result.get("items", [])

    # Check if there are upcoming events or not
    if not events:
        print(f"No upcoming events found in the calendar '{calendar_name}'")
        return

    # Print upcoming events
    print("\nUpcoming events:")

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))

        print(f"{start}\t{end}\t{event['summary']}")


# Main function to authenticate and perform actions based on input
def main():
    creds = None

    # Checking if token file exists to authenticate
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")

    # If token is invalid or doesn't exist, refresh or obtain new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Writing new credentials to token file
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        # Building Google Calendar service
        service = build("calendar", "v3", credentials=creds)

        calendar_id = get_calendar_id(service, CALENDAR_NAME)

        if calendar_id is None:
            print(f"Calendar '{CALENDAR_NAME}' not found")
            return

        """
        MENU
        """
        while True:
            print("Choose an option:")
            print("1. Add a manual event")
            print("2. Import events from CSV")
            print("3. Print upcoming events")
            print("0. Exit")

            option = input('\nEnter your choice:\n')

            try:
                option = int(option)
            except ValueError:
                print("Invalid option.\n")
                continue

            if option == 1:
                add_manual_event(service, calendar_id)
               
            elif option == 2:
                import_events_from_csv(service, calendar_id, CSV_FILE)
             
            elif option == 3:
                print_upcoming_events(service, calendar_id, CALENDAR_NAME)
               
            elif option == 0:
                break
            else:
                print("Invalid option. Please choose again.")





    # Checking for errors
    except HttpError as error:
        print("HttpError Occurred:", error)
        print("Reason:", error.reason)
        print("Status code:", error.resp.status)
        print("Error details:", error._get_reason())


if __name__ == "__main__":
    main()
