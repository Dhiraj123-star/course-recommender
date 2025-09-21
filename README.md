# CourseRecommender 📚✨

A simple course recommendation app to suggest learning paths based on your interests! 🚀

## Core Functionality 🌟

**Input Your Interests 🧠**: Type what you want to learn (e.g., "machine learning") via a friendly Streamlit web interface.  
**Smart Recommendations 🔍**: Get up to 3 relevant course suggestions powered by semantic search.

## Tech Stack ⚙️

- **FastAPI**: Serves a lightweight API to handle recommendation requests.  
- **Weaviate**: Stores course data as vectors for fast, similarity-based search.  
- **LangChain**: Manages embeddings and retrieval logic.  
- **Streamlit**: Provides a clean UI for easy interaction.  

## How It Works 🔧

Your query is embedded, searched against a vector database of courses, and returns the best matches in seconds!

## Getting Started 🚴‍♀️

1. Spin up Weaviate with Docker 🐳.  
2. Load sample courses into the vector database 📂.  
3. Launch the FastAPI backend 🌐.  
4. Open the Streamlit UI and start exploring courses 🎉!
