"""
All constants specific to the application
"""
from os import getenv

PARAMS = {
    "INPUT_LABEL": getenv("INPUT_LABEL", "temperature"),
    "WINDOW_SIZE": float(getenv("WINDOW_SIZE", 3)),
    "SEND_ON_CHANGE": True if getenv("SEND_ON_CHANGE").lower() == 'true' else False,
}
