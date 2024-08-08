import streamlit as st
import re

# Function to extract answers using regex patterns
def extract_answers(text, patterns):
    extracted_answers = {}
    for question, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            extracted_answers[question] = match.group(1).strip()
        else:
            extracted_answers[question] = "Answer not found"
    return extracted_answers

# Define regex patterns for answer extraction
patterns = {
    "Question 1": r"Question 1[:\s]*(.*?)(?:Question 2|$)",
    "Question 2": r"Question 2[:\s]*(.*?)(?:Question 3|$)",
    "Question 3": r"Question 3[:\s]*(.*?)(?:Question 4|$)",
    # Add more patterns as needed
}

# Streamlit app interface
st.title("Automatic Grading System")

# File uploader
uploaded_file = st.file_uploader("Upload your assignment", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    # Read file content
    file_content = uploaded_file.read().decode('utf-8')

    # Extract answers using regex patterns
    extracted_answers = extract_answers(file_content, patterns)

    st.write("Extracted Answers:")
    for question, answer in extracted_answers.items():
        st.write(f"{question}: {answer}")
