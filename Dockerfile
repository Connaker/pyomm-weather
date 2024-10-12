FROM  python:3.10-slim-buster

    WORKDIR /app

    COPY requirements.txt requirements.txt
    RUN pip3 install -r requirements.txt

    COPY ./src .

    EXPOSE 5000

    ENTRYPOINT ["python3"]
    CMD ["app.py"]
