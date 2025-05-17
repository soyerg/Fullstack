FROM python:3.10-slim

WORKDIR /dashboard

COPY . /dashboard


RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8050

CMD ["python", "app.py"]
