from textual.app import App, ComposeResult
from textual.widgets import Static, OptionList, Footer, Header
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets.option_list import Option
from screens.read_mail import ReadMail
from screens.send_mail import SendMail
from screens.mock_emails import mock_emails
from services.read_mail import read_mails

MENU_ITEMS = [
    ("read",  "󰇮",  "INBOX",   "Read your unread messages"),
    ("send",  "󰒊",  "COMPOSE", "Write a new message"),
    ("exit",  "󰈆",  "QUIT",    "Exit the application"),
]

class MenuItem(Static):
    def __init__(self, item_id, icon, title, desc, badge=""):
        super().__init__()
        self.item_id = item_id
        self.icon = icon
        self.title = title
        self.desc = desc
        self.badge = badge
        self.add_class("menu-item")
        
    def compose(self):
        yield Static(self.icon, classes='item-icon')
        with Static(classes='item-body'):
            yield Static(self.title, classes='item-title')
            yield Static(self.desc, classes='item-desc')
        yield Static(self.badge, classes='item-badge')
    
    # handles mouse click to select any option
    def on_click(self):
        self.app.handle_menu(self.item_id)

class TmailApp(App):
    CSS_PATH = 'app.tcss'
    BINDINGS = [
        ("q", "quit_app", "Exit"),
        ("up", "move_up", "Up"),
        ("down", "move_down", "Down"),
        ("enter", "select", "Select"),
    ]
    
    selected_index: reactive[int] = reactive(0)
    
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
  
        mail_count = len(self.mails)
        badges = [f'[{mail_count} new]', '', '']
        
        with Container(id='menu-container'):
            for i, (item_id, icon, title, desc) in enumerate(MENU_ITEMS):
                yield MenuItem(item_id, icon, title, desc, badges[i])
            
        yield Footer()
    
    def on_mount(self):
        self._update_focus()

    def _update_focus(self):
        widgets = self.query('.menu-item')
        for i, widget in enumerate(widgets):
            if i == self.selected_index:
                widget.add_class('focused')
            else:
                widget.remove_class('focused')
    
    def watch_selected_index(self, idx):
        self._update_focus()
    
    def action_move_up(self):
        self.selected_index = (self.selected_index - 1) % len(MENU_ITEMS)

    def action_move_down(self):
        self.selected_index = (self.selected_index + 1) % len(MENU_ITEMS)

    # handle enter click on focused option
    def action_select(self):
        item_id = MENU_ITEMS[self.selected_index][0]
        self.handle_menu(item_id)
        
    def handle_menu(self, item_id: str) -> None:
        if item_id == "read":
            self.push_screen(ReadMail(self.mails))
        elif item_id == "send":
            self.push_screen(SendMail())
        elif item_id == "exit":
            self.exit()
            
    def action_quit_app(self) -> None:
        self.exit()

if __name__ == "__main__":
    app = TmailApp()
    app.run()