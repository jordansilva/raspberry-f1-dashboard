import json
from .enums import Constants

def mapGear(gear, pitLimiter = False):
    if pitLimiter:
        return "P"
    elif gear == -1:
        return "R"
    elif gear == 0:
        return 'N'
    elif gear > 0:
        return gear
    else:
        return '-'

def mapRevLights(percent, drsAllowed = False, drsActive = False):
    lights = [False] * 14
    # green lights
    lights[0] = drsActive or drsAllowed
    lights[1] = drsActive == True
    lights[2] = False
    lights[3] = False

    # red lights
    lights[4] = percent >= 10
    lights[5] = percent >= 20
    lights[6] = percent >= 30
    lights[7] = percent >= 40
    lights[8] = percent >= 50

    # blue lights
    lights[9] = percent >= 60
    lights[10] = percent >= 70
    lights[11] = percent >= 80
    lights[12] = percent >= 85
    lights[13] = percent >= 92

    return lights


def deltaPreviousLap(driver):
    if not driver or not driver.lapData or not driver.miniSectors or driver.lapData.currentLapNum == 1:
        return float('inf')

    lastLap = driver.lapData.currentLapNum - 1
    currLap = driver.lapData.currentLapNum
    currMiniSector = int(driver.lapData.lapDistance / Constants.MINISECTOR_GAP)

    if lastLap not in driver.miniSectors or currMiniSector not in driver.miniSectors[lastLap] or currMiniSector not in driver.miniSectors[currLap]:
        return float('inf')

    lastTime = driver.miniSectors[lastLap][currMiniSector]
    currTime = driver.miniSectors[currLap][currMiniSector]

    return (currTime - lastTime) /1000.0

def deltaBetween(driver1, driver2):
    if not driver1 or not driver2 or not driver1.lapData or not driver2.lapData:
        return float('inf')

    driver1Lap = driver1.lapData.currentLapNum
    driver1Distance = driver1.lapData.lapDistance

    driver2Lap = driver2.lapData.currentLapNum
    driver2Distance = driver2.lapData.lapDistance

    if driver1Lap == driver2Lap or (driver1Lap == driver2Lap+1 and driver1Distance < driver2Distance):
        if driver1.miniSectors and driver2.miniSectors:
            # Last one of the seconds, is the slowest
            currMiniSector = int(driver2Distance / Constants.MINISECTOR_GAP)

            # We get the CURRENT LAP of SECOND, is the last.
            if not driver1.miniSectors[driver2Lap] or currMiniSector not in driver1.miniSectors[driver2Lap]:
                return float('inf')

            driver1Time = driver1.miniSectors[driver2Lap][currMiniSector]
            driver2Time = driver2.miniSectors[driver2Lap][currMiniSector]

            diff = driver2Time - driver1Time
            return diff / 1000.0
        else:
            return float('inf')

    return 5000.0 + (driver1Lap - driver2Lap)


def formatDelta(delta):
    if delta > 5000.0 and delta < 5100.0:
        return "+ %d LAPS" % int(delta - 5000.0)

    if delta == float('inf'):
        return ""

    if delta == 0:
        return "+/-"

    return abs(delta)


def formatLapTime(lapTime):
    timeframe = divmod(lapTime, 60) # array with [minutes, seconds]
    if timeframe[0] > 0:
        return "%d:%06.3f" % timeframe
    else:
        return "%06.3f" % timeframe[1]


def formatFuelRemainingLaps(fuel):
    if fuel > 0:
        return "(+%.2f)" % fuel
    else: 
        return "(-%.2f)" % fuel
