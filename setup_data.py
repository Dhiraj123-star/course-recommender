from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_weaviate.vectorstores import WeaviateVectorStore
import weaviate

# Connect to Weaviate (v4 syntax for local instance on custom port)
client = weaviate.connect_to_local(
    host="localhost",
    port=8081,
)

# Sample course data (as a simple text file content)
sample_courses = """
Course 1: Introduction to Python Programming. Description: Learn basics of Python, variables, loops, and functions for beginners.
Course 2: Machine Learning Fundamentals. Description: Dive into supervised and unsupervised learning with scikit-learn.
Course 3: Web Development with React. Description: Build interactive UIs using React components and state management.
Course 4: Data Science with Pandas. Description: Analyze data using Pandas for cleaning, visualization, and insights.
Course 5: Natural Language Processing. Description: Explore tokenization, sentiment analysis, and transformers.
"""

# Save to temp file for loader
with open("temp_courses.txt", "w") as f:
    f.write(sample_courses)

# Load and split documents
loader = TextLoader("temp_courses.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# Embeddings model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create vector store (deletes existing if schema exists)
vectorstore = WeaviateVectorStore.from_documents(
    docs,
    embeddings,
    client=client,
    index_name="Courses",  # Collection name
    text_key="text",  # Field for text
)

print("Sample courses added to Weaviate!")
client.close()