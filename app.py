from document_processing import process_document,extract_answers 
import streamlit as st

# Streamlit app interface
st.title("Automatic Grading System")

# File uploader
uploaded_file = st.file_uploader("Upload your assignment", type=["txt", "pdf", "docx"])


# def chain():
if uploaded_file is not None:

    # st.session_state.vector_store = vector_db()
    
    # Read file content
    file_content = process_document(uploaded_file)
    
    if file_content:
        
        # Extract answers using regex patterns
        extracted_answers = extract_answers(file_content,pattern)

        st.write("Extracted Answers:", extracted_answers)

