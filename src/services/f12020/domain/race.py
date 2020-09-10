from .driver import Driver

class Race():

    def __init__(self, packet):
        self.playerCarIndex = packet.header.playerCarIndex
        self.drivers = []
        self.positions = [None] * 21
        self.session = None
        self.finalClassification = None

    def update_motion(self, motions):
        if not self.drivers:
            return

        for idx, motion in enumerate(motions):
            self.drivers[idx].motion = motion

    def update_session(self, session):
        self.session = session

    def update_participants(self, participants):
        if not self.drivers:
            self.drivers = list(map(lambda p: Driver(p), participants))

    def update_participants_lap(self, laps):
        if not self.drivers:
            return

        for idx, lap in enumerate(laps):
            self.positions[lap.carPosition] = idx
            self.drivers[idx].update_lap(lap)

    def update_participants_car_setup(self, setups):
        if not self.drivers:
            return

        for idx, setup in enumerate(setups):
            self.drivers[idx].setup = setup

    def update_participants_car_telemetry(self, telemetries):
        if not self.drivers:
            return

        for idx, telemetry in enumerate(telemetries):
            self.drivers[idx].telemetry = telemetry

    def update_participants_car_status(self, statuses):
        if not self.drivers:
            return

        for idx, status in enumerate(statuses):
            self.drivers[idx].status = status

    def update_final_classification(self, classification):
        self.finalClassification = classification

    def me(self):
        if len(self.drivers) > 0:
            return self.drivers[self.playerCarIndex]
        else:
            return None
