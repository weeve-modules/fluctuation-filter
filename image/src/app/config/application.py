"""
All constants specific to the application
"""
from app.utils.env import env
from app.utils.floatenv import floatenv
from app.utils.booleanenv import boolenv


APPLICATION = {
    "INPUT_LABEL": env("INPUT_LABEL", "temperature"),
    "OUTPUT_LABEL": env("OUTPUT_LABEL", "temperature"),
    "WINDOW_SIZE": floatenv("WINDOW_SIZE", 3),
    "SEND_ON_CHANGE": boolenv("SEND_ON_CHANGE", False)
}
