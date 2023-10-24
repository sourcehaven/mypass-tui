from textual.widgets import Select

from mypass_tui.localization import get_language_codes


class LanguageSelect(Select):
    def __init__(self):
        codes = get_language_codes()
        super().__init__((code, code) for code in codes)

    def on_select_changed(self, changed: Select.Changed):
        changed.value
