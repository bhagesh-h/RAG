import re
import requests
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from rank_bm25 import BM25Okapi

# from langchain_ollama import OllamaLLM

def create_embeddings(text_contents, embedding_model, base_url):
    embeddings = OllamaEmbeddings(model=embedding_model, base_url=base_url)
    vector_store = FAISS.from_texts(text_contents, embeddings)
    return vector_store

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

def process_text_and_retrieve(text_contents, query, embedding_model, base_url, num_results=3):
    # Step 1: Create embeddings and vector store
    vector_store    = create_embeddings(text_contents, embedding_model, base_url)
    # Step 2: Create BM25 retriever
    bm25_retriever  = create_bm25_retriever(text_contents)
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
    context = "\n".join([f"[Source {i+1}]: {doc}" for i, doc in enumerate(retrieved_docs)])
    # Step 2: Create a structured prompt
    prompt = f"""Use the following context to answer the question:\n\nContext:\n{context}\n\nQuestion:\n{query}\n\nAnswer:
    """
    # # Step 3: Send the prompt to the language model
    # llm = OllamaLLM(model=model)
    # return llm.invoke(prompt)
    response = requests.post(f"{base_url}/api/generate", json={"model": model, "prompt": prompt, "temperature": temperature, "stream": False})
    # Step 4: Parse and return the response
    if response.status_code == 200:
        return response.json().get("response", "No answer generated.")
    else:
        return f"Error: {response.status_code} - {response.text}"




# Example usage
if __name__ == "__main__":
    # Define input text contents and query
    # text_contents = [
    #     "Supervised learning is a type of machine learning where the model is trained on labeled data.\nIt uses input-output pairs to learn a mapping function.\nThis is widely used in classification and regression tasks.\nExamples include spam detection and house price prediction.\nIt requires a labeled dataset for training.",
    #     "Unsupervised learning involves training a model on data without labeled responses.\nIt is used for clustering and dimensionality reduction.\nExamples include customer segmentation and PCA.\nIt helps discover hidden patterns in data.\nNo labeled data is required.",
    #     "Reinforcement learning is a type of machine learning where an agent learns by interacting with its environment.\nIt uses rewards and penalties to learn optimal actions.\nExamples include game playing and robotics.\nIt is based on trial-and-error learning.\nIt requires a defined reward system.",
    #     "Deep learning is a subset of machine learning that uses neural networks with many layers.\nIt is used for tasks like image recognition and natural language processing.\nExamples include convolutional neural networks and transformers.\nIt requires large datasets and high computational power.\nIt is inspired by the human brain.",
    #     "Natural language processing (NLP) is a field of AI focused on the interaction between computers and human language.\nIt includes tasks like sentiment analysis and machine translation.\nExamples include chatbots and language models.\nIt uses techniques like tokenization and embeddings.\nIt bridges the gap between human communication and machines."
    # ]
    # query = "Explain the concept of supervised learning"
    text_contents = [el.text for el in elements]
    query = "what is a Layout object?"
    embedding_model = "nomic-embed-text:latest"
    base_url = "http://127.0.0.1:11434"

    # Step 1: Retrieve relevant text content
    relevant_texts = process_text_and_retrieve(text_contents, query, embedding_model, base_url)

    # Step 2: Generate an answer using the retrieved text content
    answer = generate_answer(query, relevant_texts, model="gemma3:4b", base_url=base_url)

    # Step 3: Display the answer
    print("Generated Answer:")
    print(answer)