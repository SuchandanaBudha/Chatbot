import streamlit as st
from groq import Groq

# Set your Groq API key (either through environment or hardcoded here)
GROQ_API_KEY = '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'

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Page config
st.set_page_config(page_title="Gemma 2 Chatbot", page_icon="🤖")
st.title("💬 Chat with Gemma 2 (9B-Instruct) via Groq")

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful AI assistant."}]

# Display past messages
for msg in st.session_state.messages[1:]:  # skip system
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User prompt input
if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # LLM streaming response
    with st.chat_message("assistant"):
        response_box = st.empty()
        full_response = ""

        # Send message to Groq LLM
        stream = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=st.session_state.messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content or ""
            full_response += content
            response_box.markdown(full_response + "▌")  # typing indicator

        response_box.markdown(full_response)  # final output
        st.session_state.messages.append({"role": "assistant", "content": full_response})
