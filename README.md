# CourseRecommender 📚✨

A simple course recommendation app to suggest learning paths based on your interests! 🚀

## Core Functionality 🌟

**Input Your Interests 🧠**: Type what you want to learn (e.g., "machine learning") via a friendly Streamlit web interface.  
**Smart Recommendations 🔍**: Get up to 3 relevant course suggestions powered by semantic search.  

## Tech Stack ⚙️

- **FastAPI**: Serves a lightweight API to handle recommendation requests.  
- **Weaviate**: Stores course data as vectors for fast, similarity-based search.  
- **LangChain**: Manages embeddings and retrieval logic with HuggingFace models.  
- **Streamlit**: Provides a clean UI for easy interaction.  
- **Docker Compose**: Spins up a local Weaviate instance for persistence and search.  

## How It Works 🔧

Your query is embedded using **sentence-transformers/all-MiniLM-L6-v2**, searched against a vector database of courses, and returns the best matches in seconds!

## Getting Started 🚴‍♀️

### 1. Spin up Weaviate with Docker 🐳
```bash
docker-compose up -d
````

### 2. Load sample courses into Weaviate 📂

We’ve included a sample [`courses.csv`](courses.csv).
Run the ingestion script to populate the database:

```bash
python setup_data.py
```

### 3. Launch the FastAPI backend 🌐

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Visit [http://localhost:8000](http://localhost:8000) to check if it’s running.
Try the recommendation endpoint:

```bash
curl -X POST "http://localhost:8000/recommend" \
     -H "Content-Type: application/json" \
     -d '{"query": "python", "top_k": 3}'
```


---

✅ **New Updates**:

* Added `docker-compose.yml` for local Weaviate.
* Added sample `courses.csv` with 10 example courses.
* Added FastAPI backend (`app.py`) for course recommendations.

```
