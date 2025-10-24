import os
from dotenv import load_dotenv

load_dotenv()

print("=== Environment Variables ===")
print(f"API_TOOL_URL: {os.getenv('API_TOOL_URL', 'NOT SET')}")

# Check current base_url value
base_url = os.getenv("API_TOOL_URL", "http://tool-api-container:8011")
print(f"Current base_url: {base_url}")

# Test basic connection with requests
import requests
try:
    response = requests.get(f"{base_url}/health", timeout=5)
    print(f"Health check response: {response.json()}")
except Exception as e:
    print(f"Health check failed: {e}")

# Test with different URL patterns
test_urls = [
    "http://tool-api-container:8011",
    "http://localhost:8011", 
    "http://127.0.0.1:8011"
]

for url in test_urls:
    try:
        response = requests.get(f"{url}/health", timeout=2)
        print(f"✓ {url} works: {response.status_code}")
        break
    except Exception as e:
        print(f"✗ {url} failed: {e}")