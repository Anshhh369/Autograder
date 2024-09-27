from document_processing import process_document, extract_answers
import streamlit as st
from vectordb import vector_db
from rubrics import rubrics
from example import example
from chain import get_chain,get_scores
from chat_history import format_chat_history

if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "chain" not in st.session_state:
    st.session_state.chain = None

if "rubrics" not in st.session_state:
    st.session_state.rubrics = None

if "example" not in st.session_state:
    st.session_state.example = None



# Streamlit app interface
st.title("Automatic Grading System")

# Pattern
pattern = r"(Question\s*\d:.*?)(Answer\s*\d:.*)"

# File uploader
st.session_state.uploaded_file = st.file_uploader("Upload your assignment", type=["txt", "pdf", "docx"])

st.session_state.rubrics = rubrics()

st.session_state.example = example()


# def chain():
if st.session_state.uploaded_file:

    
    # Read file content
    st.session_state.uploaded_file = process_document(st.session_state.uploaded_file)

    # Extract answers using regex patterns
    extracted_answers = extract_answers(st.session_state.uploaded_file,pattern)

    st.write("Extracted Answers:", extracted_answers)
   
    st.session_state.vector_store = vector_db(st.session_state.uploaded_file)

    st.write("Assignment Uploaded Successfully")

    if st.session_state.vector_store:
        
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                                
        if query := st.chat_input("Ask your question here"):
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(query)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": query})

            st.session_state.chat_history = format_chat_history(st.session_state.messages)
    
            answer = get_scores(query)
        
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(answer)
            # Add assistant response to chat history                
            st.session_state.messages.append({"role": "assistant", "content": answer})
                                        
            # Button to clear chat messages
            def clear_messages():
                st.session_state.messages = []
            st.button("Clear", help = "Click to clear the chat", on_click=clear_messages)


