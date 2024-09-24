system_prompt = """

You are an expert grader. Your job is to grade students assignment based on predifined rubrics.

"""




prompt = ChatPromptTemplate.from_messages(
  
  [("system", system_prompt), ("human", "{input}")]
    )


model_name = "gpt-4"
llm = ChatOpenAI(model_name=model_name)

chain = LLMChain(llm=llm, prompt=prompt)

