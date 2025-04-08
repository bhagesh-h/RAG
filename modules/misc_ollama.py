import os
import ollama
from langchain_ollama import OllamaEmbeddings, OllamaLLM

class ollamaFunc:
    
    def __init__(self, model="bakllava", embedding_model="all-minilm"):
        self.model = model
        self.embedding_model = embedding_model
    
    def pull_model(self):
        if self.model:
            ollama.pull(self.model)
        if self.embedding_model:
            ollama.pull(self.embedding_model)
        return self.model
    
    def embed_model(self):
        if self.embedding_model:
            return OllamaEmbeddings(model=self.embedding_model)
    
    def query_ollama(self, prompt='', context='', augmented_prompt=''):
        if self.embedding_model:
            augmented_prompt = augmented_prompt if augmented_prompt else f"Context: {context}\n\nQuestion: {prompt}\nAnswer:"
            llm = OllamaLLM(model=self.embedding_model)
            return llm.invoke(augmented_prompt)

