import os
from dotenv import load_dotenv
from hindsight_client import Hindsight
from groq import Groq

load_dotenv()

# Connect to Hindsight
hindsight = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

# Connect to Groq
groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

bank_id = "socialmind-demo"

# Ask Hindsight for relevant memories
result = hindsight.recall(
    bank_id=bank_id,
    query="Which social media posts performed best for our audience and why?"
)

# Turn the memories into text
memories = "\n".join(
    memory.text for memory in result.results
)

# Ask the AI to reason over those memories
response = groq.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content": """
You are SocialMind, an AI social-media strategist.

Use ONLY the memories provided to you.
Analyze the past posts and identify useful patterns.
Then recommend what type of post the brand should create next.

Be concise and practical.
"""
        },
        {
            "role": "user",
            "content": f"""
Here are the memories from previous social-media posts:

{memories}

Based on these memories:
1. What appears to work well?
2. What should we post next?
3. Give one example post idea.
"""
        }
    ]
)

print("\n🤖 SocialMind recommendation:\n")
print(response.choices[0].message.content)

hindsight.close()