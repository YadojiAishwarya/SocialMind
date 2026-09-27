import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

bank_id = "socialmind-demo"

posts = [
    {
        "post": "5 AI tools developers should know in 2026",
        "topic": "AI tools",
        "format": "List",
        "likes": 1200,
        "comments": 180,
        "shares": 90
    },
    {
        "post": "What is machine learning? A beginner explanation.",
        "topic": "Machine learning",
        "format": "Educational",
        "likes": 180,
        "comments": 25,
        "shares": 12
    },
    {
        "post": "3 AI tools that can save developers 2 hours every day",
        "topic": "AI productivity",
        "format": "List",
        "likes": 1600,
        "comments": 240,
        "shares": 130
    }
]

for post in posts:
    memory = f"""
Social media post:
{post["post"]}

Topic: {post["topic"]}
Format: {post["format"]}
Likes: {post["likes"]}
Comments: {post["comments"]}
Shares: {post["shares"]}
"""

    client.retain(
        bank_id=bank_id,
        content=memory
    )

print("✅ 3 social-media posts added to Hindsight!")

client.close()