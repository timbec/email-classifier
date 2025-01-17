from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]


def test_authentication():
    try:
        service = authenticate_gmail()
        profile = service.users().getProfile(userId='me').execute()
        email_address = profile.get("emailAddress")
        print(f"Authentication successful! Email address: {email_address}")
        return True
    except Exception as e:
        print(f"Authentication failed: {e}")
        return False


def authenticate_gmail():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('gmail', 'v1', credentials=creds)



def delete_old_unread_emails(service):
    one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y/%m/%d')
    query = f"is:unread before:{one_year_ago}"

    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No unread emails older than a year found.")
    else:
        for message in messages:
            msg_id = message['id']
            service.users().messages().delete(userId='me', id=msg_id).execute()
            print(f"Deleted message ID: {msg_id}")
