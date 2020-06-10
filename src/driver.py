import time
from .utils import Constants, DriverStatus, PitStatus, AiControlled, TyresCompound

class Driver:

    MAX_ERS = 4000000

    def __init__(self, participant, session):
        self.carMotion = None
        self.session = session
        self.lapData = None
        self.participant = participant
        self.carSetup = None
        self.carTelemetry = None
        self.carStatus = None

        self.lastPitStopLap = 0
        self.needProcessSectors = [True, True, True]
        self.bestSectors = [float('inf')] * 3
        self.lastSectors = [float('inf')] * 3

        self.previousLaps = {}
        self.miniSectors = {}
        self.fuelUsed = {}
        self.stints = []

    def processLapData(self, lap):
        self.lapData = lap

        self.processMiniSectors(lap.currentLapNum, lap.lapDistance)
        self.processStint(lap.currentLapNum)
        self.processFuel(lap.currentLapNum)
        self.processSectors(lap)

    def processMiniSectors(self, lapNum, lapDistance):
        if (lapDistance <= 0 and lapNum <= 0):
            return

        miniSectorIdx = int(lapDistance / Constants.MINISECTOR_GAP)

        if lapNum not in self.miniSectors:
            self.miniSectors[lapNum] = { 0: time.time_ns() // 1000000 }
        elif miniSectorIdx not in self.miniSectors[lapNum]:
            self.miniSectors[lapNum][miniSectorIdx] = time.time_ns() // 1000000


    def processStint(self, lapNum):
        if self.carStatus == None or self.lapData == None:
            return

        if len(self.stints) == 0 or (self.lapData.driverStatus == DriverStatus.OUT_LAP.value \
            and self.lapData.pitStatus == PitStatus.NONE.value and lapNum != self.lastPitStopLap):
                self.stints.append({lapNum - 1: self.carStatus.actualTyreCompound})
                self.lastPitStopLap = lapNum


    def processFuel(self, lapNum):
        if self.carStatus == None:
            return

        if lapNum-1 not in self.fuelUsed:
            self.fuelUsed[lapNum - 1] = self.carStatus.fuelInTank

        return

    def processSectors(self, lap):
        # Sector 1
        if self.needProcessSectors[0] and lap.sector == 2 and lap.sector1Time > 0:
            self.needProcessSectors[0] = False
            self.needProcessSectors[1] = True
            self.lastSectors[0] = lap.sector1Time
            self.bestSectors[0] = min(self.bestSectors[0], self.lastSectors[0])

        # Sector 2
        if self.needProcessSectors[1] and lap.sector == 3 and lap.sector2Time > 0:
            self.needProcessSectors[1] = False
            self.needProcessSectors[2] = True
            self.lastSectors[1] = lap.sector2Time
            self.bestSectors[1] = min(self.bestSectors[1], self.lastSectors[1])

        # Sector 3
        if self.needProcessSectors[2] and lap.sector == 1 and lap.lastLapTime > 0 and self.lastSectors[0] and self.lastSectors[1]:
            self.needProcessSectors[2] = False
            self.lastSectors[2] = lap.lastLapTime - self.lastSectors[0] - self.lastSectors[1]
            self.bestSectors[2] = min(self.bestSectors[2], self.lastSectors[2])

        if lap.sector == 1 and lap.lastLapTime != 0:
            self.needProcessSectors[0] = True
            self.previousLaps[lap.currentLapNum - 1] = lap.lastLapTime



    def printStint(self):
        if self.participant.aiControlled == AiControlled.HUMAN.value:
            print("-------------");
            print("Stints:");

            for idx in range(len(self.stints)):
                print("    %d" % idx);
                for key, value in self.stints[idx].items():
                    print("       Lap: %d" % key)
                    print("       Compound: %s" % TyresCompound(value).name)
        return

    def tyresSurfaceTemperature(self):
        return [t for t in self.carTelemetry.tyresSurfaceTemperature]

    def tyresInnerTemperature(self):
        return [t for t in self.carTelemetry.tyresInnerTemperature]

    def brakesTemperature(self):
        return [t for t in self.carTelemetry.brakesTemperature]

    def ersStoreEnergyInPercentage(self):
        return self.carStatus.ersStoreEnergy / self.MAX_ERS * 100

    def ersDeployedThisLapInPercentage(self):
        return 100 - (self.carStatus.ersDeployedThisLap / self.MAX_ERS * 100 )

    def ersHarvestedThisLapInPercentage(self):
        return (self.carStatus.ersHarvestedThisLapMGUK + self.carStatus.ersHarvestedThisLapMGUH) / self.MAX_ERS * 100

    def tyreAges(self, stint, currentLap):
        if not self.stints or stint > len(self.stints):
            return None

        myStint = self.stints[stint]
        initLap = list(myStint)[0]
        lastLap = 0

        # This stint is not the last one.
        if stint + 1 < len(self.stints):
                nextStint = self.stints[stint + 1]
                lastLap = list(nextStint)[0]
                return lastLap - initLap

        return currentLap - initLap;
