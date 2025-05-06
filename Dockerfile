FROM python:3.12

WORKDIR /
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .env /src/.env

COPY src/ /src
WORKDIR /src

EXPOSE 8000

CMD python manage.py wait_for_db && python manage.py migrate && python manage.py runserver 0.0.0.0:8000 --noreload