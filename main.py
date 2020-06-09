# This Python file uses the following encoding: utf-8
import sys
import os

from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication

from src import Telemetry

if __name__ == "__main__":
    #pkill -9 python

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

    telemetry = Telemetry(ctx)
    telemetry.connect()
    sys.exit(app.exec_())
