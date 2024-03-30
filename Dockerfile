# syntax=docker/dockerfile:1

FROM python:3.10.13

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY .env .env

COPY . .

EXPOSE 3100

CMD ["gunicorn", "__init__:app"]