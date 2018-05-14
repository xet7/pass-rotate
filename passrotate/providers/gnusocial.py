from passrotate.provider import Provider, ProviderOption, register_provider
from passrotate.forms import get_form
import requests

class GNUSocial(Provider):
    """
    username=Your GNU Social username
    base_url=The base URL of your GNU Social instance
    """
    name = "GNU Social"
    domains = []
    options = {
        "username": ProviderOption(str, "Your GNU Social username"),
        "base_url": ProviderOption(str, "The base URL of your GNU Social instance")
    }

    def __init__(self, options):
        self.username = options["username"]
        self.base_url = options["base_url"]
        self._login_url = self.base_url + "/main/login"
        self._password_change_url = self.base_url + "/settings/password"

    def _login(self, old_password):
        r = self._session.get(self._login_url)
        form = get_form(r.text, id="form_login")
        form.update({
            "nickname": self.username,
            "password": old_password
        })
        r = self._session.post(self._login_url, data=form)
        if r.status_code != 200:
            raise Exception("Unable to log into your GNU Social account with current password")
        return r

    def prepare(self, old_password):
        self._session = requests.Session()
        self._login(old_password)
        r = self._session.get(self._password_change_url)
        self._form = get_form(r.text, id="form_password")

    def execute(self, old_password, new_password):
        self._form.update({
            "oldpassword": old_password,
            "newpassword": new_password,
            "confirm": new_password
        })
        r = self._session.post(self._password_change_url, data=self._form)

register_provider(GNUSocial)
