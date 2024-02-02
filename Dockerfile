FROM python:3.10-alpine


RUN mkdir /app/
WORKDIR /app/

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONPATH=/app

COPY . .

RUN \
    apk upgrade && \
    apk add curl make build-base python3-dev libpq-dev gcc postgresql-client && \
    curl -fsSL -o /bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64 && \
    chmod +x /bin/dbmate

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
