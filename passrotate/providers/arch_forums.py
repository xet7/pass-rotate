from passrotate.provider import Provider, ProviderOption, register_provider
from passrotate.forms import get_form
import requests

class ArchForums(Provider):
    """
    [bbs.archlinux.org]
    username=Your Arch Forums username
    """
    name = "Arch Forums"
    domains = [
        "bbs.archlinux.org",
    ]
    options = {
        "username": ProviderOption(str, "Your Arch Forums username")
    }

    def __init__(self, options):
        self.username = options["username"]

    def _login(self, old_password):
        login_url = "https://bbs.archlinux.org/login.php?action=in"
        r = self._session.post(login_url, data={"req_username": self.username, "req_password": old_password})
        if r.status_code != 200:
            raise Exception("Unable to log into your Arch Forums account with current password")
        return r

    def prepare(self, old_password):
        self._session = requests.Session()
        self._login(old_password)
        self._extract_uid()
        password_change_url = "https://bbs.archlinux.org/profile.php?action=change_pass&id=" + self._uid
        r = self._session.get(password_change_url)
        self._form = get_form(r.text, id="edit-profile-form")

    def execute(self, old_password, new_password):
        post_url = "https://aur.archlinux.org/account/" + self.username + "/update"
        self._form.update({
            "P": new_password,
            "C": new_password
        })
        r = self._session.post(post_url, data=self._form)

    def _extract_uid(self):
        # TODO
        self._uid = str(116098)

register_provider(ArchForums)
