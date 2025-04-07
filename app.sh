# docker run --rm -it -v ${PWD}:/rag/ OLLAMA_API_BASE_URL=http://ollama:11434/api -p 8080:8080 -p 11434:11434 -v //C/Users/bhage/Documents/code/ollama:/root/.ollama -P rag bash
# ollama serve &> ollama.log &

export OLLAMA_HOST=0.0.0.0
export OLLAMA_API_BASE_URL=http://host.docker.internal:11434/api

streamlit run \
    --server.port 8080 \
    HOME.py