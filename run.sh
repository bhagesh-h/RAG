#!/bin/bash

export OLLAMA_HOST=0.0.0.0
export OLLAMA_API_BASE_URL=http://host.docker.internal:11434/api
nohup ollama serve &> /dev/null &
sleep 5
cd /script
streamlit run --server.port 8080 app.py