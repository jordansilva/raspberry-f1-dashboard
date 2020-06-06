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

import pickle
import time

class F1Socket(QtCore.QThread):

    MAX_ERS = 4000000

    lap = QtCore.pyqtSignal(object)
    car = QtCore.pyqtSignal(object)
    carStatus = QtCore.pyqtSignal(object)
    revBlink = QtCore.pyqtSignal(object)

    pitLimiter = False

    def __init__(self):
        QtCore.QThread.__init__(self)

    def resetData(self):
        data = { "currentLapTime": "--:--.---", "currentLapNum": 0, "position": 0, "pitStatus": 0 }
        self.lap.emit(data)
        data = { "gear": "P", "speed": 0, "drs": 0, "revLightsPercent": 0, "tyresSurfaceTemperature": [0,0,0,0], "engineRPM": 0 }
        self.car.emit(data)
        data = { "drsAllowed": False, "ersStoreEnergy": 0, "ersDeployMode": 0, "ersStoreEnergyPercentage": 0, "ersHarvestedThisLap": 0, "ersDeployedThisLap": 0, "pitLimiterStatus": False }
        self.carStatus.emit(data)

    def initSocket(self):
        self.resetData()
        udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_socket.bind(('', 20777))

        while True:
            udp_packet = udp_socket.recv(2048)
            packet = unpack_udp_packet(udp_packet) #unpacking data
            self.processPacket(packet)

    #Only for testing
    def simulateData(self):
        with open("data/f1_2laps.p", "rb") as handler:
            data = pickle.load(handler)

        while True:
            for packet in data:
                self.processPacket(packet)
                time.sleep(0.01)

    def processPacket(self, packet):
        carIndex = packet.header.playerCarIndex

        # (2019, 1, 1) : PacketSessionData_V1
        if packet.header.packetId == PacketID.SESSION:
            self.trackLength = packet.trackLength

        # (2019, 1, 2) : PacketLapData_V1
        if packet.header.packetId == PacketID.LAP_DATA:
            lap = packet.lapData[carIndex]
#            lap.bestLapTime - self.trackLength
            arrLapTime = divmod(lap.currentLapTime, 60)
            if arrLapTime[0] > 0:
                currentLapTime = "%d:%06.3f" % arrLapTime
            else:
                currentLapTime = "%06.3f" % arrLapTime[1]

            data = {
                "currentLapTime": currentLapTime,
                "currentLapNum": lap.currentLapNum,
                "position": lap.carPosition,
                "pitStatus": lap.pitStatus,
            }
            self.lap.emit(data)

        # (2019, 1, 6) : PacketCarTelemetryData_V1,
        if packet.header.packetId == PacketID.CAR_TELEMETRY:
            carTelemetry = packet.carTelemetryData[carIndex]
            tyresSurfaceTemperature = [ carTelemetry.tyresSurfaceTemperature[0], carTelemetry.tyresSurfaceTemperature[1], carTelemetry.tyresSurfaceTemperature[2], carTelemetry.tyresSurfaceTemperature[3]]
            tyresInnerTemperature = [ carTelemetry.tyresInnerTemperature[0], carTelemetry.tyresInnerTemperature[1], carTelemetry.tyresInnerTemperature[2], carTelemetry.tyresInnerTemperature[3]]
            brakesTemperature = [ carTelemetry.brakesTemperature[0], carTelemetry.brakesTemperature[1], carTelemetry.brakesTemperature[2], carTelemetry.brakesTemperature[3]]

            data = {
                "gear": self.getMapGear(carTelemetry.gear, self.pitLimiter),
                "speed": carTelemetry.speed,
                "drs": carTelemetry.drs,
                "revLightsPercent": self.mapRevLights(carTelemetry.revLightsPercent),
                "tyresSurfaceTemperature": tyresSurfaceTemperature,
                "tyresInnerTemperature": tyresInnerTemperature,
                "brakesTemperature": brakesTemperature,
                "engineRPM": carTelemetry.engineRPM
            }
            self.car.emit(data)
            self.revBlink.emit(carTelemetry.revLightsPercent == 100)

        # (2019, 1, 7) : PacketCarStatusData_V1
        if packet.header.packetId == PacketID.CAR_STATUS:
            carStatus = packet.carStatusData[carIndex]

            fuelRemainingLaps = "(+%.2f)" if carStatus.fuelRemainingLaps > 0 else "(-%.2f)"
            fuelRemainingLaps = fuelRemainingLaps % carStatus.fuelRemainingLaps

            ersPercentage = carStatus.ersStoreEnergy/self.MAX_ERS*100
            ersDeployed = 100-(carStatus.ersDeployedThisLap/self.MAX_ERS*100)
            ersHarvestedThisLap = (carStatus.ersHarvestedThisLapMGUK + carStatus.ersHarvestedThisLapMGUH)/self.MAX_ERS*100
            data = {
                "fuelMix": carStatus.fuelMix,
                "fuelRemainingLaps": fuelRemainingLaps,
                "pitLimiterStatus": carStatus.pitLimiterStatus,
                "drsAllowed": carStatus.drsAllowed,
                "ersStoreEnergy": carStatus.ersStoreEnergy,
                "ersDeployMode": carStatus.ersDeployMode,
                "ersStoreEnergy": ersPercentage,
                "ersStoreEnergyPercentage": int(ersPercentage),
                "ersHarvestedThisLap": ersHarvestedThisLap,
                "ersDeployedThisLap": ersDeployed,
                "pitLimiterStatus": carStatus.pitLimiterStatus
            }
            self.pitLimiter = carStatus.pitLimiterStatus == 1
            self.carStatus.emit(data)


    def getMapGear(self, gear, pitLimiter):
        if pitLimiter:
            return "P"
        elif gear > 0:
            return gear
        elif gear == 0:
            return 'N'
        else:
            return 'R'


    def mapRevLights(self, percent):
        lights = [False] * 15
        # green lights
        lights[0] = False
        lights[1] = False
        lights[2] = False
        lights[3] = False
        lights[4] = False
        # red lights
        lights[5] = percent >= 10
        lights[6] = percent >= 20
        lights[7] = percent >= 30
        lights[8] = percent >= 40
        lights[9] = percent >= 50
        # blue lights
        lights[10] = percent >= 60
        lights[11] = percent >= 70
        lights[12] = percent >= 80
        lights[13] = percent >= 85
        lights[14] = percent >= 92

        return lights

    def run(self):
#        self.initSocket()
        self.simulateData()


class Telemetry():

    timer = QtCore.QTimer()

    def __init__(self, ctx):
        self.threads = []
        self.ctx = ctx
        self.timer.timeout.connect(self.setRevBlink)

    def connect(self):
        socket = F1Socket()
        socket.lap.connect(self.onLapReady)
        socket.car.connect(self.onCarReady)
        socket.carStatus.connect(self.onCarStatusReady)
        socket.revBlink.connect(self.onRevBlink)
        self.threads.append(socket)
        socket.start()

    def onLapReady(self, data):
        ctx.setContextProperty("lap", data)

    def onCarReady(self, data):
        ctx.setContextProperty("car", data)
        ctx.setContextProperty("revLights", data["revLightsPercent"])

    def onCarStatusReady(self, data):
        ctx.setContextProperty("carStatus", data)

    def onRevBlink(self, data):
        if data == True:
            self.timer.start(100)
        else:
            self.setRevBlink(False)
            self.timer.stop()

    def setRevBlink(self, shouldBlink=True):
        ctx.setContextProperty("revBlink", False)
        ctx.setContextProperty("revBlink", shouldBlink)

if __name__ == "__main__":
    #pkill -9 python

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
