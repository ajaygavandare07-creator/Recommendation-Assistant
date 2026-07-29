"""
Environment simulator that advances time and optionally applies actuator effects to sensors.
This is a minimal example: thermostat setpoints nudge temperatures toward setpoint.
"""
from typing import Any, Dict
import time

class EnvironmentSimulator:
    def __init__(self, sensors, actuators, timestep_seconds=1.0):
        self.sensors = sensors
        self.actuators = actuators
        self.timestep = timestep_seconds

    def step(self):
        # If a thermostat setpoint exists, nudge the sensor temperature
        for device, state in list(self.actuators.devices.items()):
            if device.startswith("thermostat_") and "setpoint" in state:
                room = device.split("thermostat_")[-1]
                current = self.sensors.temps.get(room)
                target = state["setpoint"]
                if current is not None:
                    # simple first-order system
                    diff = (target - current) * 0.1
                    self.sensors.temps[room] = current + diff
        time.sleep(0)  # non-blocking placeholder
