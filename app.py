import streamlit as st
import os
import google.generativeai as genai

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Replace with your actual Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

# Function to fetch AI response
def fetch_financial_advice(user_query):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(f"Provide financial insights for: {user_query}")
        return response.text if response else "⚠️ No response received."
    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}"

# Streamlit Page Config
st.set_page_config(page_title="AI Financial Assistant", page_icon="💰", layout="wide")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Custom CSS for styling
st.markdown(
    """
    <style>
        .stApp { background-color: #2E5A88; padding: 10px; }
        .title { font-size: 45px; font-weight: bold; text-align: center; color: #ffffff; }
        .quote { font-size: 16px; font-style: italic; color: #E1F5FE; text-align: center; margin-bottom: 30px; }
        .chat-container { max-width: 70%; margin: auto; padding-bottom: 80px; }
        .chat-bubble { padding: 10px; border-radius: 10px; margin: 5px; max-width: 70%; }
        .user-msg { background-color: #D1FAE5; color: #065F46; text-align: right; margin-left: auto; }
        .ai-msg { background-color: #E5E7EB; color: #1F2937; text-align: left; margin-right: auto; }
        
        /* Fixed input box at bottom */
        .input-container {
            position: fixed;
            bottom: 10px;
            left: 0;
            width: 100%;
            display: flex;
            align-items: center;
            padding: 10px;
            background-color: #F3F4F6;
            box-shadow: 0px -2px 5px rgba(0, 0, 0, 0.1);
        }
        .input-container input {
            flex-grow: 1;
            height: 40px;
            border-radius: 5px;
            padding: 5px;
            font-size: 16px;
            border: 1px solid #ccc;
        }
        .send-btn {
            height: 40px;
            padding: 0 15px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 5px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
            margin-left: 10px;
        }
        .delete-btn {
            height: 30px;
            padding: 0 10px;
            font-size: 14px;
            background-color: #FF4B4B;
            color: white;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            margin-left: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar: Chat History with Delete Buttons
with st.sidebar:
    st.title("💬 Chat History")
    if st.session_state.chat_history:
        for idx, chat in enumerate(st.session_state.chat_history):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                if st.button(f"📝 {chat['question']}", key=f"load_{idx}"):
                    st.session_state.current_question = chat['question']
                    st.session_state.current_answer = chat['answer']
                    st.rerun()
            with col2:
                if st.button("❌", key=f"delete_{idx}"):
                    del st.session_state.chat_history[idx]
                    st.rerun()
    else:
        st.write("No chat history yet.")

    # Button to clear all chat history
    if st.button("🗑️ Clear All Chats"):
        st.session_state.chat_history = []
        st.rerun()

# Main Title
st.markdown("<h1 class='title'>GenFin</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='title'>Next-gen financial intelligence</h3>", unsafe_allow_html=True)

# Financial Quotes
st.markdown(
    """
    <p class='quote'>"The stock market is filled with individuals who know the price of everything but the value of nothing." – Philip Fisher</p>
    <p class='quote'>"An investment in knowledge pays the best interest." – Benjamin Franklin</p>
    <p class='quote'>"Do not save what is left after spending, but spend what is left after saving." – Warren Buffett</p>
    """,
    unsafe_allow_html=True
)

# Chat Display
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

if "current_question" in st.session_state and "current_answer" in st.session_state:
    st.markdown(f"<div class='chat-bubble user-msg'><b>You:</b> {st.session_state.current_question}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-bubble ai-msg'><b>AI:</b> {st.session_state.current_answer}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Fixed input box at the bottom
st.markdown('<div class="input-container">', unsafe_allow_html=True)
user_input = st.chat_input("Type your financial question here...")

# Handle User Input
if user_input:
    if st.session_state.get("last_question") != user_input:
        st.session_state.last_question = user_input  # Prevents multiple API calls
        response_text = fetch_financial_advice(user_input)

        # Save to chat history
        st.session_state.chat_history.append({"question": user_input, "answer": response_text})
        st.session_state.current_question = user_input
        st.session_state.current_answer = response_text

        st.rerun() 
