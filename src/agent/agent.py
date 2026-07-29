"""
Simple smart-home agent implementing PEAS behaviors:
- perceive() reads sensor data
- decide() applies rules + a small recommendation engine
- act() executes actuator commands
"""
from typing import Dict, Any, List, Optional
import datetime
import json

class Agent:
    def __init__(self, sensors, actuators, logger=None):
        self.sensors = sensors
        self.actuators = actuators
        self.logger = logger or (lambda *args, **kwargs: None)
        # Simple world model: last seen sensor readings and device states
        self.world: Dict[str, Any] = {"sensors": {}, "devices": {}, "history": []}
        # Example user preferences (in a real app this would be persisted/configurable)
        self.user_prefs = {
            "temperature": {"living_room": 22.0, "bedroom": 20.0},
            "light_on_when_occupied": True
        }

    def perceive(self):
        readings = self.sensors.read_all()
        self.world["sensors"] = readings
        self.logger("Perceived sensors:", readings)
        return readings

    def decide(self, readings: Dict[str, Any]) -> Dict[str, Any]:
        commands = []
        now = datetime.datetime.now()

        # Rule 1: Maintain comfort temperature in occupied rooms
        occupancy = readings.get("occupancy", {})
        temps = readings.get("temperature", {})
        for room, occ in occupancy.items():
            desired = self.user_prefs["temperature"].get(room)
            if desired is None:
                continue
            current = temps.get(room)
            if current is None:
                continue
            # simple hysteresis to avoid flapping
            if occ and current < desired - 0.5:
                commands.append({"device": f"thermostat_{room}", "action": "set_temperature", "value": desired})
            elif not occ and current > desired + 1.0:
                # save energy when empty
                commands.append({"device": f"thermostat_{room}", "action": "set_temperature", "value": desired - 2.0})

        # Rule 2: Lights on when occupied (if preference)
        if self.user_prefs.get("light_on_when_occupied", True):
            light_levels = readings.get("light_level", {})
            for room, occ in occupancy.items():
                level = light_levels.get(room, 0)
                if occ and level < 200:
                    commands.append({"device": f"light_{room}", "action": "turn_on"})
                elif not occ:
                    commands.append({"device": f"light_{room}", "action": "turn_off"})

        # Safety rule example: if smoke detected, turn off smart-plug to stove and notify
        smoke = readings.get("smoke", {})
        for room, present in smoke.items():
            if present:
                commands.append({"device": f"plug_stove_{room}", "action": "turn_off"})
                commands.append({"notify": f"Smoke detected in {room}. Stove turned off."})

        # Simple recommendation engine: suggest temperature schedule change if user always adjusts
        recommendation = self._recommend_from_history(now)
        if recommendation:
            commands.append({"recommendation": recommendation})

        decision = {"time": now.isoformat(), "commands": commands}
        self.world["history"].append(decision)
        self.logger("Decided:", decision)
        return decision

    def _recommend_from_history(self, now) -> Optional[Dict[str, Any]]:
        # Very simple: if user manually set temperature many times recently, recommend schedule
        recent = [h for h in self.world["history"] if (now - datetime.datetime.fromisoformat(h["time"])) .total_seconds() < 3600*24]
        manual_sets = 0
        for h in recent:
            for cmd in h["commands"]:
                if cmd.get("action") == "set_temperature" and cmd.get("manual", False):
                    manual_sets += 1
        if manual_sets >= 3:
            return {"type": "schedule_suggestion", "message": "You've adjusted temperatures frequently; consider a schedule."}
        return None

    def act(self, decision: Dict[str, Any]):
        for cmd in decision["commands"]:
            if "device" in cmd and "action" in cmd:
                device = cmd["device"]
                action = cmd["action"]
                value = cmd.get("value")
                # dispatch to actuators
                self.actuators.execute(device, action, value)
            elif "notify" in cmd:
                self._notify_user(cmd["notify"])
            elif "recommendation" in cmd:
                # store or present recommendation via actuators.notify
                self._notify_user(f"Recommendation: {cmd['recommendation']['message']}")
        self.logger("Acted on commands")

    def _notify_user(self, message: str):
        # In a production system this would be push/email/etc.
        self.logger("NOTIFY:", message)

    def step(self):
        readings = self.perceive()
        decision = self.decide(readings)
        self.act(decision)
        return decision
