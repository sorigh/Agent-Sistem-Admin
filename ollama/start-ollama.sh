#!/bin/bash
set -e
# server ollama in background
ollama serve &

# wait for ollama to be ready
until ollama list > /dev/null 2>&1; do
  sleep 1
done

ollama run llama3.2:3b

wait
