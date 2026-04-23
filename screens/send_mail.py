from textual.screen import Screen
from textual.widgets import Static, Footer, Header, Input, TextArea, Button
from textual.containers import Vertical, Container, Horizontal
from textual.app import ComposeResult
from services.send_mail import send_mail

class SendMail(Screen):
    CSS_PATH = "send_mail.tcss"
    BINDINGS = [
        ("p", "prev", "Back"),
        ("s", "send", "Send")
    ]
    
    def compose(self) -> ComposeResult:
        yield Header()

        yield Static("󰒊 Compose Mail", id="title")
        yield Container(
            Vertical(
                Container(
                    Static("TO", classes="label"),
                    Input(placeholder="recipient@example.com", id="to"),
                    classes="input-group",
                ),

                Container(
                    Static("SUBJECT", classes="label"),
                    Input(placeholder="Subject", id="subject"),
                    classes="input-group",
                ),

                Container(
                    Static("BODY", classes="label"),
                    TextArea(id="body"),
                    classes="input-group",
                ),

                Horizontal(
                    Button("Send", id="send", classes="btn-primary"),
                    Button("Cancel", id="cancel", classes="btn-secondary"),
                    id="buttons",
                ),

                id="compose-card",
            ),
            id="compose-wrapper",
        )

        yield Footer()
        
    def action_prev(self) -> None:
        self.app.pop_screen()
    
    def handle_send(self):
        to = self.query_one("#to", Input).value
        subject = self.query_one("#subject", Input).value
        body = self.query_one("#body", TextArea).text
        res, error = send_mail(to, subject, body)
        self.app.pop_screen()
        if (res):
            self.notify('Mail successfully sent')
        else:
            self.notify(f'Some error occured: {error}', severity='error')
    
    def action_send(self):
        self.handle_send()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "send":
            self.handle_send()
        elif event.button.id == "cancel":
            self.app.pop_screen()