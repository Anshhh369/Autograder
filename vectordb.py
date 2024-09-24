azure_api_key = secrets["azure"]["api_key"]
os.environ["AZURE_API_KEY"] = azure_api_key

vector_store_address = "https://ragservices.search.windows.net"
vector_store_password = "IVMAEF98D6Tn8w4eQ53VstzUHXfelrAJn4sBPlY8hZAzSeByAPxr"
index_name = "autograder-vectordb"

OpenAIEmbeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model=model)

def vector_store():
  
  vector_store = AzureSearch(
        azure_search_endpoint=vector_store_address,
        azure_search_key=vector_store_password,
        index_name=index_name,
        api_version = "2024-05-01-preview",
        embedding_function=OpenAIEmbeddings.embed_query,
        # Configure max retries for the Azure client
        additional_search_client_options={"retry_total": 4},
    )

    db = vector_store.add_documents(documents=documents)

  return db
        
