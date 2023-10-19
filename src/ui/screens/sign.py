from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Label, TabbedContent, TabPane, Footer

from ..util.scrape import clear_inputs, scrape_inputs
from ..util.session import exit_app
from ..widgets.epic_input import EpicInput
from ..widgets.feedback import Feedback, show_feedback_on_error
from ..widgets.buttons import ButtonPair
from ..widgets.input_label import InputLabel, LabeledInput, get_invalid_fields
from ..widgets.password import Password, PasswordStrength

from ... import session
from ...exception.api import ApiException
from ...exception.validator import RequiredException, ValidatorException
from ...model.user import User
from ...settings import bindings


class SignScreen(Screen):

    BINDINGS = [
        Binding(bindings["sign_in"], "signin_tab", "Sign In", show=True),
        Binding(bindings["sign_up"], "signup_tab", "Sign Up", show=True),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="signin_tab", id="sign_tab"):
            with TabPane("Sign In", id="signin_tab"):
                yield Label("Sign In", classes="title")
                yield ScrollableContainer(
                    LabeledInput(
                        InputLabel("Username", required=True),
                        EpicInput(id="username", placeholder="signin_username", classes="labeled_input"),
                    ),
                    LabeledInput(
                        InputLabel("Password", required=True),
                        Password(id="password", placeholder="signin_password", classes="labeled_input"),
                    ),
                    id="signin_input_container"
                )
                yield ButtonPair(
                    left_text="Sign In",
                    right_text="Quit",
                    left_callback=self.on_signin_pressed,
                    right_callback=self.on_exit_pressed,
                )
                yield Feedback(id="signin_feedback")
            with TabPane("Sign Up", id="signup_tab"):
                signup_pw_strength = PasswordStrength()
                yield Label("Sign Up", classes="title")
                yield ScrollableContainer(
                    LabeledInput(
                        InputLabel("Username", required=True),
                        EpicInput(id="username", placeholder="signup_username", classes="labeled_input"),
                    ),
                    LabeledInput(
                        InputLabel("Password", required=True),
                        Password(id="password", placeholder="signup_password", classes="labeled_input", strength_bar=signup_pw_strength),
                    ),
                    signup_pw_strength,
                    LabeledInput(
                        InputLabel("First name"),
                        EpicInput(id="firstname", placeholder="signup_firstname", classes="labeled_input"),
                    ),
                    LabeledInput(
                        InputLabel("Last name"),
                        EpicInput(id="lastname", placeholder="signup_lastname", classes="labeled_input"),
                    ),
                    LabeledInput(
                        InputLabel("Email"),
                        EpicInput(id="email", placeholder="signup_email", classes="labeled_input"),
                    ),
                    id="signup_input_container"
                )
                yield ButtonPair(
                    left_text="Sign Up",
                    right_text="Quit",
                    left_callback=self.on_signup_pressed,
                    right_callback=self.on_exit_pressed,
                )
                yield Feedback(id="signup_feedback")
        yield Footer()

    def action_signin_tab(self):
        self.query_one(TabbedContent).active = "signin_tab"

    def action_signup_tab(self):
        self.query_one(TabbedContent).active = "signup_tab"

    @show_feedback_on_error(ApiException, ValidatorException, selector="#signin_feedback")
    def on_signin_pressed(self, _: Button.Pressed):
        tab = self.screen.query_one("#signin_input_container")

        invalid_fields = get_invalid_fields(tab)
        if invalid_fields:
            raise RequiredException(invalid_fields)
        else:
            inputs = {
                key: val
                for key, val in scrape_inputs(tab).items()
            }
            session.user = User.login(**inputs)

            from .main import MainScreen
            self.app.switch_screen(MainScreen())

    @show_feedback_on_error(ApiException, ValidatorException, selector="#signup_feedback")
    def on_signup_pressed(self, _: Button.Pressed):
        tab = self.screen.query_one("#signup_input_container")

        invalid_fields = get_invalid_fields(tab)
        if invalid_fields:
            raise RequiredException(invalid_fields)
        else:
            inputs = {
                key: val
                for key, val in scrape_inputs(tab).items()
            }
            clear_inputs(tab)
            session.user, token = User.registration(**inputs)

            from .token import TokenScreen
            self.app.push_screen(TokenScreen(token))

    def on_exit_pressed(self, _: Button.Pressed):
        exit_app(self.app)
