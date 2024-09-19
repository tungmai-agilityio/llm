import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from document_loader import DocumentLoader

load_dotenv()

SUPPORTED_FILE_EXT = ["csv", "txt", "json"]

def main():
    st.title("💬 E-commerce Chatbot")

    # Initialize the DocumentLoader to handle file uploads
    document_loader = DocumentLoader()

    # File uploader component in the sidebar allowing multiple file uploads
    uploaded_files = st.sidebar.file_uploader(
        label='Upload files',
        type=list(document_loader.loader_config.keys()),
        accept_multiple_files=True
    )

    # Display an informational message to the user if no files have been uploaded.
    if not uploaded_files:
        st.info('Please upload documents to continue.')
        st.stop()

    # If files are uploaded, load them using the DocumentLoader
    docs = document_loader.load_multiples(uploaded_files)
    print(docs)

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
