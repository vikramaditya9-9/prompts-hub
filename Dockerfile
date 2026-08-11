FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/src

EXPOSE 8080

CMD ["sh", "-c", "echo 'Starting Prompts Hub Insurance Claims API...' && python -m prompts_hub.claims --host 0.0.0.0 --port ${PORT}"]