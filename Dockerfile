FROM python:3.9.21

RUN apt-get update -y \
    && apt-get install -y poppler-utils tesseract-ocr
RUN pip install --upgrade pip
RUN pip install ollama "unstructured[pdf]" langchain-unstructured langchain-community langchain_ollama llama-index chromadb

RUN curl -fsSL https://ollama.com/install.sh | sh

RUN pip install streamlit

RUN mkdir -p ~/.streamlit/ && \
    streamlit config show > config.toml && \
    sed -i 's/# runOnSave = false/runOnSave = true/' config.toml && \
    sed -i 's/# fileWatcherType = "auto"/fileWatcherType = "poll"/' config.toml && \
    grep -v "#" config.toml | grep -v ' ~/.streamlit/config.toml.' > ~/.streamlit/config.toml
    
# RUN nohup ollama serve &>> ollama.log &

