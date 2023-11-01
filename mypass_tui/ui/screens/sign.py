from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Footer, Label, TabbedContent, TabPane

from mypass_tui.exception.api import ApiException
from mypass_tui.exception.validator import RequiredException, ValidatorException

from mypass_tui.globals import i18n, bindings, set_user
from mypass_tui.localization import KEY_LABEL, KEY_BUTTON, KEY_TAB, KEY_TITLE, KEY_FOOTER, KEY_QUIT, KEY_SIGN_IN, \
    KEY_SIGN_UP
from mypass_tui.model.user import User, EMAIL, LASTNAME, FIRSTNAME, PASSWORD, USERNAME
from mypass_tui.ui.util.scrape import clear_inputs, scrape_inputs
from mypass_tui.ui.util.session import exit_app
from mypass_tui.ui.widgets import ButtonPair, EpicInput, Feedback, InputLabel, LabeledInput, Password, PasswordStrength


class SignScreen(Screen):
    BINDINGS = [
        Binding(bindings[KEY_SIGN_IN], KEY_SIGN_IN, i18n[KEY_FOOTER][KEY_SIGN_IN], show=True),
        Binding(bindings[KEY_SIGN_UP], KEY_SIGN_UP, i18n[KEY_FOOTER][KEY_SIGN_UP], show=True),
    ]

    def compose(self) -> ComposeResult:
        with TabbedContent(initial=KEY_SIGN_IN, id="sign_tab"):
            with TabPane(i18n[KEY_TAB][KEY_SIGN_IN], id="sign_in"):
                yield Label(i18n[KEY_TITLE][KEY_SIGN_IN], classes="title")
                yield ScrollableContainer(
                    LabeledInput(
                        InputLabel(i18n[KEY_LABEL]["username"], required=True),
                        EpicInput(
                            id=f"{KEY_SIGN_IN}_{USERNAME}", placeholder=i18n.placeholder(KEY_SIGN_IN, USERNAME), classes="labeled_input"
                        ),
                    ),
                    LabeledInput(
                        InputLabel(i18n[KEY_LABEL]["password"], required=True),
                        Password(
                            id=f"{KEY_SIGN_IN}_{PASSWORD}", placeholder=i18n.placeholder(KEY_SIGN_IN, PASSWORD), classes="labeled_input"
                        ),
                    ),
                    id="signin_input_container",
                )
                yield ButtonPair(
                    left_text=i18n[KEY_BUTTON][KEY_SIGN_IN],
                    right_text=i18n[KEY_BUTTON][KEY_QUIT],
                    left_callback=self.on_signin_pressed,
                    right_callback=self.on_exit_pressed,
                )
                yield Feedback(id="signin_feedback")
            with TabPane(i18n[KEY_TAB][KEY_SIGN_UP], id="sign_up"):
                signup_pw_strength = PasswordStrength()
                yield Label(i18n[KEY_TITLE][KEY_SIGN_UP], classes="title")
                yield ScrollableContainer(
                    LabeledInput(
                        InputLabel(i18n[KEY_LABEL]["username"], required=True),
                        EpicInput(
                            id=f"{KEY_SIGN_UP}_{USERNAME}", placeholder=i18n.placeholder(KEY_SIGN_UP, USERNAME), classes="labeled_input"
                        ),
                    ),
                    LabeledInput(
                        InputLabel(i18n[KEY_LABEL]["password"], required=True),
                        Password(
                            id=f"{KEY_SIGN_UP}_{PASSWORD}",
                            placeholder=i18n.placeholder(KEY_SIGN_UP, PASSWORD),
                            classes="labeled_input",
                            strength_bar=signup_pw_strength,
                        ),
                    ),
                    signup_pw_strength,
                    LabeledInput(
                        InputLabel(i18n[KEY_LABEL]["firstname"]),
                        EpicInput(
                            id=f"{KEY_SIGN_UP}_{FIRSTNAME}", placeholder=i18n.placeholder(KEY_SIGN_UP, FIRSTNAME), classes="labeled_input"
                        ),
                    ),
                    LabeledInput(
                        InputLabel(i18n[KEY_LABEL]["lastname"]),
                        EpicInput(
                            id=f"{KEY_SIGN_UP}_{LASTNAME}", placeholder=i18n.placeholder(KEY_SIGN_UP, LASTNAME), classes="labeled_input"
                        ),
                    ),
                    LabeledInput(
                        InputLabel(i18n[KEY_LABEL]["email"]),
                        EpicInput(id=f"{KEY_SIGN_UP}_{EMAIL}", placeholder=i18n.placeholder(KEY_SIGN_UP, EMAIL), classes="labeled_input"),
                    ),
                    id="signup_input_container",
                )
                yield ButtonPair(
                    left_text=i18n[KEY_BUTTON][KEY_SIGN_UP],
                    right_text=i18n[KEY_BUTTON][KEY_QUIT],
                    left_callback=self.on_signup_pressed,
                    right_callback=self.on_exit_pressed,
                )
                yield Feedback(id="signup_feedback")
        yield Footer()

    def action_signin(self):
        self.query_one(TabbedContent).active = KEY_SIGN_IN

    def action_signup(self):
        self.query_one(TabbedContent).active = KEY_SIGN_UP

    @Feedback.on_error(ApiException, ValidatorException, selector="#signin_feedback")
    def on_signin_pressed(self, _: Button.Pressed):
        tab = self.screen.query_one("#signin_input_container")

        invalid_fields = LabeledInput.get_invalid_fields(tab)
        if invalid_fields:
            raise RequiredException(invalid_fields)
        else:
            inputs = {id.replace(KEY_SIGN_IN + "_", ""): inp.value for id, inp in scrape_inputs(tab, password_value=True).items()}

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

            inputs = {id.replace(KEY_SIGN_UP + "_", ""): inp.value for id, inp in scrape_inputs(tab, password_value=True).items()}
            clear_inputs(tab)
            user, token = User.registration(**inputs)
            set_user(user)

            self.app.push_screen(TokenScreen(token))

    def on_exit_pressed(self, _: Button.Pressed):
        exit_app(self.app)
