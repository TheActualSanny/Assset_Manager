FROM python:3.12

WORKDIR /
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY .env /src/.env

COPY src/ /src
WORKDIR /

CMD ["celery", "-A", "src.dependencies", "worker", "--pool=info", "-l", "info"]