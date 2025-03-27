import streamlit as st
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from chain import create_qa_history_chain
from retriever import configure_retriever
from document_loader import DocumentLoader

load_dotenv()
SUPPORTED_FILE_EXT = ['csv', 'txt', 'json']
st.set_page_config('E-Commerce Platform')

# Initialize session state
if 'chain' not in st.session_state:
    st.session_state.chain = None
if 'files' not in st.session_state:
    st.session_state.files = None

def create_chain(files):
    # Initialize the DocumentLoader to handle file uploads
    document_loader = DocumentLoader()
    # If files are uploaded, load them using the DocumentLoader
    docs = document_loader.load_multiples(files)
    # Construct retriever
    retriever = configure_retriever(docs)
    llm = ChatOpenAI(model='gpt-3.5-turbo')
    # Create QA chain
    chain = create_qa_history_chain(llm, retriever)
    return chain

def generate_response(input):
    response = st.session_state.chain.invoke(
        {
            'input': input,
            'chat_history': st.session_state.messages
        },
        config= {
            'configurable': {
                'session_id': '123'
            }
        }
    )['answer']

    return response

def main():
    st.title('💬 E-commerce Chatbot')

    try:
        # File uploader component in the sidebar allowing multiple file uploads
        uploaded_files = st.sidebar.file_uploader(
            label='Upload files',
            type=SUPPORTED_FILE_EXT,
            accept_multiple_files=True
        )

        # Display an informational message to the user if no files have been uploaded.
        if not uploaded_files:
            st.info('Please upload documents to continue.')
            st.stop()

        # NOTE: By default Streamlit reruns the entire script when there's user input.
        # Only recreate the chain if it was not created yet or a new file is uploaded.
        if st.session_state.chain is None or st.session_state.files != uploaded_files:
            st.session_state.chain = create_chain(uploaded_files)
            st.session_state.files = uploaded_files
            print('Initialized chain')

        if 'messages' not in st.session_state:
            st.session_state['messages'] = [{'role': 'assistant', 'content': 'How can I help you?'}]

        for msg in st.session_state.messages:
            st.chat_message(msg['role']).write(msg['content'])

        # User-provided prompt
        if input := st.chat_input():
            st.session_state.messages.append({'role': 'user', 'content': input})
            with st.chat_message('user'):
                st.write(input)

        # Generate a new response if last message is not from assistant
        if st.session_state.messages[-1]['role'] != 'assistant':
            with st.chat_message('assistant'):
                response = generate_response(input)
                st.write(response)
                st.session_state.messages.append({'role': 'assistant', 'content': response})
    except Exception as e:
        st.error('Error: ' + str(e))

if __name__ == '__main__':
    main()
