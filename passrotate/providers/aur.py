from passrotate.provider import Provider, ProviderOption, register_provider
from passrotate.forms import get_form
import requests

class ArchUserRepository(Provider):
    """
    [aur.archlinux.org]
    username=Your Arch User Repository username
    """
    name = "Arch User Repository"
    domains = [
        "aur.archlinux.org",
    ]
    options = {
        "username": ProviderOption(str, "Your Arch User Repository username")
    }

    def __init__(self, options):
        self.username = options["username"]

    def _login(self, old_password):
        login_url = "https://aur.archlinux.org/login/"
        r = self._session.post(login_url, data={"user": self.username, "passwd": old_password})
        if r.status_code != 200:
            raise Exception("Unable to log into your Arch User Repository account with current password")
        return r

    def prepare(self, old_password):
        self._session = requests.Session()
        self._login(old_password)
        password_change_url = "https://aur.archlinux.org/account/" + self.username + "/edit"
        r = self._session.get(password_change_url)
        self._form = get_form(r.text, id="edit-profile-form")

    def execute(self, old_password, new_password):
        post_url = "https://aur.archlinux.org/account/" + self.username + "/update"
        self._form.update({
            "P": new_password,
            "C": new_password
        })
        r = self._session.post(post_url, data=self._form)

register_provider(ArchUserRepository)
