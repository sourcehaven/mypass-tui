from typing import SupportsIndex


def rreplace(s: str, __old: str, __new: str, __count: SupportsIndex = 1):
    """
    Replace the last occurrence of a substring in a string.

    Args:
        s (str): The input string in which to perform the replacement.
        __old (str): The substring to be replaced.
        __new (str): The substring to replace the last occurrence of __old.
        __count (SupportsIndex, optional): The number of occurrences to replace.
            Defaults to 1, which replaces only the last occurrence.

    Returns:
        str: The modified string with the last occurrence of __old replaced by __new.

    Example:
        >>> input_string = "This is an example, and this is the last example."
        >>> old_substring = "example"
        >>> new_substring = "instance"
        >>> result = rreplace(input_string, old_substring, new_substring)
        >>> print(result)
        "This is an example, and this is the last instance."
    """
    li = s.rsplit(__old, __count)
    return __new.join(li)


def replace_empty_string_with_none(val: str | None):
    return val if val != "" else None
