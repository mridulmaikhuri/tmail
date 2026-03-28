from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Link
from textual.containers import Vertical, Container
from textual.app import ComposeResult

class ViewMail(Screen):
    CSS_PATH = "view_mail.tcss"
    BINDINGS = [
        ("p", "prev", "Back")
    ]
    
    def __init__(self, email):
        super().__init__()
        self.email = email
        
    def compose(self) -> ComposeResult:
        yield Header()
        
        yield Vertical(
            Static("📧 Email Viewer", id="title"),

            Container(
                Static(f"From   : {self.email['sender']}"),
                Static(f"Subject: {self.email['subject']}"),
                Static(f"Date   : {self.email['date']}"),
                id="metadata"
            ),

            Static(self.email['body'], id="body"),
            
            Link('Click to open mail in Browser or Press Enter', url=self.email['attachment'], tooltip='Click me', id='link'),

            id="mail-container"
        )
        
        yield Footer()
    
    def action_prev(self) -> None:
        self.app.pop_screen()