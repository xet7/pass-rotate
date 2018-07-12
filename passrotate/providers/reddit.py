from passrotate.provider import Provider, ProviderOption, PromptType, register_provider
from passrotate.forms import get_form
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

class Reddit(Provider):
    """
    [reddit.com]
    username=Your Reddit username
    """
    name = "Reddit"
    domains = [
        "reddit.com",
    ]
    options = {
        "username": ProviderOption(str, "Your Reddit username")
    }

    def __init__(self, options):
        self.username = options["username"]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"  # lol
        }

    def prepare(self, old_password):
        self._session = requests.Session()

        r = self._session.get("https://old.reddit.com/login", headers=self.headers)
        form = get_form(r.text, id="login-form")
        form.update({
            "user": self.username,
            "passwd": old_password,
            "api_type": "json",
            "dest": "https://old.reddit.com/prefs/update/",
        })

        r = self._session.post("https://old.reddit.com/api/login/{}".format(self.username), data=form, headers=self.headers)
        if r.status_code != 200:
            raise Exception("Unable to log into Reddit with current password")

    def execute(self, old_password, new_password):
        r = self._session.get("https://old.reddit.com/prefs/update/", headers=self.headers)

        soup = BeautifulSoup(r.text, "html5lib")
        uh = soup.find("input", {"name": "uh"})["value"]

        form = get_form(r.text, id="pref-update-password")
        form.update({
            "uh": uh,
            "curpass": old_password,
            "newpass": new_password,
            "verpass": new_password
        })

        r = self._session.post("https://old.reddit.com/api/update_password", data=form, headers=self.headers)

register_provider(Reddit)
