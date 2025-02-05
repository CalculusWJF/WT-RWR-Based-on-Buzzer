from ili9341 import Display
from machine import Pin, SPI
import music
import _thread
import time
import machine

def rwr(x):
    _thread.start_new_thread(t0, ())
    for i in range(0, x, 1):
        midi.pitch_time(440, 100)
        time.sleep_ms(900)

def t0():
    display.draw_image('1S.raw', 0, 30, 240, 240)

def rwrG(x):
    _thread.start_new_thread(t1, ())
    for i in range(0, x, 1):
        midi.pitch_time(523, 250)
        midi.pitch_time(349, 250)

def t1():
    display.draw_image('2S.raw', 0, 30, 240, 240)
    display.draw_image('1.raw', 92, 26, 55, 28)

def rwrD(x):
    global times
    times = x
    _thread.start_new_thread(t2, ())
    for i in range(0, x, 1):
        midi.pitch_time(523, 100)
        midi.pitch_time(392, 120)

def t2():
    global times
    for i in range(0, int(times*0.4), 1):
        display.draw_image('2.raw', 92, 26, 55, 28)
        time.sleep_ms(250)
        display.draw_image('3.raw', 92, 26, 55, 28)
        time.sleep_ms(250)



midi = music.MIDI(2)
pin4 = machine.Pin(4, machine.Pin.OUT)
pin4.value(1)
spi = SPI(1, baudrate=60000000, sck=Pin(6), mosi=Pin(7))
display = Display(spi, dc=Pin(15), cs=Pin(17), rst=Pin(16))
times = 0
rwr(4)
rwrG(5)
rwrD(15)
rwr(3)
rwrG(3)
rwrD(10)
_thread.start_new_thread(t0, ())
