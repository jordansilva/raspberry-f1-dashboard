# import math
# import RPi.GPIO as IO
# import threading
# from time import sleep, localtime
# # from tqdm import tqdm

# # IO.setwarnings(False)
# IO.setmode(IO.BCM)

# HexDigits = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F,
#              0x6F, 0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71, 0x3D, 0x76,
#              0x06, 0x1E, 0x76, 0x38, 0x55, 0x54, 0x3F, 0x73, 0x67,
#              0x50, 0x6D, 0x78, 0x3E, 0x1C, 0x2A, 0x76, 0x6E, 0x5B,
#              0x00, 0x40, 0x63, 0xFF]

# ADDR_AUTO = 0x40
# ADDR_FIXED = 0x44
# STARTADDR = 0xC0
# # DEBUG = False


# class TM1637:
#     __doublePoint = False
#     __Clkpin = 0
#     __Datapin = 0
#     __brightness = 1.0  # default to max brightness
#     __currentData = [0, 0, 0, 0]

#     def __init__(self, CLK, DIO, brightness):
#         self.__Clkpin = CLK
#         self.__Datapin = DIO
#         self.__brightness = brightness
#         IO.setup(self.__Clkpin, IO.OUT)
#         IO.setup(self.__Datapin, IO.OUT)

#     def cleanup(self):
#         """Stop updating clock, turn off display, and cleanup GPIO"""
#         self.StopClock()
#         self.Clear()
#         IO.cleanup()

#     def Clear(self):
#         b = self.__brightness
#         point = self.__doublePoint
#         self.__brightness = 0
#         self.__doublePoint = False
#         data = [0x7F, 0x7F, 0x7F, 0x7F]
#         self.Show(data)
#         # Restore previous settings:
#         self.__brightness = b
#         self.__doublePoint = point

#     def ShowInt(self, i):
#         s = str(i)
#         self.Clear()
#         for i in range(0, len(s)):
#             self.Show1(i, int(s[i]))

#     def Show(self, data):
#         for i in range(0, 4):
#             try:
#                 self.__currentData[i] = data[i]
#             except:
#                 self.__currentData[i] = None

#         self.start()
#         self.writeByte(ADDR_AUTO)
#         self.br()
#         self.writeByte(STARTADDR)
#         for i in range(0, 4):
#             self.writeByte(self.coding(data[i]))
#         self.br()
#         self.writeByte(0x88 + int(self.__brightness))
#         self.stop()

#     def Show1(self, DigitNumber, data):
#         """show one Digit (number 0...3)"""
#         if(DigitNumber < 0 or DigitNumber > 3):
#             return  # error

#         self.__currentData[DigitNumber] = data

#         self.start()
#         self.writeByte(ADDR_FIXED)
#         self.br()
#         self.writeByte(STARTADDR | DigitNumber)
#         self.writeByte(self.coding(data))
#         self.br()
#         self.writeByte(0x88 + int(self.__brightness))
#         self.stop()
#     # Scrolls any integer n (can be more than 4 digits) from right to left display.

#     def ShowScroll(self, n):
#         n_str = str(n)
#         k = len(n_str)

#         for i in range(0, k + 4):
#             if (i < k):
#                 self.Show([int(n_str[i-3]) if i-3 >= 0 else None, int(n_str[i-2]) if i-2 >= 0 else None,
#                            int(n_str[i-1]) if i-1 >= 0 else None, int(n_str[i]) if i >= 0 else None])
#             elif (i >= k):
#                 self.Show([int(n_str[i-3]) if (i-3 < k and i-3 >= 0) else None, int(n_str[i-2]) if (
#                     i-2 < k and i-2 >= 0) else None, int(n_str[i-1]) if (i-1 < k and i-1 >= 0) else None, None])
#             sleep(1)

#     def SetBrightness(self, percent):
#         """Accepts percent brightness from 0 - 1"""
#         max_brightness = 7.0
#         brightness = math.ceil(max_brightness * percent)
#         if (brightness < 0):
#             brightness = 0
#         if(self.__brightness != brightness):
#             self.__brightness = brightness
#             self.Show(self.__currentData)

#     def ShowDoublepoint(self, on):
#         """Show or hide double point divider"""
#         if(self.__doublePoint != on):
#             self.__doublePoint = on
#             self.Show(self.__currentData)

#     def writeByte(self, data):
#         for i in range(0, 8):
#             IO.output(self.__Clkpin, IO.LOW)
#             if(data & 0x01):
#                 IO.output(self.__Datapin, IO.HIGH)
#             else:
#                 IO.output(self.__Datapin, IO.LOW)
#             data = data >> 1
#             IO.output(self.__Clkpin, IO.HIGH)

#         # wait for ACK
#         IO.output(self.__Clkpin, IO.LOW)
#         IO.output(self.__Datapin, IO.HIGH)
#         IO.output(self.__Clkpin, IO.HIGH)
#         IO.setup(self.__Datapin, IO.IN)

#         while(IO.input(self.__Datapin)):
#             sleep(0.001)
#             if(IO.input(self.__Datapin)):
#                 IO.setup(self.__Datapin, IO.OUT)
#                 IO.output(self.__Datapin, IO.LOW)
#                 IO.setup(self.__Datapin, IO.IN)
#         IO.setup(self.__Datapin, IO.OUT)

#     def start(self):
#         """send start signal to TM1637"""
#         IO.output(self.__Clkpin, IO.HIGH)
#         IO.output(self.__Datapin, IO.HIGH)
#         IO.output(self.__Datapin, IO.LOW)
#         IO.output(self.__Clkpin, IO.LOW)

#     def stop(self):
#         IO.output(self.__Clkpin, IO.LOW)
#         IO.output(self.__Datapin, IO.LOW)
#         IO.output(self.__Clkpin, IO.HIGH)
#         IO.output(self.__Datapin, IO.HIGH)

#     def br(self):
#         """terse break"""
#         self.stop()
#         self.start()

#     def coding(self, data):
#         if(self.__doublePoint):
#             pointData = 0x80
#         else:
#             pointData = 0

#         if(data == 0x7F or data is None):
#             data = 0
#         else:
#             data = HexDigits[data] + pointData
#         return data

#     def clock(self, military_time):
#         """Clock script modified from:
#             https://github.com/johnlr/raspberrypi-tm1637"""
#         self.ShowDoublepoint(True)
#         while (not self.__stop_event.is_set()):
#             t = localtime()
#             hour = t.tm_hour
#             if not military_time:
#                 hour = 12 if (t.tm_hour % 12) == 0 else t.tm_hour % 12
#             d0 = hour // 10 if hour // 10 else 36
#             d1 = hour % 10
#             d2 = t.tm_min // 10
#             d3 = t.tm_min % 10
#             digits = [d0, d1, d2, d3]
#             self.Show(digits)
#             # # Optional visual feedback of running alarm:
#             # print digits
#             # for i in tqdm(range(60 - t.tm_sec)):
#             for i in range(60 - t.tm_sec):
#                 if (not self.__stop_event.is_set()):
#                     sleep(1)

#     def StartClock(self, military_time=True):
#         # Stop event based on: http://stackoverflow.com/a/6524542/3219667
#         self.__stop_event = threading.Event()
#         self.__clock_thread = threading.Thread(
#             target=self.clock, args=(military_time,))
#         self.__clock_thread.start()

#     def StopClock(self):
#         try:
#             print('Attempting to stop live clock')
#             self.__stop_event.set()
#         except:
#             print('No clock to close')


# if __name__ == "__main__":
#     """Confirm the display operation"""
#     display = TM1637(CLK=23, DIO=18, brightness=1.0)

#     display.Clear()

#     digits = [1, 2, 3, 4]
#     display.Show(digits)
#     print("1234  - Working? (Press Key)")
#     scrap = raw_input()

#     print("Updating one digit at a time:")
#     display.Clear()
#     display.Show1(1, 3)
#     sleep(0.5)
#     display.Show1(2, 2)
#     sleep(0.5)
#     display.Show1(3, 1)
#     sleep(0.5)
#     display.Show1(0, 4)
#     print("4321  - (Press Key)")
#     scrap = raw_input()

#     print("Add double point\n")
#     display.ShowDoublepoint(True)
#     sleep(0.2)
#     print("Brightness Off")
#     display.SetBrightness(0)
#     sleep(0.5)
#     print("Full Brightness")
#     display.SetBrightness(1)
#     sleep(0.5)
#     print("30% Brightness")
#     display.SetBrightness(0.3)
#     sleep(0.3)

    # See clock.py for how to use the clock functions!

#https://github.com/Bogdanel/Raspberry-Pi-Python-3-TM1637-Clock
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

HEXDIGITS = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f]

HEXLETTERS = {
    'A': 0x77,
    'B': 0x7f,
    'b': 0x7C,
    'C': 0x39,
    'c': 0x58,
    'D': 0x3f,
    'd': 0x5E,
    'E': 0x79,
    'F': 0x71,
    'G': 0x7d,
    'H': 0x76,
    'h': 0x74,
    'I': 0x06,
    'J': 0x1f,
    'K': 0x76,
    'L': 0x38,
    'l': 0x06,
    'n': 0x54,
    'O': 0x3f,
    'o': 0x5c,
    'P': 0x73,
    'r': 0x50,
    'S': 0x6d,
    'U': 0x3e,
    'V': 0x3e,
    'Y': 0x66,
    'Z': 0x5b,
    ' ': 0x00,
    'T1': 0x07,
    'T2': 0x31,
    'M1': 0x33,
    'M2': 0x27,
    'W1': 0x3c,
    'W2': 0x1e,
}

ADDR_AUTO = 0x40
ADDR_FIXED = 0x44
STARTADDR = 0xC0
BRIGHT_DARKEST = 0
BRIGHT_DEFAULT = 2
BRIGHT_HIGHEST = 7
OUTPUT = GPIO.OUT
INPUT = GPIO.IN
LOW = GPIO.LOW
HIGH = GPIO.HIGH


class TM1637:
    __doublepoint = False
    __clk_pin = 0
    __data_pin = 0
    __brightness = BRIGHT_DEFAULT
    __current_data = [' ', ' ', ' ', ' ']

    def __init__(self, clock_pin, data_pin, brightness=BRIGHT_DEFAULT, cs_pin=None):
        self.__clk_pin = clock_pin
        self.__data_pin = data_pin
        self.__cs_pin = cs_pin
        self.__brightness = brightness
        GPIO.setup(self.__clk_pin, OUTPUT)
        GPIO.setup(self.__data_pin, OUTPUT)
        if self.__cs_pin:
            print("CS PIN ON: ", self.__cs_pin)
            GPIO.setup(self.__cs_pin, OUTPUT)
            GPIO.output(self.__cs_pin, HIGH)

    def clear(self):
        b = self.__brightness
        point = self.__doublepoint
        self.__brightness = 0
        self.__doublepoint = False
        data = [' ', ' ', ' ', ' ']
        self.display(data)
        self.__brightness = b
        self.__doublepoint = point

    def display(self, data):
        for i in range(4):
            try:
                self.__current_data[i] = data[i]
            except:
                self.__current_data[i] = ' '

        self.start()
        self.write_byte(ADDR_AUTO)
        self.stop()
        self.start()
        self.write_byte(STARTADDR)
        for i in range(4):
            self.write_byte(self.encode(self.__current_data[i]))
        self.stop()
        self.start()
        self.write_byte(0x88 + self.__brightness)
        self.stop()

    def displayAt(self, index, value):
        if index not in range(4):
            pass

        self.__current_data[index] = value;

        self.start()
        self.write_byte(ADDR_FIXED)
        self.stop()
        self.start()
        self.write_byte(STARTADDR | index)
        self.write_byte(self.encode(value))
        self.stop()
        self.start()
        self.write_byte(0x88 + self.__brightness)
        self.stop()

    def set_brightness(self, brightness):
        brightness = min(BRIGHT_HIGHEST, max(brightness, BRIGHT_DARKEST)) #between 0-7
        self.__brightness = brightness
        self.display(self.__current_data)

    def set_doublepoint(self, value):
        self.__doublepoint = value
        self.display(self.__current_data)

    def encode(self, data):
        point = 0x80 if self.__doublepoint else 0x00;

        if data == 0x7F:
            data = 0
        elif data in HEXLETTERS:
            data = HEXLETTERS[data] + point
        else:
            data = HEXDIGITS[data] + point
        return data

    def write_byte(self, data):
        for i in range(8):
            GPIO.output(self.__clk_pin, LOW)
            if data & 0x01:
                GPIO.output(self.__data_pin, HIGH)
            else:
                GPIO.output(self.__data_pin, LOW)
            data >>= 1
            GPIO.output(self.__clk_pin, HIGH)

        GPIO.output(self.__clk_pin, LOW)
        GPIO.output(self.__data_pin, HIGH)
        GPIO.output(self.__clk_pin, HIGH)
        GPIO.setup(self.__data_pin, INPUT)

        while GPIO.input(self.__data_pin):
            time.sleep(0.001)
            if GPIO.input(self.__data_pin):
                GPIO.setup(self.__data_pin, OUTPUT)
                GPIO.output(self.__data_pin, LOW)
                GPIO.setup(self.__data_pin, INPUT)
        GPIO.setup(self.__data_pin, OUTPUT)

    def start(self):
        GPIO.output(self.__clk_pin, HIGH)
        GPIO.output(self.__data_pin, HIGH)
        GPIO.output(self.__data_pin, LOW)
        GPIO.output(self.__clk_pin, LOW)

    def stop(self):
        GPIO.output(self.__clk_pin, LOW)
        GPIO.output(self.__data_pin, LOW)
        GPIO.output(self.__clk_pin, HIGH)
        GPIO.output(self.__data_pin, HIGH)

    def cleanup(self):
        GPIO.cleanup(self.__clk_pin)
        GPIO.cleanup(self.__data_pin)
