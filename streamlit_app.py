import streamlit as st
import requests

API_URL = "http://localhost:8000/recommend"

st.title("Simple Course Recommender")
st.write("Enter your interests (e.g., 'machine learning') to get recommendations.")

query = st.text_input("Your query:", placeholder="What are you interested in learning?")

if st.button("Get Recommendations") and query:
    with st.spinner("Fetching recommendations..."):
        response = requests.post(API_URL, json={"query": query})
        if response.status_code == 200:
            data = response.json()
            st.success("Here are your top recommendations:")
            for rec in data["recommendations"]:
                st.write(f"- **{rec['course']}** ({rec['score']})")
        else:
            st.error("Error fetching recommendations. Check if API is running.")

if __name__ == "__main__":
    st.write("Backend: FastAPI on port 8000 | DB: Weaviate on port 8081")