from .formatHelper import formatLapTime, formatFuelRemainingLaps, mapRevLights, mapGear

def mapToLapViewState(driver):
    lap = driver.lapData

    data = {}
    data["currentLapTime"] = formatLapTime(lap.currentLapTime)
    data["currentLapNum"] = lap.currentLapNum
    data["position"] = lap.carPosition
    data["pitStatus"] = lap.pitStatus
    data["diffPreviousLap"] = 0

    return data
    

def mapToCarTelemetryViewState(driver):
    carTelemetry = driver.carTelemetry
    carStatus = driver.carStatus
    pitLimiterStatus = carStatus.pitLimiterStatus == 1 if carStatus else False
    drsAllowed = carStatus.drsAllowed > 0 if carStatus else False

    data = {}
    data["gear"] = mapGear(carTelemetry.gear, pitLimiterStatus)
    data["speed"] = carTelemetry.speed
    data["drs"] = carTelemetry.drs
    data["revLightsPercent"] = mapRevLights(carTelemetry.revLightsPercent, drsAllowed, carTelemetry.drs)
    data["tyresSurfaceTemperature"] = driver.tyresSurfaceTemperature()
    data["tyresInnerTemperature"] = driver.tyresInnerTemperature()
    data["brakesTemperature"] = driver.brakesTemperature()
    data["engineRPM"] = carTelemetry.engineRPM

    return data


def mapToCarStatusViewState(driver):
    carStatus = driver.carStatus
    ersPercentage = driver.ersStoreEnergyInPercentage()

    data = {}
    data["fuelMix"] = carStatus.fuelMix
    data["fuelRemainingLaps"] = formatFuelRemainingLaps(carStatus.fuelRemainingLaps)
    data["pitLimiterStatus"] = carStatus.pitLimiterStatus
    data["drsAllowed"] = carStatus.drsAllowed
    data["ersStoreEnergy"] = carStatus.ersStoreEnergy
    data["ersDeployMode"] = carStatus.ersDeployMode
    data["ersStoreEnergy"] = ersPercentage
    data["ersStoreEnergyPercentage"] = int(ersPercentage)
    data["ersHarvestedThisLap"] = driver.ersHarvestedThisLapInPercentage()
    data["ersDeployedThisLap"] = driver.ersDeployedThisLapInPercentage()
    data["pitLimiterStatus"] = carStatus.pitLimiterStatus

    return data
