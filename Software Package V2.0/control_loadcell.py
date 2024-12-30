import control_settings as cs

class loadCellTools:
    def __init__(self):
        settings = cs.importSettings()

        self.x1 = settings['load_cell_value_1']
        self.y1 = settings['load_cell_weight_1']

        self.x2 = settings['load_cell_value_2']
        self.y2 = settings['load_cell_weight_2']

        self.m = (self.y2-self.y1)/(self.x2-self.x1)

    def convertRawLoad(self, x):
        load = round(self.m*(x - self.x1) + self.y1,1)
        lineFitLoad =  .000202*(load)**3 - 0.0149*(load)**2 + 1.35*(load) - 0.122
        return lineFitLoad