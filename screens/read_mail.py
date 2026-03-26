from textual.screen import Screen
from textual.widgets import Static, Footer, Header, ListView, ListItem, Label
from textual.app import ComposeResult
from services.read_mail import read_mails
from screens.view_mail import ViewMail
from screens.mock_emails import mock_emails
from textual.containers import VerticalGroup, Vertical, Container, HorizontalScroll, HorizontalGroup
from textwrap import dedent

class MailRow(HorizontalGroup):
    def __init__(self, mail, index, **kwargs):
        super().__init__(**kwargs)
        self.mail = mail
        self.idx = index
    
    def compose(self) -> ComposeResult:
        yield Label(self.idx, classes="col no")
        yield Label(self.mail["sender"], classes="col sender")
        yield Label(self.mail["subject"], classes="col subject")
        yield Label(self.mail["date"], classes="col date")
        
class PreviewMail(VerticalGroup):
    def __init__(self, email, **kwargs):
        super().__init__(**kwargs)
        self.email = email
        
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Email Preview", id="title"),
            Container(
                Static(f"From   : {self.email['sender']}"),
                Static(f"Subject: {self.email['subject']}"),
                Static(f"Date   : {self.email['date']}"),
                id="metadata"
            ),
            Container(
                Static(self.email['body']),
                id='body'
            )
        )

class MailList(VerticalGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mails = mock_emails
        for mail in self.mails:
            mail['body'] = dedent(mail['body'])
    
    def on_mount(self):
        list_view = self.query_one("#mail_list", ListView)

        for i, mail in enumerate(self.mails):
            item = ListItem(MailRow(mail, str(i + 1)), id=f"email-{i}")
            list_view.append(item)
            
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Inbox\n", id="inbox"),
            MailRow(
                {"sender": "Sender", "subject": "Subject", "date": "Date"},
                index="S.no",
                id="header_row"
            ),
            ListView(id="mail_list")
        )

class ReadMail(Screen):
    CSS_PATH = "read_mail.tcss"
    BINDINGS = [
        ("p", "prev", "Back"),
        ("v", "preview", "Preview")
    ]
    
    def __init__(self):
        super().__init__()
        self.mails = mock_emails
    
    def on_mount(self):
        # sets the focus on mail list when we enter the screen
        list_view = self.query_one("#mail_list", ListView)
        self.set_focus(list_view)

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
    
    def action_preview(self) -> None:
        preview_mail = self.query_one(PreviewMail)
        mail_list = self.query_one(MailList)
        
        # shows preview mail pane
        preview_mail.toggle_class("show")
        
        # fixes styling of inbox
        mail_list.toggle_class("compact")
        

if __name__ == "__main__":
    mails = mock_emails
    print(len(mails))
    for mail in mails:
        print(f"id: {mail["id"]}")
        print(f"sender: {mail["sender"]}")
        print(f"subject: {mail["subject"]}")
        print(f"date: {mail["date"]}")
        print(f"body: {mail["body"]}")
        #print(f"attachment: {mail["attachments"]}")
        