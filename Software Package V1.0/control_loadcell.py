import control_settings as cs
settings = cs.importSettings()

x1 = settings['load_cell_value_1']
y1 = settings['load_cell_weight_1']

x2 = settings['load_cell_value_2']
y2 = settings['load_cell_weight_2']

m = (y2-y1)/(x2-x1)

def convertRawLoad(x):
    global m, x1, y1
    load = round(m*(x - x1) + y1,1)
    lineFitLoad =  .000202*(load)^3 - 0.0149*(load)^2 + 1.35*(load) - 0.122
    return round(m*(x - x1) + y1,1)