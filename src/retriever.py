from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def configure_retriever(docs):
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Create embeddings and store in vector db
    embeddings = OpenAIEmbeddings()
    vector_db = Chroma.from_documents(splits, embeddings)

    # Define retriever
    retriever = vector_db.as_retriever()
    return retriever