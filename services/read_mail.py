import base64
from services.authenticate import get_gmail_service

def get_body(payload):
    texts = []
    attachments = []
    
    def parse_part(part):
        mime_type = part.get("mimeType", "")
        body = part.get("body", {})
        filename = part.get("filename", "")
        
        # attachments
        if filename:
            attachments.append(filename)
            return
        
        data = body.get("data")
        
        if mime_type == "text/plain" and data:
            decoded = base64.urlsafe_b64decode(data).decode(errors="ignore")
            text = decoded.strip()
            if text:
                texts.append(text)
        elif mime_type == "text/html":
            texts.append("[HTML content]")
        elif "parts" in part:
            for subpart in part["parts"]:
                parse_part(subpart)
        else:
            if mime_type:
                texts.append(f"[{mime_type} Content]")
    
    parse_part(payload)
    res = []
    seen = set()
    for line in texts:
        if line not in seen:
            seen.add(line)
            res.append(line)
    
    return {
        "text": "\n".join(res).strip(),
        "attachments": attachments
    }
    
def read_mails(max_results=10):
    service = get_gmail_service()
    results = service.users().messages().list(
        userId="me",
        q="is:unread category:primary",
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
            {
                "id": msg["id"],
                "sender": sender,
                "subject": subject or "[No subject]",
                "date": date,
                "body": body["text"] or "[No body]",
                "attachments": body["attachments"] or "[No attachments]"
            }
        )
    return mails

if __name__ == "__main__":
    mails = read_mails()
    print(len(mails))
    for mail in mails:
        print(f"id: {mail["id"]}")
        print(f"sender: {mail["sender"]}")
        print(f"subject: {mail["subject"]}")
        print(f"date: {mail["date"]}")
        print(f"body: {mail["body"]}")
        print(f"attachment: {mail["attachments"]}")