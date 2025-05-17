FROM python:3.10-slim

WORKDIR /app

COPY ./app /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["./entrypoint.sh"]
