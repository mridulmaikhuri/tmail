from textual.screen import Screen
from textual.widgets import Static, Footer, Header, Input, TextArea, Button
from textual.containers import Vertical, Container, Horizontal
from textual.app import ComposeResult
from services.send_mail import send_mail

class SendMail(Screen):
    CSS_PATH = "send_mail.tcss"
    BINDINGS = [
        ("p", "prev", "Back")
    ]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("✉️ Compose Mail", id="title"),
            Container(
                Static("To:"),
                Input(placeholder="recipient@example.com",id="to"),
                id="to-container"
            ),
            Container(
                Static("Subject:"),
                Input(placeholder="Subject",id="subject"),
                id="subject-container"
            ),
            Static("Body:", id="body-heading"),
            TextArea(id="body"),
            Horizontal(
                Button("Send", id="send", variant="success"),
                Button("Cancel", id="cancel", variant="error"),
                id="buttons"
            ),
            id="compose-container"
        )
        yield Footer()
        
    def action_prev(self) -> None:
        self.app.pop_screen()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "send":
            to = self.query_one("#to", Input).value
            subject = self.query_one("#subject", Input).value
            body = self.query_one("#body", TextArea).text
            send_mail(to, subject, body)
            self.app.pop_screen()
        elif event.button.id == "cancel":
            self.app.pop_screen()