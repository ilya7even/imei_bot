import json
import os

WHITELIST_FILE = os.path.join(os.path.dirname(__file__), "whitelist.json")

def is_user_whitelisted(user_id: int) -> bool:
    try:
        with open(WHITELIST_FILE, "r") as file:
            whitelist = json.load(file)
        return user_id in whitelist
    except (FileNotFoundError, json.JSONDecodeError):
        return False