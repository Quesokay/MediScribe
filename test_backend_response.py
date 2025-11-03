"""
Test script to verify backend is sending responses correctly
"""
import requests
import json
import sys

def test_agent_response():
    """Test if the agent is responding correctly"""
    
    # Configuration
    base_url = "http://localhost:8000"  # Adjust if your server runs on a different port
    
    print("Testing ADK backend response...")
    print("=" * 60)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print("✓ Server is running")
    except requests.exceptions.RequestException as e:
        print(f"✗ Server is not responding: {e}")
        print("\nMake sure the ADK server is running:")
        print("  adk api_server --allow_origins=http://localhost:4200")
        return False
    
    # Test 2: List available apps
    try:
        response = requests.get(f"{base_url}/apps", timeout=5)
        if response.status_code == 200:
            apps = response.json()
            print(f"✓ Available apps: {apps}")
            if not apps:
                print("  Warning: No apps found")
                return False
            app_name = apps[0]
        else:
            print(f"✗ Failed to get apps: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error getting apps: {e}")
        return False
    
    # Test 3: Create a session
    try:
        response = requests.post(
            f"{base_url}/users/test_user/apps/{app_name}/sessions",
            json={},
            timeout=5
        )
        if response.status_code == 200:
            session_data = response.json()
            session_id = session_data.get('id')
            print(f"✓ Created session: {session_id}")
        else:
            print(f"✗ Failed to create session: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error creating session: {e}")
        return False
    
    # Test 4: Send a test message
    try:
        print("\nSending test message: 'Hello, can you hear me?'")
        response = requests.post(
            f"{base_url}/users/test_user/apps/{app_name}/sessions/{session_id}/run",
            json={
                "newMessage": {
                    "role": "user",
                    "parts": [{"text": "Hello, can you hear me?"}]
                },
                "streaming": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Received response from backend")
            
            # Check if response has content
            if 'content' in result and 'parts' in result['content']:
                parts = result['content']['parts']
                print(f"\n✓ Response has {len(parts)} part(s)")
                
                for i, part in enumerate(parts):
                    if 'text' in part:
                        print(f"\n  Part {i+1} text:")
                        print(f"  {part['text'][:200]}...")  # First 200 chars
                        return True
                    else:
                        print(f"  Part {i+1}: {list(part.keys())}")
                
                print("\n✗ No text parts found in response")
                print(f"  Full response: {json.dumps(result, indent=2)}")
                return False
            else:
                print("\n✗ Response missing content/parts")
                print(f"  Response keys: {list(result.keys())}")
                print(f"  Full response: {json.dumps(result, indent=2)}")
                return False
        else:
            print(f"✗ Failed to send message: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error sending message: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("ADK Backend Response Test")
    print("=" * 60 + "\n")
    
    success = test_agent_response()
    
    print("\n" + "=" * 60)
    if success:
        print("✓ Backend is working correctly!")
        print("\nIf responses still don't show in the web UI:")
        print("1. Open browser DevTools (F12)")
        print("2. Check Console tab for errors")
        print("3. Check Network tab for SSE responses")
        print("4. Look for [DEBUG] logs in console")
    else:
        print("✗ Backend test failed")
        print("\nPlease fix the backend issues first")
    print("=" * 60 + "\n")
    
    sys.exit(0 if success else 1)
