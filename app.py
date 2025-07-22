import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from utils.retriever import Retriever
from utils.generator import Generator
from utils.prompt_utils import build_prompt
import json
load_dotenv()

# def chat_bubble(message, is_user=True):
#     align = "right" if is_user else "left"
#     color = "#DCF8C6" if is_user else "#F1F0F0"
#     st.markdown(
#         f"""
#         <div style='text-align: {align}; background-color: {color}; padding: 12px 18px;
#                     border-radius: 15px; margin: 10px; display: inline-block; max-width: 80%;'>
#             {message}
#         </div>
#         """,
#         unsafe_allow_html=True
#     )



# Load and cache tweet data
@st.cache_data
def load_data():
    df = pd.read_csv("data/tweets.csv")
    return df['Tweet'].dropna().astype(str).tolist()

# Configure layout
st.set_page_config(page_title="World Cup RAG Chatbot", layout="centered")


st.title("🏆 World Cup 2022 Chatbot 🏆")

# Initialize state
if "retriever" not in st.session_state:
    st.session_state.retriever = Retriever()
    st.session_state.docs = load_data()
    st.session_state.retriever.fit(st.session_state.docs)
    
    
    

if "generator" not in st.session_state:
    st.session_state.generator = Generator()

if "history" not in st.session_state:
    st.session_state.history = []
    
    
    
    
# Suggested questions
st.markdown("#### 💡 Suggested questions")
suggested_queries = [
    "Is Messi liked?",
    "Who were the top players in World Cup 2022?",
    "What do people think about Ronaldo?",
    "Which team had the most support?",
    "Was the World Cup controversial?"
]

cols = st.columns(len(suggested_queries))
for i, question in enumerate(suggested_queries):
    with cols[i]:
        if st.button(question):
            st.session_state.suggested_query = question


# Chat input
query = st.chat_input("Ask something about the tweets...")

# If user clicked a suggested question, auto-fill it
if "suggested_query" in st.session_state:
    query = st.session_state.suggested_query
    del st.session_state.suggested_query  # reset after use


# FINAL SO FAR THAT IT WORKS

for i, msg in enumerate(st.session_state.history):
    with st.chat_message("user"):
        st.markdown(msg["query"])

    with st.chat_message("assistant"):
        st.markdown(msg["answer"])

        if f"feedback_{i}" not in st.session_state:
            st.session_state[f"feedback_{i}"] = "none"

        col1, col2, _ = st.columns([1, 1, 4])
        with col1:
            if st.button("👍", key=f"like_{i}"):
                st.session_state[f"feedback_{i}"] = "like"
        with col2:
            if st.button("👎", key=f"dislike_{i}"):
                st.session_state[f"feedback_{i}"] = "dislike"
        if st.session_state[f"feedback_{i}"] != "none":
            st.markdown(
                f"**You selected:** 👍" if st.session_state[f"feedback_{i}"] == "like" else "**You selected:** 👎"
            )


# for i, msg in enumerate(st.session_state.history):
#     with st.chat_message("user"):
#         st.markdown(
#             f"""
#             <div class="chat-bubble user">
#                 {msg['query']}
#                 <button class="copy-btn" onclick="navigator.clipboard.writeText(`{msg['query']}`)">📋</button>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#     with st.chat_message("assistant"):
#         st.markdown(
#             f"""
#             <div class="chat-bubble assistant">
#                 {msg['answer']}
#                 <button class="copy-btn" onclick="navigator.clipboard.writeText(`{msg['answer']}`)">📋</button>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#         # Feedback buttons
#         col1, col2, _ = st.columns([1, 1, 4])
#         with col1:
#             if st.button("👍", key=f"like_{i}"):
#                 st.session_state[f"feedback_{i}"] = "like"
#         with col2:
#             if st.button("👎", key=f"dislike_{i}"):
#                 st.session_state[f"feedback_{i}"] = "dislike"

#         if f"feedback_{i}" in st.session_state and st.session_state[f"feedback_{i}"] != "none":
#             st.markdown(
#                 f"**You selected:** {'👍' if st.session_state[f'feedback_{i}'] == 'like' else '👎'}"
#             )

# Handle user query
if query:
    with st.chat_message("user"):
        st.markdown(query)

    retrieved_docs = st.session_state.retriever.retrieve(query)

    with st.expander("🔍 Retrieved Tweets"):
        for doc, score in retrieved_docs:
            st.markdown(f"> {doc}\n\n**Score:** {score:.2f}")

    prompt = build_prompt(retrieved_docs, query)
    with st.spinner("Generating answer..."):
        #response = st.session_state.generator.generate(prompt)
        response = st.session_state.generator.generate(query, retrieved_docs)


    with st.chat_message("assistant"):
        st.markdown(response)

    # Save to history
    # st.session_state.history.append({
    #     "query": query,
    #     "answer": response
    # })
    
    
    #     # Save to history
    # st.session_state.history.append({
    #     "query": query,
    #     "answer": response
    # })

    # # Invisible anchor for scroll target
    # st.markdown("<div id='scroll-anchor'></div>", unsafe_allow_html=True)

    # # Auto-scroll after response
    # st.markdown("""
    # <script>
    #     setTimeout(() => {
    #         const anchor = document.getElementById("scroll-anchor");
    #         if (anchor) {
    #             anchor.scrollIntoView({ behavior: "smooth" });
    #         }
    #     }, 100);  // slight delay to allow DOM to render
    # </script>
    # """, unsafe_allow_html=True)

        
        # Save to history
    st.session_state.history.append({
        "query": query,
        "answer": response,
        "retrieved_docs": retrieved_docs
    })

    # Scroll anchor directly after response
    st.markdown("<div id='scroll-anchor'></div>", unsafe_allow_html=True)
    st.markdown("""
    <script>
        setTimeout(() => {
            const anchor = document.getElementById("scroll-anchor");
            if (anchor) {
                anchor.scrollIntoView({ behavior: "smooth" });
            }
        }, 300);  // Adjust delay if needed
    </script>
    """, unsafe_allow_html=True)

    
    
    
    
    
    
    
    
     # Invisible anchor for scroll target
    st.markdown("<div id='scroll-anchor'></div>", unsafe_allow_html=True)
  

    # Auto-scroll script
    st.markdown("""
    <script>
        const anchor = document.getElementById("scroll-anchor");
        const scrollY = window.scrollY + window.innerHeight;
        const bottomThreshold = document.body.scrollHeight - 200;
        const showBtn = scrollY < bottomThreshold;

        if (anchor && !showBtn) {
            anchor.scrollIntoView({ behavior: "smooth" });
        }
    </script>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        #scroll-btn {
            position: fixed;
            bottom: 60px;
            right: 30px;
            background-color: #4CAF50;
            color: white;
            padding: 10px 14px;
            border-radius: 30px;
            border: none;
            cursor: pointer;
            z-index: 9999;
            font-size: 18px;
            display: none;
        }
    </style>
    <button id="scroll-btn">⬇️</button>
    <script>
        const scrollBtn = document.getElementById("scroll-btn");
        const threshold = document.body.scrollHeight - 300;
        if (window.scrollY + window.innerHeight < threshold) {
            scrollBtn.style.display = "block";
        }

        scrollBtn.onclick = () => {
            document.getElementById("scroll-anchor").scrollIntoView({ behavior: "smooth" });
        }
    </script>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Send Feedback")
    if st.sidebar.button("Send Feedback"):
        feedback_data = []
        for i, msg in enumerate(st.session_state.history):
            feedback = st.session_state.get(f"feedback_{i}", "none")
            feedback_data.append({
                "query": msg["query"],
                "answer": msg["answer"],
                "feedback": feedback
            })

        st.sidebar.download_button(
            label="📥 Download Feedback JSON",
            data=json.dumps(feedback_data, indent=2),
            file_name="feedback.json",
            mime="application/json"
        )
        
    
    if st.sidebar.button("Download Chat History"):
        import json
        st.download_button(
            label="Download Chat",
            data=json.dumps(st.session_state.history, indent=2),
            file_name="chat_history.json",
            mime="application/json"
        )

