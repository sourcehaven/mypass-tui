from textual.events import Key
from textual.widgets import TextArea


class DynamicTextArea(TextArea):
    DEFAULT_CSS = """
    DynamicTextArea {   
        width: 1fr;
        height: 1;
    }
    """

    def on_mount(self):
        self.styles.height = self.document.line_count

    def on_key(self, key: Key):
        line_count = self.document.line_count
        if key.name == "enter":
            self.styles.height = line_count + 1
        elif key.name == "backspace":
            x, y = self.cursor_location
            if x == 0:
                return
            elif y > 0:
                self.styles.height = line_count
            else:
                self.styles.height = line_count - 1
