import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SUPPORTED_FILE_EXT = ["csv", "txt", "json"]

def main():
    st.title("💬 E-commerce Chatbot")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input('Message'):
        client = OpenAI()

        # Append user's message to history and show on the UI
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Get response from OpenAI
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content

        # Append response message to history and show on the UI
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

main()
