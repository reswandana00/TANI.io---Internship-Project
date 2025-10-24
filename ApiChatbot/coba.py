import os
from dotenv import load_dotenv

load_dotenv()
base_url = os.getenv("API_BASE_URL")
print(f"Using API_BASE_URL: {base_url}")