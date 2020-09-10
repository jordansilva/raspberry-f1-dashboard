from .services import F12019Socket
from .services import F12020Socket

class Telemetry():

    F1_VERSION = 2020

    def __init__(self, ctx):
        self.threads = []
        self.ctx = ctx

    def connect(self):
        socket = self.initF1Socket(self.F1_VERSION)
        self.threads.append(socket)
        socket.start()

    def onLapReady(self, data):
        self.ctx.setContextProperty("lap", data)

    def onCarReady(self, data):
        self.ctx.setContextProperty("car", data)

    def onCarStatusReady(self, data):
        self.ctx.setContextProperty("carStatus", data)

    def onRaceUpdate(self, data):
        self.ctx.setContextProperty("raceStatus", data)

    def initF1Socket(self, version):
        if (version == 2019):
            socket = F12020Socket()
            socket.lap.connect(self.onLapReady)
            socket.car.connect(self.onCarReady)
            socket.carStatus.connect(self.onCarStatusReady)
            return socket
        elif (version == 2020):
            socket = F12020Socket()
            socket.raceStatus.connect(self.onRaceUpdate)
            return socket
        else:
            return null

