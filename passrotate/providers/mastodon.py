from passrotate.provider import Provider, ProviderOption, register_provider
from passrotate.forms import get_form
import requests

class Mastodon(Provider):
    """
    [some.masto.instance]
    username=Your login email
    """
    name = "Mastodon"
    domains = []
    options = {
        "username": ProviderOption(str, "Your login email")
    }

    def __init__(self, options):
        self.username = options["username"]
        self.domain = options["domain"]

    @staticmethod
    def detect(dom):
        score = 0.0
        element_fingerprints = [
            (["a"], {"class_": "button button-alternative", "href": "https://joinmastodon.org/"}, 0.25),
            (["a"], {"class_": "button button-alternative-2 webapp-btn", "href": "/auth/sign_in"}, 0.5),
            (["a"], {"href": "https://github.com/tootsuite/mastodon", "text": "Source code"}, 0.2),
            (["h3"], {"text": "What is Mastodon?"}, 0.1),
            (["h6"], {"text": "A more humane approach"}, 0.1),
            (["div"], {"class_": 'row__mascot'}, 0.2),
            (["form"], {"id": "new_user", "class_": "simple_form new_user"}, 0.25),
        ]
        for fp in element_fingerprints:
            if dom.find(*fp[0], **fp[1]):
                score += fp[2]

        return min(score, 1.0)  # Clamp score to max 1

    def prepare(self, old_password):
        self._session = requests.Session()
        r = self._session.get("https://{}/auth/sign_in".format(self.domain))
        self._form = get_form(r.text, id="new_user")
        self._form.update({
            "user[email]": self.username,
            "user[password]": old_password
        })
        r = self._session.post(
            "https://{}/auth/sign_in".format(self.domain),
            data=self._form,
            allow_redirects=False
        )
        if not r.ok or r.status_code != 302:
            raise Exception("Unable to log into {} with current password".format(self.domain))
        r = self._session.get("https://{}/auth/edit".format(self.domain))
        self._form = get_form(r.text, id="edit_user")

    def execute(self, old_password, new_password):
        self._form.update({
            "user[password]": new_password,
            "user[password_confirmation]": new_password,
            "user[current_password]": old_password
        })
        r = self._session.post(
            "https://{}/auth".format(self.domain),
            data=self._form,
            allow_redirects=False
        )
        if not r.ok or r.status_code != 302:
            raise Exception("Failed to update Mastodon password")

register_provider(Mastodon)
