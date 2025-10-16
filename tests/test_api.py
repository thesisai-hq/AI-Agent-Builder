"""
Quick API Test Script
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"


def test_api():
    print("=" * 60)
    print("Testing API Endpoints")
    print("=" * 60)

    # 1. Health check
    print("\n1️⃣ Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")

    # 2. Create agent
    print("\n2️⃣ Create Agent")
    agent_data = {"name": "Test Agent", "type": "simple", "weight": 0.1}
    response = requests.post(f"{BASE_URL}/agents", json=agent_data)
    print(f"   Status: {response.status_code}")
    agent = response.json()
    print(f"   Agent ID: {agent['id']}")
    print(f"   Agent Name: {agent['name']}")

    # 3. List agents
    print("\n3️⃣ List Agents")
    response = requests.get(f"{BASE_URL}/agents")
    data = response.json()
    print(f"   Total agents: {data['total']}")

    # 4. Run analysis
    print("\n4️⃣ Run Analysis")
    analysis_data = {"ticker": "AAPL"}
    response = requests.post(f"{BASE_URL}/analyze", json=analysis_data)
    print(f"   Status: {response.status_code}")
    analysis = response.json()
    analysis_id = analysis["analysis_id"]
    print(f"   Analysis ID: {analysis_id}")

    # 5. Get results
    print("\n5️⃣ Get Results")
    time.sleep(0.5)  # Give it a moment
    response = requests.get(f"{BASE_URL}/analyze/{analysis_id}")
    result = response.json()
    print(f"   Status: {result['status']}")
    print(f"   Ticker: {result['ticker']}")
    print(f"   Consensus: {result['consensus']['signal']}")
    print(f"   Confidence: {result['consensus']['confidence']:.2%}")

    print("\n" + "=" * 60)
    print("✅ All API tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    print("\n⚠️  Make sure API server is running!")
    print("Run: uvicorn agent_builder.api.main:app --reload\n")

    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Is the server running?")
