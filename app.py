import streamlit as st
import re
import pdfplumber
import docx
import os
import tempfile
import os.path
import pathlib
from langchain_community.vectorstores import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader,TextLoader



secrets = st.secrets  # Accessing secrets (API keys) stored securely

openai_api_key = secrets["openai"]["api_key"]  # Accessing OpenAI API key from secrets
os.environ["OPENAI_API_KEY"] = openai_api_key  # Setting environment variable for OpenAI API key



azure_api_key = secrets["azure"]["api_key"]
os.environ["AZURE_API_KEY"] = azure_api_key

vector_store_address = "https://ragservices.search.windows.net"
vector_store_password = "IVMAEF98D6Tn8w4eQ53VstzUHXfelrAJn4sBPlY8hZAzSeByAPxr"
index_name = "autograder-vectordb"

OpenAIEmbeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None


def vector_db():
    
    vector_store = AzureSearch(
        azure_search_endpoint=vector_store_address,
        azure_search_key=vector_store_password,
        index_name=index_name,
        api_version = "2024-05-01-preview",
        embedding_function=OpenAIEmbeddings.embed_query,
    )

    db = vector_store.add_documents(documents=docs)
    
    return db


# Function to extract text from uploaded files
def extract_text_from_file(uploaded_file):
    
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
        text = uploaded_file.read().decode('utf-8')
    elif file_extension == "pdf":
        loader = PyPDFLoader(path)
        with pdfplumber.open(uploaded_file) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
            text = "\n".join(pages)
    elif file_extension == "docx":
        loader = Docx2txtLoader(path)
        pages = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in pages.paragraphs])        
    else:
        st.error("Unsupported file type.")
        return None

    # Load documents and split text
    docs = loader.load()
    
    st.write("file contents: \n", text)
                    
    text_splitter =  RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(docs)
        
    return docs


# Function to extract answers using regex patterns
def extract_answers(text,pattern):
    extracted_answers = []

    # Use re.search to iterate through the matches
    search_result = re.search(pattern, text, re.DOTALL)
    

    if search_result:
        # Extract the question and answer from the matched groups
        question = search_result.group(1).strip()

        extracted_answers.append(question)
        
        answer = search_result.group(2).strip()
        answers_cleaned = re.sub(r'(^#)', r'\\#', answer, flags=re.MULTILINE)
        
        extracted_answers.append(answers_cleaned)
        
    else:
        
        extracted_answers = st.write("Answers not found")
            
    return extracted_answers

# Patterns
pattern = r"(Question\s*\d:.*?)(Answer\s*\d:.*)"

# Streamlit app interface
st.title("Automatic Grading System")

# File uploader
uploaded_file = st.file_uploader("Upload your assignment", type=["txt", "pdf", "docx"])


# def chain():
if uploaded_file is not None:
    # Read file content
    file_content = extract_text_from_file(uploaded_file)
    
    if file_content:
        # Extract answers using regex patterns
        extracted_answers = extract_answers(file_content,pattern)

        st.write("Extracted Answers:", extracted_answers)

        st.session_state.vector_store = vector_db()
        
        # for question, answer in extracted_answers.items():
        #     st.write(f"{question}: {answer}")











    # if uploaded_file.type == "text/plain":
    #     # If the file is a .txt file
    #     doc = uploaded_file.read().decode('utf-8')
    # elif uploaded_file.type == "application/pdf":
        
    #     If the file is a .pdf file
    #     with pdfplumber.open(uploaded_file) as pdf:
    #         pages = [page.extract_text() for page in pdf.pages]
    #         doc = "\n".join(pages)
    # elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
    #     # If the file is a .docx file
    #     pages = docx.Document(uploaded_file)
    #     doc = "\n".join([para.text for para in pages.paragraphs])
