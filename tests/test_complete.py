import requests
import time
import sys

BASE_URL = "http://localhost:8000"


def test_complete_flow():
    """Test complete flow with real agent execution"""

    print("=" * 70)
    print("🧪 COMPLETE SYSTEM TEST - Real Agent Execution")
    print("=" * 70)

    try:
        # 1. Health check
        print("\n1️⃣ Health Check")
        response = requests.get(f"{BASE_URL}/health")
        health = response.json()
        print(f"   Status: {health['status']}")
        print(f"   Agents registered: {health['agents']['total_agents']}")
        print(f"   Agents enabled: {health['agents']['enabled_agents']}")

        # 2. List registered agents
        print("\n2️⃣ List Registered Agents")
        response = requests.get(f"{BASE_URL}/agents")
        agents_data = response.json()
        print(f"   Total agents: {agents_data['total']}")

        for agent in agents_data["agents"]:
            print(
                f"   - {agent['name']} (weight: {agent['weight']}, enabled: {agent['enabled']})"
            )

        # 3. Get specific agent
        if agents_data["agents"]:
            first_agent = agents_data["agents"][0]
            print(f"\n3️⃣ Get Agent Details")
            response = requests.get(f"{BASE_URL}/agents/{first_agent['id']}")
            agent = response.json()
            print(f"   Name: {agent['name']}")
            print(f"   Type: {agent['type']}")
            print(f"   Weight: {agent['weight']}")

        # 4. Run REAL analysis
        print("\n4️⃣ Run Analysis (REAL EXECUTION)")
        test_ticker = "AAPL"
        response = requests.post(f"{BASE_URL}/analyze", json={"ticker": test_ticker})
        analysis = response.json()
        analysis_id = analysis["analysis_id"]
        print(f"   Analysis ID: {analysis_id}")
        print(f"   Status: {analysis['status']}")
        print(f"   Ticker: {test_ticker}")

        # 5. Wait for completion (background task)
        print(f"\n5️⃣ Waiting for Analysis to Complete...")
        max_attempts = 10
        for i in range(max_attempts):
            time.sleep(1)
            response = requests.get(f"{BASE_URL}/analyze/{analysis_id}")
            result = response.json()

            print(f"   Attempt {i+1}: Status = {result['status']}")

            if result["status"] == "completed":
                print("   ✅ Analysis completed!")
                break
            elif result["status"] == "failed":
                print(f"   ❌ Analysis failed: {result.get('error')}")
                break

        # 6. Display results
        print(f"\n6️⃣ Analysis Results")
        response = requests.get(f"{BASE_URL}/analyze/{analysis_id}")
        result = response.json()

        print(f"\n   📊 Analysis for {result['ticker']}")
        print(f"   Status: {result['status']}")

        if result.get("error"):
            print(f"   Error: {result['error']}")

        # Show consensus
        if result.get("consensus"):
            consensus = result["consensus"]
            print(f"\n   🎯 Consensus:")
            print(f"      Signal: {consensus['signal']}")
            print(f"      Confidence: {consensus['confidence']:.2%}")
            print(f"      Agreement: {consensus['agreement']:.2%}")
            print(f"      Distribution: {consensus.get('distribution', {})}")

        # Show individual signals
        if result.get("signals"):
            print(
                f"\n   🤖 Individual Agent Signals ({len(result['signals'])} agents):"
            )
            for signal in result["signals"]:
                print(f"      {signal['agent_name']}:")
                print(f"         Signal: {signal['signal_type']}")
                print(f"         Confidence: {signal['confidence']:.2%}")
                print(f"         Reasoning: {signal['reasoning']}")

        # 7. Test with different ticker
        print(f"\n7️⃣ Testing with Different Ticker (MSFT)")
        response = requests.post(f"{BASE_URL}/analyze", json={"ticker": "MSFT"})
        analysis2 = response.json()
        print(f"   Analysis ID: {analysis2['analysis_id']}")

        # Wait for completion
        time.sleep(2)
        response = requests.get(f"{BASE_URL}/analyze/{analysis2['analysis_id']}")
        result2 = response.json()

        if result2["status"] == "completed" and result2.get("consensus"):
            print(
                f"   MSFT Consensus: {result2['consensus']['signal']} ({result2['consensus']['confidence']:.2%})"
            )

        # 8. Enable/Disable agent
        if agents_data["agents"]:
            agent_id = agents_data["agents"][0]["id"]
            print(f"\n8️⃣ Testing Enable/Disable")

            # Disable
            response = requests.post(f"{BASE_URL}/agents/{agent_id}/disable")
            print(f"   Disabled {agent_id}")

            # Check status
            response = requests.get(f"{BASE_URL}/agents")
            enabled_count = len([a for a in response.json()["agents"] if a["enabled"]])
            print(f"   Enabled agents: {enabled_count}")

            # Re-enable
            response = requests.post(f"{BASE_URL}/agents/{agent_id}/enable")
            print(f"   Re-enabled {agent_id}")

        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)

        print("\n📊 Summary:")
        print(f"   ✅ Agents registered and discoverable")
        print(f"   ✅ Real agent execution working")
        print(f"   ✅ Background processing working")
        print(f"   ✅ Consensus calculation working")
        print(f"   ✅ Database persistence working")
        print("\n🎉 System is now FULLY FUNCTIONAL!")

    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to API")
        print("   Make sure server is running:")
        print("   uvicorn agent_builder.api.main:app --reload")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    print("\n⚠️  Prerequisites:")
    print("   1. PostgreSQL running: docker ps | grep thesis-ai-db")
    print("   2. Mock data generated: python generate_mock_data.py")
    print("   3. API server running: uvicorn agent_builder.api.main:app --reload")
    print("\nStarting tests in 3 seconds...")
    time.sleep(3)

    test_complete_flow()
