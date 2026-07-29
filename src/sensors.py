"""
Simulated sensors interface.
Provides read_all() to be consumed by the agent.
"""
from typing import Dict, Any
import random
import time

class SimulatedSensors:
    def __init__(self, rooms=None):
        self.rooms = rooms or ["living_room", "bedroom", "kitchen"]
        # initial baseline temps
        self.temps = {r: 20.0 + random.uniform(-1, 1) for r in self.rooms}
        self.occupancy = {r: False for r in self.rooms}
        self.light = {r: 300 for r in self.rooms}
        self.smoke = {r: False for r in self.rooms}

    def read_all(self) -> Dict[str, Any]:
        # Simulate some drift
        for r in self.rooms:
            self.temps[r] += random.uniform(-0.2, 0.2)
            # random occupancy events
            if random.random() < 0.05:
                self.occupancy[r] = not self.occupancy[r]
            # light fluctuates
            self.light[r] = max(0, self.light[r] + random.randint(-30, 30))
            # very rare smoke event
            if random.random() < 0.001:
                self.smoke[r] = True
        return {
            "temperature": dict(self.temps),
            "occupancy": dict(self.occupancy),
            "light_level": dict(self.light),
            "smoke": dict(self.smoke),
            "timestamp": time.time()
        }
