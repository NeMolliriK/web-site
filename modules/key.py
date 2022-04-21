from json import load
import os

with open('api.json') as json:
    print(os.getcwd())
    keys = load(json)['api_keys']


def check_key(key):
    if key in keys:
        return True
    else:
        return False
