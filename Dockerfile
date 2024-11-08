FROM  python:3.10-slim-buster

RUN adduser -D worker && pip install --upgrade
USER worker
WORKDIR /app
COPY --chown=worker:worker ./requirements.txt .
RUN pip install --user -r --no-cache-dir --upgrade -r requirements.txt
ENV PATH="/home/worker/.local/bin:${PATH}"
COPY --chown=worker:worker ./weatherapp .
EXPOSE 8080

CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:8080"]