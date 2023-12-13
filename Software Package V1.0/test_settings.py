import json
import control_settings as cs

templateData = {}

templateData['SSID'] = 'Shadesmar'
templateData['PASSWORD'] = 'lifebeforedeath2016'
templateData['load_cell_value_1'] = -29456.0
templateData['load_cell_weight_1'] = 0
templateData['load_cell_value_2'] = -295082.0
templateData['load_cell_weight_2'] = 13
templateData['sampleRate'] = 50

cs.writeSettings(templateData)