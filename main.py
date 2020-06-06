# This Python file uses the following encoding: utf-8
import sys
import os

import json
import socket
from f1_2019_telemetry.packets import unpack_udp_packet, PacketID

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtProperty, QObject
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt5.QtWidgets import QApplication, QLabel

class F1Socket(QtCore.QThread):

    lap = QtCore.pyqtSignal(object)
    car = QtCore.pyqtSignal(object)
    carStatus = QtCore.pyqtSignal(object)

    def getMapGear(self, gear):
        if gear > 0:
            return gear
        elif gear == 0:
            return 'N'
        else:
            return 'R'


    def __init__(self):
        QtCore.QThread.__init__(self)

    def resetData(self):
        data = { "currentLapTime": "--:--.---", "currentLapNum": 0, "position": 0, "pitStatus": 0 }
        self.lap.emit(data)
        data = { "gear": "P", "speed": 0, "drs": 0, "revLightsPercent": 0, "tyresSurfaceTemperature": [0,0,0,0], "engineRPM": 0 }
        self.car.emit(data)
        data = { "drsAllowed": False, "ersStoreEnergy": 0, "ersDeployMode": 0, "ersStoreEnergyPercentage": 0, "ersHarvestedThisLap": 0, "ersDeployedThisLap": 0, "pitLimiterStatus": False }
        self.carStatus.emit(data)

    def run(self):
        self.resetData()
        udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_socket.bind(('', 20777))

        while True:
            udp_packet = udp_socket.recv(2048)
            packet = unpack_udp_packet(udp_packet)
            carIndex = packet.header.playerCarIndex

            # (2019, 1, 2) : PacketLapData_V1
            if packet.header.packetId == PacketID.LAP_DATA:
                data = packet.lapData[carIndex]
                data.bestLapTime - data.currentLapTime
                currentLapTime = "%d:%.3f" % divmod(data.currentLapTime, 60)
                data = {
                    "currentLapTime": currentLapTime,
                    "currentLapNum": data.currentLapNum,
                    "position": data.carPosition,
                    "pitStatus": data.pitStatus,
                }
                self.lap.emit(data)

            # (2019, 1, 6) : PacketCarTelemetryData_V1,
            if packet.header.packetId == PacketID.CAR_TELEMETRY:
                carTelemetry = packet.carTelemetryData[carIndex]
                tyresSurfaceTemperature = [ carTelemetry.tyresSurfaceTemperature[0], carTelemetry.tyresSurfaceTemperature[1], carTelemetry.tyresSurfaceTemperature[2], carTelemetry.tyresSurfaceTemperature[3]]
                data = {
                    "gear": self.getMapGear(carTelemetry.gear),
                    "speed": carTelemetry.speed,
                    "drs": carTelemetry.drs,
                    "revLightsPercent": carTelemetry.revLightsPercent,
                    "tyresSurfaceTemperature": tyresSurfaceTemperature,
                    "engineRPM": carTelemetry.engineRPM
                }
                self.car.emit(data)

            # (2019, 1, 7) : PacketCarStatusData_V1
            if packet.header.packetId == PacketID.CAR_STATUS:
                carStatus = packet.carStatusData[carIndex]
                ersHarvestedThisLap = carStatus.ersHarvestedThisLapMGUK + carStatus.ersHarvestedThisLapMGUH
                data = {
                    "drsAllowed": carStatus.drsAllowed,
                    "ersStoreEnergy": carStatus.ersStoreEnergy,
                    "ersDeployMode": carStatus.ersDeployMode,
                    "ersStoreEnergyPercentage": carStatus.ersStoreEnergy / 40000,
                    "ersHarvestedThisLap": ersHarvestedThisLap,
                    "ersDeployedThisLap": 100-carStatus.ersDeployedThisLap,
                    "pitLimiterStatus": carStatus.pitLimiterStatus
                }
                self.carStatus.emit(data)


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
        ctx.setContextProperty("lap", data)

    def onCarReady(self, data):
        ctx.setContextProperty("car", data)

    def onCarStatusReady(self, data):
        ctx.setContextProperty("carStatus", data)

if __name__ == "__main__":
    # Setup the application window PyQt5
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)

    ctx = engine.rootContext()

    # Load QML File
    qml_file = os.path.join(os.path.dirname(__file__), "main.qml")
    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)

    telemetry = Telemetry(ctx)
    telemetry.connect()
    sys.exit(app.exec_())
