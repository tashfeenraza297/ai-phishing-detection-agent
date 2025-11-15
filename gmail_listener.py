# gmail_listener.py
import os, pickle, base64, time
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDS_FILE = "token.pickle"
CLIENT_SECRET = "client_secret.json"  # download from Google Cloud

def get_service():
    creds = None
    if os.path.exists(CREDS_FILE):
        with open(CREDS_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(CREDS_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def extract_urls(text):
    import re
    return re.findall(r'https?://[^\s]+', text)

service = get_service()
last_id = None

while True:
    results = service.users().messages().list(userId='me', q='is:unread').execute()
    messages = results.get('messages', [])
    for msg in messages:
        if last_id and msg['id'] == last_id: continue
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = txt['payload']
        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode()
        else:
            body = base64.urlsafe_b64decode(payload['body']['data']).decode()

        urls = extract_urls(body)
        for url in urls:
            requests.post("http://localhost:8000/scan", json={"input": url, "type": "url"})
        # Mark read
        service.users().messages().modify(userId='me', id=msg['id'], body={'removeLabelIds': ['UNREAD']}).execute()
    last_id = messages[0]['id'] if messages else last_id
    time.sleep(15)