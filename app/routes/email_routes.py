from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import BackgroundTasks
from app.services.email_service import authenticate_gmail, test_authentication, list_recent_unread_emails, delete_old_unread_emails


from datetime import datetime, timedelta

email_router = APIRouter()

# Route to test Gmail authentication
@email_router.get("/test-auth")
def test_auth():
    if test_authentication():
        return {"message": "Authentication successful!"}
    else:
        raise HTTPException(status_code=401, detail="Authentication failed, please check your credentials.")
    


# Route to list unread emails for the past month
@email_router.get("/list-recent-unread")
async def list_recent_unread():
    service = await authenticate_gmail()
    emails = list_recent_unread_emails(service, days=30)  # Adjust the `days` parameter as needed
    return {"emails": emails}


# Route to list unread emails for the past month
@email_router.get("/list-one-year-unread")
async def list_oneyear_unread():
    service = await authenticate_gmail()
    emails = await list_recent_unread_emails(service, days=365)  # Adjust the `days` parameter as needed
    return {"emails": emails}


@email_router.get("/delete-old")
def delete_old_emails():
    service = authenticate_gmail()
    print(service)
    return {"message": "Gmail service authenticated."}
    delete_old_unread_emails(service)
    return {"message": "Old unread emails have been deleted."}
