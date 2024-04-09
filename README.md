# Zoom Meeting Creation in Google Calendar or Outlook

The Python program `auth.py` authenticates Zoom, Google and Microsoft via their respective APIs and stored the bearer tokens in your .env file.

The Python program `createmeeting.py` allows you to use natural language to create a meeting in your Google or Microsoft Outlook Calendar.

Example Queries:
* `Create a Google Meeting for 10 PM on April 12, 2024`
* `Create a Microsoft meeting for today at 5:30`
* `Google Meeting for 5:30 AM on 04/13/24`
* `Microsoft meeting for 6:30 PM on 4/12/2024`

## Instructions

1. Clone repo
2. Install ngrok: https://ngrok.com/
3. `python -m http.server 5000`
4. Grab Forwarding URL

5. Update Zoom Redirect URI (`https://NGROKURL/zoom_callback`) in App Marketplace (https://marketplace.zoom.us/user/build)

![Zoom Oauth](https://i.imgur.com/4JDHoo7.png)

6. Update Microsoft Redirect URI (`https://NGROKURL/microsoft_callback`) in Microsoft Entra Admin Center (https://entra.microsoft.com/#home)

![Microsoft Oauth](https://i.imgur.com/qGlgRJz.png)

7. Update Google Redirect URI (`https://NGROKURL/google_callback`) in Google Cloud Console (https://console.cloud.google.com/apis/credentials)

![Google Oauth](https://i.imgur.com/QtWZf4z.png)

8. Ensure .env file has respective client IDs and client secrets
9. Run `python auth.py`
10. Navigate to `localhost:5000` if browser does not launch OAuth URLs automatically
11. Verify bearer tokens are generated
12. Run `python createmeeting.py`


## App Flow
![Google Meeting](https://i.imgur.com/VPLplWZ.png)

![Microsoft Meeting](https://i.imgur.com/AlZgnPo.png)


## APIs Used:
* [Google Calendar API](https://developers.google.com/calendar/api/guides/overview)
* [Microsoft Graph API](https://learn.microsoft.com/en-us/graph/use-the-api)
* [Zoom API](https://developers.zoom.us/docs/api/)

## .env Variables Used:
* [ZOOM_CLIENT_ID](https://developers.zoom.us/docs/api/rest/using-zoom-apis/)
* [ZOOM_CLIENT_SECRET](https://developers.zoom.us/docs/api/rest/using-zoom-apis/)
* [ZOOM_BEARER_TOKEN](https://developers.zoom.us/docs/api/rest/using-zoom-apis/)
* [ZOOM_REDIRECT_URI](https://developers.zoom.us/docs/api/rest/using-zoom-apis/)
* [MICROSOFT_CLIENT_ID](https://learn.microsoft.com/en-us/graph/auth-v2-user?tabs=http)
* [MICROSOFT_CLIENT_SECRET](https://learn.microsoft.com/en-us/graph/auth-v2-user?tabs=http)
* [MICROSOFT_BEARER_TOKEN](https://learn.microsoft.com/en-us/graph/auth-v2-user?tabs=http)
* [MICROSOFT_REDIRECT_URI](https://learn.microsoft.com/en-us/graph/auth-v2-user?tabs=http)
* [GOOGLE_CLIENT_ID](https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid)
* [GOOGLE_CLIENT_SECRET](https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid)
* [GOOGLE_BEARER_TOKEN](https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid)
* [GOOGLE_REDIRECT_URI](https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid)
