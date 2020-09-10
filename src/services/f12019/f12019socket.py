import socket
import pickle
import time

from f1_2019_telemetry.packets import unpack_udp_packet, PacketID, EventStringCode
from .utils.formatHelper import deltaBetween
from .utils.uiHelper import mapToLapViewState, mapToCarTelemetryViewState, mapToCarStatusViewState
from .utils.enums import ResultStatus
from .driver import Driver
from termcolor import colored
from ..publisher import Publisher

import threading

from PyQt5.QtCore import pyqtSignal, QThread

# class F12019Socket(QThread):
# lap = pyqtSignal(object)
# car = pyqtSignal(object)
# carStatus = pyqtSignal(object)


class F12019Socket(threading.Thread):

    lap = Publisher()
    car = Publisher()
    carStatus = Publisher()

    myCarIndex = None
    pitLimiter = False
    drsAllowed = False
    drivers = []
    positions = {}

    def __init__(self):
        # QThread.__init__(self)
        threading.Thread.__init__(self)
        self.lastPackets = {}

    def initSocket(self):
        udp_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_socket.bind(('', 20777))

        while True:
            udp_packet = udp_socket.recv(2048)
            packet = unpack_udp_packet(udp_packet)  # unpacking data
            self.processPacket(packet)

    # Only for testing
    def simulateData(self):
        with open("data/f1_5laps.pickle", "rb") as handler:
            data = pickle.load(handler)

        for packet in data:
            self.processPacket(packet)
            # time.sleep(0.01)

        print(colored("POS   NAME\t\tLAPS\tTOTAL\tSTATUS", 'green'))
        for pos, i in sorted(self.positions.items(), key=lambda item: item[0]):
            d = self.drivers[i]

            isMe = self.myCarIndex == i
            color = 'red' if isMe == i else 'grey'
            text = "%d   %s\t%d\t%.3f\t%s" % (d.lapData.carPosition,
                                              d.participant.name.decode(
                                                  'utf8'),
                                              len(d.previousLaps),
                                              sum(d.previousLaps.values())/60,
                                              ResultStatus(d.lapData.resultStatus).name)
            print(text)

            if isMe:
                print(self.carsDelta())

        return

    def getMyData(self):
        return self.drivers[self.myCarIndex]

    def processPacket(self, packet):
        self.lastPackets[packet.header.packetId] = packet

        if packet.header.packetId == PacketID.EVENT:
            self.updateEvent(packet)

        if packet.header.packetId == PacketID.PARTICIPANTS:
            self.updateParticipants(packet)

        if not self.drivers:
            return

        if packet.header.packetId == PacketID.MOTION:
            self.processMotion(packet)

        if packet.header.packetId == PacketID.LAP_DATA:
            self.processLapData(packet)

        if packet.header.packetId == PacketID.CAR_SETUPS:
            self.processCarSetup(packet)

        if packet.header.packetId == PacketID.CAR_TELEMETRY:
            self.processTelemetry(packet)

        if packet.header.packetId == PacketID.CAR_STATUS:
            self.processCarStatus(packet)

        return

    # (2019, 1, 3) : PacketEventData_V1

    def updateEvent(self, packet):
        if EventStringCode(packet.eventStringCode) == EventStringCode.SSTA:
            self.drivers = []

    # (2019, 1, 4) : ParticipantData_V1
    def updateParticipants(self, packet):
        self.myCarIndex = packet.header.playerCarIndex

        if not self.drivers:
            session = self.lastPackets[PacketID.SESSION]
            self.drivers = list(
                map(lambda p: Driver(p, session), packet.participants))
        else:
            for idx, participant in enumerate(packet.participants):
                self.drivers[idx].participant = participant

        return

    # (2019, 1, 0) : PacketMotionData_V1
    def processMotion(self, packet):
        for idx, carMotion in enumerate(packet.carMotionData):
            self.drivers[idx].carMotion = carMotion

    # (2019, 1, 2) : PacketLapData_V1
    def processLapData(self, packet):
        for idx, lap in enumerate(packet.lapData):
            self.drivers[idx].processMiniSectors(
                lap.currentLapNum, lap.lapDistance)

        for idx, lap in enumerate(packet.lapData):
            computeSectors = self.drivers[idx].processLapData(lap)
            self.positions[lap.carPosition] = idx

            if idx == self.myCarIndex and computeSectors:
                print(self.carsDelta())

        self.lap.emit(mapToLapViewState(self.getMyData()))

    def carsDelta(self):
        driver = self.getMyData()
        myPosition = driver.lapData.carPosition

        deltaA = 0
        deltaB = 0
        # driver ahead
        if myPosition > 1:
            driverAheadIdx = self.positions[myPosition - 1]
            driverAhead = self.drivers[driverAheadIdx]
            deltaA = deltaBetween(driverAhead, driver)

        # driver behind
        if myPosition < len(self.drivers):
            driverBehindIdx = self.positions[myPosition + 1]
            driverBehind = self.drivers[driverBehindIdx]
            deltaB = deltaBetween(driver, driverBehind)

        return [deltaA, deltaB]

    # (2019, 1, 5) : CarSetupData_V1
    def processCarSetup(self, packet):
        for idx, setup in enumerate(packet.carSetups):
            self.drivers[idx].carSetup = setup

    # (2019, 1, 6) : PacketCarTelemetryData_V1,
    def processTelemetry(self, packet):
        for idx, carTelemetry in enumerate(packet.carTelemetryData):
            self.drivers[idx].carTelemetry = carTelemetry

        self.car.emit(mapToCarTelemetryViewState(self.getMyData()))

    # (2019, 1, 7) : PacketCarStatusData_V1
    def processCarStatus(self, packet):
        for idx, carStatus in enumerate(packet.carStatusData):
            self.drivers[idx].carStatus = carStatus

        self.carStatus.emit(mapToCarStatusViewState(self.getMyData()))

    def run(self):
        #        self.initSocket()
        self.simulateData()
