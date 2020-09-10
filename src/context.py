from .ui.processors import RevProcessor, FourDigitsDisplayProcessor, EightDigitsDisplayProcessor
from .ui import UILog
import json


class Context:
    data = {}

    def __init__(self):
        self.data = {}
        self.initUi()

    def initUi(self):
        try:
            print("Initialising processors...")
            self.revProcessor = RevProcessor()
            self.fourDigitProcessor = FourDigitsDisplayProcessor()
            self.eightDigitProcessor = EightDigitsDisplayProcessor()
        except Exception as e:
            print("Error ", e)
            self.revProcessor = UILog()
            self.fourDigitDisplay = UILog()

    def setContextProperty(self, name, value):
        self.data[name] = value
        self.handleSignal(name, value)

    def handleSignal(self, name, value):
        # self.processRawPacket(value) 
        if name == 'raceStatus': self.processMyDriver(value.me())
        if name == 'revLights': self.revProcessor.process(value)
        if name == 'speed': 
            self.fourDigitProcessor.process(value)
            self.eightDigitProcessor.process(value)
        if name == 'carStatus':
            self.eightDigitProcessor.process(value)
        if name == 'lap':
            self.eightDigitProcessor.process(value)

    def processRawPacket(self, packet):
        carIdx = packet.header.playerCarIndex
            
        if packet.header.packetId == 2:
            lapData = packet.lapData[carIdx]
            self.eightDigitProcessor.process({ 
                'sector1': lapData.sector1TimeInMS, 'sector2': lapData.sector2TimeInMS, 
                'lastLap': lapData.lastLapTime, 'pitStatus': lapData.pitStatus,
                'currentLapNum': lapData.currentLapNum
                })
        

        if packet.header.packetId == 6:
            telemetry = packet.carTelemetryData[carIdx]
            self.fourDigitProcessor.process({ 'speed': telemetry.speed })
            self.revProcessor.process({'percentage': telemetry.revLightsPercent,
                                            'drs': {
                                                'allowed': False,
                                                'active': telemetry.drs}
                                            })
            self.eightDigitProcessor.process({ 'gear': telemetry.gear })

        if packet.header.packetId == 7:
            carStatusData = packet.carStatusData[carIdx]
            self.eightDigitProcessor.process({'fuelInTank': carStatusData.fuelInTank, 'fuelRemainingLaps': carStatusData.fuelRemainingLaps })

    def processMyDriver(self, me):
        if not me:
            return

        if me.lapData:
            self.handleSignal('lap', { 
                'sector1': me.lapData.sector1TimeInMS, 'sector2': me.lapData.sector2TimeInMS, 'lastLap': me.lapData.lastLapTime,
                'pitStatus': me.lapData.pitStatus, 'currentLapNum': me.lapData.currentLapNum
                })


        if me.telemetry:
            self.handleSignal('speed', { 'gear': me.telemetry.gear, 'speed': me.telemetry.speed })
            self.handleSignal('revLights', {'percentage': me.telemetry.revLightsPercent,
                                            'drs': {
                                                'allowed': me.status.drsAllowed if me.status else False,
                                                'active': me.telemetry.drs}
                                            })
        if me.status:
            self.handleSignal('carStatus', { 'fuelInTank': me.status.fuelInTank, 'fuelRemainingLaps': me.status.fuelRemainingLaps })
