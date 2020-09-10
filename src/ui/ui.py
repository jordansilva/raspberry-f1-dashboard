from abc import ABC, abstractmethod

class UIObject(ABC):

    @abstractmethod
    def process(self, data):
        pass


class UILog(UIObject):
    def process(self, data):
        print(data)

