from textual.screen import Screen
from textual.widgets import Static, Footer, Header, ListView, ListItem, Label
from textual.app import ComposeResult
from services.read_mail import read_mails
from screens.view_mail import ViewMail
from screens.mock_emails import mock_emails
from textual.containers import VerticalGroup, Vertical, Container, HorizontalScroll

def format_row(no, sender, subject, date):
    no = no[:4].replace('[', '(').replace(']', ')').ljust(4)
    sender = sender[:18].replace('[', '(').replace(']', ')').ljust(18)
    subject = subject[:25].replace('[', '(').replace(']', ')').ljust(25)
    date = date[:10].replace('[', '(').replace(']', ')').ljust(10)
    return f"{no} | {sender} | {subject} | {date}"

class PreviewMail(VerticalGroup):
    def __init__(self, email):
        super().__init__()
        self.email = email
        
    def compose(self) -> ComposeResult:
        yield Vertical(
            Container(
                Static(f"From   : {self.email['sender']}"),
                Static(f"Subject: {self.email['subject']}"),
                Static(f"Date   : {self.email['date']}"),
                id="metadata"
            ),
            Container(
                Static(self.email['body'])
            )
        )

class MailList(VerticalGroup):
    def __init__(self):
        super().__init__()
        self.mails = mock_emails
    
    def on_mount(self):
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
        yield Vertical(
            Static("Inbox\n", id="inbox"),
            Static(
                format_row("S.no", "Sender", "Subject", "Date"),
                id="header_row"
            ),
            ListView(id="mail_list")
        )

class ReadMail(Screen):
    CSS_PATH = "read_mail.tcss"
    BINDINGS = [
        ("p", "prev", "Back")
    ]
    
    def __init__(self):
        super().__init__()
        self.mails = mock_emails
    
    def on_mount(self):
        mailList = self.query_one(MailList)
        self.set_focus(mailList)
    
    # def on_mount(self):
    #     list_view = self.query_one("#mail_list", ListView)

    #     for i, mail in enumerate(self.mails):
    #         row = format_row(
    #             str(i + 1),
    #             mail["sender"],
    #             mail["subject"],
    #             mail["date"]
    #         )
    #         list_view.append(ListItem(Label(row), id=f"email-{i}"))

    def compose(self) -> ComposeResult:
        yield Header()
        yield HorizontalScroll(
            MailList(),
            PreviewMail(self.mails[0]),
        )
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
        