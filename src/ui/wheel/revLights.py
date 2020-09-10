from rpi_ws281x import *
import time

class RevLights():
    DEFAULT_LED_COUNT=16
    DEFAULT_LED_PIN = 13
    DEFAULT_BRIGHTNESS = 100

    COLOR_GREEN = Color(0, 255, 0)
    COLOR_RED = Color(255, 0, 0)
    COLOR_BLUE = Color(0, 0, 255)
    COLOR_YELLOW = Color(255, 255, 0)
    COLOR_BLACK = Color(0, 0, 0)
    COLORS = [
        COLOR_GREEN, COLOR_GREEN, COLOR_YELLOW,
        COLOR_GREEN, COLOR_GREEN, COLOR_GREEN,
        COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED, COLOR_RED,
        COLOR_BLUE, COLOR_BLUE, COLOR_BLUE, COLOR_BLUE, COLOR_BLUE
    ]

    lights = []

    def __init__(self, ledCount=DEFAULT_LED_COUNT, ledPin=DEFAULT_LED_PIN, brightness=DEFAULT_BRIGHTNESS):
        self.initSetup(ledCount, ledPin, brightness)
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(
            self.ledCount,
            self.ledPin,
            self.ledFreqHz,
            self.ledDma,
            self.ledInvert,
            self.ledBrightness,
            self.ledChannel
        )
        self.strip.begin()
        self.lights = [self.COLOR_BLACK] * self.ledCount
        self.start()
        self.clear()

    def initSetup(self, ledCount, ledPin, ledBrightness):
        # LED strip configuration:
        self.ledCount       = ledCount
        self.ledPin         = ledPin
        self.ledFreqHz      = 800000
        self.ledDma         = 10
        self.ledBrightness  = ledBrightness
        self.ledChannel     = 1
        self.ledInvert      = False
        self.reverse        = True

    def displayLed(self, idx, color):
        idxLed = self.ledCount - 1 - idx if self.reverse else idx
        self.strip.setPixelColor(idxLed, color)
        self.strip.show()
        self.lights[idxLed] = color

    def displayLedWithDelay(self, idx, color, interval=.02):
        time.sleep(interval)
        self.displayLed(idx, color)

    def start(self):
        [self.displayLedWithDelay(i, self.COLOR_GREEN) for i in range(self.ledCount)]
        [self.displayLedWithDelay(i, self.COLOR_RED) for i in range(self.ledCount)]
        [self.displayLedWithDelay(i, self.COLOR_BLUE) for i in range(self.ledCount)]

    def clear(self):
        [self.displayLedWithDelay(i, self.COLOR_BLACK) for i in range(self.ledCount)]

    def process(self, rev):
        if len(rev) > self.strip.numPixels(): return

        for idx, r in enumerate(rev):
            color = self.COLORS[idx] if r == True else self.COLOR_BLACK
            self.displayLed(idx, color)
