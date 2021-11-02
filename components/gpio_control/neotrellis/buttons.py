import time
import numpy
import math
from subprocess import check_call
from signal import pause
from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis

# create the i2c object for the trellis
i2c = busio.I2C(SCL, SDA)

while not busio.I2C.try_lock:
   pass

# create the trellis
trellis = NeoTrellis(i2c, False, addr=0x2E)

# some color definitions
OFF = [0, 0, 0]
EMPTY = [20, 20, 20]
GRAY = [128, 255, 128]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
ROSE = [255, 0, 128]
MAGENTA = [255, 0, 255]
VIOLET = [128, 0, 255]
BLUE = [0, 0, 255]
AZURE = [0, 128, 255]
CYAN = [0, 255, 255]
SPRINGGREEN = [0, 255, 128]
GREEN = [0, 255, 0]
CHARTREUSE = [128, 255, 0]
YELLOW = [255, 255, 0]
ORANGE = [255, 128, 0]

# define button dictionaries for neotrellis
buttons = [
    {   # rainy
        "command": "~/RPi-Jukebox-RFID/scripts/rfid_trigger_play.sh --cardid=0003536651",
        "color": BLUE
    },
    {   # dance
        "command": "~/RPi-Jukebox-RFID/scripts/rfid_trigger_play.sh --cardid=0010009126",
        "color": MAGENTA
    },
    {   # sunny
        "command": "~/RPi-Jukebox-RFID/scripts/rfid_trigger_play.sh --cardid=0003271620",
        "color": YELLOW
    },
    {   # beautiful
        "command": "~/RPi-Jukebox-RFID/scripts/rfid_trigger_play.sh --cardid=0003714140",
        "color": VIOLET
    },
    {   # roar
        "command": "~/RPi-Jukebox-RFID/scripts/rfid_trigger_play.sh --cardid=0003714999",
        "color": ORANGE
    },
    {   # kids songs
        "command": "~/RPi-Jukebox-RFID/scripts/rfid_trigger_play.sh --cardid=0003536785",
        "color": RED
    },
    {   # story pirates
        "command": "~/RPi-Jukebox-RFID/scripts/rfid_trigger_play.sh --cardid=0003268847",
        "color": AZURE
    },
    {   # 
        "command": "",
        "color": EMPTY
    },
    {   # 
        "command": "",
        "color": EMPTY
    },
    {   # 
        "command": "",
        "color": EMPTY
    },
    {   # 
        "command": "",
        "color": EMPTY
    },
    {   # 
        "command": "",
        "color": EMPTY
    },
    {   # 
        "command": "",
        "color": EMPTY
    },
    {   # prev
        "command": "~/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=playerprev",
        "color": GREEN
    },
    {   # play/pause
        "command": "~/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=playerpause",
        "color": GREEN
    },
    {   # next
        "command": "~/RPi-Jukebox-RFID/scripts/playout_controls.sh -c=playernext",
        "color": GREEN
    }
]

dimmed_colors = [None] * 16

for i in range(16):
    divider = 8
    dimmed_color = [ math.ceil(x / divider) for x in buttons[i]["color"] ]
    dimmed_colors[i] = dimmed_color

print(dimmed_colors[2])

# this will be called when button events are received
def blink(event):
    print(event.number)

    # turn the LED on when a rising edge is detected
    if event.edge == NeoTrellis.EDGE_RISING:
        trellis.pixels[event.number] = buttons[event.number]["color"]
    # turn the LED off when a rising edge is detected
    elif event.edge == NeoTrellis.EDGE_FALLING:
        print(buttons[event.number]["command"])
        trellis.pixels[event.number] = dimmed_colors[event.number]
        check_call(buttons[event.number]["command"], shell=True)

for i in range(16):
    # activate rising edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_RISING)
    # activate falling edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
    # set all keys to trigger the blink callback
    trellis.callbacks[i] = blink

    # cycle the LEDs on startup
    trellis.pixels[i] = dimmed_colors[i]
    time.sleep(0.1)


while True:
    # call the sync function call any triggered callbacks
    trellis.sync()
    # the trellis can only be read every 17 millisecons or so
    time.sleep(0.02)
