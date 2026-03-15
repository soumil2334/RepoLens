from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_neo4j import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from dotenv import load_dotenv
from qdrant_client import QdrantClient
import os
import asyncio
load_dotenv()

client = QdrantClient(
    url=os.getenv('QDRANT_CLUSTER'),
    api_key=os.getenv('QDRANT_API_KEY')
)

graph=Neo4jGraph(
    url=os.getenv('NEO4J_URI'),
    username=os.getenv('NEO4J_USERNAME'),
    password=os.getenv('NEO4J_PASSWORD')
)
sempaphore=asyncio.Semaphore(3)

import os
load_dotenv()
OPENAI_KEY=os.getenv('OPENAI_API_KEY')

llm=ChatOpenAI(model='gpt-4o-mini', api_key=OPENAI_KEY, temperature=0)

llm_transformer=LLMGraphTransformer(llm=llm)

async def Create_KG(collection_name:str='documents'):
    points=[]
    offset=None

    while True:
        result, offset= client.scroll(
            collection_name=collection_name,
            limit=50,
            with_payload=True,
            with_vectors=False,
            offset=offset
        )
        points.extend(result)

        if offset is None:
            break
    
    document=[]

    for point in points:
        payload=point.payload
        doc=Document(
            page_content=payload.get('text'),
            metadata={
                'file':payload.get('file', "unknown"),
                'node_type': payload.get('node_type', "unknown"),
                'name' : payload.get('name', "unknown"),
                'start_line':payload.get('start_line',0),
                'end_line':payload.get('end_line',0)
            })
        document.append(doc)

    sempaphore=asyncio.Semaphore(3)
    graph_documents=[]
    async def semaphore_doc_processing(doc):
        async with sempaphore:
            return await llm_transformer.aconvert_to_graph_documents([doc])
        
    tasks=[semaphore_doc_processing(doc) for doc in document]
    graph_documents=await asyncio.gather(*tasks)

    return graph_documents

    

def Store_graph(documents):
    graph.add_graph_documents(
        documents,
        baseEntityLabel=True,
        include_source=True
    )

