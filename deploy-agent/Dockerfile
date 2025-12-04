FROM python:3
WORKDIR /app

RUN pip install google-adk mcp litellm

COPY my_agent /app/my_agent
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENV OLLAMA_API_BASE=http://ollama:11434
ENV URL_MCP=http://mcp_server:8100/mcp

ENTRYPOINT ["/app/entrypoint.sh"]