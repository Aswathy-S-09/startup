"""Quick test script for Market Agent API endpoint."""
import requests
import json

payload = {
    "startup_name": "EcoRide",
    "problem_statement": "Urban commuters waste hours in traffic and contribute to pollution due to lack of affordable eco-friendly last-mile transportation.",
    "proposed_solution": "An electric scooter rental platform with app-based booking, solar-powered charging stations, and AI-optimized route planning.",
    "target_audience": "Urban commuters aged 18-40, college students, and office workers in metro cities",
    "industry": "Green Transportation / Urban Mobility",
}

print("=" * 60)
print("Testing Market Agent...")
print("=" * 60)

try:
    resp = requests.post(
        "http://localhost:8000/api/v1/analyze/market",
        json=payload,
        timeout=120,
    )
    print(f"Status: {resp.status_code}")
    print(json.dumps(resp.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
