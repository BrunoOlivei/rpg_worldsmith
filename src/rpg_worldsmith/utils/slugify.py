import re

from unidecode import unidecode


def slugify(name: str) -> str:
    """
    Convert a string into a compatible name for a directory.
    This function removes any non-alphanumeric characters, converts the string to lowercase,
    replaces spaces with hyphens, and ensures the result is suitable for use as a directory.

    Args:
        name (str): The string to be converted into a slug.

    Returns:
        str: A slugified version of the input string, containing only alphanumeric characters and hyphens.
    """
    return re.sub(r"[^\w\-]", "", unidecode(name).lower().replace(" ", "-"))
