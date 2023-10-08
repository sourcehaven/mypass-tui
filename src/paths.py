from pathlib import Path

ROOT_PATH = Path.home().joinpath(".mypass", "tui")
SETTINGS_PATH = ROOT_PATH.joinpath("settings.json")
KEY_BINDINGS_PATH = ROOT_PATH.joinpath("key_bindings.json")
