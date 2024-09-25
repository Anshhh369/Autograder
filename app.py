from document_processing import process_document,extract_answers 
import streamlit as st

if "vector_store" not in st.session_state:
    st.session_state.vextor_store = None
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# Streamlit app interface
st.title("Automatic Grading System")

# File uploader
uploaded_file = st.file_uploader("Upload your assignment", type=["txt", "pdf", "docx"])


# def chain():
if uploaded_file is not None:
    
    # Read file content
    file_content = process_document(uploaded_file)

    # Extract answers using regex patterns
    extracted_answers = extract_answers(uploaded_file,pattern)

    st.write("Extracted Answers:", extracted_answers)

    
    if file_content:

        st.session_state.vector_store = vector_db(file_content)

