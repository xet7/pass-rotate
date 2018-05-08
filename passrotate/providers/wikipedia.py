from passrotate.provider import Provider, ProviderOption, register_provider
from passrotate.forms import get_form
import requests

class Wikipedia(Provider):
    """
    [wikipedia.org]
    username=Your Wikipedia username
    """
    name = "Wikipedia"
    domains = [
        "wikipedia.org",
    ]
    options = {
        "username": ProviderOption(str, "Your Wikipedia username")
    }
    _login_url = "https://en.wikipedia.org/w/index.php?title=Special:UserLogin"
    _password_change_url = "https://en.wikipedia.org/w/index.php?" \
                           "title=Special:ChangeCredentials" \
                           "/MediaWiki\Auth\PasswordAuthenticationRequest"

    def __init__(self, options):
        self.username = options["username"]

    def _login(self, old_password):
        r = self._session.get(self._login_url)
        form = get_form(r.text)
        form.update({
            "wpName": self.username,
            "wpPassword": old_password
        })
        r = self._session.post(self._login_url, data=form)
        if r.status_code != 200:
            raise Exception("Unable to log into Wikipedia account with current password")
        return r

    def prepare(self, old_password):
        self._session = requests.Session()
        self._login(old_password)
        r = self._session.get(self._password_change_url)
        self._form = get_form(r.text)

    def execute(self, old_password, new_password):
        self._form.update({
            "password": new_password,
            "retype": new_password
        })
        r = self._session.post(self._password_change_url, data=self._form)

register_provider(Wikipedia)
