"""Utility functions for getting the boolean env variable"""
import os


def boolenv(name: str, default=False) -> bool:
    """ return value from boolena environment variable otherwise False

    Args:
        name (str): [ENVIRONMENT_VARIABLE]

    Returns:
        bool: [value of the ENVIRONMENT_VARIABLE]
    """

    if os.getenv(name).lower() == 'true':
        return True
    else:
        return False
