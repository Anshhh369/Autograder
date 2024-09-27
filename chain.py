from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, create_retrieval_chain
from langchain.prompts.chat import ChatPromptTemplate
from langchain_community.retrievers import AzureAISearchRetriever
import streamlit as st
import os

secrets = st.secrets


azure_api_key = secrets["azure"]["api_key"]
os.environ["AZURE_AI_SEARCH_API_KEY"] = azure_api_key
os.environ["AZURE_AI_SEARCH_SERVICE_NAME"] = "https://ragservices.search.windows.net"


def get_chain(assignment,predefined_rubrics,example,chat_history):
        
        system_prompt = """
        
        You are an expert grader. Your job is to grade students assignment based on predefined rubrics.

        The user has already uploaded {assignment} so consider that for grading.

        Start by greeting the user respectfully, collect the name of the user. After that verify {predefined_rubrics} with the user by displaying whole exact rubrics to them clearly.
        Move to the next step only after successfully verifying. Next, refer the example given below in context and use only it's format for reference.
        
        Context : {example}
        
        Provide a clear, comprehensable output with scores and detailed feedback to the user, highlight the mistakes that user made in the {assignment} and explain them in detail with soultions.
        Be consistent with the scores and feedback generated.
        Lastly, ask user if they want any modification or adjustments to the scores generated, if user says no then end the conversation.

        Keep the chat history to have memory and do not repeat questions.
        
        chat history: {chat_history}
        
        
        """

        prompt = ChatPromptTemplate.from_messages(
                [("system", system_prompt), ("human", "{input}")]
        )

        prompt.format_messages(input = "query", assignment = "st.session_state.vector_store", example = "st.session_state.example", predefined_rubrics = "st.session_state.rubrics", chat_history = "st.session_state.chat_history")

        model_name = "gpt-4o"
        llm = ChatOpenAI(model_name=model_name)

        chain = LLMChain(llm=llm, prompt=prompt)
                
        retriever = AzureAISearchRetriever(
                content_key="st.session_state.vector_store", 
                top_k=1, 
                index_name="autograder-vectordb",
        )
        chain = create_retrieval_chain(retriever, chain)

        st.session_state.chat_active = True

        st.session_state.chain = chain

        return st.session_state.chain

def get_scores(query):
        
        chains = get_chain(st.session_state.vector_store,st.session_state.rubrics,st.session_state.example,st.session_state.chat_history)
        response = chains.invoke({"input": query, "assignment": st.session_state.vector_store, "example" : st.session_state.example, "predefined_rubrics": st.session_state.rubrics,"chat_history": st.session_state.chat_history})
        
        try:
                answer = response['text']
                
        except:
                ans = response['answer']
                answer = ans['text']
              
        return answer

