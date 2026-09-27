import os
import nest_asyncio
import streamlit as st
from dotenv import load_dotenv
from hindsight_client import Hindsight
from groq import Groq

nest_asyncio.apply()

load_dotenv()
import streamlit as st
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
groq = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

bank_id = "socialmind-demo"
if "post_count" not in st.session_state:
    st.session_state.post_count = 3


# -----------------------------
# Page setup
# -----------------------------

st.set_page_config(
    page_title="SocialMind",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 SocialMind")
st.subheader("An AI Social Media Agent That Learns From Your Audience")

st.caption(
    "Powered by Hindsight memory + AI"
)
st.write(
    "SocialMind remembers your past posts and learns what your audience responds to."
)

st.divider()


# -----------------------------
# Dashboard
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Posts Remembered", "5")
with col2:
    st.metric("Memory System", "Hindsight")

with col3:
    st.metric("AI Model", "Groq")


st.divider()


# -----------------------------
# Ask SocialMind
# -----------------------------

st.header("💬 Ask SocialMind")

question = st.text_input(
    "What would you like to know?",
    placeholder="What should I post tomorrow?"
)

if st.button("🚀 Ask SocialMind"):

    if not question:
        st.warning("Please enter a question.")

    else:
        with st.spinner("🧠 Searching SocialMind's memory..."):

            result = hindsight.recall(
                bank_id=bank_id,
                query=question
            )

            memories = "\n".join(
                memory.text for memory in result.results
            )

        with st.spinner("🤖 Creating recommendation..."):

            response = groq.chat.completions.create(
              model="openai/gpt-oss-120b",  
                messages=[
                    {
                        "role": "system",
                        "content": """
You are SocialMind, an AI social-media strategist.

Use ONLY the memories provided to you.

Analyze the previous social-media performance and identify useful patterns.

Then give a practical recommendation for the user's question.

Be concise, clear, and useful.
"""
                    },
                    {
                        "role": "user",
                        "content": f"""
Question:

{question}

Memories from previous social-media activity:

{memories}

Based on these memories, answer the user's question.
"""
                    }
                ]
            )

            recommendation = response.choices[0].message.content

        st.success("✅ SocialMind has learned from its memory!")

        st.subheader("🤖 Recommendation")

        st.write(recommendation)

        with st.expander("🧠 Memories used by SocialMind"):
            st.write(memories)


st.divider()

st.header("📈 Learning")

st.write(
    "SocialMind improves its recommendations by remembering previous "
    "posts and their audience responses."
)
st.divider()

st.header("🧠 Teach SocialMind")

st.write("Add a new post result so SocialMind can learn from it.")

new_post = st.text_input(
    "Post",
    placeholder="Example: 5 AI coding tools developers should try"
)

col1, col2, col3 = st.columns(3)

with col1:
    likes = st.number_input("Likes", min_value=0, value=0)

with col2:
    comments = st.number_input("Comments", min_value=0, value=0)

with col3:
    shares = st.number_input("Shares", min_value=0, value=0)

if st.button("🧠 Remember This Post"):

    if new_post:
        memory = f"""
Social media post:
{new_post}

Likes: {likes}
Comments: {comments}
Shares: {shares}
"""

        hindsight.retain(
            bank_id=bank_id,
            content=memory
        )
        

        st.success("✅ SocialMind remembered this post!")

    else:
        st.warning("Please enter the post first.")
        st.divider()

st.header("🧠 What SocialMind Learned")

st.success("Practical AI content performs well with this audience.")
st.success("Developer-focused topics receive strong engagement.")
st.success("List-style posts have performed well.")

st.info(
    "📈 Recent high-performing post: "
    "5 AI coding tools developers should try — 2,400 likes"
)

st.divider()

st.header("🏆 Best Performing Posts")

best_posts = hindsight.recall(
    bank_id=bank_id,
    query="Which social media posts had the highest likes, comments, and shares?"
)

if best_posts.results:

    shown = set()

    for memory in best_posts.results:

        text = memory.text.strip()

        if text not in shown:
            st.write("📌", text)
            shown.add(text)

        if len(shown) == 3:
            break

else:
    st.write("No performance data found yet.")
st.divider()

st.header("🔄 Before vs After Learning")

st.write(
    "See how SocialMind's recommendation changes after learning "
    "from your audience's previous performance."
)

if st.button("✨ Show Learning Improvement"):

    st.subheader("Before Learning")

    st.write(
        "Post about AI because AI is currently popular."
    )

    st.subheader("🧠 After Learning")

    st.write(
        "Create a practical, developer-focused AI post, preferably "
        "in a list format. Previous audience data shows that "
        "practical AI and developer-focused content received strong "
        "engagement."
    )

    st.success(
        "SocialMind changed from a generic suggestion to a "
        "memory-informed recommendation."
    ) 


    

