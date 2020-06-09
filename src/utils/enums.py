from enum import Enum

class Constants:
    MINISECTOR_GAP = 100

class DriverStatus(Enum):
    IN_GARAGE = 0
    FLYING_LAP = 1
    IN_LAP = 2
    OUT_LAP = 3
    ON_TRACK = 4

class PitStatus(Enum):
    NONE = 0
    PITTING = 1
    IN_PIT_AREA = 2

class AiControlled(Enum):
    AI = 1
    HUMAN = 0

class TyresCompound(Enum):
    #F1 Classic
    F1CLASSIC_DRY = 9
    F1CLASSIC_WET = 10
    #F2
    F2_SUPERSOFT = 11
    F2_SOFT = 12
    F2_MEDIUM = 13
    F2_HARD = 14
    F2_WET = 15
    #F1
    HYPERSOFT = 16 #C5
    ULTRASOFT = 17 #C4
    SOFT = 18 #C3
    MEDIUM = 19 #C2
    HARD = 20 #C1
    INTER = 7
    WET = 8
