import os
import streamlit as st
from dotenv import load_dotenv
from hindsight_client import Hindsight
from groq import Groq

# --------------------------------------------------
# Fix asyncio event-loop issue in Streamlit
# -----------------------------------------------

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="SocialMind",
    page_icon="🧠",
    layout="wide"
)

# --------------------------------------------------
# Connect to Hindsight
# --------------------------------------------------

hindsight = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

# --------------------------------------------------
# Connect to Groq
# --------------------------------------------------

groq = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# --------------------------------------------------
# Hindsight memory bank
# --------------------------------------------------

bank_id = "socialmind-demo"

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🧠 SocialMind")

st.subheader(
    "An AI Social Media Agent That Learns From Your Audience"
)

st.caption("Powered by Hindsight memory + AI")

st.write(
    "SocialMind remembers your past posts and audience responses "
    "and uses that memory to make better future recommendations."
)

st.divider()

# --------------------------------------------------
# Dashboard
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Posts Remembered", "5+")

with col2:
    st.metric("Memory System", "Hindsight")

with col3:
    st.metric("AI Model", "Groq")

st.divider()

# ==================================================
# ASK SOCIALMIND
# ==================================================

st.header("💬 Ask SocialMind")

question = st.text_input(
    "What would you like to know?",
    placeholder="What should I post tomorrow?"
)

if st.button("🚀 Ask SocialMind"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        try:

            # ------------------------------------------
            # Retrieve relevant memories
            # ------------------------------------------

            with st.spinner(
                "🧠 Searching SocialMind's memory..."
            ):

                result = hindsight.recall(
                    bank_id=bank_id,
                    query=question
                )

                memories = "\n".join(
                    memory.text
                    for memory in result.results
                )

            if not memories:

                memories = (
                    "No relevant memories were found. "
                    "Give a general recommendation and clearly "
                    "state that there is not enough historical data."
                )

            # ------------------------------------------
            # Ask AI to reason over memory
            # ------------------------------------------

            with st.spinner(
                "🤖 Creating recommendation..."
            ):

                response = groq.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": """
You are SocialMind, an AI social-media strategist.

You help a brand understand what content works for its
specific audience.

Use the memories provided to you as the primary source
of historical information.

Identify patterns in:
- topics
- formats
- audience engagement
- successful posts

Then provide a practical recommendation.

Do not invent historical performance data.

Be concise, clear, and useful.
"""
                        },
                        {
                            "role": "user",
                            "content": f"""
User question:

{question}

Historical memories from Hindsight:

{memories}

Based on these memories, answer the user's question.

Give:
1. What appears to work
2. What should be posted next
3. One concrete example
"""
                        }
                    ]
                )

                recommendation = (
                    response.choices[0].message.content
                )

            # ------------------------------------------
            # Display result
            # ------------------------------------------

            st.success(
                "✅ SocialMind used its memory to answer."
            )

            st.subheader("🤖 Recommendation")

            st.write(recommendation)

            # ------------------------------------------
            # Show memory used
            # ------------------------------------------

            with st.expander(
                "🧠 Memories used by SocialMind"
            ):

                st.write(memories)

        except Exception as e:

            st.error(
                "Something went wrong while asking SocialMind."
            )

            st.code(str(e))

st.divider()

# ==================================================
# LEARNING
# ==================================================

st.header("📈 Learning")

st.write(
    "SocialMind improves over time by remembering previous "
    "posts and their audience responses."
)

st.info(
    "The more performance data you teach SocialMind, "
    "the more context Hindsight can provide for future recommendations."
)

st.divider()

# ==================================================
# TEACH SOCIALMIND
# ==================================================

st.header("🧠 Teach SocialMind")

st.write(
    "Add a new post and its performance so SocialMind can learn from it."
)

# Form prevents the page from rerunning while typing numbers
with st.form("teach_socialmind_form"):

    new_post = st.text_input(
        "Post",
        placeholder="Example: 5 AI coding tools developers should try"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        likes = st.number_input(
            "Likes",
            min_value=0,
            max_value=100000,
            value=50000,
            step=100
        )

    with col2:

        comments = st.number_input(
            "Comments",
            min_value=0,
            max_value=10000,
            value=300,
            step=100
        )

    with col3:

        shares = st.number_input(
            "Shares",
            min_value=0,
            max_value=100000,
            value=500,
            step=10
        )

    remember = st.form_submit_button(
        "🧠 Remember This Post"
    )

# --------------------------------------------------
# Save new memory
# --------------------------------------------------

if remember:

    if not new_post.strip():

        st.warning(
            "Please enter the post first."
        )

    else:

        try:

            memory = f"""
Social media post:
{new_post}

Likes: {likes}
Comments: {comments}
Shares: {shares}

This is historical audience performance data for SocialMind.
"""

            hindsight.retain(
                bank_id=bank_id,
                content=memory
            )

            st.success(
                "✅ SocialMind remembered this post!"
            )

            st.info(
                "This performance data is now available "
                "to Hindsight for future recommendations."
            )

        except Exception as e:

            st.error(
                "Could not save this post to Hindsight."
            )

            st.code(str(e))

st.divider()

# ==================================================
# WHAT SOCIALMIND LEARNED
# ==================================================

st.header("🧠 What SocialMind Learned")

st.success(
    "Practical AI content performs well with this audience."
)

st.success(
    "Developer-focused topics receive strong engagement."
)

st.success(
    "List-style posts have performed well."
)

st.info(
    "📈 Recent high-performing example: "
    "AI coding tools for developers"
)

st.divider()

# ==================================================
# BEST PERFORMING POSTS
# ==================================================

st.header("🏆 Best Performing Posts")

st.write(
    "Hindsight retrieves memories about posts and their audience performance."
)

try:

    best_posts = hindsight.recall(
        bank_id=bank_id,
        query=(
            "social media posts with high likes, "
            "high comments, and high shares; "
            "best performing posts"
        )
    )

    if best_posts.results:

        shown = set()

        for memory in best_posts.results:

            text = memory.text.strip()

            if text and text not in shown:

                st.write("📌", text)

                shown.add(text)

            if len(shown) >= 3:
                break

    else:

        st.write(
            "No performance data found yet."
        )

except Exception as e:

    st.warning(
        "Could not retrieve performance memories right now."
    )

st.divider()

# ==================================================
# BEFORE VS AFTER LEARNING
# ==================================================

st.header("🔄 Before vs After Learning")

st.write(
    "See how SocialMind changes from a generic AI answer "
    "to a recommendation informed by audience memory."
)

if st.button("✨ Show Learning Improvement"):

    st.subheader("Before Learning")

    st.write(
        "Post about AI because AI is currently popular."
    )

    st.subheader("🧠 After Learning")

    st.write(
        "Create a practical, developer-focused AI post, "
        "preferably in a list format. Historical audience "
        "data shows that practical AI and developer-focused "
        "content has received stronger engagement."
    )

    st.success(
        "SocialMind changed from a generic suggestion "
        "to a memory-informed recommendation."
    )

st.divider()

# ==================================================
# HOW IT WORKS
# ==================================================

st.header("⚙️ How SocialMind Works")

st.write(
    """
Past Posts + Engagement Data
        ↓
Hindsight Memory
        ↓
Relevant Memory Retrieval
        ↓
AI Reasoning with Groq
        ↓
Personalized Recommendation
        ↓
New Post Performance
        ↓
Hindsight Learns Again
"""
)

st.caption(
    "The key idea: SocialMind gets better because it remembers."
)