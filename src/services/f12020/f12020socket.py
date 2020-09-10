import socket
import pickle
import time

from termcolor import colored
from f1_2020_telemetry.packets import unpack_udp_packet, PacketID, EventStringCode
from .domain.race import Race
from .domain.driver import Driver
from ..publisher import Publisher

import threading


class F12020Socket(threading.Thread):

    race = None
    raceStatus = Publisher()

    def __init__(self):
        threading.Thread.__init__(self)
        self.lastPackets = {}

    def initSocket(self):
        udp_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_socket.bind(('', 20777))

        while True:
            udp_packet = udp_socket.recv(2048)
            packet = unpack_udp_packet(udp_packet)  # unpacking data
            # self.process_packet(packet)
            self.raceStatus.emit(packet)

    ######
    # Process the F1 2020 packages received
    ######
    def process_packet(self, packet):
        if not self.race:
            self.race = Race(packet)

        self.lastPackets[packet.header.packetId] = packet

        if packet.header.packetId == PacketID.MOTION:
            self.process_motion(packet)
        if packet.header.packetId == PacketID.SESSION:
            self.process_session(packet)
        if packet.header.packetId == PacketID.LAP_DATA:
            self.process_lap(packet)
        if packet.header.packetId == PacketID.EVENT:
            self.process_event(packet)
        if packet.header.packetId == PacketID.PARTICIPANTS:
            self.process_participants(packet)
        if packet.header.packetId == PacketID.CAR_SETUPS:
            self.process_car_setup(packet)
        if packet.header.packetId == PacketID.CAR_TELEMETRY:
            self.process_telemetry(packet)
        if packet.header.packetId == PacketID.CAR_STATUS:
            self.process_car_status(packet)
        if packet.header.packetId == PacketID.FINAL_CLASSIFICATION:
            self.process_classification(packet)

        self.raceStatus.emit(self.race)

    # (2020, 1, 0) : PacketMotionData_V1
    def process_motion(self, packet):
        return self.race.update_motion(packet.carMotionData)

    # (2020, 1, 1) : PacketSessionData_V1
    def process_session(self, packet):
        return self.race.update_session(packet)

    # (2019, 1, 2) : PacketLapData_V1
    def process_lap(self, packet):
        self.race.update_participants_lap(packet.lapData)

    # (2020, 1, 3) : PacketEventData_V1
    def process_event(self, packet):
        if EventStringCode(packet.eventStringCode) == EventStringCode.SSTA:
            self.race = Race(packet)

    # (2019, 1, 4) : ParticipantData_V1
    def process_participants(self, packet):
        return self.race.update_participants(packet.participants)

    # (2019, 1, 5) : CarSetupData_V1
    def process_car_setup(self, packet):
        return self.race.update_participants_car_setup(packet.carSetups)

    # (2019, 1, 6) : PacketCarTelemetryData_V1,
    def process_telemetry(self, packet):
        return self.race.update_participants_car_telemetry(packet.carTelemetryData)

    # (2019, 1, 7) : PacketCarStatusData_V1
    def process_car_status(self, packet):
        return self.race.update_participants_car_status(packet.carStatusData)

    # (2019, 1, 8) : PacketFinalClassificationData_V1
    def process_classification(self, packet):
        return self.race.update_final_classification(packet.classificationData)

    def run(self):
        #self.initSocket()
        self.simulateData()

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

    # Only for testing

    def simulateData(self):
        with open("data/f1_2020_5laps.pickle", "rb") as handler:
            data = pickle.load(handler)

#        while True:
        for packet in data:
            self.process_packet(packet)
            # self.raceStatus.emit(packet)
            # time.sleep(0.01)

        if self.race.finalClassification:
            print(colored("POS   NAME\t\tLAPS\tTOTAL\tSTATUS", 'green'))
            for pos, i in enumerate(self.race.positions):
                d = self.race.drivers[i]
                print(self.race.finalClassification)
                f = self.race.finalClassification.classificationData[i]

                isMe = i == self.race.playerCarIndex
                color = 'red' if isMe == i else 'grey'
                text = "%d   %s\t%d\t%.3f\t%s" % (f.position,
                                                d.participant.name.decode('utf8'),
                                                f.numLaps,
                                                totalRaceTime/60,
                                                ResultStatus(f.resultStatus).name)
                print(text)

        return
