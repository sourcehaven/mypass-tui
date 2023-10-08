from urllib.parse import urljoin

_auth_url: str | None = None
_vault_url: str | None = None


def set_url(auth_url: str, vault_url: str):
    global _auth_url, _vault_url
    _auth_url = auth_url
    _vault_url = vault_url


def join_auth_url(endpoint: str):
    return urljoin(_auth_url, endpoint)


def join_vault_url(endpoint: str):
    return urljoin(_vault_url, endpoint)
