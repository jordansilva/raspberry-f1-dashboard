class Context:
    def __init__(self):
        self.data = {}

    def setContextProperty(self, name, value):
        self.data[name] = value
        # if name == 'revLights':
            # print(name, value)
            # self.revProcessor.process(value)
