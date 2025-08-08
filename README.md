<h1>📅 Event Grabber</h1>
<p><em>Adapted from <a href="https://github.com/QuixSens/gmail-event-extractor">QuixSens/gmail-event-extractor</a></em></p>

<p>Event Grabber allows you to fetch and extract key events and dates from your Gmail and automatically add them to your Google Calendar.<br>
This version has been customized for my personal workflow, with a few tweaks for smoother usage.</p>

<hr>

<h2>🔧 Requirements</h2>
<ul>
  <li>Python 3.8 or higher</li>
  <li>Gmail account with IMAP enabled</li>
  <li>Google Calendar API credentials (JSON file from Google Cloud Console)</li>
  <li>Required Python packages:
    <ul>
      <li>google-auth</li>
      <li>google-api-python-client</li>
      <li>google-auth-httplib2</li>
      <li>google-auth-oauthlib</li>
      <li>imaplib (standard library)</li>
      <li>email (standard library)</li>
      <li>(and any other dependencies as needed)</li>
    </ul>
  </li>
</ul>

<hr>

<h2>⚙️ Installation</h2>

<p><strong>Clone this repository:</strong></p>
<pre><code>git clone https://github.com/brantcass/Event-grabber.git
cd Event-grabber
</code></pre>

<p><strong>Install required Python packages:</strong></p>
<pre><code>pip install -r requirements.txt
</code></pre>
<p>(If you don’t have a <code>requirements.txt</code> yet, create one with the needed packages)</p>

<p><strong>Set up your Google Calendar API credentials:</strong></p>
<ul>
  <li>Follow the <a href="https://developers.google.com/calendar/api/quickstart/python">Google Calendar API Python Quickstart</a> to create <code>credentials.json</code></li>
  <li>Save <code>credentials.json</code> in the project root folder</li>
</ul>

<p><strong>Enable IMAP in your Gmail account:</strong></p>
<ul>
  <li>Go to Gmail Settings → Forwarding and POP/IMAP → Enable IMAP</li>
</ul>

<hr>

<h2>🚀 Usage</h2>
<p><strong>Configure your script if needed:</strong></p>
<ul>
  <li>Adjust any config variables (email address, labels, date ranges, etc.) inside the Python script.</li>
</ul>

<p><strong>Run the script:</strong></p>
<pre><code>python main.py
</code></pre>

<p><strong>Authorize access to your Google Calendar:</strong></p>
<ul>
  <li>On first run, a browser window will open to authorize the app to access your calendar.</li>
</ul>

<p>Enjoy your events automatically added to your Google Calendar!</p>

<hr>

<h2>📚 Notes</h2>
<ul>
  <li>Make sure your Gmail account has emails with calendar event details for the script to extract.</li>
  <li>The script parses dates and events based on heuristics — it might need tweaking for specific email formats.</li>
  <li>Keep your credentials secure and don’t share them publicly.</li>
</ul>

