FROM python:3.10-slim

WORKDIR /app

COPY docker/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY collections/ collections/
COPY scripts/ scripts/
RUN mkdir -p output

ENTRYPOINT ["python", "src/document_intelligence.py"]
