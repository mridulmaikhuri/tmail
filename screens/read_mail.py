from textual.screen import Screen
from textual.widgets import Static, Footer, Header, ListView, ListItem, Label
from textual.app import ComposeResult
from screens.view_mail import ViewMail
from textual.containers import VerticalGroup, Vertical, Container, HorizontalScroll, HorizontalGroup, VerticalScroll
from services.read_mail import mark_as_read

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
    def __init__(self, mail, **kwargs):
        super().__init__(**kwargs)
        self.mail = mail
        
    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Static("Email Preview", id="title")
            yield Container(
                Static(f"From   :", id="from"),
                Static(f"Subject:", id="subject"),
                Static(f"Date   :", id="date"),
                id="metadata"
            )
            yield Container(
                Static(id='body'),
                id='body-container'
            )
        
    
    def update_mail(self, mail):
        self.mail = mail
        
        self.query_one("#from").update(f"From   : {self.mail['sender']}")
        self.query_one("#subject").update(f"Subject: {self.mail['subject']}")
        self.query_one("#date").update(f"Date   : {self.mail['date']}")
        self.query_one("#body").update(self.mail["body"])
        
        self.refresh()

class MailList(VerticalGroup):
    def __init__(self, mails, **kwargs):
        super().__init__(**kwargs)
        self.mails = mails
    
    def on_mount(self):
        list_view = self.query_one("#mail_list", ListView)

        for i, mail in enumerate(self.mails):
            item = ListItem(MailRow(mail, str(i + 1)), id=f"mail-{i}")
            item.mail = mail
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
    
    def renumber(self, mail):
        self.mails.remove(mail)
        list_view = self.query_one('#mail_list', ListView)
        for i, item in enumerate(list_view.children):
            row = item.query_one(MailRow)
            row.query_one('.no').update(str(i + 1))
    
    def on_screen_resume(self) -> None:
        self.refresh_data()

class ReadMail(Screen):
    CSS_PATH = "read_mail.tcss"
    BINDINGS = [
        ("p", "prev", "Back"),
        ("v", "preview", "Preview")
    ]
    
    def __init__(self, mails):
        super().__init__()
        self.mails = mails
    
    def on_mount(self):
        # sets the focus on mail list when we enter the screen
        list_view = self.query_one("#mail_list", ListView)
        self.set_focus(list_view)
    
    def on_show(self) -> None:
        # Clear any lingering styles from ViewMail screen
        body = self.query_one("#body", Static)
        body.set_styles("border: none; padding: 0; margin: 0;background: transparent;")

    def compose(self) -> ComposeResult:
        yield Header()
        yield HorizontalScroll(
            MailList(self.mails),
            PreviewMail(mail=None, id="preview"),
        )
        yield Footer()
        
    def action_prev(self) -> None:
        self.app.pop_screen()
        
    async def mark_read_worker(self, msg_id):
        mark_as_read(msg_id)
        
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        mail = event.item.mail
        
        self.app.push_screen(ViewMail(mail))
        
        preview_mail = self.query_one(PreviewMail)
        mail_list = self.query_one(MailList)
        
        #sets the preview mail to no mail
        new_mail = {
            "id": '',
            "sender": '',
            "subject": '',
            "date": '',
            "body": '',
            "attachments": '',
            "link": ''
        }
        preview_mail.update_mail(new_mail)
        
        if preview_mail.has_class("show"):
            preview_mail.toggle_class("show")
            mail_list.toggle_class("compact")
        
        msg_id = mail.get('id')
        msg_id and self.run_worker(self.mark_read_worker(msg_id))
        
        event.item.remove()
        mail_list.renumber(mail)
    
    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        idx = int(event.item.id.removeprefix("mail-"))
        mail = self.mails[idx]
        
        preview = self.query_one("#preview")
        preview.update_mail(mail)
    
    def action_preview(self) -> None:
        preview_mail = self.query_one(PreviewMail)
        mail_list = self.query_one(MailList)
        
        # shows preview mail pane
        preview_mail.toggle_class("show")
        
        # fixes styling of inbox
        mail_list.toggle_class("compact")
        