from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pdfplumber
import docx
import tempfile
import os.path
import pathlib


# Function to extract text from uploaded files
def process_document(uploaded_file):
    
    # for uploaded_file in uploaded_files:
        
    file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type}
    
    # Save file to a temporary directory
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, uploaded_file.name)
        
    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())

    # Determine file extension
    file_extension = uploaded_file.name.split(".")[-1].lower()

    # Load document based on its extension
    if file_extension == "txt":
        loader = TextLoader(path)
    elif file_extension == "pdf":
        loader = PyPDFLoader(path)
    elif file_extension == "docx":
        loader = Docx2txtLoader(path)     
    else:
        st.error("Unsupported file type.")
        return None

    # Load documents and split text
    docs = loader.load()
    
    text_splitter =  RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(docs)

    return documents     
