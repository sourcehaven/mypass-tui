from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Footer, Label, TabbedContent, TabPane

from mypass_tui import session
from mypass_tui.exception.api import ApiException
from mypass_tui.exception.validator import RequiredException, ValidatorException
from mypass_tui.localization import i18n
from mypass_tui.model.user import User
from mypass_tui.settings import bindings
from mypass_tui.ui.util.scrape import clear_inputs, scrape_inputs
from mypass_tui.ui.util.session import exit_app
from mypass_tui.ui.widgets import ButtonPair, EpicInput, Feedback, InputLabel, LabeledInput, Password, PasswordStrength


class SignScreen(Screen):
    BINDINGS = [
        Binding(bindings["sign_in"], "signin_tab", i18n.footer__sign_in, show=True),
        Binding(bindings["sign_up"], "signup_tab", i18n.footer__sign_up, show=True),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="signin_tab", id="sign_tab"):
            with TabPane(i18n.tab__sign_in, id="signin_tab"):
                yield Label(i18n.title__sign_in, classes="title")
                yield ScrollableContainer(
                    LabeledInput(
                        InputLabel(i18n.label__username, required=True),
                        EpicInput(
                            id="username", placeholder=i18n.placeholder__sign_in__username, classes="labeled_input"
                        ),
                    ),
                    LabeledInput(
                        InputLabel(i18n.label__password, required=True),
                        Password(
                            id="password", placeholder=i18n.placeholder__sign_in__password, classes="labeled_input"
                        ),
                    ),
                    id="signin_input_container",
                )
                yield ButtonPair(
                    left_text=i18n.button__sign_in,
                    right_text=i18n.button__quit,
                    left_callback=self.on_signin_pressed,
                    right_callback=self.on_exit_pressed,
                )
                yield Feedback(id="signin_feedback")
            with TabPane(i18n.tab__sign_up, id="signup_tab"):
                signup_pw_strength = PasswordStrength()
                yield Label(i18n.title__sign_up, classes="title")
                yield ScrollableContainer(
                    LabeledInput(
                        InputLabel(i18n.label__username, required=True),
                        EpicInput(
                            id="username", placeholder=i18n.placeholder__sign_up__username, classes="labeled_input"
                        ),
                    ),
                    LabeledInput(
                        InputLabel(i18n.label__password, required=True),
                        Password(
                            id="password",
                            placeholder=i18n.placeholder__sign_up__password,
                            classes="labeled_input",
                            strength_bar=signup_pw_strength,
                        ),
                    ),
                    signup_pw_strength,
                    LabeledInput(
                        InputLabel(i18n.label__first_name),
                        EpicInput(
                            id="firstname", placeholder=i18n.placeholder__sign_up__first_name, classes="labeled_input"
                        ),
                    ),
                    LabeledInput(
                        InputLabel(i18n.label__last_name),
                        EpicInput(
                            id="lastname", placeholder=i18n.placeholder__sign_up__last_name, classes="labeled_input"
                        ),
                    ),
                    LabeledInput(
                        InputLabel(i18n.label__email),
                        EpicInput(id="email", placeholder=i18n.placeholder__sign_up__email, classes="labeled_input"),
                    ),
                    id="signup_input_container",
                )
                yield ButtonPair(
                    left_text=i18n.button__sign_up,
                    right_text=i18n.button__quit,
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
            session.user = User.login(**inputs)

            from .main import MainScreen

            self.app.switch_screen(MainScreen())

    @Feedback.on_error(ApiException, ValidatorException, selector="#signup_feedback")
    def on_signup_pressed(self, _: Button.Pressed):
        tab = self.screen.query_one("#signup_input_container")

        invalid_fields = LabeledInput.get_invalid_fields(tab)
        if invalid_fields:
            raise RequiredException(invalid_fields)
        else:
            inputs = {key: val for key, val in scrape_inputs(tab).items()}
            clear_inputs(tab)
            session.user, token = User.registration(**inputs)

            from .token import TokenScreen

            self.app.push_screen(TokenScreen(token))

    def on_exit_pressed(self, _: Button.Pressed):
        exit_app(self.app)
