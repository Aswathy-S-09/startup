"""Direct test of Market Agent without the API layer."""
import json
import traceback

from models.input import StartupInput
from agents.market_agent import MarketAgent

startup = StartupInput(
    idea="An electric scooter rental platform with app-based booking, solar-powered charging stations, and AI-optimized route planning. Targeted at urban commuters aged 18-40 in metro cities. Green Transportation industry."
)

agent = MarketAgent()

try:
    result = agent.run(startup)
    print("SUCCESS!")
    print(json.dumps(result, indent=2))
except Exception as e:
    traceback.print_exc()
