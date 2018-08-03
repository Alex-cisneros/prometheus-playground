FROM python:3

RUN pip install pip-tools prometheus_client

WORKDIR /app

COPY server.py /app/server.py

CMD ["python", "/app/server.py"]