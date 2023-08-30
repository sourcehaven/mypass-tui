from textual.widgets import Label, Static, Switch


class LabeledSwitch(Static):

    DEFAULT_CSS = """
    LabeledSwitch {
        layout: horizontal;
    }
    """

    def __init__(
            self,
            text: str,
            gap_size: int,
            id: str | None = None,
            classes: str | None = None,
            name: str | None = None,
    ):
        super().__init__(id=id, classes=classes, name=name)
        self.text = text
        self.gap_size = gap_size

    def compose(self):
        yield Label(f"{self.text:<{self.gap_size}}", classes="switch_label")
        yield Switch(animate=True, value=True, classes="labeled_switch")
