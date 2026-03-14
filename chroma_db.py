import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path="./chroma_db")

# set up embedding function
embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

collection = client.get_or_create_collection(
    name="code_chunks",
    embedding_function=embedding_fn
)

def add_chunks_to_chroma(chunks: list, collection):
    documents = []
    metadatas = []
    ids = []

    for i, chunk in enumerate(chunks):
        # text is the main content that gets embedded
        documents.append(chunk["text"])

        # everything else goes into metadata
        metadatas.append({
            "file":       chunk.get("file", "unknown"),
            "node_type":  chunk.get("node_type", "unknown"),
            "name":       chunk.get("name", "unknown"),
            "parent":     chunk.get("parent") or "none",   # chroma doesn't accept None
            "start_line": chunk.get("start_line", 0),
            "end_line":   chunk.get("end_line", 0),
        })

        # unique id per chunk
        ids.append(f"{chunk.get('file', 'file')}_{i}_{chunk.get('name', 'chunk')}")

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Added {len(documents)} chunks to ChromaDB")


# use it
chunks = chunk_tree(code_string, "python", "save_as_pdf.py")
add_chunks_to_chroma(chunks, collection)