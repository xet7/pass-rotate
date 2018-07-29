from passrotate.exceptions import PrepareException, ExecuteException
from passrotate.provider import Provider, ProviderOption, register_provider
from passrotate.forms import get_form, custom_get_form
import requests


class PyPI(Provider):
    """
    [pypi.python.org]
    username=Your PyPI username
    """
    name = "PyPI"
    domains = [
        "pypi.python.org",
    ]
    options = {
        "username": ProviderOption(str, "Your PyPI username")
    }

    def __init__(self, options):
        self.username = options["username"]

    def prepare(self, old_password):
        self._session = requests.Session()
        r = self._session.get("https://pypi.python.org/pypi?%3Aaction=login_form")
        self._form = get_form(r.text, type="div", id="content")
        self._form.update({
            "username": self.username,
            "password": old_password
        })
        r = self._session.post("https://pypi.python.org/pypi",
                               data=self._form, allow_redirects=False)
        if not r.ok:
            raise PrepareException("Unable to log into PyPI with current password")
        r = self._session.get("https://pypi.python.org/pypi?%3Aaction=user_form")
        self._form = custom_get_form(
            r.text,
            lambda x: x.find(id="content").find("form").find_all("input")
        )

    def execute(self, old_password, new_password):
        self._form.update({
            "password": new_password,
            "confirm": new_password
        })
        r = self._session.post("https://pypi.python.org/pypi",
                               data=self._form, allow_redirects=False)
        if not r.ok:
            raise ExecuteException("Failed to update PyPI password")

register_provider(PyPI)
