import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

bank_id = "socialmind-demo"

result = client.recall(
    bank_id=bank_id,
    query="Which types of social media posts have performed best for our audience?"
)

print("\n🧠 SocialMind remembers:\n")

for memory in result.results:
    print("-", memory.text)

client.close()