from machine import Pin, Timer
import utime

class stepper:

    def __init__(self, setupData):
        self.step_pin = Pin(setupData['step_pin'], Pin.OUT)
        self.dir_pin  = Pin(setupData['dir_pin'], Pin.OUT)
        
        self.steps_per_revolution = setupData['steps_per_revolution']
        self.steps_per_in = setupData['steps_per_in']
        self.maxFrequiency = setupData['maxFrequiency']
        self.FWD = bool(setupData['FWD'])
        
        self.RVS = not self.FWD 
        self.halfSteps = 0
        self.stepTarget = 0
        self.stepDirection = 0
        self.currentFrequency = 0
        self.ready = True
        
        self.minFrequincy = 10
        self.frequiencyStep = 80
        self.decelDistance = 3200
        self.minDecellFreq = 250
        self.decelStep = 10
        
        self.stepTimer = Timer()
        self.accelTimer = Timer()
    
    def step(self, t):
        if self.halfSteps != self.stepTarget:
            self.halfSteps += self.stepDirection
            self.step_pin.value(not self.step_pin.value())
        else:
            self.stepTimer.deinit()
            self.accelTimer.deinit()
            self.currentFrequency = 0
            self.ready = True
        
    def spin(self, freq):
        self.stepTimer.deinit()
        self.stepTimer.init(freq=freq, mode=Timer.PERIODIC, callback=self.step)
        
    def changeSpeed(self, t):
        self.currentFrequency = max(self.minFrequincy, self.currentFrequency)
        
        if abs(self.stepTarget - self.halfSteps) < self.decelDistance:
            if self.currentFrequency > self.minDecellFreq:
                self.currentFrequency -= self.decelStep
                self.spin(self.currentFrequency)
            else:
                self.currentFrequency += self.frequiencyStep
                self.spin(self.currentFrequency)
        else:
            if self.currentFrequency < self.maxFrequiency:
                self.currentFrequency += self.frequiencyStep
                self.spin(self.currentFrequency)
                
    def setZeroPos(self):
        self.halfSteps = 0
        self.stepTarget = 0
            
    def getCurrentPos(self):
        return (self.halfSteps / 2) / self.steps_per_in
        

    def setDirection(self):
        if self.stepTarget - self.halfSteps > 0:
            self.dir_pin.value(self.FWD)
            self.stepDirection = 1
        else:
            self.dir_pin.value(self.RVS)
            self.stepDirection = -1
            
    def goTo(self, target): #target in inches
        self.ready = False
        print('going to {}'.format(target))
        self.stepTarget = int(2 * target * 462.0050)
        self.setDirection()
        print(self.stepTarget)        
        self.accelTimer.init(freq=50, mode=Timer.PERIODIC, callback=self.changeSpeed)





