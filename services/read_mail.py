import base64
from services.authenticate import get_gmail_service
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import re
from bs4 import BeautifulSoup

def decode_base64url(data):
    if not data:
        return ""
    padded = data + '=' * (4 - len(data) % 4)
    return base64.urlsafe_b64decode(padded).decode("utf-8", errors="ignore")

def download_attachment(msg_id, attachment_id, filename):
    service = get_gmail_service()
    
    attachment = service.users().messages().attachments().get(
        userId="me",
        messageId=msg_id,
        id=attachment_id
    ).execute()
    
    file_data = decode_base64url(attachment["data"])
    
    downloads_dir = Path.home() / "Downloads"
    downloads_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = downloads_dir / filename
    
    with open(file_path, "wb") as f:
        f.write(file_data)
    
    return filename

def clean_text(text):
    # remove excessive newlines
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    
    # replace tabs with single space
    text = text.replace('\t', ' ')
    
    return text.strip()

def get_body(payload):
    texts = []
    plain_texts = []
    html_texts = []
    attachments = []
    
    def parse_parts(parts):
        for part in parts:
            # attachment part
            filename = part.get("filename", "")
            body = part.get("body", {})
            mime_type = part.get("mimeType", "")
            
            if filename and body.get("attachmentId"):
                attachments.append({
                    "filename": filename,
                    "mimeType": part.get("mimeType"),
                    "attachmentId": body['attachmentId']
                })
                continue
                     
            if part.get('parts'):
                parse_parts(part.get('parts'))
            
            data = body.get("data")
            
            if mime_type == "text/plain" and data:
                decoded = decode_base64url(data)
                text = clean_text(decoded.strip())
                if text:
                    plain_texts.append(text)
            elif mime_type == "text/html" and data:
                html = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                soup = BeautifulSoup(html, "html.parser")
                text = clean_text(soup.get_text())
                html_texts.append(text)
                # converter.ignore_links = False
                # converter.body_width = 0 
                # html_texts.append(converter.handle(decoded).strip())
    
    parts = payload.get('parts')
    if parts:
        parse_parts(parts)
    else:
        # Handle single-part email
        mime_type = payload.get("mimeType", "")
        body = payload.get("body", {})
        data = body.get("data")
        
        if mime_type == "text/plain" and data:
            decoded = decode_base64url(data)
            text = clean_text(decoded.strip())
            if text:
                plain_texts.append(text)
        elif mime_type == "text/html" and data:
            html = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html, "html.parser")
            text = clean_text(soup.get_text())
            html_texts.append(text)
            # decoded = decode_base64url(data)
            # converter = html2text.HTML2Text()
            # converter.ignore_links = False
            # converter.body_width = 0 
            # html_texts.append(converter.handle(decoded).strip())
    
    if plain_texts:
        texts.extend(plain_texts)
    elif html_texts:
        texts.extend(html_texts)
    
    res = []
    seen = set()
    for line in texts:
        if line not in seen:
            seen.add(line)
            res.append(line)
    
    body = "(No Body)"
    if len(texts) > 0:
        body = "\n".join(res).strip()
    
    return {
        "body": body,
        "attachments": attachments
    }

cache = {}

def fetch_message(msg_id):
    if msg_id in cache:
        return cache[msg_id]
    
    service = get_gmail_service()
    message = service.users().messages().get(
        userId="me",
        id=msg_id
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
    
    msg = {
        "id": msg_id,
        "sender": sender,
        "subject": subject,
        "date": date,
        "body": body["body"],
        "attachments": body["attachments"],
        "link": f"https://mail.google.com/mail/u/0/#inbox/{msg_id}"
    }
    
    cache[msg_id] = msg
    
    return msg
    
def read_mails():
    service = get_gmail_service()
    
    results = service.users().messages().list(
        userId="me",
        q="is:unread category:primary",
        
    ).execute()
    
    messages = results.get("messages", [])
    
    if len(messages) == 0:
        return []
    
    message_ids = []
    for msg in messages:
        message_ids.append(msg['id'])
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        mails = list(executor.map(fetch_message, message_ids))
    
    return mails

def mark_as_read(msg_id: str):
    service = get_gmail_service()
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={
            "removeLabelIds": ["UNREAD"]
        }
    ).execute()

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