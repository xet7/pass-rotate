from passrotate.exceptions import PrepareException, ExecuteException
from passrotate.provider import Provider, ProviderOption, register_provider
from passrotate.forms import get_form
import requests


class AnkiWeb(Provider):
    """
    [ankiweb.net]
    username=Your AnkiWeb username (email)
    """
    name = "AnkiWeb"
    domains = [
        "ankiweb.net",
    ]
    options = {
        "username": ProviderOption(str, "Your AnkiWeb username")
    }

    def __init__(self, options):
        self.username = options["username"]

    def prepare(self, old_password):
        self._session = requests.Session()
        r = self._session.get("https://ankiweb.net/account/login")
        self._form = get_form(r.text, id="form")
        self._form.update({
            "username": self.username,
            "password": old_password
        })
        r = self._session.post("https://ankiweb.net/account/login",
                               data=self._form, allow_redirects=False)
        if not r.ok or r.status_code != 302:
            raise PrepareException("Unable to log into AnkiWeb with current password")
        r = self._session.get("https://ankiweb.net/account/settings")
        self._form = get_form(r.text)

    def execute(self, old_password, new_password):
        self._form.update({
            "oldpw": old_password,
            "pass1": new_password,
            "pass2": new_password
        })
        r = self._session.post("https://ankiweb.net/account/settings",
                               data=self._form, allow_redirects=False)
        if not r.ok or r.status_code != 302:
            raise ExecuteException("Failed to update AnkiWeb password")


register_provider(AnkiWeb)
