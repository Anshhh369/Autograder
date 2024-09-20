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
def extract_answers(text,pattern):
    extracted_answers = []

    # Use re.search to iterate through the matches
    search_result = re.search(pattern, text, re.DOTALL)
    

    while search_result:
        # Extract the question and answer from the matched groups
        question = search_result.group(1).strip()
        
        answer = search_result.group(2).strip()
        answers_cleaned = re.sub(r'(^#)', r'\\#', answer, flags=re.MULTILINE)
        extracted_answers = extracted_answers.append(answers_cleaned)

            
    return extracted_answers

# Patterns
pattern = r"(Question\s*\d:.*?)(Answer\s*\d:.*?)((?=Question\s*\d:|$))"

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
        
        # for question, answer in extracted_answers.items():
        #     st.write(f"{question}: {answer}")
