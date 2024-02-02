FROM python:3.9

RUN mkdir /app/
WORKDIR /app/

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONPATH=/app

COPY . .

RUN \
    apt-get update && \
    apt-get install -y libpq-dev gcc postgresql-client && \
    python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
