import streamlit as st
import os
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_community.retrievers import AzureAISearchRetriever
from langchain_community.retrievers.azure_ai_search import AzureCognitiveSearchRetriever
from langchain_openai import OpenAIEmbeddings
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

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
  vector_store = AzureSearch(
    azure_search_endpoint=vector_store_address,
    azure_search_key=vector_store_password,
    index_name=index_name,
    api_version = "2023-11-01",
    embedding_function=OpenAIEmbeddings.embed_query,
    # Configure max retries for the Azure client
    additional_search_client_options={"retry_total": 4},
  )

  if vector_store:
    docs = vector_store.similarity_search(
      query="rubrics",
      k=1, 
      search_type="similarity"
    )
    docs = docs[0].page_content
    st.write("Assignment: ", docs)

  return docs
        
