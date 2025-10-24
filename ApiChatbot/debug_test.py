import asyncio
import aiohttp
import sys
import os

# Add the current directory to Python path
sys.path.append('/app')

from utils import (
    get_data_panen_prompt_summary,
    get_data_total_panen,
    get_data_wilayah_panen_tertinggi,
    get_chat_response
)

async def test_individual_functions():
    print("=== Testing Individual API Functions ===")
    
    print("\n1. Testing get_data_panen_prompt_summary...")
    try:
        result1 = await get_data_panen_prompt_summary("jawa timur")
        print(f"Success: {result1[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n2. Testing get_data_total_panen...")
    try:
        result2 = await get_data_total_panen("jawa timur")
        print(f"Success: {result2}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n3. Testing get_data_wilayah_panen_tertinggi...")
    try:
        result3 = await get_data_wilayah_panen_tertinggi("jawa timur")
        print(f"Success: {result3}")
    except Exception as e:
        print(f"Error: {e}")

def test_chat_response():
    print("\n=== Testing Chat Response Function ===")
    try:
        response = get_chat_response("data panen jawa timur")
        print(f"Chat response: {response[:300]}...")
    except Exception as e:
        print(f"Chat error: {e}")

if __name__ == "__main__":
    print("Starting API tests...")
    asyncio.run(test_individual_functions())
    test_chat_response()
    print("Tests completed!")