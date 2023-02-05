from typing import List
from difflib import SequenceMatcher


def similar(source_name: str, nameslist: List[str]) -> List[str]:
    """
    Find similar names to a source name in a list of names.

    Args:
        source_name (str): the name to compare.
        nameslist (List[str]): the list of names to compare with the source name.

    Returns:
        List[str]: A list of similar names.
    """
    similar_names = []
    for name in nameslist:
        if SequenceMatcher(None, source_name, name).ratio() > 0.8:
            similar_names.append(name)
    return similar_names