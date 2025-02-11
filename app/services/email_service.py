import asyncio
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta

import logging

logger = logging.getLogger(__name__)

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]


def test_authentication():
    try:
        service = authenticate_gmail()
        profile = service.users().getProfile(userId='me').execute()
        email_address = profile.get("emailAddress")
        logging.info(f"Authentication successful! Email address: {email_address}")
        return True
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        return False


async def authenticate_gmail():
    loop = asyncio.get_running_loop()
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)

    creds = await loop.run_in_executor(None, lambda: flow.run_local_server(port=0))

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
            print(message)
            msg_id = message['id']
            service.users().messages().delete(userId='me', id=msg_id).execute()
            print(f"Deleted message ID: {msg_id}")



async def list_recent_unread_emails(service, days=30):
    # Set up the query to fetch emails from the past `days` days
    date_cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y/%m/%d')
    query = f"is:unread after:{date_cutoff}"
    
    try:
        loop = asyncio.get_running_loop()

        # Run blocking API call in thread pool
        results = await loop.run_in_executor(None, lambda: service.users().messages().list(userId='me', q=query, maxResults=20).execute())
        messages = results.get('messages', [])
        

        email_list = []
        if not messages:
            print("No unread emails found for the specified period.")
            return email_list
        
        # Fetch emails concurrently
        email_tasks = [
            loop.run_in_executor(None, lambda: service.users().messages().get(userId='me', id=message['id']).execute())
            for message in messages
        ]
        messages_data = await asyncio.gather(*email_tasks)  # Fetch emails in parallel
        
        for msg in messages_data:
            headers = msg['payload']['headers']
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "No Subject")
            from_email = next((header['value'] for header in headers if header['name'] == 'From'), "Unknown Sender")
            email_list.append({"from": from_email, "subject": subject})

            # Print each email
            print(f"From: {from_email}, Subject: {subject}")

        return email_list
    except Exception as e:
        print(f"Error occurred while listing emails: {e}")
        return []
