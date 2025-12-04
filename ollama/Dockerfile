FROM ollama/ollama

EXPOSE 11434

RUN echo '#!/bin/bash\n\
set -e\n\
ollama serve &\n\
until ollama list > /dev/null 2>&1; do\n\
  sleep 1\n\
done\n\
ollama run llama3.2:3b\n\
wait' > /usr/local/bin/start-ollama.sh && chmod +x /usr/local/bin/start-ollama.sh

ENTRYPOINT ["/usr/local/bin/start-ollama.sh"]