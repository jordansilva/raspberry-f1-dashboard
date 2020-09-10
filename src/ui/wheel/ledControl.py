import time
from datetime import datetime

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment

import RPi.GPIO as GPIO

class LedControl():

    def __init__(self):
        # create seven segment device
        serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(serial, cascaded=1)
        self.seg = sevensegment(self.device)

        # Brightness
        # print('Brightness...')
        # for x in range(5):
        #     for intensity in range(16):
        #         seg.device.contrast(intensity * 16)
        #         time.sleep(0.1)
        # device.contrast(0x7F)

    def clock(self, seconds):
        """
        Display current time on device.
        """
        interval = 0.5
        for i in range(int(seconds / interval)):
            now = datetime.now()
            self.seg.text = now.strftime("%H-%M-%S")

            # calculate blinking dot
            if i % 2 == 0:
                self.seg.text = now.strftime("%H-%M-%S")
            else:
                self.seg.text = now.strftime("%H %M %S")

            time.sleep(interval)


    def show_message_vp(self, msg, delay=0.1):
        # Implemented with virtual viewport
        width = self.device.width
        padding = " " * width
        msg = padding + msg + padding
        n = len(msg)

        virtual = viewport(self.device, width=n, height=8)
        sevensegment(virtual).text = msg
        for i in reversed(list(range(n - width))):
            virtual.set_position((i, 0))
            time.sleep(delay)

    def show_text(self, text):
        if len(text.replace('.', '')) <= self.device.width:
            self.seg.text = text
        else:
            # show_message_alt - Does same as above but does string slicing itself
            width = self.device.width
            padding = " " * width
            text = padding + text + padding

            for i in range(len(text)):
                self.seg.text = text[i:i + width]
                time.sleep(0.1)

    def show_char(self, index, text):
        if index < self.device.width: 
            self.seg.text[index] = str(text)
        else:
            self.seg.text[self.device.width - 1] = srt(text)

    def test(self):
        for _ in range(8):
            self.show_text("HELLO")
            time.sleep(0.6)
            self.show_text(" GOODBYE")
            time.sleep(0.6)

        for i, ch in enumerate([9, 8, 7, 6, 5, 4, 3, 2]):
            self.show_char(i, ch)
            time.sleep(0.6)

        for i in range(len(self.seg.text)):
            del self.seg.text[0]
            time.sleep(0.6)

        # Scrolling Alphabet Text
        self.show_text("HELLO EVERYONE!")
        self.show_text("PI is 3.14159 ... ")
        self.show_text("IP is 127.0.0.1 ... ")
        self.show_text("0123456789 abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        # Digit futzing
        self.clock(seconds=10)