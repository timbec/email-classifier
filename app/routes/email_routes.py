from fastapi import APIRouter
from app.services.email_service import authenticate_gmail, test_authentication

from datetime import datetime, timedelta

email_router = APIRouter()

# Route to test Gmail authentication
@email_router.get("/test-auth")
def test_auth():
    if test_authentication():
        return {"message": "Authentication successful!"}
    else:
        return {"message": "Authentication failed, please check your credentials."}
    


# Route to list unread emails for the past month
@email_router.get("/list-recent-unread")
def list_recent_unread():
    service = authenticate_gmail()
    emails = list_recent_unread_emails(service, days=30)  # Adjust the `days` parameter as needed
    return {"emails": emails}



def list_recent_unread_emails(service, days=30):
    # Set up the query to fetch emails from the past `days` days
    date_cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y/%m/%d')
    query = f"is:unread after:{date_cutoff}"
    
    try:
        results = service.users().messages().list(userId='me', q=query, maxResults=20).execute()
        messages = results.get('messages', [])

        email_list = []
        if not messages:
            print("No unread emails found for the specified period.")
            return email_list
        else:
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
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

    

@email_router.get("/delete-old")
def delete_old_emails():
    service = authenticate_gmail()
    print(service)
    return {"message": "Gmail service authenticated."}
    # delete_old_unread_emails(service)
    # return {"message": "Old unread emails have been deleted."}
