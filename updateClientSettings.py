import json

def updateClientSettings(client_settings):
    with open("client_settings.json", 'w') as file:
        return json.dump(client_settings, file, indent=4)
# end _readClientSettings