from bs4 import BeautifulSoup


def get_form_data(inputs):
    """Returns data dictionary from list of BeautifulSoup input elements."""
    return {
        i.get("name", ""): i.get("value", "") or "" for i in inputs if i.get("name", "")
    }


def get_form(text, type="form", **kwargs):
    """Helper method to get the data from a form."""
    soup = BeautifulSoup(text, "html5lib")
    form = soup.find(type, attrs=kwargs)
    inputs = form.find_all("input")
    return get_form_data(inputs)


def custom_get_form(text, func):
    """Helper method to get data from a form using a custom function."""
    soup = BeautifulSoup(text, "html5lib")
    inputs = func(soup)
    return get_form_data(inputs)
