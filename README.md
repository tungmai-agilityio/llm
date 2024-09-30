# Practice - Build a Customer Support Chatbot for an E-commerce Platform

## Introduction

- Develop a chatbot system that can handle common customer support queries and provide relevant responses for an e-commerce platform, using LangChain components and OpenAI models.

## Requirements

- Create a knowledge base and a set of documents containing information about the e-commerce platform's products, ordering process, shipping, returns, and common customer issues/solutions
- Understand the user’s query or issue related to the e-commerce platform
- Retrieve relevant information from the knowledge base
- Generate a relevant and helpful response based on the query and retrieved information
- Output will display the chatbot’s response to the user’s query
- Handle and display any errors or exceptions that occur during the process
- Design and structure the prompts effectively specifying the e-commerce domain, orchestrate the different steps using appropriate chains, and manage conversation flow.
- Using LangSmith to inspect the input, output, and token usage

## Tech Stack

- Model: OpenAI gpt-3.5-turbo
- Application UI: [Streamlit](https://python.langchain.com/docs/integrations/providers/streamlit/)
- Python
- LangChain: Prompt Templates, Chains, Parsers, RAG
- LangSmith: <https://www.langchain.com/langsmith>

## Set up

- Create `.env` file and add environment variables

  ```
  OPENAI_API_KEY=<openai-api-key>

  # LangSmith environment
  LANGCHAIN_TRACING_V2=true
  LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
  LANGCHAIN_API_KEY="<your-api-key>"
  LANGCHAIN_PROJECT="<your-project-name>"

  ```

- Create the virtual env and install the requirements

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

## Running

  ```bash
  streamlit run src/main.py
  ```

## Evaluation

  ```bash
  promptfoo eval
  ```

Afterwards, you can view the results by running `promptfoo view`
