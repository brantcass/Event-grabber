# Adapted from https://github.com/QuixSens/gmail-event-extractor/blob/main/main.py
# This script extracts event details from emails and adds them to Google Calendar.

import imaplib
import email
import re
import os
import json
import subprocess
import unicodedata
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# --- CONFIG ---
EMAIL_ACCOUNT = 'Email goes here'
APP_PASSWORD = 'kpsguklnrcinsint'  # Remove the spaces
SCOPES = ['https://www.googleapis.com/auth/calendar']

# --- CLEAN FORWARDED EMAILS ---
def clean_forwarded_header(text):
    return re.sub(r"-{2,} Forwarded message -{2,}.*?(From:|Date:|Subject:|To:).*?(\n\n|\r\n\r\n)", "", text, flags=re.DOTALL | re.IGNORECASE)

# --- GMAIL FETCHING ---
def get_emails():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
    mail.select('inbox')
    status, data = mail.search(None, 'ALL')
    email_ids = data[0].split()[-1:]  # last 5 emails
    emails = []

    for e_id in email_ids:
        status, data = mail.fetch(e_id, '(RFC822)')
        raw = data[0][1]
        msg = email.message_from_bytes(raw)
        subject = msg["subject"]
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode()
            except:
                pass

        emails.append((subject, body))
    return emails

# --- Regex Extraction ---
def extract_details(body):
    date_match = re.search(r'(\d{1,2}(st|nd|rd|th)? [A-Za-z]+ \d{4})', body)
    time_match = re.search(r'(\d{1,2}:\d{2} ?(AM|PM|am|pm)?( onwards| sharp)?)', body)
    venue_match = re.search(r'(?:venue|location)[:\- ]+([^\n]+)', body, re.IGNORECASE)

    return {
        'date': date_match.group(1) if date_match else None,
        'time': time_match.group(1) if time_match else None,
        'venue': venue_match.group(1) if venue_match else None
    }

# --- AI Extraction ---
def extract_using_ollama(body):
    clean_body = unicodedata.normalize("NFKD", body).encode("ascii", "ignore").decode("ascii")
    prompt = f"""Extract event details from this email and return in JSON format only and not a single word other than json. The date and time(No extra words like from, onwards etc. Just the time and AM/PM) must follow same format like in this:
{{"date": "10 July 2025", "time": "4:00 PM", "venue": "Seminar Hall"}}

Email:
{clean_body}
"""
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    try:
        print("🧠 Model said:\n", result.stdout)
        return json.loads(result.stdout.strip())
    except Exception as e:
        print("⚠️ AI returned invalid JSON:", e)
        return {}

# --- Mandatory Event Detection ---
def is_mandatory_event(subject, body):
    body = body.lower()
    subject = subject.lower()
    keywords = [
        "mandatory",
        "compulsory",
        "Event",
        "must attend",
        "required to attend",
        "attend",
        "invited",
        "please attend",
        "join us",
        "reminder"
    ]
    known_types = [
        "meeting",
        "appointment",
        "phone call",
        "conference",
        "interview",
        "wedding",
        "birthday",
        "ceremony",
        "gathering",
        "dinner",
        "lunch",
        "training",
        "workshop",
        "seminar",
        "webinar",
        "town hall",
        "all-hands",
        "review",
        "presentation",
        "shift",
        "deadline",
        "check-in",
        "planning session",
        "catch-up",
        "orientation",
        "onboarding",
        "kickoff"
    ]
    return any(kw in body for kw in keywords) or any(kt in body or kt in subject for kt in known_types)

# --- Google Calendar Setup ---
def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            try:
                creds = flow.run_local_server(port=0)
            except:
                creds = flow.run_local_server(port=0, open_browser=False)
                print("If browser didn't open, visit this URL manually:")
                print(flow.authorization_url()[0])
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

# --- Cleaner for messy date/time ---
def clean_date_time(date_str, time_str):
    # Remove ordinal suffixes (st, nd, rd, th)
    date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
    # Remove "onwards", "sharp", etc.
    time_str = re.sub(r'\b(onwards|sharp)\b', '', time_str, flags=re.IGNORECASE).strip()
    # Add space between digit and AM/PM if needed
    time_str = re.sub(r'(\d)(am|pm|AM|PM)', r'\1 \2', time_str)
    # Ensure AM/PM is present, default to AM if missing
    if not re.search(r'\b(am|pm|AM|PM)\b', time_str):
        time_str += ' AM'

    dt_str = f"{date_str} {time_str}"
    return datetime.strptime(dt_str, '%d %B %Y %I:%M %p')

# --- Add to Google Calendar ---
def add_to_calendar(event_details, service):
    try:
        dt = clean_date_time(event_details['date'], event_details['time'])
        summary = 'Club Activity (Mandatory)' if event_details.get("mandatory") else 'Club Activity'
        event = {
            'summary': summary,
            'location': event_details.get('venue'),
            'start': {'dateTime': dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': (dt + timedelta(hours=1)).isoformat(), 'timeZone': 'Asia/Kolkata'}
        }
        service.events().insert(calendarId='primary', body=event).execute()
        print(f"✅ Event added: {summary} at {event['location']} on {event['start']['dateTime']}")
    except Exception as e:
        print("❌ Failed to add event:", e)

# --- MAIN ---
if __name__ == "__main__":
    service = get_calendar_service()
    emails = get_emails()

    for subject, body in emails:
        print(f"\n📩 Processing email: {subject}")
        if not body.strip():
            print("⚠️ Empty email body. Skipping.")
            continue

        body = clean_forwarded_header(body)

        # Step 1: Try Regex
        details = extract_details(body)

        # Step 2: Fallback to AI if incomplete
        if not (details.get("date") and details.get("time") and details.get("venue")):
            print("🔄 Incomplete info via regex. Trying AI...")
            details = extract_using_ollama(body)

        print("🔍 Extracted:", details)

        if details.get("date") and details.get("time") and details.get("venue"):
            details["mandatory"] = is_mandatory_event(subject, body)
            add_to_calendar(details, service)
        else:
            print("⚠️ Skipping: Missing one or more fields (date/time/venue)")