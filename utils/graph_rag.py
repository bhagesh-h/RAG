import re
import requests
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from rank_bm25 import BM25Okapi

from langchain_ollama import OllamaLLM

# Step 1: Create embeddings and vector store
def create_embeddings(text_contents, embedding_model, base_url):
    embeddings = OllamaEmbeddings(model=embedding_model, base_url=base_url)
    vector_store = FAISS.from_texts(text_contents, embeddings)
    return vector_store

# Step 2: Create BM25 retriever
def create_bm25_retriever(text_contents):
    bm25_retriever = BM25Retriever.from_texts(
        text_contents,
        bm25_impl=BM25Okapi,
        preprocess_func=lambda text: re.sub(r"\W+", " ", text).lower().split()
    )
    return bm25_retriever

def perform_hybrid_retrieval(query, vector_store, bm25_retriever, K_value=5, top_results=3):
    bm25_results = bm25_retriever.invoke(query)
    faiss_results = vector_store.similarity_search(query, k=int(K_value))
    combined_results = bm25_results + faiss_results
    return combined_results[:int(top_results)]

def process_text_and_retrieve(query, embedding_model=None, num_results=3, embeddings=None, retriever=None, text_contents=None):
    vector_store    = embeddings if embeddings else create_embeddings(text_contents, embedding_model, base_url)
    bm25_retriever  = retriever if retriever else create_bm25_retriever(text_contents)
    # Step 3: Perform hybrid retrieval
    results         = perform_hybrid_retrieval(query, vector_store, bm25_retriever)
    # Step 4: Extract and return only the top X lines from the relevant text content
    relevant_texts  = []
    for doc in results:
        # Split the content into lines and take the top X
        lines = doc.page_content.splitlines()
        top_lines = "\n".join(lines[:int(num_results)])  # Get the first X lines
        relevant_texts.append(top_lines)
    return relevant_texts

def generate_answer(query, retrieved_docs, model, base_url, temperature=0.7):
    """
    Generates an answer to the query using the retrieved documents as context.

    Parameters:
    - query: The user's question.
    - retrieved_docs: List of retrieved documents (results from process_text_and_retrieve).
    - model: The language model to use (e.g., "deepseek-r1:7b").
    - base_url: The base URL of the language model API.
    - temperature: Sampling temperature for the model.

    Returns:
    - The generated answer.
    """
    # Step 1: Extract context from retrieved documents
    context = None
    if retrieved_docs:
        context = "\n".join([f"[Source {i+1}]: {doc}" for i, doc in enumerate(retrieved_docs)])
    # Step 2: Create a structured prompt
    prompt = f"""Use the following context to answer the question:\n\nContext:\n{context}\n\nQuestion:\n{query}\n\nAnswer:
    """
    # Step 3: Send the prompt to the language model
    try:
        response = requests.post(f"{base_url}/api/generate", json={"model": model, "prompt": prompt, "temperature": temperature, "stream": False})
        # Step 4: Parse and return the response
        if response.status_code == 200:
            return response.json().get("response", "No answer generated.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.RequestException as e:
        # Step 4: Parse and return the response
        llm = OllamaLLM(model=model)
        return llm.invoke(prompt)