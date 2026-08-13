FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Verify the application modules can be imported during the image build
RUN python -c "import prompts_hub.health; import prompts_hub.claims; import prompts_hub.leave; print('SUCCESS: All prompts_hub modules imported correctly')"

EXPOSE 10000

CMD ["sh", "-c", "echo '=== CONTAINER STARTED ==='; echo 'PORT='$PORT; echo '=== FILES ==='; pwd; ls -la /app; echo '=== PACKAGE ==='; ls -la /app/src/prompts_hub; echo '=== STARTING PYTHON ==='; exec python -u -m prompts_hub.leave --host 0.0.0.0 --port ${PORT:-10000}"]