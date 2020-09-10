class Publisher:

    def __init__(self):
        self.observers = []

    def connect(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remove(self, observer):
        self.observers.remove(observer)

    def emit(self, data):
        [o(data) for o in self.observers]
