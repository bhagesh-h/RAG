# docker run --rm -it -v /mnt/c/Users/bhage/Documents/code/ollama_models:/root/.ollama -p 11434:11434 -p 8080:8080 rag bash
export OLLAMA_HOST=0.0.0.0
export OLLAMA_API_BASE_URL=http://host.docker.internal:11434/api
nohup ollama serve &> /dev/null &
sleep 5
streamlit run --server.port 8080 app.py