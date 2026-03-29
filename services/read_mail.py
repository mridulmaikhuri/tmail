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
        if filename and body.get("attachmentId"):
            attachments.append({
                "filename": filename,
                "mimeType": part.get("mimeType"),
                "attachmentId": body['attachmentId']
            })
            return
        
        data = body.get("data")
        
        if mime_type == "text/plain" and data:
            decoded = base64.urlsafe_b64decode(data).decode(errors="ignore")
            text = decoded.strip()
            if text:
                texts.append(text)
        elif mime_type == "text/html":
            texts.append("(HTML content)")
        elif "parts" in part:
            for subpart in part["parts"]:
                parse_part(subpart)
        else:
            if mime_type:
                texts.append(f"({mime_type} Content)")
    
    parse_part(payload)
    res = []
    seen = set()
    for line in texts:
        if line not in seen:
            seen.add(line)
            res.append(line)
    
    body = "(No Body)"
    attach = "(No Attachments)"
    if len(texts) > 0:
        body = "\n".join(res).strip()
    if len(attachments) > 0:
        attach = attachments
    
    return {
        "body": body,
        "attachments": attach
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
        
        sender, subject, date = None, None, None
        for h in headers:
            if h["name"] == "From":
                sender = h["value"]
            elif h["name"] == "Subject":
                subject = h["value"]
            elif h["name"] == "Date":
                date = h["value"]
        
        sender = (sender or "").strip() or "(No Sender)"
        subject = (subject or "").strip() or "(No Subject)"
        date = (date or "").strip() or "(No Date)"       
        body = get_body(message["payload"])
        
        mails.append(
            {
                "id": msg["id"],
                "sender": sender,
                "subject": subject,
                "date": date,
                "body": body["body"],
                "attachments": body["attachments"],
                "link": f"https://mail.google.com/mail/u/0/#inbox/{msg['id']}"
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
        print(f"link: {mail['link']}")