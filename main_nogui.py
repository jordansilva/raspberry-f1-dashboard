# This Python file uses the following encoding: utf-8
import sys
import os

from src import Telemetry
from src import Context

if __name__ == "__main__":
    ctx = Context()
    telemetry = Telemetry(ctx)
    telemetry.connect()