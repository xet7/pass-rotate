from typing import Dict, Callable
from bs4 import BeautifulSoup
from bs4.element import ResultSet

FormData = Dict[str, str]


def get_form_data(inputs: ResultSet) -> FormData:
    """Returns data dictionary from list of BeautifulSoup input elements.

    Parameters:
        inputs: The list of BeautifulSoup input elements.

    Returns dictionary with (name, value) pairs from inputs.
    """
    return {
        i.get("name", ""): i.get("value", "") or "" for i in inputs if i.get("name", "")
    }


def get_form(text: str, type: str = "form", **kwargs) -> FormData:
    """Helper method to get the data from a form.

    Parameters:
        text: HTML text to be processed.
        type: HTML element type to find in page.
        **kwargs: Additional parameters to pass to `soup.find()`

    Returns dictionary with (name, value) pairs from inputs from first match.
    """
    soup = BeautifulSoup(text, "html5lib")
    form = soup.find(type, attrs=kwargs)
    inputs = form.find_all("input")
    return get_form_data(inputs)


def custom_get_form(text: str,
                    func: Callable[[BeautifulSoup], ResultSet]) -> FormData:
    """Helper method to get data from a form using a custom function.

    Parameters:
        text: HTML text to be processed.
        func: A function that takes in a BeautifulSoup object and outputs a
              list of input objects from the form desired.

    Returns dictionary with (name, value) pairs from inputs returned by func.
    """
    soup = BeautifulSoup(text, "html5lib")
    inputs = func(soup)
    return get_form_data(inputs)
