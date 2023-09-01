from textual import on
from textual.app import ComposeResult
from textual.widgets import Static, Input, Button, Label, ProgressBar

SHOW = 'Show'
HIDE = "Hide"


class PasswordShowHide(Static):

    DEFAULT_CSS = """
    PasswordShowHide {
        layout: horizontal;
    }
    
    .input_label {
        margin-top: 1;
        width: auto;
        content-align: left middle;
    }
    
    .password_input {
        align: left middle;
        width: 80%;
    }
    
    .show_hide_button {
        width: 2%;
    }
    """

    def __init__(
            self,
            text: str,
            gap_size: int = 20,
            id: str | None = None,
            classes: str | None = None,
            name: str | None = None,
    ):
        super().__init__(id=id, classes=classes, name=name)
        self.text = text
        self.gap_size = gap_size

    def compose(self) -> ComposeResult:
        yield Label(f"{self.text:<{self.gap_size}}", classes="input_label")
        yield Input(password=True, classes="password_input")
        yield Button(SHOW, classes="show_hide_button")

    @on(Button.Pressed, ".show_hide_button")
    def show_hide_password(self, pressed: Button.Pressed):
        password_widget = self.query_one(".password_input")
        if pressed.button.label.plain == SHOW:
            pressed.button.label = HIDE
            password_widget.password = False
        else:
            pressed.button.label = SHOW
            password_widget.password = True


class PasswordStrength(Static):

    DEFAULT_CSS = """
    #password {
        width: 80%;
    }

    #password_strength_bar {
        margin: 0 1;
    }
    
    #password_strength_label {
        
    }
    """

    def __init__(self, strength=True):
        super().__init__()
        self.strength = strength

    def compose(self):
        yield ProgressBar(total=100, show_eta=False, show_percentage=True, id="password_strength_bar")
        yield Label("Weak", id="password_strength_label")
