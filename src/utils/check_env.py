from os import environ

keys = ("DB_PATH", "TOKEN")


def check_env():
    for var in keys:
        if var not in environ.keys():
            print(f"| warning: environment variable {var} not found")
