from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Link, ListView, ListItem, Label
from textual.containers import Vertical, Container
from textual.app import ComposeResult
from services.read_mail import download_attachment

class ViewMail(Screen):
    CSS_PATH = "view_mail.tcss"
    BINDINGS = [
        ("p", "prev", "Back"),
        ("d", "download", "Download Attachment")
    ]
    
    def __init__(self, email):
        super().__init__()
        self.email = email
        
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Vertical():
            Static("📧 Email Viewer", id="title"),

            Container(
                Static(f"From   : {self.email['sender']}"),
                Static(f"Subject: {self.email['subject']}"),
                Static(f"Date   : {self.email['date']}"),
                id="metadata"
            ),

            Static(self.email['body'], id="body"),
            
            if (self.email['attachments']):
                yield Static('Attachments')
                self.attachment_list = ListView(
                    *[
                        ListItem(Label(attachment['filename'])) for attachment in self.email['attachments']
                    ]
                )
                yield self.attachment_list
            else:
                yield Static('No Attachments')
            
            Link('Click to open mail in Browser or Press Enter', url=self.email['link'], tooltip='Click me', id='link'),

            id="mail-container"
        
        yield Footer()
    
    def action_prev(self) -> None:
        self.app.pop_screen()
    
    def action_download(self):
        if not self.email['attachments']:
            return
        
        selected = self.attachment_list.index or 0
        attachment = self.email['attachments'][selected]
        
        filename = attachment['filename']
        
        download_attachment(
            self.email['id'],
            attachment['attachmentId'],
            filename
        )
        
        self.notify(f'Downloaded: {filename}')