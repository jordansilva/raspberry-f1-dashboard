from ..wheel import Display
from .. import UIObject, UILog


class FourDigitsDisplayProcessor(UIObject):

    NUM_SPEED_DIGITS = 3

    def __init__(self):
        try:
            self.ui = Display()
            self.start()
            print("4-Digit display initialised!")
        except Exception as e:
            print(e)
            self.ui = UILog()

    def start(self):
        self.ui.clear()
        self.ui.display([0,0,0,0])
        self.ui.clear()

    def process(self, data):
        try:
            # self.ui.displayAt(0, data['gear'])
            speed = [x for x in str(data['speed']).rjust(self.NUM_SPEED_DIGITS, ' ')]
            for idx, value in enumerate(speed):
                self.ui.displayAt(idx+1, value)
        except Exception as e:
            print(e)
