FROM python:3.11-slim

WORKDIR /service

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY app ./app
COPY monitoring ./monitoring

# The model will be loaded through MLflow from S3.
# Do not copy the local model into the image.

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "app.app:app"]