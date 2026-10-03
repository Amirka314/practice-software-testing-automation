import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://practicesoftwaretesting.com")
API_URL = os.getenv("API_URL", "https://api.practicesoftwaretesting.com")