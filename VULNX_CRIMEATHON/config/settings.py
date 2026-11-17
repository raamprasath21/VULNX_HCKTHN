import os
from dotenv import load_dotenv

load_dotenv()

APP_PORT = int(os.getenv("APP_PORT", "5000"))
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8765")
SIMULATION_MODE = os.getenv("SIMULATION_MODE", "vulnerable")
