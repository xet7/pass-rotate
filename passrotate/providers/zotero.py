from passrotate.exceptions import PrepareException, ExecuteException
from passrotate.provider import Provider, ProviderOption, register_provider
import requests


class Zotero(Provider):
    """
    [zotero.org]
    username=Your Zotero username
    """
    name = "Zotero"
    domains = [
        "zotero.org",
        "www.zotero.org"
    ]
    options = {
        "username": ProviderOption(str, "Your Zotero username")
    }

    def __init__(self, options):
        self.username = options["username"]

    def prepare(self, old_password):
        self._session = requests.Session()
        self._session.get("https://www.zotero.org/user/login")
        r = self._session.post("https://www.zotero.org/user/login", data={
            "username": self.username,
            "password": old_password,
            "remember": 0,
            "login": "",
            "oid_identifier": ""
        })
        if "Invalid credentials provided" in r.text:
            raise PrepareException("Unable to log into Zotero with current password")
        r = self._session.get("https://www.zotero.org/settings/account")

    def execute(self, old_password, new_password):
        form_data = {
            "password": old_password,
            "new_password": new_password,
            "new_password2": new_password,
            "updatesettings": ""
        }
        r = self._session.post(
            "https://www.zotero.org/settings/account",
            data=form_data, allow_redirects=False
        )
        if "Account Settings Saved" not in r.text:
            raise ExecuteException("Failed to update Zotero password")


register_provider(Zotero)
