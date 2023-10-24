from textual.widgets import Static


class Gap(Static):

    DEFAULT_CSS = """
    Gap {
        height: 1; 
    }
    """

    def __init__(self, height=1):
        super().__init__()
        self.height = height

    def on_mount(self):
        self.styles.height = self.height
