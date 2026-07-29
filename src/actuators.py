"""
Simulated actuators interface.
Provides execute(device, action, value) which updates simulated device state.
"""
from typing import Dict, Any

class SimulatedActuators:
    def __init__(self):
        self.devices: Dict[str, Dict[str, Any]] = {}
    def execute(self, device: str, action: str, value=None):
        state = self.devices.setdefault(device, {})
        if action == "set_temperature":
            state["setpoint"] = value
            print(f"[ACTUATOR] {device} setpoint -> {value}")
        elif action == "turn_on":
            state["state"] = "on"
            print(f"[ACTUATOR] {device} -> ON")
        elif action == "turn_off":
            state["state"] = "off"
            print(f"[ACTUATOR] {device} -> OFF")
        else:
            # generic action
            state[action] = value
            print(f"[ACTUATOR] {device} action {action} -> {value}")
