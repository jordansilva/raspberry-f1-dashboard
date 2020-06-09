from src.f1socket import F1Socket

class Telemetry():

    def __init__(self, ctx):
        self.threads = []
        self.ctx = ctx

    def connect(self):
        socket = F1Socket()
        socket.lap.connect(self.onLapReady)
        socket.car.connect(self.onCarReady)
        socket.carStatus.connect(self.onCarStatusReady)
        self.threads.append(socket)
        socket.start()

    def onLapReady(self, data):
        self.ctx.setContextProperty("lap", data)

    def onCarReady(self, data):
        self.ctx.setContextProperty("car", data)
        self.ctx.setContextProperty("revLights", data["revLightsPercent"])

    def onCarStatusReady(self, data):
        self.ctx.setContextProperty("carStatus", data)
