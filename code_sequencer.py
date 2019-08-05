# CircuitPython + Trellis M4 Keyboard emulator.
# Designed for use with Scratch 16-beat Sequencer
# https://scratch.mit.edu/projects/282414002/
# January 2019 Sandy Roberts @KaleidoscopeSci and Steve Kosciolek

import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import adafruit_trellism4

RED = 0xFF0000  # (255, 0, 0)
ORANGE = 0xFF6600  # (255, 122, 0)
YELLOW = 0xFFFF00  # (255, 255, 0)
GREEN = 0x008000  # (0, 255, 0)
BLUE = 0x0000FF  # (0, 0, 255)
PURPLE = 0x660066  # (102, 0, 102)
WHITE = 0xFFFFFF  # (255, 255, 255)
TEAL = 0x00FFFF  # (0, 255, 255)
FUSCHIA = 0xFF00FF  # (255, 0, 255)
BLACK = 0x000000  # (0, 0, 0)

trellis = adafruit_trellism4.TrellisM4Express()
trellis.pixels.brightness = 0.25

# The keyboard
keyboard = Keyboard()
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

print("object setup")

trls = [[[1 for z in range(3)] for y in range(4)] for x in range(8)]

print("Create array")

# think of this array as three sheets of 8x4 graph paper, stacked together
# the top sheet (accessed as [x][y][0]) is the keyboard mappings
# the next sheet ([x][y][1]) is the color coding for the keys
# and the last sheet is used to track whether the particular key has been
# pressed.we don't actually use this last piece much, but it is used for
# the origional codeavailable in the comments below

trls[0][0][0] = '1'
trls[1][0][0] = '2'
trls[2][0][0] = '3'
trls[3][0][0] = '4'
trls[4][0][0] = '5'
trls[5][0][0] = '6'
trls[6][0][0] = '7'
trls[7][0][0] = '8'

trls[0][1][0] = 'q'
trls[1][1][0] = 'w'
trls[2][1][0] = 'e'
trls[3][1][0] = 'r'
trls[4][1][0] = 't'
trls[5][1][0] = 'y'
trls[6][1][0] = 'u'
trls[7][1][0] = 'i'

trls[0][2][0] = 'a'
trls[1][2][0] = 's'
trls[2][2][0] = 'd'
trls[3][2][0] = 'f'
trls[4][2][0] = 'g'
trls[5][2][0] = 'h'
trls[6][2][0] = 'j'
trls[7][2][0] = 'k'

trls[0][3][0] = 'z'
trls[1][3][0] = 'x'
trls[2][3][0] = 'c'
trls[3][3][0] = 'v'
trls[4][3][0] = 'b'
trls[5][3][0] = 'n'
trls[6][3][0] = 'm'
trls[7][3][0] = 'l'

trls[0][0][1] = RED
trls[1][0][1] = RED
trls[2][0][1] = RED
trls[3][0][1] = RED
trls[4][0][1] = RED
trls[5][0][1] = RED
trls[6][0][1] = RED
trls[7][0][1] = RED

trls[0][1][1] = RED
trls[1][1][1] = RED
trls[2][1][1] = RED
trls[3][1][1] = RED
trls[4][1][1] = RED
trls[5][1][1] = RED
trls[6][1][1] = RED
trls[7][1][1] = RED

trls[0][2][1] = PURPLE
trls[1][2][1] = BLUE
trls[2][2][1] = TEAL
trls[3][2][1] = GREEN
trls[4][2][1] = GREEN
trls[5][2][1] = YELLOW
trls[6][2][1] = ORANGE
trls[7][2][1] = FUSCHIA

trls[0][3][1] = PURPLE
trls[1][3][1] = BLUE
trls[2][3][1] = TEAL
trls[3][3][1] = GREEN
trls[4][3][1] = GREEN
trls[5][3][1] = YELLOW
trls[6][3][1] = ORANGE
trls[7][3][1] = FUSCHIA

# trls[x][y][2] is loaded with 1 when created
# this is used to tell whether the pixels are lit or not.

print("Load array")

# no test, since all the pixels are lit at this point.
for y in range(4):
        for x in range(8):
            trellis.pixels[x, y] = trls[x][y][1]

print("light pixels")

current_press = set()  # start with nothing currently pressed

while True:
    pressed = set(trellis.pressed_keys)  # look for keypresses
    for press in pressed - current_press:  # loop through all pressed keys
        x, y = press  # read coordinates of press
# default action, flash and stay lit; then send keyboard press
        trellis.pixels[x, y] = WHITE  # flash the pressed key white
        time.sleep(0.02)  # and pause before turning on/off
        trellis.pixels[x, y] = trls[x][y][1]
        keyboard_layout.write(trls[x][y][0])
        print("Pressed: ", press)
# play turns white when pressed
        if x == 2 and y == 2:
            print("Pressed Play: ", press)
            trellis.pixels[2, 2] = WHITE
# stop turns play back to lit
        if x == 2 and y == 3:
            print("Pressed stop: ", press)
            trellis.pixels[2, 2] = trls[2][2][1]
# record alternates between white and lit
        if x == 0 and y == 2:
            if trls[x][y][2] == 1:
                trls[x][y][2] = 0
                trellis.pixels[x,y] = WHITE
            else:
                trls[x][y][2] = 1
                trellis.pixels[x, y] = trls[x][y][1]
    current_press = pressed

""" This is the basic turn on/off when pressed) code.  We're not using this.
        But since it may be useful, i'm leaving it here commented out.
        if trls[x][y][2] == 0:  # if off, turn on.
            print("Turning on: ", press)
            trls[x][y][2] = 1
            trellis.pixels[x, y] = trls[x][y][1]
        else:  # if on, turn off
            print("turning off: ", press)
            trls[x][y][2] = 0
            trellis.pixels[x, y] = BLACK
"""