from enum import Enum

import requests
from bs4 import BeautifulSoup

_providers = list()
_provider_map = dict()
_provider_domains = dict()
_provider_detectors = dict()

def register_provider(provider):
    _providers.append(provider)
    _provider_map[provider.name] = provider
    for d in provider.domains:
        _provider_domains[d] = provider
    if hasattr(provider, "detect"):
        _provider_detectors[provider.detect] = provider

def get_provider(domain):
    return _provider_map.get(domain) or _provider_domains.get(domain)

def detect_provider_score(domain):
    homepage = requests.get("https://" + domain)
    if not homepage.ok:
        return None
    dom = BeautifulSoup(homepage.text, "html5lib")

    scores = []
    for detector in _provider_detectors.keys():
        scores.append((detector, detector(dom)))
    scores = list(filter(lambda el: el[1] >= 0.5, scores))
    scores.sort(key=lambda el: el[1], reverse=True)

    return _provider_detectors[scores[0][0]] if scores else None

def get_providers():
    return _providers

class PromptType(Enum):
    generic = "generic"
    totp = "totp"
    sms = "sms"

class ProviderOption:
    def __init__(self, type, doc, optional=False):
        self.type = type
        self.doc = doc
        self.optional = optional

class Provider:
    def prompt(self, prompt, prompt_type):
        return self._prompt(prompt, prompt_type)
