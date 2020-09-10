from ..wheel import RevLights
from .. import UIObject, UILog


class RevProcessor(UIObject):

    LED_COUNT = 16

    def __init__(self):
        try:
            self.lights = [False] * self.LED_COUNT
            self.ui = RevLights(brightness=80)
            print("Rev Initialised!")
        except Exception as e:
            print("Error ", e)
            self.ui = UILog()

    def process(self, data):
        drs = data['drs']
        percentage = data['percentage']

        self.lights[0] = bool(drs['active'] or drs['allowed'])
        self.lights[1] = bool(drs['active'])
        self.lights[2] = False

        # green lights
        self.lights[3] = percentage >= 5
        self.lights[4] = percentage >= 10
        self.lights[5] = percentage >= 20

        # red lights
        self.lights[6] = percentage >= 30
        self.lights[7] = percentage >= 40
        self.lights[8] = percentage >= 50
        self.lights[9] = percentage >= 60
        self.lights[10] = percentage >= 70

        # blue lights
        self.lights[11] = percentage >= 80 
        self.lights[12] = percentage >= 85
        self.lights[13] = percentage >= 90
        self.lights[14] = percentage >= 92
        self.lights[15] = percentage >= 95

        self.ui.process(self.lights)