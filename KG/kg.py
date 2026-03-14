from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
GROQ_KEY=os.getenv('GROQ_API_KEY')
llm=ChatGroq(model="llama3-70b-8192", api_key=GROQ_KEY)

