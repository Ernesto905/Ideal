FROM python:3.12-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./app /app
COPY .env /app

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

EXPOSE 5000


CMD ["flask", "run","--debug", "--host=0.0.0.0"]




