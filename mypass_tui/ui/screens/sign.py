from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Footer, Label, TabbedContent, TabPane

from mypass_tui.exception.api import ApiException
from mypass_tui.exception.validator import RequiredException, ValidatorException

from mypass_tui.globals import i18n, bindings, set_user
from mypass_tui.localization import KEY_LABEL, KEY_BUTTON, KEY_TAB, KEY_TITLE, KEY_FOOTER, KEY_QUIT, KEY_SIGNIN, \
    KEY_SIGNUP
from mypass_tui.model.user import User, EMAIL, LASTNAME, FIRSTNAME, PASSWORD, USERNAME
from mypass_tui.ui.util.scrape import clear_inputs, scrape_inputs
from mypass_tui.ui.util.session import exit_app
from mypass_tui.ui.widgets import ButtonPair, EpicInput, Feedback, InputLabel, LabeledInput, Password, PasswordStrength


class SignScreen(Screen):
    BINDINGS = [
        Binding(bindings[KEY_SIGNIN], KEY_SIGNIN, i18n[KEY_FOOTER][KEY_SIGNIN], show=True),
        Binding(bindings[KEY_SIGNUP], KEY_SIGNUP, i18n[KEY_FOOTER][KEY_SIGNUP], show=True),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent(initial=KEY_SIGNIN, id="sign_tab"):
            with TabPane(i18n[KEY_TAB][KEY_SIGNIN], id="sign_in"):
                yield Label(i18n[KEY_TITLE][KEY_SIGNIN], classes="title")
                yield ScrollableContainer(
                    LabeledInput(
                        InputLabel(i18n[KEY_LABEL]["username"], required=True),
                        EpicInput(
                            id=f"{KEY_SIGNIN}_{USERNAME}", placeholder=i18n.placeholder(KEY_SIGNIN, USERNAME), classes="labeled_input"
                        ),
                    ),
                    LabeledInput(
                        InputLabel(i18n[KEY_LABEL]["password"], required=True),
                        Password(
                            id=f"{KEY_SIGNIN}_{PASSWORD}", placeholder=i18n.placeholder(KEY_SIGNIN, PASSWORD), classes="labeled_input"
                        ),
                    ),
                    id="signin_input_container",
                )
                yield ButtonPair(
                    left_text=i18n[KEY_BUTTON][KEY_SIGNIN],
                    right_text=i18n[KEY_BUTTON][KEY_QUIT],
                    left_callback=self.on_signin_pressed,
                    right_callback=self.on_exit_pressed,
                )
                yield Feedback(id="signin_feedback")
            with TabPane(i18n[KEY_TAB][KEY_SIGNUP], id="sign_up"):
                signup_pw_strength = PasswordStrength()
                yield Label(i18n[KEY_TITLE][KEY_SIGNUP], classes="title")
                yield ScrollableContainer(
                    LabeledInput(
                        InputLabel(i18n[KEY_LABEL]["username"], required=True),
                        EpicInput(
                            id=f"{KEY_SIGNUP}_{USERNAME}", placeholder=i18n.placeholder(KEY_SIGNUP, USERNAME), classes="labeled_input"
                        ),
                    ),
                    LabeledInput(
                        InputLabel(i18n[KEY_LABEL]["password"], required=True),
                        Password(
                            id=f"{KEY_SIGNUP}_{PASSWORD}",
                            placeholder=i18n.placeholder(KEY_SIGNUP, PASSWORD),
                            classes="labeled_input",
                            strength_bar=signup_pw_strength,
                        ),
                    ),
                    signup_pw_strength,
                    LabeledInput(
                        InputLabel(i18n[KEY_LABEL]["firstname"]),
                        EpicInput(
                            id=f"{KEY_SIGNUP}_{FIRSTNAME}", placeholder=i18n.placeholder(KEY_SIGNUP, FIRSTNAME), classes="labeled_input"
                        ),
                    ),
                    LabeledInput(
                        InputLabel(i18n[KEY_LABEL]["lastname"]),
                        EpicInput(
                            id=f"{KEY_SIGNUP}_{LASTNAME}", placeholder=i18n.placeholder(KEY_SIGNUP, LASTNAME), classes="labeled_input"
                        ),
                    ),
                    LabeledInput(
                        InputLabel(i18n[KEY_LABEL]["email"]),
                        EpicInput(id=f"{KEY_SIGNUP}_{EMAIL}", placeholder=i18n.placeholder(KEY_SIGNUP, EMAIL), classes="labeled_input"),
                    ),
                    id="signup_input_container",
                )
                yield ButtonPair(
                    left_text=i18n[KEY_BUTTON][KEY_SIGNUP],
                    right_text=i18n[KEY_BUTTON][KEY_QUIT],
                    left_callback=self.on_signup_pressed,
                    right_callback=self.on_exit_pressed,
                )
                yield Feedback(id="signup_feedback")
        yield Footer()

    def action_signin(self):
        self.query_one(TabbedContent).active = KEY_SIGNIN

    def action_signup(self):
        self.query_one(TabbedContent).active = KEY_SIGNUP

    @Feedback.on_error(ApiException, ValidatorException, selector="#signin_feedback")
    def on_signin_pressed(self, _: Button.Pressed):
        tab = self.screen.query_one("#signin_input_container")

        invalid_fields = LabeledInput.get_invalid_fields(tab)
        if invalid_fields:
            raise RequiredException(invalid_fields)
        else:
            inputs = {id.replace(KEY_SIGNIN + "_", ""): inp.value for id, inp in scrape_inputs(tab).items()}
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

            inputs = {id.replace(KEY_SIGNUP + "_", ""): inp.value for id, inp in scrape_inputs(tab).items()}
            clear_inputs(tab)
            user, token = User.registration(**inputs)
            set_user(user)

            self.app.push_screen(TokenScreen(token))

    def on_exit_pressed(self, _: Button.Pressed):
        exit_app(self.app)
