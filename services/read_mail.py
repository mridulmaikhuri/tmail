import base64
from services.authenticate import get_gmail_service
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import re
from bs4 import BeautifulSoup

def download_attachment(msg_id, attachment_id, filename):
    try:
        service = get_gmail_service()
        
        attachment = service.users().messages().attachments().get(
            userId="me",
            messageId=msg_id,
            id=attachment_id
        ).execute()
        
        data = attachment.get("data")
        if not data:
            return False, "Attachment not found", ""
        
        file_data = base64.urlsafe_b64decode(data)
        
        downloads_dir = Path.home() / "Downloads"
        downloads_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = downloads_dir / filename
        
        with open(file_path, "wb") as f:
            f.write(file_data)
        
        return True, "", str(file_path)
    except Exception as e:
        return False, str(e), ""

def clean_text(text):
    # Replace unnecessary unicode chars with empty string 
    text = re.sub(r'[\u2000-\u200F\u2028-\u202F\u2060-\u206F\u00A0\u00AD]', '', text)
    
    # Remove ALL invisible / zero-width characters
    text = re.sub(r'[\u200B-\u200F\u202A-\u202F\u2060-\u206F\uFEFF\u034f]', '', text)

    # Replace non-breaking space with normal space
    text = text.replace('\u00A0', ' ')
    
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Replace tabs with single space
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Remove leading/trailing spaces from each line
    lines = [line.strip() for line in text.split('\n')]
    
    # Remove empty lines (but keep paragraph spacing)
    cleaned_lines = []
    prev_empty = False
    for line in lines:
        if line == "":
            if not prev_empty:
                cleaned_lines.append("")
            prev_empty = True
        else:
            cleaned_lines.append(line)
            prev_empty = False
    
    # Join back
    text = "\n".join(cleaned_lines)
    
    # Final cleanup: collapse excessive newlines again and weird unicode characters
    text = re.sub(r'\n{3,}', '\n\n', text)
    
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
                decoded = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                text = clean_text(decoded.strip())
                if text:
                    plain_texts.append(text)
            elif mime_type == "text/html" and data:
                html = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                soup = BeautifulSoup(html, "html.parser")
                text = clean_text(soup.get_text())
                if text:
                    html_texts.append(text)
    
    parts = payload.get('parts')
    if parts:
        parse_parts(parts)
    else:
        # Handle single-part email
        mime_type = payload.get("mimeType", "")
        body = payload.get("body", {})
        data = body.get("data")
        
        if mime_type == "text/plain" and data:
            decoded = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
            text = clean_text(decoded.strip())
            if text:
                plain_texts.append(text)
        elif mime_type == "text/html" and data:
            html = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html, "html.parser")
            text = clean_text(soup.get_text())
            if text:
                html_texts.append(text)
    
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
    
def read_mails():
    service = get_gmail_service()
    
    results = service.users().messages().list(
        userId="me",
        q="is:unread category:primary",
        
    ).execute()
    
    messages = results.get("messages", [])
    
    if len(messages) == 0:
        return []
    
    mails = []
    
    def cb(request_id, response, exception):
        if exception:
            print(f'Error for {request_id}: {exception}')
            return
        
        msg_id = response['id']
        headers = response['payload']['headers']
        
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
        
        res = get_body(response["payload"])
        body = res.get('body')
        attachments = res.get('attachments')
        
        link = f"https://mail.google.com/mail/u/0/#inbox/{msg_id}"    
        
        msg = {
            "id": msg_id,
            "sender": sender,
            "subject": subject,
            "date": date,
            "body": body,
            "attachments": attachments,
            "link": link
        }
        
        mails.append(msg)

        return
    
    BATCH_SIZE = 50
    
    message_ids = [msg['id'] for msg in messages]
    
    for i in range(0, len(message_ids), BATCH_SIZE):
        batch = service.new_batch_http_request(callback = cb)
        for msg_id in message_ids[i: i + BATCH_SIZE]:
            batch.add(
                service.users().messages().get(
                    userId = 'me',
                    id = msg_id
                ),
                request_id = msg_id
            )
        batch.execute()
    
    
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
        print(ascii(mail['body']))
    # for mail in mails:
    #     print(f"id: {mail["id"]}")
    #     print(f"sender: {mail["sender"]}")
    #     print(f"subject: {mail["subject"]}")
    #     print(f"date: {mail["date"]}")
    #     print(f"body: {mail["body"]}")
    #     print(f"attachment: {mail["attachments"]}")
    #     print(f"link: {mail['link']}")