from textual.screen import Screen
from textual.widgets import Header, Footer, Static, RichLog
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

            RichLog(id="body"),

            id="mail-container"
        )
        
        yield Footer()
    
    def on_mount(self, event):
        body = self.query_one("#body", RichLog)
        body.write(self.email["body"])
    
    def action_prev(self) -> None:
        self.app.pop_screen()