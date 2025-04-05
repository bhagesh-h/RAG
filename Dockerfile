FROM python:3.9.21

RUN apt-get update -y \
    && apt-get install -y poppler-utils tesseract-ocr
RUN pip install --upgrade pip
RUN pip install ollama "unstructured[pdf]" langchain-unstructured langchain-community langchain_ollama llama-index chromadb

RUN curl -fsSL https://ollama.com/install.sh | sh
# RUN nohup ollama serve &>> ollama.log &

