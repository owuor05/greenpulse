#!/usr/bin/env python3
"""
Test the new unified /ask endpoint
"""
import os
import sys
import asyncio
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:8000"  # Adjust if needed

async def test_ask_endpoint():
    """Test the unified /ask endpoint with different scenarios"""
    print("🧪 Testing /api/ai/ask endpoint\n")
    
    async with aiohttp.ClientSession() as session:
        
        # Test 1: Simple weather question
        print("1️⃣ Simple weather question:")
        data = aiohttp.FormData()
        data.add_field('question', "What's the weather in Nairobi?")
        data.add_field('location', 'Nairobi')
        data.add_field('mode', 'community')
        
        try:
            async with session.post(f"{BASE_URL}/api/ai/ask", data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"   ✅ SUCCESS")
                    print(f"   📍 Location: {result.get('location', 'N/A')}")
                    print(f"   🤖 Response preview: {result.get('answer', '')[:100]}...")
                else:
                    print(f"   ❌ FAILED - Status: {response.status}")
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
        print()
        
        # Test 2: Risk assessment question
        print("2️⃣ Risk assessment question:")
        data = aiohttp.FormData()
        data.add_field('question', "What are the environmental risks for manufacturing in Mombasa?")
        data.add_field('location', 'Mombasa')
        data.add_field('mode', 'professional')
        
        try:
            async with session.post(f"{BASE_URL}/api/ai/ask", data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"   ✅ SUCCESS")
                    print(f"   📍 Location: {result.get('location', 'N/A')}")
                    print(f"   🤖 Response preview: {result.get('answer', '')[:100]}...")
                else:
                    print(f"   ❌ FAILED - Status: {response.status}")
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
        print()
        
        # Test 3: No location question
        print("3️⃣ General question (no location):")
        data = aiohttp.FormData()
        data.add_field('question', "What are the main environmental challenges in Kenya?")
        data.add_field('mode', 'community')
        
        try:
            async with session.post(f"{BASE_URL}/api/ai/ask", data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"   ✅ SUCCESS")
                    print(f"   🤖 Response preview: {result.get('answer', '')[:100]}...")
                else:
                    print(f"   ❌ FAILED - Status: {response.status}")
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
        print()

if __name__ == "__main__":
    print("🚀 TESTING NEW UNIFIED /ASK ENDPOINT")
    print("=" * 50)
    asyncio.run(test_ask_endpoint())
    print("✅ Test complete!")