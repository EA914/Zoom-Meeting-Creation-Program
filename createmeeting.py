import requests
import spacy
import re
import dateparser
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import json
import pytz

# Load environment variables
load_dotenv()

# Get the access tokens from the .env file
google_access_token = os.getenv("GOOGLE_BEARER_TOKEN")
zoom_access_token = os.getenv("ZOOM_BEARER_TOKEN")
ms_access_token = os.getenv("MICROSOFT_BEARER_TOKEN")

# Set the headers for the API requests
google_headers = {
	"Authorization": f"Bearer {google_access_token}",
	"Content-Type": "application/json"
}
zoom_headers = {
	"Authorization": f"Bearer {zoom_access_token}",
	"Content-Type": "application/json"
}
ms_headers = {
	"Authorization": f"Bearer {ms_access_token}",
	"Content-Type": "application/json"
}

# Function to create a Zoom meeting
def create_zoom_meeting(start_time):
	zoom_meeting_data = {
		"topic": "Zoom Meeting",
		"start_time": start_time,
		"duration": 60,	 # Duration in minutes
		"timezone": "America/New_York"
	}
	zoom_response = requests.post("https://api.zoom.us/v2/users/me/meetings", headers=zoom_headers, data=json.dumps(zoom_meeting_data))
	return zoom_response.json().get("join_url")

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Get user input
meeting_request = input("Enter your meeting request: ")

# Extract information using SpaCy
doc = nlp(meeting_request)

# Find calendar choice
calendar_choice = "google" if "google" in meeting_request.lower() else "microsoft"

# Find date and time
date_str = ""
time_str = ""
for ent in doc.ents:
	if ent.label_ == "TIME":
		time_str = ent.text
	elif ent.label_ == "DATE":
		date_str = ent.text

if not date_str or not time_str:
	print("Could not parse the meeting information.")
	exit()

# Combine date and time into a datetime object using dateparser
meeting_datetime = dateparser.parse(f"{date_str} {time_str}")


if not meeting_datetime:
	print("Could not parse the date and time.")
	exit()

start_time = meeting_datetime.isoformat()

# Create the Zoom meeting
zoom_meeting_link = create_zoom_meeting(start_time)

# Create the event in the chosen calendar
if calendar_choice == "google":
	event_data = {
		"summary": "Zoom Meeting",
		"description": f"Join the Zoom meeting: {zoom_meeting_link}",
		"start": {
			"dateTime": start_time,
			"timeZone": "America/New_York"
		},
		"end": {
			"dateTime": (meeting_datetime + timedelta(hours=1)).isoformat(),
			"timeZone": "America/New_York"
		}
	}
	response = requests.post("https://www.googleapis.com/calendar/v3/calendars/primary/events", headers=google_headers, data=json.dumps(event_data))
elif calendar_choice == "microsoft":
	event_data = {
		"subject": "Zoom Meeting",
		"body": {
			"contentType": "HTML",
			"content": f"Join the Zoom meeting: <a href='{zoom_meeting_link}'>{zoom_meeting_link}</a>"
		},
		"start": {
			"dateTime": start_time,
			"timeZone": "America/New_York"
		},
		"end": {
			"dateTime": (meeting_datetime + timedelta(hours=1)).isoformat(),
			"timeZone": "America/New_York"
		},
		"location": {
			"displayName": "Zoom Meeting",
			"locationUri": zoom_meeting_link
		},
		"attendees": [],
		"isOnlineMeeting": True
	}
	response = requests.post("https://graph.microsoft.com/v1.0/me/events", headers=ms_headers, data=json.dumps(event_data))
else:
	print("Invalid calendar choice.")
	exit()

# Check the response
if response.status_code in [200, 201]:
	print(f"Zoom meeting created and added to {calendar_choice.capitalize()} Calendar successfully for {meeting_datetime.strftime('%I:%M %p')} on {meeting_datetime.strftime('%m/%d/%Y')}.")
else:
	print(f"Failed to create event in {calendar_choice.capitalize()} Calendar: {response.status_code} {response.text}")
