import control_settings as cs

class loadCellTools:
    def __init__(self):
        settings = cs.importSettings()

        self.x1 = settings['load_cell_value_1']
        self.y1 = settings['load_cell_weight_1']

        self.x2 = settings['load_cell_value_2']
        self.y2 = settings['load_cell_weight_2']

        self.a = -1.96034E-18
        self.b = -1.45362E-12
        self.c = -4.96120E-05
        self.d = 4.57435E-02


    def convertRawLoad(self, x):
        lineFitLoad =  self.a * (x**3) + self.b * (x**2) + self.c * x + self.d
        return lineFitLoad