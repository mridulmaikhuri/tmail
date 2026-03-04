import base64
from services.authenticate import get_gmail_service

def get_body(payload):
    if "parts" in payload:
        for part in payload["parts"]:
            mime_type = part.get("mimeType")
            if mime_type == "text/plain":
                data = part["body"].get("data")
                if data:
                    return base64.urlsafe_b64decode(data).decode()
            if "parts" in part:
                return get_body(part)
    data = payload["body"].get("data")
    if data:
        return base64.urlsafe_b64decode(data).decode()
    return ""

def read_mails(max_results=10):
    service = get_gmail_service()
    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=max_results
    ).execute()
    messages = results.get("messages", [])
    mails = []
    for msg in messages:
        message = service.users().messages().get(
            userId="me",
            id=msg["id"]
        ).execute()
        headers = message["payload"]["headers"]
        sender = subject = date = ""
        for h in headers:
            if h["name"] == "From":
                sender = h["value"]
            elif h["name"] == "Subject":
                subject = h["value"]
            elif h["name"] == "Date":
                date = h["value"]
        body = get_body(message["payload"])
        mails.append(
            {"id": msg["id"],
            "sender": sender,
            "subject": subject,
            "date": date,
            "body": body}
        )
    return mails