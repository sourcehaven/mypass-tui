from typing import Any

import requests

from .vault_entry import VaultEntry
from .auth import BearerAuth
from .shared import join_auth_url, join_vault_url
from ..exception.api import ApiException
from ..utils.string import replace_empty_string_with_none


class User:
    def __init__(
        self,
        access_token: str,
        refresh_token: str,
        session: requests.Session,
    ):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self._session = session
        self.vault_entries = self.vault_read()

    def auth(self):
        return BearerAuth(self.access_token)

    @classmethod
    def login(cls, username: str, password: str):
        session = requests.Session()
        resp = session.post(url=join_auth_url("login"), json={"username": username, "password": password})
        if resp.status_code == 201:
            data = resp.json()
            return cls(**data, session=session)
        else:
            raise ApiException(resp.status_code, resp.json())

    @classmethod
    def registration(
        cls,
        username: str,
        password: str,
        email: str = None,
        firstname: str = None,
        lastname: str = None,
    ):
        session = requests.Session()
        resp = session.post(
            url=join_auth_url("registration"),
            json={
                "username": username,
                "password": password,
                "email": replace_empty_string_with_none(email),
                "firstname": replace_empty_string_with_none(firstname),
                "lastname": replace_empty_string_with_none(lastname),
            },
        )
        if resp.status_code == 201:
            data = resp.json()
            token: str = data["token"]
            return cls.login(username, password), token
        else:
            raise ApiException(resp.status_code, resp.json())

    def logout(self):
        resp = requests.delete(url=join_auth_url("logout"), auth=self.auth())

        if resp.status_code == 204:
            self._session.close()
        else:
            raise Exception(resp.json)

    def refresh(self) -> None:
        resp = requests.post(url=join_auth_url("refresh"), auth=self.auth())

        if resp.status_code == 201:
            data = resp.json()
            self.access_token = data["access_token"]
            self.refresh_token = data["refresh_token"]
        else:
            raise Exception(resp.json())

    @property
    def username(self):
        return self._session.cookies.get("username")

    @property
    def firstname(self):
        return self._session.cookies.get("firstname")

    @property
    def lastname(self):
        return self._session.cookies.get("lastname")

    @property
    def email(self):
        return self._session.cookies.get("email")

    def vault_add(self, entry: VaultEntry):
        resp = requests.post(url=join_vault_url("add"), json={"fields": entry.to_dict()}, auth=self.auth())

        if resp.status_code == 200:
            data = resp.json()["entry"]
            entry = VaultEntry.from_dict(data)
            self.vault_entries.append(entry)
        else:
            raise ValueError(resp.json())

    def vault_read(self) -> list[VaultEntry]:
        resp = requests.post(url=join_vault_url("select"), json={}, auth=self.auth())

        if resp.status_code == 200:
            data = resp.json()
            if not isinstance(data, list):
                data = [data]

            return [VaultEntry.from_dict(entry) for entry in data]
        else:
            raise Exception(resp.json())

    def vault_update(self, crit: dict[str, str], fields: dict[str, str]) -> dict[str, Any]:
        resp = requests.post(url=join_vault_url("update"), json={"crit": crit, "fields": fields}, auth=self.auth())

        if resp.status_code == 200:
            return resp.json()
        else:
            raise Exception(resp.json())

    def vault_delete(self, crit: dict[str, str]) -> dict[str, Any]:
        resp = requests.post(url=join_vault_url("delete"), json={"crit": crit}, auth=self.auth())

        if resp.status_code == 200:
            return resp.json()
        else:
            raise Exception(resp.json())
