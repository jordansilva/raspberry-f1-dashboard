import time
from threading import Timer
from ..wheel import LedControl
from .. import UIObject, UILog


class EightDigitsDisplayProcessor(UIObject):

    NUM_DIGITS = 8
    GEARS = {
        1: '1',
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: '6',
        7: '7',
        8: '8',
        0: 'N',
        -1: 'R',
        'P': 'P'
        }

    def __init__(self):
        try:
            self.ui = LedControl()
            self.start()
            print("8-Digit display initialised")
        except Exception as e:
            print(e)
            self.ui = UILog()

    def start(self):
        self.displayStatus=['GEAR', 'LAPS']
        self.gear = 'P'
        self.sector1 = 0
        self.sector2 = 0
        self.currentLapNum = 0
        self.lastLap = 0
        self.pitStatus = 0
        self.fuelInTank = 0
        self.fuelRemainingLaps = 0
        self.currentText = ''

        self.display('Good Luck')
        time.sleep(0.1)
        self.display('JORDAN')
        time.sleep(0.5)

    def process(self, data):
        if 'gear' in data and self.gear != data['gear']:
            self.gear = data['gear']
            self.displayCurrentStatus()
            
        if 'sector1' in data:
            if self.sector1 != data['sector1']:
                self.sector1 = data['sector1']
                self.displaySector(1, self.sector1)
            
            if self.sector2 != data['sector2']:
                self.sector2 = data['sector2']
                self.displaySector(2, self.sector2)
            
            if self.lastLap != data['lastLap']:
                self.lastLap = data['lastLap']
                self.displayLastLap(self.lastLap)

            if self.currentLapNum != data['currentLapNum']:
                self.currentLapNum = data['currentLapNum']
                self.displayCurrentStatus()

            if self.pitStatus != data['pitStatus']:
                self.pitStatus = data['pitStatus']
                self.displayCurrentStatus()

        # if 'fuelInTank' in data:
        #     # fuelInTank 10.796666145324707
        #     # fuelRemainingLaps 0.9498028755187988
        #     if self.fuelInTank != data['fuelInTank']:
        #         self.fuelInTank = data['fuelInTank']
        #         print('fuelInTank', self.fuelInTank)
            
        #     if self.fuelRemainingLaps != data['fuelRemainingLaps']:
        #         self.fuelRemainingLaps = data['fuelRemainingLaps']
        #         print('fuelRemainingLaps', self.fuelRemainingLaps)
            

    def displaySector(self, sector, time):
        cent = int((time/1000%1)*1000)
        seconds = int((time/1000)%60)
        minutes = int((time/(1000*60))%60)

        sector = '  S%d' % sector
        text = list(self.currentText)
        idx = self.NUM_DIGITS - len(sector)
        text[idx:] = sector
        self.display(''.join(text))

        self.sectorText = '%d:%02d.%03d' % (minutes, seconds, cent) if minutes > 0 else '%2d.%03d' % (seconds, cent)
        Timer(2, self.setDisplayStatus, [['GEAR', 'SECTOR']]).start()

    def displayLastLap(self, time):
        sector3 = time - (self.sector1/1000 + self.sector2/1000)
        self.displaySector(3, sector3 * 1000)

    def displayCurrentStatus(self):
        text = self.NUM_DIGITS * [' ']

        if 'GEAR' in self.displayStatus:
            text[0] = self.GEARS[self.gear] if self.pitStatus == 0 else self.GEARS['P']

        if 'LAPS' in self.displayStatus:
            lap = 'L%d' % self.currentLapNum
            idx = self.NUM_DIGITS - len(lap)
            text[idx:] = lap

        if 'SECTOR' in self.displayStatus:
            idx = self.NUM_DIGITS - len(self.sectorText.replace('.', ''))
            text[idx:] = self.sectorText
            Timer(3, self.setDisplayStatus, [['GEAR', 'LAPS']]).start()
        
        self.display(''.join(text))    

    def display(self, text):
        self.currentText = text.rjust(8, ' ')
        self.ui.show_text(self.currentText)

    def setDisplayStatus(self, status):
        self.displayStatus = status
        self.displayCurrentStatus()

