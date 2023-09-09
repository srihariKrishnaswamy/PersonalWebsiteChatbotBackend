FROM --platform=linux/amd64 python:3.8

RUN apt-get update && apt-get install -y libsndfile1

WORKDIR /app

COPY . /app

RUN pip install -r dependencies.txt

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "server:app"]
