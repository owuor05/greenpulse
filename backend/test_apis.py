"""
Comprehensive API Test Suite for GreenPulse Backend
Tests Google Weather API, NASA POWER, AI Service, and all endpoints
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.data.google_weather import google_weather_client
from app.data.nasa_power import nasa_client
from app.services.ai_service import ai_service
from app.services.google_maps_service import gmaps_service
from app.config import settings
import httpx

# Test coordinates (Nairobi, Kenya)
TEST_LAT = -1.286389
TEST_LON = 36.817223
TEST_LOCATION = "Nairobi, Kenya"


async def test_google_weather_api():
    """Test Google Maps Weather API"""
    print("\n" + "="*70)
    print("🌤️  TESTING GOOGLE MAPS WEATHER API")
    print("="*70)
    
    try:
        weather_data = await google_weather_client.get_current_weather(TEST_LAT, TEST_LON)
        
        if weather_data and weather_data.get('temperature') is not None:
            print("✅ Google Weather API: SUCCESS")
            print(f"   📍 Location: {TEST_LOCATION}")
            print(f"   🌡️  Temperature: {weather_data.get('temperature')}°C")
            print(f"   🌡️  Feels Like: {weather_data.get('feels_like')}°C")
            print(f"   💧 Humidity: {weather_data.get('humidity')}%")
            print(f"   💨 Wind Speed: {weather_data.get('wind_speed')} km/h")
            print(f"   💨 Wind Direction: {weather_data.get('wind_direction', 'N/A')}")
            print(f"   ☁️  Conditions: {weather_data.get('conditions', 'N/A')}")
            print(f"   🌧️  Precipitation: {weather_data.get('precipitation', 0)}mm")
            print(f"   ☀️  UV Index: {weather_data.get('uv_index', 'N/A')}")
            print(f"   ☁️  Cloud Cover: {weather_data.get('cloud_cover', 'N/A')}%")
            print(f"   🌞 Daytime: {'Yes' if weather_data.get('is_daytime') else 'No'}")
            return True
        else:
            print("❌ Google Weather API: FAILED - No data returned or API not enabled")
            print("   💡 Make sure Weather API is enabled in Google Cloud Console")
            return False
            
    except Exception as e:
        print(f"❌ Google Weather API: ERROR - {str(e)}")
        return False


async def test_nasa_power_api():
    """Test NASA POWER API"""
    print("\n" + "="*70)
    print("🛰️  TESTING NASA POWER API")
    print("="*70)
    
    try:
        climate_data = await nasa_client.get_recent_30_days(TEST_LAT, TEST_LON)
        
        if climate_data and len(climate_data) > 0:
            print("✅ NASA POWER API: SUCCESS")
            print(f"   📍 Location: Lat {TEST_LAT}, Lon {TEST_LON}")
            print(f"   📊 Parameters Retrieved: {', '.join(climate_data.keys())}")
            
            # Show temperature data
            if 'T2M' in climate_data:
                temps = list(climate_data['T2M'].values())
                valid_temps = [t for t in temps if t != -999]
                if valid_temps:
                    avg_temp = sum(valid_temps) / len(valid_temps)
                    print(f"   🌡️  30-Day Avg Temperature: {avg_temp:.1f}°C")
            
            # Show precipitation data
            if 'PRECTOTCORR' in climate_data:
                precip = list(climate_data['PRECTOTCORR'].values())
                valid_precip = [p for p in precip if p != -999]
                if valid_precip:
                    total_precip = sum(valid_precip)
                    print(f"   🌧️  30-Day Total Precipitation: {total_precip:.1f}mm")
            
            # Show humidity
            if 'RH2M' in climate_data:
                humidity = list(climate_data['RH2M'].values())
                valid_humidity = [h for h in humidity if h != -999]
                if valid_humidity:
                    avg_humidity = sum(valid_humidity) / len(valid_humidity)
                    print(f"   💧 30-Day Avg Humidity: {avg_humidity:.1f}%")
            
            return True
        else:
            print("❌ NASA POWER API: FAILED - No data returned")
            return False
            
    except Exception as e:
        print(f"❌ NASA POWER API: ERROR - {str(e)}")
        return False


async def test_ai_service():
    """Test OpenRouter AI Service"""
    print("\n" + "="*70)
    print("🤖 TESTING AI SERVICE (OpenRouter GPT-4o)")
    print("="*70)
    
    try:
        test_prompt = "Explain in one sentence what agroforestry is."
        system_prompt = "You are a conservation expert. Be brief and clear."
        
        response = await ai_service.chat_response_with_system(
            user_message=test_prompt,
            system_prompt=system_prompt
        )
        
        if response and len(response) > 10:
            print("✅ AI Service: SUCCESS")
            print(f"   📝 Test Question: {test_prompt}")
            print(f"   💬 AI Response: {response[:150]}...")
            return True
        else:
            print("❌ AI Service: FAILED - No response or too short")
            return False
            
    except Exception as e:
        print(f"❌ AI Service: ERROR - {str(e)}")
        return False


async def test_google_maps_geocoding():
    """Test Google Maps Geocoding"""
    print("\n" + "="*70)
    print("📍 TESTING GOOGLE MAPS GEOCODING")
    print("="*70)
    
    try:
        location_data = await gmaps_service.geocode_address(TEST_LOCATION)
        
        if location_data and location_data.get('latitude') and location_data.get('longitude'):
            print("✅ Google Maps Geocoding: SUCCESS")
            print(f"   🔍 Query: {TEST_LOCATION}")
            print(f"   📍 Result: {location_data.get('formatted_address')}")
            print(f"   🌐 Coordinates: ({location_data.get('latitude')}, {location_data.get('longitude')})")
            return True
        else:
            print("❌ Google Maps Geocoding: FAILED - No coordinates returned")
            return False
            
    except Exception as e:
        print(f"❌ Google Maps Geocoding: ERROR - {str(e)}")
        return False


async def test_land_data_endpoint():
    """Test the main /api/land-data endpoint (integration test)"""
    print("\n" + "="*70)
    print("🌍 TESTING LAND DATA ENDPOINT (Full Integration)")
    print("="*70)
    
    try:
        base_url = "https://greenpulse-production-370c.up.railway.app"
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{base_url}/api/land-data/analyze",
                json={"location": TEST_LOCATION}
            )
            
            if response.status_code == 200:
                payload = response.json()
                data = payload.get("data") if isinstance(payload, dict) else None
                print("✅ Land Data Endpoint: SUCCESS")
                if not isinstance(data, dict):
                    print("❌ Land Data Endpoint: FAILED - Unexpected response shape")
                    print(f"   Payload keys: {list(payload.keys()) if isinstance(payload, dict) else type(payload)}")
                    return False

                print(f"   📍 Location: {data.get('location_name')}")
                print(f"   🌡️  Current Temperature: {data.get('current_temperature_celsius')}°C (Google Weather)")
                print(f"   🌡️  Feels Like: {data.get('feels_like_celsius')}°C")
                print(f"   🔎 Temp Status: {data.get('temperature_status', 'N/A')}")
                print(f"   ⚠️  Drought Risk: {data.get('climate_risks', {}).get('drought', {}).get('severity', 'N/A').upper()}")
                print(f"   💧 Flood Risk: {data.get('climate_risks', {}).get('flood', {}).get('severity', 'N/A').upper()}")
                print(f"   📊 Data Sources:")
                sources = data.get('data_source', {})
                if isinstance(sources, dict):
                    for key, value in sources.items():
                        print(f"      - {key}: {value}")
                else:
                    print(f"      - {sources}")
                
                # Check AI summary
                ai_summary = data.get('ai_summary', '')
                if ai_summary and len(ai_summary) > 100:
                    print(f"   🤖 AI Summary: Generated ({len(ai_summary)} characters)")
                else:
                    print(f"   ⚠️  AI Summary: Missing or too short")

                # Require temperature when Google Weather is the only source
                if data.get('current_temperature_celsius') is None:
                    print("❌ Land Data Endpoint: FAILED - Temperature missing (Google Weather not working)")
                    return False

                return True
            else:
                print(f"❌ Land Data Endpoint: FAILED - Status {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False
                
    except Exception as e:
        print(f"❌ Land Data Endpoint: ERROR - {str(e)}")
        return False


async def test_health_endpoint():
    """Test health endpoint"""
    print("\n" + "="*70)
    print("❤️  TESTING HEALTH ENDPOINT")
    print("="*70)
    
    try:
        base_url = "https://greenpulse-production-370c.up.railway.app"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{base_url}/health")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Health Endpoint: SUCCESS")
                print(f"   Status: {data.get('status')}")
                print(f"   Message: {data.get('message')}")
                print(f"   Database: {data.get('database')}")
                print(f"   Messaging:")
                messaging = data.get('messaging', {})
                for platform, status in messaging.items():
                    print(f"      - {platform}: {status}")
                return True
            else:
                print(f"❌ Health Endpoint: FAILED - Status {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Health Endpoint: ERROR - {str(e)}")
        return False


async def run_all_tests():
    """Run all tests and generate summary"""
    print("\n")
    print("🚀 " + "="*66 + " 🚀")
    print("   GREENPULSE BACKEND COMPREHENSIVE API TEST SUITE")
    print("🚀 " + "="*66 + " 🚀")
    print(f"\n📅 Test Date: {asyncio.get_event_loop().time()}")
    print(f"🔑 API Keys Configured:")
    print(f"   - Google Maps API Key: {'✓ Set' if settings.GOOGLE_MAPS_API_KEY else '✗ Missing'}")
    print(f"   - OpenRouter API Key: {'✓ Set' if settings.OPENROUTER_API_KEY else '✗ Missing'}")
    print(f"   - Supabase URL: {'✓ Set' if settings.SUPABASE_URL else '✗ Missing'}")
    print(f"   - Telegram Bot Token: {'✓ Set' if settings.TELEGRAM_BOT_TOKEN else '✗ Missing'}")
    
    results = {}
    
    # Run all tests
    results['health'] = await test_health_endpoint()
    results['google_weather'] = await test_google_weather_api()
    results['nasa_power'] = await test_nasa_power_api()
    results['ai_service'] = await test_ai_service()
    results['geocoding'] = await test_google_maps_geocoding()
    results['land_data'] = await test_land_data_endpoint()
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"   {status} - {test_name.replace('_', ' ').title()}")
    
    print("\n" + "="*70)
    print(f"   TOTAL: {passed}/{total} tests passed ({(passed/total)*100:.0f}%)")
    print("="*70 + "\n")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Backend is fully operational! 🎉\n")
    elif passed > 0:
        print(f"⚠️  SOME TESTS FAILED! {total - passed} issue(s) need attention.\n")
    else:
        print("❌ ALL TESTS FAILED! Check your configuration and API keys.\n")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
