#ngrok http --domain=carefully-intense-bedbug.ngrok-free.app 5000

from flask import Flask, request, redirect
import requests
import base64
import webbrowser
from datetime import datetime, timedelta
from dotenv import load_dotenv, set_key
import os
import json
import pytz

# Load environment variables
load_dotenv()

# OAuth credentials
MICROSOFT_CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
MICROSOFT_SECRET = os.getenv("MICROSOFT_SECRET")
MICROSOFT_REDIRECT_URI = os.getenv("MICROSOFT_REDIRECT_URI")
ZOOM_CLIENT_ID = os.getenv("ZOOM_CLIENT_ID")
ZOOM_CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET")
ZOOM_REDIRECT_URI = os.getenv("ZOOM_REDIRECT_URI")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

# Flask app setup
app = Flask(__name__)

@app.route("/")
def index():
	# Open Microsoft login page in browser
	microsoft_auth_url = (
		"https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
		"?client_id={}&response_type=code&redirect_uri={}&scope=User.Read Calendars.ReadWrite&response_mode=query"
	).format(MICROSOFT_CLIENT_ID, MICROSOFT_REDIRECT_URI)
	webbrowser.open(microsoft_auth_url)

	# Open Zoom login page in browser
	zoom_auth_url = (
		"https://zoom.us/oauth/authorize?response_type=code&client_id={}&redirect_uri={}"
	).format(ZOOM_CLIENT_ID, ZOOM_REDIRECT_URI)
	webbrowser.open(zoom_auth_url)

	# Open Google login page in browser
	google_auth_url = (
		"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={}&redirect_uri={}&scope=https://www.googleapis.com/auth/calendar&access_type=offline&prompt=consent"
	).format(GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI)
	webbrowser.open(google_auth_url)

	return "Authentication in progress..."

@app.route("/microsoft_callback")
def microsoft_callback():
	# Exchange authorization code for access token
	auth_code = request.args.get("code")
	token_data = {
		"client_id": MICROSOFT_CLIENT_ID,
		"scope": "User.Read Calendars.ReadWrite",
		"code": auth_code,
		"redirect_uri": MICROSOFT_REDIRECT_URI,
		"grant_type": "authorization_code",
		"client_secret": MICROSOFT_SECRET
	}
	token_response = requests.post("https://login.microsoftonline.com/common/oauth2/v2.0/token", data=token_data)
	access_token = token_response.json().get("access_token")
	if access_token:
		set_key(".env", "MICROSOFT_BEARER_TOKEN", access_token)

	return "Microsoft access token stored."

@app.route("/zoom_callback")
def zoom_callback():
	# Exchange authorization code for access token
	auth_code = request.args.get("code")
	auth_header = base64.b64encode(f"{ZOOM_CLIENT_ID}:{ZOOM_CLIENT_SECRET}".encode()).decode()
	headers = {"Authorization": f"Basic {auth_header}"}
	payload = {"grant_type": "authorization_code", "code": auth_code, "redirect_uri": ZOOM_REDIRECT_URI}
	token_response = requests.post("https://zoom.us/oauth/token", headers=headers, data=payload)
	access_token = token_response.json().get("access_token")
	if access_token:
		set_key(".env", "ZOOM_BEARER_TOKEN", access_token)

	return "Zoom access token stored."

@app.route("/google_callback")
def google_callback():
	# Exchange authorization code for access token
	auth_code = request.args.get("code")
	token_data = {
		"client_id": GOOGLE_CLIENT_ID,
		"client_secret": GOOGLE_CLIENT_SECRET,
		"code": auth_code,
		"redirect_uri": GOOGLE_REDIRECT_URI,
		"grant_type": "authorization_code"
	}
	token_response = requests.post("https://oauth2.googleapis.com/token", data=token_data)
	access_token = token_response.json().get("access_token")
	if access_token:
		set_key(".env", "GOOGLE_BEARER_TOKEN", access_token)

	return "Google access token stored."

if __name__ == "__main__":
	app.run(debug=True, port=5000)
