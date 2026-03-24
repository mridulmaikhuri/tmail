from textual.screen import Screen
from textual.widgets import Static, Footer, Header, ListView, ListItem, Label
from textual.app import ComposeResult
from services.read_mail import read_mails
from screens.view_mail import ViewMail

def format_row(no, sender, subject, date):
    no = no[:10].strip().ljust(10)
    sender = sender[:25].strip().ljust(25)
    subject = subject[:40].strip().ljust(40)
    date = date[:16].strip().ljust(16)
    return f"{no} | {sender} | {subject} | {date}"

class ReadMail(Screen):
    CSS_PATH = "read_mail.tcss"
    BINDINGS = [
        ("p", "prev", "Back")
    ]
    
    def __init__(self):
        super().__init__()
        self.mails = []
    
    def on_mount(self):
        self.mails = read_mails()
        list_view = self.query_one("#mail_list", ListView)

        for i, mail in enumerate(self.mails):
            row = format_row(
                str(i + 1),
                mail["sender"],
                mail["subject"],
                mail["date"]
            )
            list_view.append(ListItem(Label(row), id=f"email-{i}"))

    def compose(self) -> ComposeResult:
        header_row = format_row("S.No", "Sender", "Subject", "Date")
            
        yield Header()
        yield Static("Inbox\n")
        yield Static(header_row)
        yield Static("-" * len(header_row))
        yield ListView(id="mail_list")
        yield Footer()
        
    def action_prev(self) -> None:
        self.app.pop_screen()
        
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        idx = int(event.item.id.removeprefix("email-"))
        self.app.push_screen(ViewMail(self.mails[idx]))

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
        