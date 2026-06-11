#!/usr/bin/env python3
"""Test script voor de demo functionaliteit"""

import requests
import json
import time

BASE_URL = "http://localhost:5001"

def test_demo_flow():
    print("🧪 Testing Botlease Demo Flow...")
    print("-" * 50)
    
    # 1. Start conversation
    print("\n1. Starting conversation...")
    start_response = requests.post(
        f"{BASE_URL}/api/start-conversation",
        json={}
    )
    
    if start_response.status_code == 200:
        data = start_response.json()
        session_id = data['session_id']
        print(f"✅ Session started: {session_id}")
        print(f"📝 Welcome message:\n{data['message']}\n")
    else:
        print(f"❌ Failed to start conversation: {start_response.text}")
        return
    
    # 2. Send website URL
    print("\n2. Sending website URL...")
    website_response = requests.post(
        f"{BASE_URL}/api/send-message",
        json={
            "session_id": session_id,
            "message": "www.bakkerij-jansen.nl"
        }
    )
    
    if website_response.status_code == 200:
        response = website_response.json()['response']
        print(f"🤖 Bot: {response}\n")
    else:
        print(f"❌ Failed: {website_response.text}")
        return
    
    # 3. Test demo questions
    print("\n3. Testing demo mode with customer questions...")
    demo_questions = [
        "Wat zijn jullie openingstijden?",
        "Kan ik online bestellen?",
        "Hebben jullie glutenvrije producten?"
    ]
    
    for question in demo_questions:
        print(f"\n👤 User: {question}")
        
        msg_response = requests.post(
            f"{BASE_URL}/api/send-message",
            json={
                "session_id": session_id,
                "message": question
            }
        )
        
        if msg_response.status_code == 200:
            response = msg_response.json()['response']
            print(f"🤖 Bot: {response}")
        else:
            print(f"❌ Failed: {msg_response.text}")
        
        time.sleep(1)
    
    print("\n" + "-" * 50)
    print("✅ Demo test completed!")

if __name__ == "__main__":
    # Check if server is running
    try:
        health = requests.get(f"{BASE_URL}/health")
        if health.status_code == 200:
            print("✅ Server is running")
            test_demo_flow()
        else:
            print("❌ Server health check failed")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server at http://localhost:5001")
        print("Start the server with: python app.py")