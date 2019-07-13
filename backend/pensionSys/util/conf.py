import json

def conf():
    with open('config.json', 'r') as f:
        js = json.load(f)
        return js