FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]

# docker-compose build
# docker-compose up