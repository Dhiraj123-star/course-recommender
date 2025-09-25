
# CourseRecommender 📚✨

A simple course recommendation app to suggest learning paths based on your interests! 🚀

## Core Functionality 🌟

**Query Input 🔍**: Enter what you want to learn (e.g., "machine learning").
**Smart Search 🧠**: Matches your query to relevant courses using vector similarity.
**Top Picks 🏆**: Displays the top 3 course recommendations with titles, descriptions, and AI-generated explanations.

## Tech Stack 🛠️

* **FastAPI**: Serves a lightweight API to handle recommendation requests.
* **Weaviate**: Stores course data as vectors for fast, similarity-based search.
* **LangChain**: Manages embeddings and retrieval logic with HuggingFace models + GPT-4o-mini for explanations.
* **Streamlit**: Provides a clean UI for easy interaction.
* **Docker Compose**: Spins up a local Weaviate instance for persistence and search.
* **GitHub Actions**: Automates CI/CD for testing and deployment.

## How It Works 🔧

Your query is embedded using **sentence-transformers/all-MiniLM-L6-v2**, searched against a vector database of courses, and returns the best matches in seconds!
Each course result is then explained by **GPT-4o-mini**, showing *why* it’s relevant to your query.

## Getting Started 🚦

### 1. Run Weaviate locally with Docker Compose (port 8081) 🐳

```bash
docker-compose up -d
```

### 2. Load sample courses into Weaviate 📂

We’ve included a sample [`courses.csv`](courses.csv).
Run the ingestion script to populate the database:

```bash
python setup_data.py
```

### 3. Set up environment variables 🔑

Create a `.env` file with your **OpenAI API key**:

```
OPENAI_API_KEY=your_api_key_here
```

### 4. Launch the FastAPI backend (port 8000) ⚙️

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

### 5. Launch the Streamlit UI (port 8501) 🌐

```bash
streamlit run streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser and enter a query to get recommendations with explanations! 🎉

---

## CI/CD with GitHub Actions ⚡

We’ve added **GitHub Actions workflows** for continuous integration and deployment:

* ✅ **Build & Test**: Automatically runs Python tests on every push and pull request.
* 🐳 **Docker Build Check**: Ensures the Docker image builds successfully.
* 🚀 **Deploy Ready**: Prepares the app for deployment pipelines.

Workflows are defined in [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

To enable CI/CD:

1. Push your changes to GitHub.
2. GitHub Actions will automatically run tests and verify builds.
3. On success, you’re ready to deploy! 🎯

---

✅ **New Updates**:

* Integrated **GPT-4o-mini** for generating concise course explanations.
* Added **"Why?" section** in Streamlit to show reasons behind each recommendation.
* Added **GitHub Actions workflows** for CI/CD automation.
* Updated README with clearer setup instructions and CI/CD guide.

---
