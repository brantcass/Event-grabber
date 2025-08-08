📅 Event Grabber
Adapted from QuixSens/gmail-event-extractor

Event Grabber allows you to fetch and extract key events and dates from your Gmail and automatically add them to your Google Calendar.
This version has been customized for my personal workflow, with a few tweaks for smoother usage.

🔧 Requirements
Python 3.8 or higher

Gmail account with IMAP enabled

Google Calendar API credentials (JSON file from Google Cloud Console)

Required Python packages:

google-auth

google-api-python-client

google-auth-httplib2

google-auth-oauthlib

imaplib (standard library)

email (standard library)

(and any other dependencies as needed)

⚙️ Installation
Clone this repository:

bash
Copy
Edit
git clone https://github.com/your-username/Event-grabber.git
cd Event-grabber
Create and activate a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
Install required Python packages:

bash
Copy
Edit
pip install -r requirements.txt
(If you don’t have a requirements.txt yet, you can create one with the needed packages)

Set up your Google Calendar API credentials:

Follow the Google Calendar API Python Quickstart to create credentials.json

Save credentials.json in the project root folder

Enable IMAP in your Gmail account:

Go to Gmail Settings → Forwarding and POP/IMAP → Enable IMAP

🚀 Usage
Configure your script if needed:

Adjust any config variables (email address, labels, date ranges, etc.) inside the Python script.

Run the script:

bash
Copy
Edit
python main.py
Authorize access to your Google Calendar:

On first run, a browser window will open to authorize the app to access your calendar.

Enjoy your events automatically added to your Google Calendar!

📚 Notes
Make sure your Gmail account has emails with calendar event details for the script to extract.

The script parses dates and events based on heuristics — it might need tweaking for specific email formats.

Keep your credentials secure and don’t share them publicly.

