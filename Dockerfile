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

RUN pip install streamlit-image-select
RUN apt-get install -y libgl1-mesa-glx
# RUN nohup ollama serve &>> ollama.log &

