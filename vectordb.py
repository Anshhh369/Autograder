import streamlit as st
import os
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_community.retrievers import AzureAISearchRetriever
from langchain_community.retrievers.azure_ai_search import AzureCognitiveSearchRetriever
from langchain_openai import OpenAIEmbeddings
from azure.search.documents import SearchClient

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

  query = "*" 

  # Retrieve relevant documents from the index
  rubrics = retriever.get_relevant_documents(query)

  for rubric in rubrics:
    document_id = rubric.metadata.get('id')


  # Log the list of retrieved documents for debugging
  st.write(f"Retrieved rubrics: {document_id}")

  # Retrieve the document
  retrieved_document = retriever.get_document(document_id)

  # Extract and display the content
  if retrieved_document:
    content = retrieved_document["page_content"]  # Adjust based on the actual field name
    st.write(f"Document Content: {content}")
  else:
    st.write("Document not found.")

  return rubrics
        
