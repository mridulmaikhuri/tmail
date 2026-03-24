from textual.app import App, ComposeResult
from textual.widgets import Static, OptionList, Footer, Header
from textual.widgets.option_list import Option
from screens.read_mail import ReadMail
from screens.send_mail import SendMail

class TmailApp(App):
    BINDINGS = [
        ("q", "quit_app", "Exit")
    ]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Use arrow keys to move, Enter to select\n")
        yield OptionList(
            Option("Unread mail", id="read"),
            Option("Send mail", id="send"),
            Option("Exit", id="exit"),
            id="menu"
        )
        yield Footer()
    
    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        option_id = event.option.id
        if option_id == "read":
            self.push_screen(ReadMail())
        elif option_id == "send":
            self.push_screen(SendMail()  )
        elif option_id == "exit":
            self.exit()
            
    def action_quit_app(self) -> None:
        self.exit()

if __name__ == "__main__":
    app = TmailApp()
    app.run()