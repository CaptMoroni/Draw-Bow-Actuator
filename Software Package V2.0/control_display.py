import st7789
import config_display
import time
import lib_font as font

bgColor = st7789.color565(52, 56, 65)
fontColor = st7789.color565(230, 242, 255)
textBG = st7789.color565(19, 22, 28)

def initScreen():
    global tft
    tft = config_display.config(1, buffer_size=4096)
    tft.init()
    tft.fill(st7789.color565(52, 56, 65))
    tft.png(f'wifi-icon.png', 10, 10)
    tft.text(font, '---', 55, 8, fontColor, bgColor)
    tft.text(font, '---', 40, 162, fontColor, textBG)
    tft.text(font, '---', 180, 162, fontColor, textBG)
    #tft.text(font, "Initializing", 10, 75, fontColor, bgColor)


def updateWifi(ipStatus):
    global tft
    x = '{}               '.format(ipStatus)
    x = x[:15]
    tft.text(font, '{}'.format(x), 55, 8, fontColor, bgColor)

def updatePos(x, l):
    global tft
    x = '{}       '.format(x)
    l = '{}       '.format(l)
    x = x[:6]
    l = l[:6]
    tft.text(font, x, 40, 162, fontColor, textBG)
    tft.text(font, l, 180, 162, fontColor, textBG)
    
#initScreen()
#updatePos(1.231246,4)
#time.sleep(.2)
#updatePos(1.0,4)
