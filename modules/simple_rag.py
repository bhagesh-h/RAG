from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM

class ImageDescriptionChain:
    def __init__(self, model="gemma3:4b", temperature=0):
        """
        Initialize the class with the desired model and temperature for ChatOllama.
        """
        self.llm = ChatOllama(model=model, temperature=temperature)
        self.chain = self._build_chain()

    def _build_chain(self):
        """
        Build the chain by combining the prompt function, LLM, and output parser.
        """
        return self.prompt_func | self.llm | StrOutputParser()

    @staticmethod
    def prompt_func(data):
        """
        Create a prompt based on the input data containing text and image.
        """
        text = data["text"]
        image = data["image"]

        image_part = {
            "type": "image_url",
            "image_url": f"data:image/jpeg;base64,{image}",
        }

        content_parts = []

        text_part = {"type": "text", "text": text}

        content_parts.append(image_part)
        content_parts.append(text_part)

        return [HumanMessage(content=content_parts)]

    def query(self, text, image_b64):
        """
        Execute the chain with the provided text and image data.
        """
        input_data = {"text": text, "image": image_b64}
        return self.chain.invoke(input_data)

class RAGDescriptionChain:
    def __init__(self, retrieved_doc='', metadata='', query_text='', llm_model='gemma3:4b'):
        self.retrieved_docs = retrieved_doc
        self.metadata = metadata
        self.query_text = query_text
        self.llm_model = llm_model
    def rag_pipeline(self):
        if self.retrieved_docs and self.metadata:
            context = " ".join(self.retrieved_docs[0]) if self.retrieved_docs else "No relevant documents found."
            augmented_prompt = f"Context: {context}\n\nQuestion: {self.query_text}\nAnswer:"
        else:
            augmented_prompt = f"Question: {self.query_text}\nAnswer:"
        return augmented_prompt
    def query_ollama(self):
        llm = OllamaLLM(model=self.llm_model)
        return llm.invoke(self.rag_pipeline())
                 
# Example usage:
if __name__ == "__main__":
    # Initialize the chain with a specific model and temperature
    description_chain = ImageDescriptionChain(model="gemma3:4b", temperature=0)

    # Provide input data
    image_b64 = "<base64_encoded_image_here>"  # Replace with actual base64-encoded image string
    result = description_chain.query("Describe the image", image_b64)

    # Print the result
    print(result)
