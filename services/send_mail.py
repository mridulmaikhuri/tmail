import base64
from email.message import EmailMessage
from googleapiclient.errors import HttpError
from services.authenticate import get_gmail_service

def send_mail(to, subject, body):
    service = get_gmail_service()
    message = EmailMessage()
    message["To"] = to
    message["From"] = "me"
    message["Subject"] = subject
    message.set_content(body)
    
    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()
    create_message = {
        "raw": encoded_message
    }
    try:
        send_message = service.users().messages().send(
            userId = "me",
            body = create_message
        ).execute()
        return True
    except HttpError as e:
        print(f"An error occured: {e}")
        return False
    
    
    