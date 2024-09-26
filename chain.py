def get_chain(assignment,predefined_rubrics,example):
        
        system_prompt = """
        
        You are an expert grader. Your job is to grade students assignment based on predifined rubrics.

        Start by greeting the user respectfully, collect the name of the user.
        The user has already uploaded {assignment} for grading, consider that and refer to {predifined_rubrics} for assigning scores accordingly.
        Next, make sure you refer the example given below in context before generating the output and use the same format in the output as given in the example.
        
        Context : {example}
        
        Lastly, ask user if you want any modification or adjustments to the scores generated? If the user says no then end the conversation.
        
        
        """

        prompt = ChatPromptTemplate.from_messages(
                [("system", system_prompt), ("human", "{input}")]
        )

        prompt.format_messages(input = "query", assignment = "st.session_state.vector_store", example = "st.session_state.example", predefined_rubrics = "st.session_state.rubrics")

        model_name = "gpt-4"
        llm = ChatOpenAI(model_name=model_name)

        chain = LLMChain(llm=llm, prompt=prompt)

        if st.session_state.vector_store:
        
                retriever = AzureAISearchRetriever(
                    content_key="assignment", 
                    top_k=1, 
                    index_name="autograder-vectordb",
                )
                chain = create_retrieval_chain(retriever, chain)

                st.session_state.chat_active = True

                st.session_state.chain = chain

                return st.session_state.chain

def get_scores():
        
        chains = get_chain(st.session_state.vector_store,st.session_state.predefined_rubrics,st.session_state.example)
        response = chains.invoke({"input": query, "assignment": st.session_state.vector_store,"example" : st.session_state.example, "predefined_rubrics": st.session_state.rubrics})
        
        try:
                answer = response['text']
                
        except:
                ans = response['answer']
                answer = ans['text']
              
        return answer

