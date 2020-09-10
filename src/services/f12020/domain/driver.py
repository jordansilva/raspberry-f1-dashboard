import time

class Driver():

    MINISECTOR_GAP = 100  # mini sector each 100 meters

    def __init__(self, participant):
        self.participant = participant

        self.motion = None
        self.lapData = None
        self.setup = None
        self.telemetry = None
        self.status = None

        self.miniSectors = {}
        self.fuelUsed = {}

    def update_lap(self, lap):
        self.lapData = lap
        self.process_minisector(lap.currentLapNum, lap.lapDistance)
        # self.processStint(lap.currentLapNum)
        self.process_fuel(lap.currentLapNum)

    def process_minisector(self, lapNum, lapDistance):
        if (lapDistance <= 0 and lapNum <= 0):
            return

        minisectorId = int(lapDistance / self.MINISECTOR_GAP)
        if lapNum not in self.miniSectors:
            self.miniSectors[lapNum] = {0: time.time_ns() // 1000000}
        elif minisectorId not in self.miniSectors[lapNum]:
            self.miniSectors[lapNum][minisectorId] = time.time_ns() // 1000000

    def process_fuel(self, lapNum):
        if self.status == None:
            return

        if lapNum-1 not in self.fuelUsed:
            self.fuelUsed[lapNum - 1] = self.status.fuelInTank
