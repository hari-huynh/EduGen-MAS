from pydantic_ai import Agent, RunContext
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from pydantic_ai.common_tools.tavily import tavily_search_tool
from agents.pydantic_models import CollectDataDeps
from utils.setup import setup_gemini
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import time
import os
from dotenv import load_dotenv

load_dotenv()
setup_gemini()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

collect_data_agent = Agent(
    'google-gla:gemini-2.0-flash',
    deps_type = CollectDataDeps,
    tools=[tavily_search_tool(TAVILY_API_KEY)],
    result_type = str
)


@collect_data_agent.tool
def retrieval(ctx: RunContext, question: str) -> str:
    """Retrieve documents from vector store.
    
    This tool performs semantic search on a vector database to find relevant documents based on the input question.
    It uses the multilingual-e5-base model for embeddings and returns the top 2 most similar documents.
    
    Args:
        question (str): The query/question to search for in the vector store
        
    Returns:
        str: A concatenated string containing the content of the top 2 most relevant documents
    """
    print("---RETRIEVE---")
    
    embedings=HuggingFaceEmbeddings(model_name='intfloat/multilingual-e5-base')
    
    vector_store = Chroma(
        collection_name=  'chatbotDB',  #"example_collection2",
        embedding_function=embedings, 
        persist_directory="./VectorDB/",  
        #"./chroma_langchain_db"
    )
    
    print("______________Retrieval OK______________")
    try:
        # Retrieval
        documents = vector_store.similarity_search(
            question,
            k=2
        )
        result = "Result Retrieval: " + documents[0].page_content + documents[1].page_content
        print("retrieval result: ", result)
        time.sleep(5)
        return result  
    
    except Exception as e:
        print(f"Error retrieving documents: {e}")
        # return ToolOutput(result=f"Simulated retrieval result for question: {question}")


@collect_data_agent.system_prompt
def system_prompt(ctx: RunContext) -> str:
    return f"""
            First, using `tavily_search` for information about {ctx.deps.task.description}    
            Second, you will use `retrieval` to perform a database query based on the {ctx.deps.task.description}
            Based on the available data:
            Create a detailed report and get exactly relevance content from searched information for each result pages.
        """



# f"""
#     From task description: '{ctx.deps.task.description}, extract keyword and search Tavily for information.
#     Analyze the top search results from Tavily to create a comprehensive report of approximately 1000 words on '{ctx.deps.task.description}'.
#     """
    # Create a detailed report and get exactly relevance content from searched information for each result pages.

