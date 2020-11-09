# This short script allows the faders on any of the Roland consoles
# show a demo type wave. It sends commands via telnet to the ip specified below.
# Make sure to update the number of faders so it shows on the whole console.
#
# NOTE: This may damage your faders, not sure what other effects it may have on
# the hardware. No warranty is implied.
#
# This has been tested on a Roland M-200i, but should work on other consoles
# as well.
# © Gabriel Csizmadia 2020

import telnetlib
import math
import time

mixer_ip = "192.168.0.100"
mixer_number_of_faders = 16

try:
    mixer = telnetlib.Telnet(host=mixer_ip, port=8023)
except TimeoutError:
    print("Timeout, check IP and try again.")


def translate(value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min
    value_scaled = float(value - left_min) / float(left_span)
    return right_min + (value_scaled * right_span)


def generate_and_send_frame(frame_number):
    print(f"Sending {frame_number}")
    for fader in range(1, mixer_number_of_faders+1):
        mixer.write(f"FDC:I{fader},{str(round(translate(math.sin(fader / 2 - frame_number * (2 * math.pi / 10)) + 1, 0, 2,-80, 10), 1))};\r\n".encode("ascii"))
        time.sleep(0.01)


while True:
    for i in range(0, 10):
        generate_and_send_frame(i)
