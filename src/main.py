import streamlit as st
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from chain import create_qa_history_chain
from retriever import configure_retriever
from document_loader import DocumentLoader

load_dotenv()
SUPPORTED_FILE_EXT = ['csv', 'txt', 'json']

# Initialize session state
if 'chain' not in st.session_state:
    st.session_state.chain = None
if 'files' not in st.session_state:
    st.session_state.files = None

def main():
    st.title('💬 E-commerce Chatbot')

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

    # NOTE: By default Streamlit reruns the entire script when there's user input.
    # Only recreate the chain if it was not created yet or a new file is uploaded.
    if st.session_state.chain is None or st.session_state.files != uploaded_files:
        print('Initiating Chain')
        # If files are uploaded, load them using the DocumentLoader
        docs = document_loader.load_multiples(uploaded_files)
        # Construct retriever
        retriever = configure_retriever(docs)
        llm = ChatOpenAI(model='gpt-3.5-turbo')

        # Save the state
        st.session_state.chain = create_qa_history_chain(llm, retriever)
        st.session_state.files = uploaded_files

    if 'messages' not in st.session_state:
        st.session_state['messages'] = [{'role': 'assistant', 'content': 'How can I help you?'}]

    for msg in st.session_state.messages:
        st.chat_message(msg['role']).write(msg['content'])

    if prompt := st.chat_input('Message'):
        # Append user's message to history and show on the UI
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        st.chat_message('user').write(prompt)

        # Get response
        response = st.session_state.chain.invoke(
            {
                'input': prompt,
                'chat_history': st.session_state.messages
            },
            config= {
                'configurable': {
                    'session_id': '123'
                }
            }
        )['answer']

        # Append response message to history and show on the UI
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.chat_message('assistant').write(response)

if __name__ == "__main__":
    main()
