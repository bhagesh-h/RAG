from langchain_ollama import OllamaEmbeddings
import chromadb
import os

class embeddings:
    """
    A class to manage RAG workflows with ChromaDB and Ollama embeddings.
    
    Features:
    - Persistent ChromaDB storage
    - Custom Ollama embedding integration
    - Document management
    - Query functionality
    """
    
    def __init__(self, model_name: str = "all-minilm", 
                 collection_name: str = "rag_collection",
                 persist_dir: str = None):
        """
        Initialize RAG Manager with configuration.
        
        Args:
            model_name: Ollama model name (default: 'all-minilm')
            collection_name: ChromaDB collection name (default: 'rag_collection')
            persist_dir: Directory for ChromaDB storage (default: cwd/chroma_db)
        """
        # Configure paths and models
        self.model_name = model_name
        self.collection_name = collection_name
        self.persist_dir = persist_dir or os.path.join(os.getcwd(), "chroma_db")
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        
        # Setup embedding pipeline
        self.embeddings = OllamaEmbeddings(model=self.model_name)
        self.embedding_function = self._create_embedding_function()
        
        # Initialize collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "A collection for RAG with Ollama"},
            embedding_function=self.embedding_function
        )
    
    def _delete_collection(self, collection_name=''):
        """Delete the ChromaDB collection"""
        self.client.delete_collection(name=collection_name if collection_name else self.collection_name)
        print(f"Collection '{collection_name if collection_name else self.collection_name}' deleted.")

    def _create_embedding_function(self):
        """Create custom embedding function wrapper"""
        class EmbeddingWrapper:
            def __init__(self, embeddings):
                self.embeddings = embeddings
                
            def __call__(self, input):
                if isinstance(input, str):
                    input = [input]
                return self.embeddings.embed_documents(input)
                
        return EmbeddingWrapper(self.embeddings)

    def add_documents(self, documents: list, ids: list):
        """
        Add documents to ChromaDB collection.
        
        Args:
            documents: List of text documents
            ids: List of unique document identifiers
        """
        self.collection.add(
            documents=documents,
            ids=ids
        )

    def query_chromadb(self, query_text: str, n_results: int = 1):
        """
        Query the ChromaDB collection for relevant documents.

        Args:
            query_text (str): The input query.
            n_results (int): The number of top results to return.

        Returns:
            tuple: A tuple containing two lists:
                - list of str: The top matching documents.
                - list of dict: Their associated metadata.
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results["documents"], results["metadatas"]

    def __repr__(self):
        return f"RAGManager(model='{self.model_name}', collection='{self.collection_name}')"

if __name__ == "__main__":
    rag = embeddings()

    documents, doc_ids = [], []
    
    # Add documents to the collection
    rag.add_documents(documents, doc_ids)

    # Query the collection for relevant results
    query_text = "explain LayoutParser ?"
    documents, metadata = rag.query_chromadb(query_text, n_results=2)

    print("Matched Documents:", documents)
    print("Metadata:", metadata)