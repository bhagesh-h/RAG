from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

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