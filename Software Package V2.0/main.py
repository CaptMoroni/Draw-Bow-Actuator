# Control Functions

import control_loadcell as cl #This line might not be needed and 'cl' conflicts with the network
from control_machine import actuator
import control_display as tft_c

import control_settings as cs
settings = cs.importSettings()

import helper_functions as hf

act = actuator()

import network
import socket

from machine import Timer

import time
import json
import gc

gc.enable()
print('free memory: {}'.format(gc.mem_free()))

htmlHeader = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
javascriptHeader = 'HTTP/1.0 200 OK\r\nContent-type: text/javascript\r\n\r\n'
jsonHeader = 'HTTP/1.0 200 OK\r\nContent-type: text/json\r\n\r\n'
csvHeader = 'HTTP/1.0 200 OK\r\nContent-type: application/csv\r\n\r\n'
cssHeader = 'HTTP/1.0 200 OK\r\nContent-type: text/css\r\n\r\n'

sampleRate = 10


def updateCallback(t):
    tft_c.updatePos(act.S1.getCurrentPos(), act.getLoad())
    
time.sleep(.1)

tft_c.initScreen()

updateScreen = Timer()
updateScreen.init(freq=3, mode=Timer.PERIODIC, callback=updateCallback)
print('{}, {}'.format(settings['SSID'], settings['PASSWORD']))
requestData = {}
tft_c.updateWifi("CONNECTING")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(settings['SSID'], settings['PASSWORD'])
print(wlan.isconnected())

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    tft_c.updateWifi("CONNECTING")
    act.onBoardLED.off()
    time.sleep(.25)
    act.onBoardLED.on()
    time.sleep(.25)

if wlan.isconnected():
    act.onBoardLED.on()
    sta_if = network.WLAN(network.STA_IF)
    print(sta_if.ifconfig()[0])
    tft_c.updateWifi(sta_if.ifconfig()[0])

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    while True:
        cl, addr = s.accept()
        cl_file = cl.makefile('rwb', 0)
        print('client connected from', addr)
#         request = cl.recv(1024)
#         print(request)
        requestData = {}
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
            else:
                temp = line.decode('utf-8').split(' ')
                requestData[temp[0]] = temp[1]
                
        URL_Data = hf.parseGet(hf.getParameter(requestData,'GET')) #This line is giving me errors. I need to see if sometime browsers send other types of requests other than GET
        #print(URL_Data)
        gc.collect()
        print('free memory: {}'.format(gc.mem_free()))
        response = ''
        
        URL = URL_Data['URL']
        responseHeaders = htmlHeader
        updateScreen.deinit()
        
        print('Request URL: {}'.format(URL))
        if URL == '/':
            print('root')
            page = open("index.html", "r")
            response = page.read()
            page.close()

        elif URL == '/calibration':
            print('Calibration Page')
            page = open("page_calibration.html", "r")
            response = page.read()
            page.close()

        elif URL == '/settings':
            print('settings Page')
            page = open("page_settings.html", "r")
            response = page.read()
            page.close()

        elif URL == '/main.js':
            page = open("main.js", "r")
            response = page.read()
            page.close()
            responseHeaders = javascriptHeader

        elif URL == '/page_settings.js':
            page = open("page_settings.js", "r")
            response = page.read()
            page.close()
            responseHeaders = javascriptHeader

        elif URL == '/page_calibration.js':
            page = open("page_calibration.js", "r")
            response = page.read()
            page.close()
            responseHeaders = javascriptHeader

        elif URL == '/main.css':
            page = open("main.css", "r")
            response = page.read()
            page.close()
            responseHeaders = cssHeader

        elif URL == '/testData.csv':
            csvData = open("testData.csv", "r")
            response = csvData.read()
            csvData.close()
            responseHeaders = csvHeader

        elif URL == '/setTare':
            act.setTare()
            load = act.getLoad()
            position = act.S1.getCurrentPos()
            testData = {'x':position, 'l':load}
            response = json.dumps(testData)
            responseHeaders = jsonHeader

        elif URL == '/setZero':
            act.S1.setZeroPos()
            load = act.getLoad()
            position = act.S1.getCurrentPos()
            testData = {'x':position, 'l':load}
            response = json.dumps(testData)
            responseHeaders = jsonHeader

        elif URL == '/m':
            load = act.getLoad()
            position = act.S1.getCurrentPos()
            testData = {'x':position, 'l':load}
            response = json.dumps(testData)
            responseHeaders = jsonHeader

        elif URL == '/mr':
            rawload = act.getRawLoad()
            load = act.getLoad()
            position = act.S1.getCurrentPos()
            testData = {'x':position, 'l':load, 'r': rawload}
            response = json.dumps(testData)
            responseHeaders = jsonHeader

        elif URL == '/getSettings':
            settings = cs.importSettings()
            response = json.dumps(settings)
            responseHeaders = jsonHeader

        elif URL == '/saveSettings':
            jsonText = URL_Data['data'].replace('%22', '"')
            print(jsonText)
            if jsonText != 'undefined':
                inputData = json.loads(jsonText)
                print(inputData)
                cs.writeSettings(inputData)
            else:
                inputData = {}
            settings = cs.importSettings()
            response = json.dumps(settings)
            responseHeaders = jsonHeader

        elif URL == '/c':
            print(URL_Data['data'].replace('%22', '"'))
            jsonText = URL_Data['data'].replace('%22', '"')
            if jsonText != 'undefined':
                inputData = json.loads(URL_Data['data'].replace('%22', '"'))
                act.handelCommand(inputData)
            else:
                inputData = {}
            load = act.getLoad()
            position = act.S1.getCurrentPos()
            testData = {'x':position, 'l':load}
            response = json.dumps(testData)
            responseHeaders = jsonHeader

        else:
            print('error 404')
            response = '404 Error'
            print('response error:')
        
        cl.send(responseHeaders)
        cl.send(response)
        cl.close()
        updateScreen.init(freq=3, mode=Timer.PERIODIC, callback=updateCallback)
        
        
else:
    if wlan.status() == 0:
        print('Status: {} - Looking for network  '.format(wlan.status()))
        tft_c.updateWifi('Looking for network')
    if wlan.status() == -1:
        print('Status: {} - Failed  '.format(wlan.status()))
        tft_c.updateWifi('Failed')
    if wlan.status() == -2:
        print('Status: {} - No Network  '.format(wlan.status()))
        tft_c.updateWifi('No Network')
    if wlan.status() == -3:
        print('Status: {} - Incorrect Password  '.format(wlan.status()))
        tft_c.updateWifi('Incorrect Password')
    act.onBoardLED.off()


