from textual.screen import Screen
from textual.widgets import Static, Footer, Header, ListView, ListItem, Label
from textual.app import ComposeResult
from services.read_mail import read_mails
from screens.view_mail import ViewMail

mock_emails = read_mails()

def format_row(no, sender, subject, date):
    no = no[:10].ljust(10)
    sender = sender[:25].ljust(25)
    subject = subject[:40].ljust(40)
    date = date[:16].ljust(16)
    return f"{no} | {sender} | {subject} | {date}"

class ReadMail(Screen):
    BINDINGS = [
        ("p", "prev", "Back")
    ]

    def compose(self) -> ComposeResult:
        items = []
        for i, email in enumerate(mock_emails):
            row = format_row(
                email["id"],
                email["sender"],
                email["subject"],
                email["date"]
            )

            items.append(
                ListItem(
                    Label(row),
                    id=f"email-{i}"
                )
            )
        
        header_row = format_row("S.No", "Sender", "Subject", "Date")
            
        yield Header()
        yield Static("Inbox\n")
        yield Static(header_row)
        yield Static("-" * len(header_row))
        yield ListView(*items)
        yield Footer()
        
    def action_prev(self) -> None:
        self.app.pop_screen()
        
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        idx = int(event.item.id.removeprefix("email-"))
        self.app.push_screen(ViewMail(mock_emails[idx]))
        