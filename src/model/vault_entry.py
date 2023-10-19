from datetime import datetime
from typing import Any

from .folder import Folder
from ..model.password import Password
from ..utils.string import to_string


class VaultEntry:
    FIELDS = "username", "password", "title", "website", "folder", "notes", "tags"
    REQUIRED = True, True, False, False, False, False, False

    __slots__ = (
        "id",
        "username",
        "password",
        "title",
        "website",
        "folder",
        "notes",
        "tags",
        "parent_id",
        "active",
        "deleted",
        "created_at",
        "deleted_at",
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
        folder: Folder = None,
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

    @classmethod
    def from_dict(cls, data: dict[str, Any], date_format="%Y-%m-%dT%H:%M:%S", hide_password=True):
        created_at = data.pop("created_at", None)
        if created_at and isinstance(created_at, str):
            created_at = datetime.strptime(created_at, date_format)

        deleted_at = data.pop("deleted_at", None)
        if deleted_at and isinstance(deleted_at, str):
            deleted_at = datetime.strptime(deleted_at, date_format)

        password = data.pop("password", None)
        if password and isinstance(password, str):
            password = Password(password, hide_password)

        return cls(**data, password=password, created_at=created_at, deleted_at=deleted_at)

    def to_dict(self, password_to_string=True, filter_empty=True) -> dict:
        dct = {
            field: value
            for field, value in zip(VaultEntry.FIELDS, self.values)
        }
        if password_to_string:
            dct['password'] = to_string(dct['password'])

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
            ", ".join(self.tags)
        )

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"username={self.username}, "
            f"title={self.title}, "
            f"website={self.website}, "
            f"folder={self.folder}, "
            f"notes={self.notes}, "
            f"tags={self.tags})"
        )
