from fastapi import FastAPI
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import weaviate
import os
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()

# Global variables
client = None
vectorstore = None
chain = None

# FastAPI lifespan to manage Weaviate client
@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, vectorstore, chain
    # Startup: Connect to Weaviate and initialize
    client = weaviate.connect_to_local(
        host="localhost",
        port=8081,
    )
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = WeaviateVectorStore(client=client, index_name="Courses", text_key="text", embedding=embeddings)

    # Initialize LLM (gpt-4o-mini)
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.7
    )

    # Define prompt template
    prompt_template = PromptTemplate(
        input_variables=["query", "context"],
        template="""
You are an educational advisor. Given a user's query and a list of relevant courses, provide a concise explanation (1-2 sentences) for why each course is recommended based on the query. Format the response as a list of explanations, one per course.

Query: {query}
Courses: {context}

Return a list of explanations like:
- Course: [Title] - [Explanation]
"""
    )

    # Set up RunnableSequence (replacing LLMChain)
    chain = prompt_template | llm

    yield  # Application runs here

    # Shutdown: Close Weaviate client
    client.close()

app = FastAPI(title="Course Recommendation API", lifespan=lifespan)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@app.get("/")
def read_root():
    return {"message": "Course Recommendation API is running!"}

@app.post("/recommend")
def recommend_courses(request: QueryRequest):
    # Retrieve relevant documents
    docs = vectorstore.similarity_search(request.query, k=request.top_k)
    # Format context for LLM
    context = "\n".join([f"{doc.metadata.get('title', 'Untitled')}: {doc.page_content}" for doc in docs])
    # Run chain
    result = chain.invoke({"query": request.query, "context": context})
    # Parse LLM output (expecting a list of explanations)
    explanations = result.content.strip().split("\n")
    recommendations = [
        {
            "title": doc.metadata.get("title", "Untitled"),
            "description": doc.page_content,
            "explanation": explanations[i].split(" - ", 1)[1] if i < len(explanations) and " - " in explanations[i] else "Explanation not available."
        }
        for i, doc in enumerate(docs)
    ]
    return {"recommendations": recommendations}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)