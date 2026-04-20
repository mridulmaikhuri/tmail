from textual.app import App, ComposeResult
from textual.widgets import Static, OptionList, Footer, Header
from textual.containers import Container
from textual.widgets.option_list import Option
from screens.read_mail import ReadMail
from screens.send_mail import SendMail
from screens.mock_emails import mock_emails
from services.read_mail import read_mails
from textwrap import dedent

class TmailApp(App):
    CSS_PATH = 'app.tcss'
    BINDINGS = [
        ("q", "quit_app", "Exit")
    ]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.mails = mock_emails
        # for mail in self.mails:
        #     mail['body'] = dedent(mail['body'])
        self.mails = read_mails()
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(
            "████████╗███╗   ███╗ █████╗ ██╗██╗      \n"
            "╚══██╔══╝████╗ ████║██╔══██╗██║██║      \n"
            "   ██║   ██╔████╔██║███████║██║██║      \n"
            "   ██║   ██║╚██╔╝██║██╔══██║██║██║      \n"
            "   ██║   ██║ ╚═╝ ██║██║  ██║██║███████╗ \n"
            "   ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝",
            id="brand",
        )
        yield Static("Use arrow keys to move, Enter to select\n", id = "subtitle")
        yield Container(
            OptionList(
                Option(f"Unread Mails ({len(self.mails)})", id="read"),
                Option("Send Mail", id="send"),
                Option("Exit", id="exit"),
                id="menu"
            ),
            id='menu-container'
        )
        yield Footer()
    
    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        option_id = event.option.id
        if option_id == "read":
            self.push_screen(ReadMail(self.mails))
        elif option_id == "send":
            self.push_screen(SendMail())
        elif option_id == "exit":
            self.exit()
            
    def action_quit_app(self) -> None:
        self.exit()

if __name__ == "__main__":
    app = TmailApp()
    app.run()