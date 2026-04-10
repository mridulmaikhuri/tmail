from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Link, ListView, ListItem, Label
from textual.containers import VerticalScroll, Container
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
        
        with VerticalScroll(id="mail-container"):
            yield Static("📧 Email Viewer", id="title")

            yield Container(
                Static(f"From   : {self.email['sender']}"),
                Static(f"Subject: {self.email['subject']}"),
                Static(f"Date   : {self.email['date']}"),
                id="metadata"
            )

            yield Static(self.email['body'], id="body")
            
            if (self.email['attachments']):
                self.attachment_list = ListView(
                    *[
                        ListItem(Label(attachment['filename'])) for attachment in self.email['attachments']
                    ],
                    id="attachment-list"
                )
                yield self.attachment_list
            else:
                yield Static('No Attachments', id='no-attachment')
            
            yield Container(
                Link('Click to open mail in Browser or Press Enter', 
                     url=self.email['link'], tooltip='Open in Browser', id='link'),
                id='link-container'
            )
        
        yield Footer()
    
    def action_prev(self) -> None:
        self.app.pop_screen()
    
    def action_download(self):
        if not self.email['attachments']:
            return
        
        selected = self.attachment_list.index or 0
        attachment = self.email['attachments'][selected]
        
        filename = attachment['filename']
        
        res, err, file_path = download_attachment(
            self.email['id'],
            attachment['attachmentId'],
            filename
        )
        
        if res == True:
            self.notify(f'Downloaded at: {file_path}')
        else:
            self.notify(f"An error occured: {err}", severity='error')