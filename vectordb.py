import streamlit as st
import os
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_community.retrievers import AzureAISearchRetriever
from langchain_community.retrievers.azure_ai_search import AzureCognitiveSearchRetriever
from langchain_openai import OpenAIEmbeddings


secrets = st.secrets  # Accessing secrets (API keys) stored securely

openai_api_key = secrets["openai"]["api_key"]  # Accessing OpenAI API key from secrets
os.environ["OPENAI_API_KEY"] = openai_api_key  # Setting environment variable for OpenAI API key

azure_api_key = secrets["azure"]["api_key"]
os.environ["AZURE_API_KEY"] = azure_api_key

vector_store_address = "https://ragservices.search.windows.net"
vector_store_password = azure_api_key

index_name = "predefined_rubrics"
model = "text-embedding-ada-002"

OpenAIEmbeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model=model)

def vector_db():
  

  retriever = AzureAISearchRetriever(
    content_key="content", 
    top_k=1, 
    index_name="predefined_rubrics"
  )

  query = "content" 

  # Retrieve relevant documents from the index
  rubrics = retriever.get_relevant_documents(query)

  # Log the list of retrieved documents for debugging
  st.write(f"Retrieved rubrics: {rubrics}")

  return rubrics
        
