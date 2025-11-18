"""
Example usage script for testing the CRM Chatbot API
"""

import requests
import json

BASE_URL = "http://localhost:5001/api/v1"

def test_chatbot():
    """Test the chatbot API"""
    
    print("=" * 50)
    print("CRM Chatbot API Test")
    print("=" * 50)
    
    # 1. Login
    print("\n1. Logging in...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "user", "password": "user123"}
    )
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        return
    
    token = login_response.json()["access_token"]
    print(f"✓ Login successful! Token: {token[:20]}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Test chat
    print("\n2. Testing chat endpoint...")
    test_messages = [
        "Hello, I need help",
        "What products do you have?",
        "How much does it cost?",
        "I want to track my order",
        "Goodbye"
    ]
    
    for message in test_messages:
        print(f"\n  Sending: '{message}'")
        chat_response = requests.post(
            f"{BASE_URL}/chat",
            headers=headers,
            json={"message": message, "user_id": "test_user_123"}
        )
        
        if chat_response.status_code == 200:
            data = chat_response.json()
            print(f"  Response: {data['response']}")
            print(f"  Intent: {data['intent']} (confidence: {data['confidence']:.2f})")
            print(f"  Sentiment: {data['sentiment']}")
        else:
            print(f"  Error: {chat_response.text}")
    
    # 3. Get context
    print("\n3. Getting conversation context...")
    context_response = requests.get(
        f"{BASE_URL}/context/test_user_123",
        headers=headers
    )
    
    if context_response.status_code == 200:
        context = context_response.json()
        print(f"  ✓ Context retrieved: {len(context['history'])} messages")
        print(f"  Profile: {context['profile']}")
    
    # 4. Test analytics (requires analyst/admin role)
    print("\n4. Testing analytics (login as analyst)...")
    analyst_login = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "analyst", "password": "analyst123"}
    )
    
    if analyst_login.status_code == 200:
        analyst_token = analyst_login.json()["access_token"]
        analyst_headers = {"Authorization": f"Bearer {analyst_token}"}
        
        stats_response = requests.get(
            f"{BASE_URL}/analytics/statistics",
            headers=analyst_headers
        )
        
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"  ✓ Statistics retrieved:")
            print(f"    Total interactions: {stats.get('total_interactions', 0)}")
            print(f"    Average confidence: {stats.get('average_confidence', 0):.2f}")
            print(f"    Intent distribution: {stats.get('intent_distribution', {})}")
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("=" * 50)


if __name__ == "__main__":
    try:
        test_chatbot()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API.")
        print("Make sure the Flask server is running (python app.py)")
    except Exception as e:
        print(f"Error: {e}")

