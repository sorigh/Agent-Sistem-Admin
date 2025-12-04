FROM ollama/ollama

EXPOSE 11434

COPY start-ollama.sh /usr/local/bin/start-ollama.sh
# make script executable
RUN chmod +x /usr/local/bin/start-ollama.sh

# set entrypoint to the start script
ENTRYPOINT ["/usr/local/bin/start-ollama.sh"]