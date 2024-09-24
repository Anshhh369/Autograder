import streamlit as st
import re
import pdfplumber
import docx
import os
import tempfile
import os.path
import pathlib
import uuid
from langchain_community.vectorstores import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader,TextLoader






# Streamlit app interface
st.title("Automatic Grading System")

# File uploader
uploaded_file = st.file_uploader("Upload your assignment", type=["txt", "pdf", "docx"])


# def chain():
if uploaded_file is not None:

    # st.session_state.vector_store = vector_db()
    
    # Read file content
    file_content = extract_text_from_file(uploaded_file)
    
    if file_content:
        
        # Extract answers using regex patterns
        extracted_answers = extract_answers(file_content,pattern)

        st.write("Extracted Answers:", extracted_answers)

