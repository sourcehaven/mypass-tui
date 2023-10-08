class ApiException(Exception):
    def __init__(self, code: int, details: dict[str, str | bool]):
        self.code: int = code
        self.err: str = details.get("err")
        self.msg: str = details.get("msg")
        self.dtm: str = details.get("dtm")
        super().__init__(self.msg)
