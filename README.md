# RAG
Local PDF RAG Application

## Docker

### Build/Create Image

Use one of the following commands:


1. Pull Image

```bash
docker pull bhagesh/rag
```

2. Build Image

```bash
docker build -t rag .
```

3. Docker Build - Builders Cloud

```bash
docker buildx build --builder <builder-name> -t rag .
```

P.S. Estimated Image Size **12 GB**

## Run Application

1. Linux Based OS

```bash
docker run --rm -it \
    -v /local/path/ollama_models:/root/.ollama \
    -v /local/RAG:/script \
    -v /local/test_data:/tmp \
    -p 11434:11434 \
    -p 8080:8080 \
    rag bash /script/run.sh
```

2. Windows OS

```shell
docker run --rm -it `
    -v "C:\Users\bhage\Documents\ollama_models:/root/.ollama" `
    -v "C:\Users\bhage\Documents\RAG:/script" `
    -v "C:\Users\bhage\Documents\RAG\test_data:/tmp" `
    -p 11434:11434 `
    -p 8080:8080 `
    rag bash /script/run.sh
```

replace container name `rag` with `bhagesh/rag` if you are pulling the image instead of building it.

### User Details


**Username**: admin<br>
**Password**: admin 

### Packages
```python
faiss-cpu 
hf_xet 
langchain 
langchain-community 
langchain-unstructured 
langchain-ollama 
llama-index 
networkx 
ollama 
pandas 
PyPDF2 
rank-bm25 
sentence-transformers 
streamlit 
streamlit-image-select 
torch
"unstructured[pdf]" 
```

### Requirements
**Storage**: 15GB<br>
**RAM**: 8GB


Tested on *Asus Zephyrus G14* (2024), **CPU** Ryzen 9 8945HS, **RAM** 16GB, **Storage** 1TB SSD
