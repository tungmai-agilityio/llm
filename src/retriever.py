from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sympy import O

# Function to dynamically set chunk size and overlap
def get_dynamic_chunk_params(document, max_chunk_size=1000, min_chunk_size=500, max_overlap=200):
    # Get the length of the document
    doc_length = len(document)

    # Set chunk_size based on the document length (simple linear scaling as an example)
    if doc_length > 10000:  # Large document
        chunk_size = max_chunk_size
        chunk_overlap = max_overlap
    elif doc_length > 3000:  # Medium document
        chunk_size = int(max_chunk_size * 0.75)
        chunk_overlap = int(max_overlap * 0.75)
    else:  # Small document
        chunk_size = min_chunk_size
        chunk_overlap = int(max_overlap * 0.5)

    return chunk_size, chunk_overlap

def configure_retriever(docs):
    # Split documents
    splits = []

    for doc in docs:
        chunk_size, chunk_overlap = get_dynamic_chunk_params(doc.page_content)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_documents([doc])
        splits.extend(chunks)

    # Create embeddings and store in vector db
    embeddings = OpenAIEmbeddings()
    vector_db = Chroma.from_documents(splits, embeddings)

    # Define retriever
    retriever = vector_db.as_retriever()
    return retriever
