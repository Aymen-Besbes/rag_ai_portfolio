import streamlit as st
from chat import query_portfolio
from retrieval import _load_resources  

# Streamlit page setup
st.set_page_config(page_title="Portfolio RAG Assistant", page_icon="🤖", layout="centered")
st.title("🤖 Portfolio RAG Assistant")

# Preload model, index, and chunks
with st.spinner("Loading model and portfolio data..."):
    _load_resources()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input 
user_input = st.chat_input("Ask a question about the portfolio:")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Display assistant typing placeholder
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Generating answer...")

    # Get response from your RAG assistant
    response = query_portfolio(user_input)

    # Update assistant message
    message_placeholder.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
