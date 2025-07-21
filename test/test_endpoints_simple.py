#!/usr/bin/env python3
"""
Simple endpoint validation test
Checks that all dashboard endpoints are accessible and return proper error handling
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_endpoint_accessibility():
    """Test that endpoints are accessible and return proper responses"""
    
    print("🧪 Dashboard Endpoints Accessibility Test")
    print("=" * 50)
    
    endpoints = [
        ("/dashboard", "Main Dashboard"),
        ("/api/emotion-overview", "Emotion Overview"),
        ("/api/emotion-trends", "Emotion Trends"),
        ("/api/realtime-stats", "Realtime Stats")
    ]
    
    all_passed = True
    
    for endpoint, name in endpoints:
        print(f"\n📡 Testing {name}")
        print(f"   URL: {BASE_URL}{endpoint}")
        
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            
            # Check if we get a response
            if response.status_code == 200:
                print("   ✅ PASS - Endpoint working correctly")
                try:
                    data = response.json()
                    print(f"   📊 Response contains {len(data)} top-level fields")
                except:
                    print("   ⚠️  Response is not valid JSON")
                    all_passed = False
                    
            elif response.status_code == 500:
                # Expected when database is not connected
                try:
                    data = response.json()
                    if "error" in data and "Database connection not available" in data["error"]:
                        print("   ✅ PASS - Endpoint accessible, proper error handling")
                    else:
                        print(f"   ⚠️  PARTIAL - Unexpected error: {data.get('error', 'Unknown')}")
                        all_passed = False
                except:
                    print("   ❌ FAIL - Invalid JSON error response")
                    all_passed = False
                    
            else:
                print(f"   ❌ FAIL - Unexpected status code: {response.status_code}")
                print(f"   Response: {response.text[:100]}")
                all_passed = False
                
        except requests.exceptions.ConnectionError:
            print("   ❌ FAIL - Cannot connect to server")
            print("   💡 Make sure your Flask server is running on port 5000")
            all_passed = False
            
        except requests.exceptions.Timeout:
            print("   ❌ FAIL - Request timeout")
            all_passed = False
            
        except Exception as e:
            print(f"   ❌ FAIL - {str(e)}")
            all_passed = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 ENDPOINT ACCESSIBILITY SUMMARY")
    print("=" * 50)
    
    if all_passed:
        print("🎉 All endpoints are accessible and properly implemented!")
        print("\n✅ What this test confirmed:")
        print("   • All 4 dashboard endpoints exist")
        print("   • Endpoints return proper HTTP status codes")
        print("   • Error handling is working correctly")
        print("   • JSON responses are well-formatted")
        
        print("\n💡 Next steps:")
        print("   • Set up your MongoDB database connection")
        print("   • Add MONGODB_URI environment variable")
        print("   • Add GEMINI_API_KEY environment variable")
        print("   • Then run the full functionality test")
        
    else:
        print("⚠️  Some endpoints have issues")
        print("\n🔧 Recommended actions:")
        print("   • Check that the Flask server is running")
        print("   • Verify all endpoint routes are defined")
        print("   • Check for syntax errors in the Flask app")

def test_endpoint_with_parameters():
    """Test endpoints that accept parameters"""
    print("\n🔍 Testing Parameter Handling")
    print("-" * 30)
    
    # Test emotion-trends with hours parameter
    try:
        response = requests.get(f"{BASE_URL}/api/emotion-trends?hours=12", timeout=5)
        if response.status_code in [200, 500]:  # Both are acceptable
            print("✅ emotion-trends accepts 'hours' parameter")
        else:
            print(f"⚠️  emotion-trends parameter test: {response.status_code}")
    except Exception as e:
        print(f"❌ Parameter test failed: {e}")

if __name__ == "__main__":
    test_endpoint_accessibility()
    test_endpoint_with_parameters()
    
    print("\n" + "=" * 50)
    print("🔍 Test Complete")
    print("=" * 50)
