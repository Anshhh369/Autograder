from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, create_retrieval_chain
from langchain.prompts.chat import ChatPromptTemplate
from langchain_community.retrievers import AzureAISearchRetriever
import streamlit as st
import os
from langchain import hub

secrets = st.secrets


azure_api_key = secrets["azure"]["api_key"]
os.environ["AZURE_AI_SEARCH_API_KEY"] = azure_api_key
os.environ["AZURE_AI_SEARCH_SERVICE_NAME"] = "https://ragservices.search.windows.net"


def get_chain(assignment,predefined_rubrics,chat_history):
        
        system_prompt = """
        
        You are an expert grader, your name is AutoGrader. Your job is to grade {assignment} based on {predefined_rubrics}.

        Start by greeting the user respectfully, collect the name of the user. 
        After that verify predefined_rubrics with the user by displaying whole exact rubrics to them clearly.
        Move to the next step only after successfully verifying.
        Next step is to grade the assignment, go through the {assignment} and highlight the mistakes that user made, make sure you explain all the mistakes in detail with soultions.
        Be consistent with the scores and feedbacks generated.
        Lastly, ask user if they want any modification or adjustments to the scores generated, if user says no then end the conversation.

        Keep the chat history to have memory and do not repeat questions.
        
        chat history: {chat_history}
        
        """

        prompt = ChatPromptTemplate.from_messages(
                [("system", system_prompt), ("human", "{input}")]
        )

        prompt.format_messages(input = "query", assignment = "st.session_state.extracted_answers", predefined_rubrics = "st.session_state.rubrics", chat_history = "st.session_state.chat_history")

        model_name = "gpt-4o"
        llm = ChatOpenAI(model_name=model_name)
        

        chain = LLMChain(llm = llm,prompt = prompt)

        retriever = AzureAISearchRetriever(
                content_key="predefined_rubrics", 
                top_k=1, 
                index_name="autorubrics-vectordb",
        )
        
        retrieval_chain = create_retrieval_chain(retriever, chain)

        st.session_state.chat_active = True

        st.session_state.chain = retrieval_chain

        return st.session_state.chain

def get_scores(query):
        
        chains = get_chain(st.session_state.extracted_answers,st.session_state.rubrics,st.session_state.chat_history)
        response = chains.invoke({"input": query, "assignment": st.session_state.extracted_answers, "predefined_rubrics": st.session_state.rubrics,"chat_history": st.session_state.chat_history})
        
        try:
                answer = response['text']
                
        except:
                ans = response['answer']
                answer = ans['text']
              
        
        return answer

