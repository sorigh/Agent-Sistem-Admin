FROM python:3
WORKDIR /usr/src/app


RUN pip install fastmcp fastapi uvicorn

COPY . .

CMD ["python", "server.py"]