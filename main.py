# This Python file uses the following encoding: utf-8
import sys
import os

from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication

from src import Telemetry


class Context():
    data = {}

    def __init__(self, ctx):
        self.data = {}
        self.ctx = ctx
        print(ctx)

    def setContextProperty(self, name, value):
        self.data[name] = value
        self.ctx.setContextProperty(name, value)


if __name__ == "__main__":
    # pkill -9 python

    # Setup the application window PyQt5
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)

    ctx = engine.rootContext()

    # Load QML File
    qml_file = os.path.join(os.path.dirname(__file__), "main.qml")
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    context = Context(ctx)
    telemetry = Telemetry(context)
    telemetry.connect()
    sys.exit(app.exec_())
