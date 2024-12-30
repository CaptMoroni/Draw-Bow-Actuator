from control_stepper import stepper
import control_display as tft_c
import control_loadcell as cl

import utime
import time
from machine import Pin, Timer

from hx711_pio import HX711


import control_settings as cs
settings = cs.importSettings()

class actuator:
    def __init__(self):
        self.item = 1
        self.lock_enable = True
        self.stepstoinch = 1600 * 25.4 / ( 28 * 3.14159 )
        self.S1 = stepper({
            'step_pin':1, # should be set to pin 1 for actual usage, using 25 for testing
            'dir_pin':0, # 'dir_pin':0
            'steps_per_revolution': 16000,
            'steps_per_in': 462.004063, # 1600 sp/rev * 25.4 in / mm / ( 28 mm * pi() )
            'maxFrequiency': 5000,
            'FWD': 0,
            })
        self.lock_pin = Pin(17, Pin.OUT)
        self.lock_enable = True

        self.pin_OUT = Pin(26, Pin.IN, pull=Pin.PULL_DOWN)
        self.pin_SCK = Pin(27, Pin.OUT)

        self.hx711 = HX711(self.pin_SCK, self.pin_OUT)
        self.hx711.tare()

        self.onBoardLED = Pin('LED', Pin.OUT)
        self.onBoardLED.on()

        self.tareValue = 0

    def getLoad( self ):
        raw_val = self.hx711.read()
        load = cl.convertRawLoad(raw_val) - self.tareValue
        return load

    def setTare(self):
        self.tareValue += self.getLoad()

    def handelCommand( self, cData ):
        tft_c.updatePos('---', '---')
        if cData['c'] == 'to':
            if cData['x'] != 'undefined':
                if self.lock_enable:
                    if self.S1.getCurrentPos() > cData['x']:
                        if self.lock_pin.value() != 1:
                            #down command
                            self.lock_pin.value(1)
                            utime.sleep_ms(100)
                            self.S1.goTo(self.S1.getCurrentPos() + .15)
                            while self.S1.ready == False:
                                utime.sleep_ms(100)
                    else:
                        self.lock_pin.value(0)
                self.S1.goTo(cData['x'])
                while self.S1.ready == False:
                    utime.sleep_ms(500)
        if cData['c'] == 'run':
            if cData['x'] != 'undefined':
                self.drawAndLog(cData['x'], settings['sampleRate'])

    def drawAndLog( self, goToY , sampleRate):
        settings = cs.importSettings()
        print('logging')
        self.measurements = []
        initPos = self.S1.getCurrentPos()
        if self.lock_enable:
            self.lock_pin.value(0)
        else:
            self.lock_pin.value(1)
        self.S1.goTo(goToY)
        initTime = time.ticks_ms()
        while self.S1.ready == False:
            load = self.getLoad()
            position = self.S1.getCurrentPos()
            self.measurements.append([position, load])
            utime.sleep_ms(int(1000/sampleRate))
        
        print('ready to lower')
        utime.sleep_ms(1000)
        
        if self.lock_enable:
            print('unlocking')
            self.lock_pin.value(1)
            utime.sleep_ms(100)
            self.S1.goTo(self.S1.getCurrentPos() + .075)
            while self.S1.ready == False:
                #print('Height: {}, Load: {}'.format(cp, load))
                utime.sleep_ms(100)
        
        self.S1.goTo(initPos)
        
        while self.S1.ready == False:
            cp = self.S1.getCurrentPos()
            #print('Height: {}, Load: {}'.format(cp, load))
            utime.sleep_ms(100)
        
        savedFile = open('testData.csv', 'w')
        savedFile.write('position (in), load (lbf)\n')
        for line in self.measurements:
            lineData = ''
            for value in line:
                lineData += '{}, '.format(value)
            lineData += '\n'
            savedFile.write(lineData)
        print('done')
        return True