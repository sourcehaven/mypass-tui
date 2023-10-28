from datetime import datetime
from typing import Any, Final

from mypass_tui.model.input_info import InputInfo
from mypass_tui.model.password import Password
from mypass_tui.utils.string import split_path, to_string

ID: Final = "id"
PARENT_ID: Final = "parent_id"
USERNAME: Final = "username"
PASSWORD: Final = "password"
TITLE: Final = "title"
WEBSITE: Final = "website"
FOLDER: Final = "folder"
NOTES: Final = "notes"
TAGS: Final = "tags"
ACTIVE: Final = "active"
DELETED: Final = "deleted"
CREATED_AT: Final = "created_at"
DELETED_AT: Final = "deleted_at"


class VaultEntry:
    API_FIELDS = USERNAME, PASSWORD, TITLE, WEBSITE, FOLDER, NOTES, TAGS
    REQUIRED = True, True, False, False, False, False, False

    __slots__ = (
        ID,
        USERNAME,
        PASSWORD,
        TITLE,
        WEBSITE,
        FOLDER,
        NOTES,
        TAGS,
        PARENT_ID,
        ACTIVE,
        DELETED,
        CREATED_AT,
        DELETED_AT,
    )

    def __init__(
        self,
        id: int = None,
        username: str = None,
        password: Password = None,
        tags: list[str] = None,
        created_at: datetime = None,
        deleted_at: datetime = None,
        title: str = None,
        website: str = None,
        folder: str = None,
        notes: str = None,
        parent_id: int = None,
        active: bool = True,
        deleted: bool = False,
    ):
        self.id = id
        self.username = username
        self.password = password
        self.created_at = created_at
        self.deleted_at = deleted_at
        self.title = title
        self.website = website
        self.folder = folder
        self.notes = notes
        self.tags = tags
        self.parent_id = parent_id
        self.active = active
        self.deleted = deleted

    def update(self, dct: dict[str, Any]):
        self.username = dct.get(USERNAME, self.username)
        self.password = dct.get(PASSWORD, self.password)
        self.title = dct.get(TITLE, self.title)
        self.folder = dct.get(FOLDER, self.folder)
        self.notes = dct.get(NOTES, self.notes)
        self.tags = dct.get(TAGS, self.tags)

    def input_details(self, texts: str):
        return {
            id: InputInfo(text=text, value=val, required=req)
            for id, text, val, req
            in zip(VaultEntry.API_FIELDS, texts, self.values, VaultEntry.REQUIRED)
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any], date_format="%Y-%m-%dT%H:%M:%S", hide_password=True):
        created_at = data.pop(CREATED_AT, None)
        if created_at and isinstance(created_at, str):
            created_at = datetime.strptime(created_at, date_format)

        deleted_at = data.pop(DELETED_AT, None)
        if deleted_at and isinstance(deleted_at, str):
            deleted_at = datetime.strptime(deleted_at, date_format)

        password = data.pop(PASSWORD, None)
        if password and isinstance(password, str):
            password = Password(password, hide_password)

        return cls(**data, password=password, created_at=created_at, deleted_at=deleted_at)

    def to_dict(self, password_to_string=True, filter_empty=True) -> dict:
        dct = {field: value for field, value in zip(VaultEntry.API_FIELDS, self.values)}
        if password_to_string:
            dct[PASSWORD] = to_string(dct[PASSWORD])

        if filter_empty:
            dct = {key: val for key, val in dct.items() if val}
        return dct

    @property
    def values(self):
        return self.username, self.password, self.title, self.website, self.folder, self.notes, self.tags

    @property
    def row(self):
        return (
            self.username or "",
            self.password or "",
            self.title or "",
            self.website or "",
            self.folder or "",
            self.notes or "",
            ", ".join(self.tags),
        )

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"{ID}={self.id}, "
            f"{USERNAME}={self.username}, "
            f"{TITLE}={self.title}, "
            f"{WEBSITE}={self.website}, "
            f"{FOLDER}={self.folder}, "
            f"{NOTES}={self.notes}, "
            f"{TAGS}={self.tags})"
        )


def append_tree(root_node: list, entry: VaultEntry):
    i = 0
    split_folder = split_path(entry.folder)
    depth = len(split_folder)

    def build_tree(node: list):
        nonlocal i

        for e in node:
            if isinstance(e, tuple) and e[0] == split_folder[i]:
                next_node = e[1]
                break
        else:
            next_node = []
            node.append((split_folder[i], next_node))

        i += 1
        if i == depth:
            next_node.append(entry)

        while i < depth:
            build_tree(next_node)

    if depth == 0:
        root_node.append(entry)
    else:
        build_tree(root_node)
