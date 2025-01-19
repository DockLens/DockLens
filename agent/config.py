import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000/api")
INTERVAL = int(os.getenv("INTERVAL", 2))  # detik
