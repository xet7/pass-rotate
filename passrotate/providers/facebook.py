from passrotate.exceptions import PrepareException
from passrotate.provider import Provider, ProviderOption, register_provider
from passrotate.forms import get_form
import requests

class Facebook(Provider):
    """
    [facebook.com]
    username=Your Facebook username
    """
    name = "Facebook"
    domains = [
        "facebook.com",
    ]
    options = {
        "username": ProviderOption(str, "Your Facebook username")
    }

    def __init__(self, options):
        self.username = options["username"]

    def prepare(self, old_password):
        self._session = requests.Session()

        ###authenticate
        r = self._session.get("https://m.facebook.com/login.php")
        form = get_form(r.text, id="login_form")
        form.update({
            "email": self.username,
            "pass": old_password
            })
        r = self._session.post("https://m.facebook.com/login.php", data=form)

        ###check for authentication failure
        if "The email address that you&#039;ve entered doesn&#039;t match any account" in r.text:
            raise PrepareException("Facebook doesn't recognise this email")
        if "The password you entered is incorrect" in r.text:
            raise PrepareException("Incorrect password")

        ###load form
        r = self._session.get("https://m.facebook.com/settings/security/password/")
        self._form = get_form(r.text, method="post")

    def execute(self, old_password, new_password):
        self._form.update({
            "password_old" : old_password,
            "password_new" : new_password,
            "password_confirm" : new_password
            })
        r = self._session.post("https://m.facebook.com/password/change/", data=self._form)

register_provider(Facebook)
