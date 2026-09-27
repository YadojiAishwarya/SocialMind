import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

# Load our secret settings from .env
load_dotenv()

# Connect to Hindsight
client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

# Our first memory bank
bank_id = "socialmind-demo"

# Create the memory bank
client.create_bank(
    bank_id=bank_id,
    name="SocialMind Demo"
)

# Store a memory
client.retain(
    bank_id=bank_id,
    content="Our audience responds very well to practical AI tips for developers."
)

print("✅ Memory stored!")

# Ask Hindsight to remember it
result = client.recall(
    bank_id=bank_id,
    query="What kind of content does our audience respond well to?"
)

print("\n🧠 Hindsight remembered:")

for memory in result.results:
    print("-", memory.text)

client.close()