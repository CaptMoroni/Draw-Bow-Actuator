import json

settingList = {
    "SSID": "WIFI NAME",
    "PASSWORD": "PASSWORD",
    "sampleRate": 50,
    "a": -1.96034E-18,
    "b": -1.45362E-12,
    "c": -4.96120E-05,
    "d": 4.57435E-02,
    "workOffset":0,
    "calibration_values":[
        [922, 0],
        [-99304, 4.96],
        [-196637, 9.76],
        [-493281, 24.4]
    ]
}

def preProcessSettings( settings ):
    global settingList
    for setting in settings:
        if setting == 'SSID' :
            settingList[setting] = settings[setting].replace('%20',' ')
        else:
            settingList[setting] = settings[setting]
    return json.dumps(settingList)

def writeSettings( settings ):
    settingList = preProcessSettings(settings)
    settingsFile = open("settings.json", "w")
    settingsFile.write(settingList)
    settingsFile.close()

def importSettings():
    settingsFile = open("settings.json", "r")
    newData = settingsFile.read()
    settingsFile.close()
    return json.loads(newData)

def updateCalibration( a, b, c, d, calValues ):
    #write the new Data to the settings file
    currentSettings = importSettings()

    currentSettings['a'] = a
    currentSettings['b'] = b
    currentSettings['c'] = c
    currentSettings['d'] = d
    currentSettings['calibration_values'] = calValues

    writeSettings(currentSettings)
    return

def updateWorkOffset( workOffset ):
    #write the new Data to the settings file
    currentSettings = importSettings()
    currentSettings['workOffset'] = workOffset
    writeSettings(currentSettings)
    return

def updateSettingsPage( SSID, Password, SampleRate):
    currentSettings = importSettings()
    currentSettings['SSID'] = SSID
    currentSettings['PASSWORD'] = Password
    currentSettings['sampleRate'] = SampleRate
    writeSettings(currentSettings)
    return