FROM --platform=linux/amd64 docker.io/python:3.9-alpine

RUN apk add --update nodejs npm

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "-t", "180", "-w", "4", "expander.wsgi:app"]
