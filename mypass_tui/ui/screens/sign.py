from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Footer, Label, TabbedContent, TabPane

from mypass_tui.exception.api import ApiException
from mypass_tui.exception.validator import RequiredException, ValidatorException

from mypass_tui.globals import i18n, bindings, set_user
from mypass_tui.model.user import User, EMAIL, LASTNAME, FIRSTNAME, PASSWORD, USERNAME
from mypass_tui.ui.util.scrape import clear_inputs, scrape_inputs
from mypass_tui.ui.util.session import exit_app
from mypass_tui.ui.widgets import ButtonPair, EpicInput, Feedback, InputLabel, LabeledInput, Password, PasswordStrength


class SignScreen(Screen):
    BINDINGS = [
        Binding(bindings["sign_in"], "signin_tab", i18n["footer"]["sign_in"], show=True),
        Binding(bindings["sign_up"], "signup_tab", i18n["footer"]["sign_up"], show=True),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="signin_tab", id="sign_tab"):
            with TabPane(i18n["tab"]["sign_in"], id="signin_tab"):
                yield Label(i18n["title"]["sign_in"], classes="title")
                yield ScrollableContainer(
                    LabeledInput(
                        InputLabel(i18n["label"]["username"], required=True),
                        EpicInput(
                            id=USERNAME, placeholder=i18n.placeholder("sign_in", "username"), classes="labeled_input"
                        ),
                    ),
                    LabeledInput(
                        InputLabel(i18n["label"]["password"], required=True),
                        Password(
                            id=PASSWORD, placeholder=i18n.placeholder("sign_in", "password"), classes="labeled_input"
                        ),
                    ),
                    id="signin_input_container",
                )
                yield ButtonPair(
                    left_text=i18n["button"]["sign_in"],
                    right_text=i18n["button"]["quit"],
                    left_callback=self.on_signin_pressed,
                    right_callback=self.on_exit_pressed,
                )
                yield Feedback(id="signin_feedback")
            with TabPane(i18n["tab"]["sign_up"], id="signup_tab"):
                signup_pw_strength = PasswordStrength()
                yield Label(i18n["title"]["sign_up"], classes="title")
                yield ScrollableContainer(
                    LabeledInput(
                        InputLabel(i18n["label"]["username"], required=True),
                        EpicInput(
                            id=USERNAME, placeholder=i18n.placeholder("sign_up", "username"), classes="labeled_input"
                        ),
                    ),
                    LabeledInput(
                        InputLabel(i18n["label"]["password"], required=True),
                        Password(
                            id=PASSWORD,
                            placeholder=i18n.placeholder("sign_up", "password"),
                            classes="labeled_input",
                            strength_bar=signup_pw_strength,
                        ),
                    ),
                    signup_pw_strength,
                    LabeledInput(
                        InputLabel(i18n["label"]["firstname"]),
                        EpicInput(
                            id=FIRSTNAME, placeholder=i18n.placeholder("sign_up", "firstname"), classes="labeled_input"
                        ),
                    ),
                    LabeledInput(
                        InputLabel(i18n["label"]["lastname"]),
                        EpicInput(
                            id=LASTNAME, placeholder=i18n.placeholder("sign_up", "lastname"), classes="labeled_input"
                        ),
                    ),
                    LabeledInput(
                        InputLabel(i18n["label"]["email"]),
                        EpicInput(id=EMAIL, placeholder=i18n.placeholder("sign_up", "email"), classes="labeled_input"),
                    ),
                    id="signup_input_container",
                )
                yield ButtonPair(
                    left_text=i18n["button"]["sign_up"],
                    right_text=i18n["button"]["quit"],
                    left_callback=self.on_signup_pressed,
                    right_callback=self.on_exit_pressed,
                )
                yield Feedback(id="signup_feedback")
        yield Footer()

    def action_signin_tab(self):
        self.query_one(TabbedContent).active = "signin_tab"

    def action_signup_tab(self):
        self.query_one(TabbedContent).active = "signup_tab"

    @Feedback.on_error(ApiException, ValidatorException, selector="#signin_feedback")
    def on_signin_pressed(self, _: Button.Pressed):
        tab = self.screen.query_one("#signin_input_container")

        invalid_fields = LabeledInput.get_invalid_fields(tab)
        if invalid_fields:
            raise RequiredException(invalid_fields)
        else:
            inputs = {key: val for key, val in scrape_inputs(tab).items()}
            user = User.login(**inputs)
            set_user(user)

            from .main import MainScreen

            self.app.switch_screen(MainScreen())

    @Feedback.on_error(ApiException, ValidatorException, selector="#signup_feedback")
    def on_signup_pressed(self, _: Button.Pressed):
        tab = self.screen.query_one("#signup_input_container")

        invalid_fields = LabeledInput.get_invalid_fields(tab)
        if invalid_fields:
            raise RequiredException(invalid_fields)
        else:
            from .token import TokenScreen

            inputs = {key: val for key, val in scrape_inputs(tab).items()}
            clear_inputs(tab)
            user, token = User.registration(**inputs)
            set_user(user)

            self.app.push_screen(TokenScreen(token))

    def on_exit_pressed(self, _: Button.Pressed):
        exit_app(self.app)
