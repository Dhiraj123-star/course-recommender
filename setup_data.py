from langchain_huggingface import HuggingFaceEmbeddings
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_core.documents import Document
import weaviate
import pandas as pd

# Connect to Weaviate (v4 syntax for local instance on custom port)
client = weaviate.connect_to_local(
    host="localhost",
    port=8081,
)

try:
    # Load courses from CSV
    csv_file = "courses.csv"
    # Read CSV with explicit encoding and error handling
    df = pd.read_csv(csv_file, encoding="utf-8", on_bad_lines="skip")

    # Log raw CSV data for debugging
    print("Raw CSV data:")
    print(df.to_string())

    # Filter out rows with missing or non-string titles/descriptions
    df = df.dropna(subset=["title", "description"])  # Drop rows where either is NaN
    df = df[df["title"].apply(lambda x: isinstance(x, str) and x.strip() != "")]  # Valid title
    df = df[df["description"].apply(lambda x: isinstance(x, str) and x.strip() != "")]  # Valid description

    # Convert CSV rows to LangChain Documents
    documents = [
        Document(
            page_content=row["description"],
            metadata={"title": row["title"]}
        )
        for _, row in df.iterrows()
    ]

    # Log documents for inspection
    print("Documents to be ingested:")
    for doc in documents:
        print(f"Title: {doc.metadata['title']}, Description: {doc.page_content}")

    # Embeddings model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Delete existing Courses collection to avoid duplicates
    try:
        client.collections.delete("Courses")
    except:
        pass  # Ignore if collection doesn't exist

    # Create vector store (no splitting, as descriptions are short)
    vectorstore = WeaviateVectorStore.from_documents(
        documents=documents,  # Correct keyword
        embedding=embeddings,  # Correct keyword
        client=client,
        index_name="Courses",
        text_key="text",
    )

    print(f"Added {len(documents)} courses to Weaviate from {csv_file}!")

finally:
    client.close()  # Ensure connection closes even on error