import document_process from document_processing
import extract_answers from answers_extraction
import streamlit as st

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

