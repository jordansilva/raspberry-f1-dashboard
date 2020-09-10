from . import TM1637


class Display():

    def __init__(self, clock_pin=21, data_pin=20, brightness=7, pad_left=4, cs_pin=None):
        self.tm = TM1637(clock_pin, data_pin, brightness, cs_pin)
        self.pad_left = pad_left
        self.tm.start()

    def display(self, data):
        if data:
            if isinstance(data, int):
                self.tm.display([int(x) for x in str(data).rjust(self.pad_left, '0')])
            else:
                self.tm.display(list(data))
        else:
            self.tm.clear()

    def displayAt(self, index, value):
        if isinstance(value, int) or value.isdigit():
            self.tm.displayAt(index, int(value))
        else:
            self.tm.displayAt(index, value)

    def clear(self):
        self.tm.clear()

    def stop(self):
        self.tm.stop()