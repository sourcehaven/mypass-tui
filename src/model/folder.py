
class Folder:
    def __init__(self, path: str):
        self.path = path

    @property
    def parts(self):
        return [value for value in self.path.split("/") if value]

    @property
    def parent(self):
        path = "/".join(self.parts[:-1])
        if path:
            return Folder(path)
        else:
            raise ValueError(f"There are no parent for {self!r} because it is the root!")

    def __len__(self):
        return len(self.parts)

    def __str__(self):
        return self.path

    def __repr__(self):
        return f"{self.__class__.__name__}({self.path!r})"
