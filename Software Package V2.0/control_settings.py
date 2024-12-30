import json

settingList = {
    "load_cell_value_1": -29456.0,
    "SSID": "Shadesmar",
    "PASSWORD": "lifebeforedeath2016!",
    "load_cell_weight_1": 0,
    "load_cell_value_2": -295082.0,
    "load_cell_weight_2": 13,
    "sampleRate": 50
}

def writeSettings( settings ):
    global settingList
    for setting in settings:
        if setting == 'SSID' :
            settingList[setting] = settings[setting].replace('%20',' ')
        else:
            settingList[setting] = settings[setting]
    settingsFile = open("settings.json", "w")
    settingsFile.write(json.dumps(settingList))
    settingsFile.close()

def importSettings():
    settingsFile = open("settings.json", "r")
    newData = settingsFile.read()
    settingsFile.close()
    return json.loads(newData)