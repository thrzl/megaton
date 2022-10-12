keys = ("DB_URL", "TOKEN", "STATCORD_KEY", "KSOFT_KEY", "RAPIDAPI_KEY")
from os import environ


def check_env():
    for var in keys:
        if var not in environ.keys():
            print(f"| warning: environment variable {var} not found")
