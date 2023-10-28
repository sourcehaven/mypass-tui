import typing


class DefaultList(list):

    def __init__(self, args: typing.Iterable, default_value):
        super().__init__(args)
        self.default_value = default_value

