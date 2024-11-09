FROM  python:3.10-slim-buster

RUN useradd -ms /bin/bash worker
USER worker
WORKDIR /app
COPY --chown=worker:worker ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
ENV PATH="/home/worker/.local/bin:${PATH}"
COPY --chown=worker:worker ./weatherapp .
EXPOSE 5000

CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:5000"]