# Smart Home Controller & Recommendation Assistant (PEAS demo)

This is a small simulator and agent demonstrating a PEAS-designed smart-home controller with a simple recommendation assistant.

Features:
- PEAS mapping described in repository.
- Agent with perceive -> decide -> act loop.
- Simulated sensors, actuators, and environment.
- FastAPI endpoints to interact with the system (sensors, actuator commands, run step, get recommendation).

Run locally:
1. Create a virtualenv and install requirements:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Start the app:
   uvicorn src.app:app --reload --port 8000

3. Try:
   GET  http://localhost:8000/sensors
   POST http://localhost:8000/step
   POST http://localhost:8000/actuator  (body: {"device":"light_living_room","action":"turn_on"})

Next steps and extensions:
- Persist user preferences and history to a DB.
- Replace rule-based recommender with a learning model (e.g., supervised re-ranking or bandit for recommendations).
- Integrate real devices via MQTT/home assistant or vendor APIs.
- Add authentication and web/mobile UI for users.
