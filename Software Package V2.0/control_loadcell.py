import control_settings as cs
from matrix import *

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
    
    def setLineFitValues(self, d=0, c=0, b=0, a=0):
        self.a = a
        self.b = b
        self.c = c 
        self.d = d 
        return
    
    def solveCurveFit(self, r1, a1, r2, a2):
        return
