"""
FastAPI app to interact with the simulated smart-home agent.
Endpoints:
- GET /sensors
- POST /actuator (device, action, value)
- POST /step  -> runs agent.step() and environment step
- GET /recommend -> returns last recommendation if any (read-only)
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .sensors import SimulatedSensors
from .actuators import SimulatedActuators
from .agent.agent import Agent
from .environment.simulator import EnvironmentSimulator

app = FastAPI(title="Smart Home Agent Simulator")

sensors = SimulatedSensors()
actuators = SimulatedActuators()
env = EnvironmentSimulator(sensors, actuators)
agent = Agent(sensors, actuators, logger=print)

class ActuatorCommand(BaseModel):
    device: str
    action: str
    value: float | None = None
    manual: bool = False

@app.get("/sensors")
def get_sensors():
    return sensors.read_all()

@app.post("/actuator")
def actuator(cmd: ActuatorCommand):
    # execute manual command (flag it so the agent can learn if needed)
    actuators.execute(cmd.device, cmd.action, cmd.value)
    # record as manual change in agent history so recommender can see it
    agent.world["history"].append({
        "time": __import__("datetime").datetime.now().isoformat(),
        "commands": [{"device": cmd.device, "action": cmd.action, "value": cmd.value, "manual": cmd.manual}]
    })
    return {"status": "ok"}

@app.post("/step")
def step():
    decision = agent.step()
    env.step()
    return decision

@app.get("/recommend")
def recommend():
    # return last recommendation if present
    for h in reversed(agent.world["history"]):
        for c in h["commands"]:
            if "recommendation" in c:
                return c["recommendation"]
    return {"recommendation": None}
