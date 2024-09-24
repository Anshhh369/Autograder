


# Pattern
pattern = r"(Question\s*\d:.*?)(Answer\s*\d:.*)"


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


