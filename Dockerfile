FROM  python:3.10-slim-buster
WORKDIR /app
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./weatherapp .
EXPOSE 8080

CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:8080"]