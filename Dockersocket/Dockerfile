FROM python:3.12-slim

RUN mkdir /fastapi_web_socket

WORKDIR /fastapi_web_socket

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD WebSocket .

CMD uvicorn main:app --host=0.0.0.0 --port=8002
