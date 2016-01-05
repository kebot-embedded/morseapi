import pygatt.backends
import time
import logging
import struct
import binascii
from colour import Color

logging.getLogger().setLevel(logging.DEBUG)

DEVICE_HANDLE = 19
COMMANDS={
    "neck_color":0x03,
    "eye_brightness":0x08,
    "eye":0x09,
    "left_ear_color":0x0b,
    "right_ear_color":0x0c,
    "head_color":0x0d,
    "head_pitch":0x07,
    "head_yaw":0x06,
    "say":0x18,
}

NOISES={
    k:v.decode("hex")
    for (k,v) in {
        "elephant":   "53595354454c455048414e545f300e460000",  # SYSTELEPHANT_0.F
        "tiresqueal": "535953545449524553515545414c0e460000",  # SYSTTIRESQUEAL.F
        "hi":         "53595354444153485f48495f564f0b00c900",  # SYSTDASH_HI_VO
        "bragging":   "535953544252414747494e4731410b232300",  # SYSTBRAGGING1A##
        "ohno":       "5359535456375f4f484e4f5f30390b000000",  # SYSTV7_OHNO_09
        "ayayay":     "53595354434f4e46555345445f310b000000",  # SYSTCONFUSED_1
        "confused2":  "53595354434f4e46555345445f320b000000",  # SYSTCONFUSED_2
        "confused3":  "53595354434f4e46555345445f330b000000",  # SYSTCONFUSED_3
        "confused5":  "53595354434f4e46555345445f350b000000",  # SYSTCONFUSED_5
        "confused8":  "53595354434f4e46555345445f380b000000",  # SYSTCONFUSED_8
        "brrp":       "53595354434f4e46555345445f360b000000",  # SYSTCONFUSED_6
        "charge":     "535953544348415247455f3033000b000000",  # SYSTCHARGE_03
    }.items()}

def one_byte_array(value):
    return bytearray(struct.pack(">B", value))

def two_byte_array(value):
    return bytearray(struct.pack(">H", value))

def color_byte_array(color_value):
    color = Color(color_value)
    return bytearray([
        int(color.get_red()*255),
        int(color.get_green()*255),
        int(color.get_blue()*255),
    ])

def angle_array(angle):
    if angle < 0:
        angle = (abs(angle) ^ 0xff) + 1
    return bytearray([angle & 0xff])

class WonderControl(object):
    def __init__(self, address):
        adapter = pygatt.backends.GATTToolBackend()
        adapter.start()
        self.device = adapter.connect(address, address_type='random')

    def command(self, command_name, command_values):
        message = bytearray([COMMANDS[command_name]]) + command_values
        logging.debug(binascii.hexlify(message))
        self.device.char_write_handle(DEVICE_HANDLE, message)

    def eye(self, value):
        self.command("eye", two_byte_array(value))

    def eye_brightness(self, value):
        self.command("eye_brightness", one_byte_array(value))

    def neck_color(self, color):
        self.command("neck_color", color_byte_array(color))

    def left_ear_color(self, color):
        self.command("left_ear_color", color_byte_array(color))

    def right_ear_color(self, color):
        self.command("right_ear_color", color_byte_array(color))

    def ear_color(self, color):
        self.left_ear_color(color)
        self.right_ear_color(color)

    def head_color(self, color):
        self.command("head_color", color_byte_array(value))

    def head_yaw(self, angle):
        """
        Angle range is from -53 to 53
        """
        angle = max(-53, angle)
        angle = min(53, angle)
        self.command("head_yaw", angle_array(angle))

    def head_pitch(self, angle):
        """
        Angle range is from -5 to 10
        """
        angle = max(-5, angle)
        angle = min(10, angle)
        self.command("head_pitch", angle_array(angle))

    def say(self, sound_name):
        self.command("say", bytearray(NOISES[sound_name]))


if __name__ == "__main__":
    wc = WonderControl("C0:F0:84:3C:51:FA")
    import pdb; pdb.set_trace()  # here you can experiment
