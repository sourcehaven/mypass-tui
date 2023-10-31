from pathlib import Path

USER_PATH = Path.home().joinpath(".mypass", "tui")
SETTINGS_PATH = USER_PATH.joinpath("settings.json")
KEY_BINDINGS_PATH = USER_PATH.joinpath("key_bindings.json")

SOURCE_CODE_PATH = Path(__file__).resolve().parent
MAIN_PATH = SOURCE_CODE_PATH.joinpath("main.py")
PROJECT_PATH = SOURCE_CODE_PATH.parent
ASSETS_PATH = PROJECT_PATH.joinpath("assets")
I18N_PATH = ASSETS_PATH.joinpath("i18n")
