import streamlit as st
import re
import pdfplumber
import docx



# Function to extract text from uploaded files
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "text/plain":
        # If the file is a .txt file
        return uploaded_file.read().decode('utf-8')
    elif uploaded_file.type == "application/pdf":
        # If the file is a .pdf file
        with pdfplumber.open(uploaded_file) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
            return "\n".join(pages)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # If the file is a .docx file
        pages = docx.Document(uploaded_file)
        return "\n".join([para.text for para in pages.paragraphs])
    else:
        st.error("Unsupported file type.")
        return None
    return pages


# Function to extract answers using regex patterns
def extract_answers(text, patterns):
    extracted_answers = {}
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        extracted_answers = match.group(0).strip()
    else:
        extracted_answers = "Answer not found"
return extracted_answers

# Define regex patterns for answer extraction
patterns = {
    "(Question\s*\d:.*?)(?=Answer\s*\d:)[\s\S]*?"
    # "Question 1": r"Question 1:\s*(.*?)\s*Answer 1:\s*(.*?)(?=\s*Question 2:|$)",
    # "Question 2": r"Question 2:\s*(.*?)\s*Answer 2:\s*(.*?)(?=\s*Question 3:|$)",
    # "Question 3": r"Question 3:\s*(.*?)\s*Answer 3:\s*(.*?)(?=\s*Question 4:|$)",
    # "Question 4": r"Question 4:\s*(.*?)\s*Answer 4:\s*(.*?)(?=\s*Question 5:|$)",
    # "Question 5": r"Question 5:\s*(.*?)\s*Answer 5:\s*(.*?)(?=$)"
    # Add more patterns as needed
}

# Streamlit app interface
st.title("Automatic Grading System")

# File uploader
uploaded_file = st.file_uploader("Upload your assignment", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    # Read file content
    file_content = extract_text_from_file(uploaded_file)
    
    if file_content:
        # Extract answers using regex patterns
        extracted_answers = extract_answers(file_content, patterns)

        st.write("Extracted Answers:", extracted_answers)
        
        # for question, answer in extracted_answers.items():
        #     st.write(f"{question}: {answer}")
