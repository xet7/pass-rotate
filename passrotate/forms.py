from bs4 import BeautifulSoup


def get_form_data(inputs):
    """Returns data dictionary from list of BeautifulSoup input elements.

    :param list inputs: The list of BeautifulSoup input elements.
    :returns: dictionary with (name, value) pairs from inputs.
    :rtype: dict(str, str)
    """
    return {
        i.get("name", ""): i.get("value", "") or "" for i in inputs if i.get("name", "")
    }


def get_form(text, type="form", **kwargs):
    """Helper method to get the data from a form.

    :param str text: HTML text to be processed.
    :param str type: HTML element type to find in page.
    :param \**kwargs: Additional parameters to pass to ``soup.find()``
    :returns: dictionary with (name, value) pairs from inputs from first match.
    :rtype: dict(str, str)
    """
    soup = BeautifulSoup(text, "html5lib")
    form = soup.find(type, attrs=kwargs)
    inputs = form.find_all("input")
    return get_form_data(inputs)


def custom_get_form(text, func):
    """Helper method to get data from a form using a custom function.
    :param str text: HTML text to be processed.
    :param func:
        A function that takes in a BeautifulSoup and outputs a list of inputs.
    :returns: dictionary with (name, value) pairs from inputs returned by func.
    :rtype: dict(str, str)
    """
    soup = BeautifulSoup(text, "html5lib")
    inputs = func(soup)
    return get_form_data(inputs)
