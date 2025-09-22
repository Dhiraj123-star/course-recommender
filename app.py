from fastapi import FastAPI
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_weaviate.vectorstores import WeaviateVectorStore
import weaviate

app = FastAPI(title="Course Recommendation API")

# Global vectorstore (load once)
client = weaviate.connect_to_local(
    host="localhost",
    port=8081,
)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = WeaviateVectorStore(client=client, index_name="Courses", text_key="text", embedding=embeddings)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@app.get("/")
def read_root():
    return {"message": "Course Recommendation API is running!"}

@app.post("/recommend")
def recommend_courses(request: QueryRequest):
    # Simple retrieval chain (no LLM yet—just similarity search)
    docs = vectorstore.similarity_search(request.query, k=request.top_k)
    recommendations = [
        {
            "title": doc.metadata.get("title", "Untitled"),
            "description": doc.page_content,
            "score": f"Similarity: {i+1}"
        }
        for i, doc in enumerate(docs)
    ]
    return {"recommendations": recommendations}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)