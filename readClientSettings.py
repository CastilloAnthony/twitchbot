import json
from pathlib import Path

def readClientSettings():
    if not Path('./client_settings.json').is_file():
            with open('client_settings.json', 'w') as file:
                json.dump({
                "client_id": "",
                "client_secret" : "",
                "bot_id": "",
                "owner_id": "",
                "prefix": "!",
                "owner_username": "",
                "bot_username": ""
            },
            file)
            print('Created new file client_settings.json. Please fill out the information missing from the file.')
    else:
        with open("client_settings.json", 'r') as file:
            return json.load(file)
# end _readClientSettings