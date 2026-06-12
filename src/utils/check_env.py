from os import environ

keys = ("DB_PATH", "TOKEN", "STATCORD_KEY", "KSOFT_KEY", "RAPIDAPI_KEY")


def check_env():
    for var in keys:
        if var not in environ.keys():
            print(f"| warning: environment variable {var} not found")
