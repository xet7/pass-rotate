import json

from passrotate.provider import Provider, ProviderOption, PromptType, register_provider
from passrotate.forms import get_form
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

class GitLab(Provider):
    """
    [gitlab.com]
    username=Your GitLab username
    """
    name = "GitLab"
    domains = [
        "gitlab.com",
    ]
    options = {
        "username": ProviderOption(str, "Your GitLab username")
    }

    def __init__(self, options):
        self.username = options["username"]

    def _read_userid(self):
        try:
            r = self._session.get("https://gitlab.com/api/v4/user")
            self.user_id = json.loads(r.text)["id"]
        except:
            raise Exception("Can't read user id from API")


    def _handle_two_factor_auth(self, r):
        soup = BeautifulSoup(r.text, "html5lib")

        # look for the OTP input field
        otp_input = soup.find("input", attrs={ 'id': 'user_otp_attempt' })

        # if we didn't find it its probably not enabled, great!
        if otp_input is None:
            return

        # else we ask the user to provide its token and send it
        code = self.prompt("Enter your two factor (TOTP) code", PromptType.totp)
        form = get_form(r.text)
        form.update({
            "user[otp_attempt]": code
        })
        r = self._session.post("https://gitlab.com/users/sign_in", data=form)
        if r.status_code != 200:
            raise Exception("Unable to login via OTP")


    def _login(self, old_password):
        r = self._session.get("https://gitlab.com/users/sign_in")
        form = get_form(r.text)
        form.update({
            "user[login]": self.username,
            "user[password]": old_password
        })
        r = self._session.post("https://gitlab.com/users/sign_in", data=form)
        if r.status_code != 200:
            raise Exception("Unable to log into GitLab account with current password")

        return r

    def _set_form(self):
        r = self._session.get("https://gitlab.com/profile/password/edit")
        self._form = get_form(r.text, id="edit_user_{}".format(self.user_id))

    def prepare(self, old_password):
        self._session = requests.Session()

        r = self._login(old_password)
        self._handle_two_factor_auth(r)
        self._read_userid()
        self._set_form()


    def execute(self, old_password, new_password):
        self._form.update({
            "user[current_password]": old_password,
            "user[password]": new_password,
            "user[password_confirmation]": new_password,
        })
        r = self._session.post("https://gitlab.com/profile/password", data=self._form)

register_provider(GitLab)
