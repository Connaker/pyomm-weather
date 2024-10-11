FROM python

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn -b 0.0.0.0:80 flaskapp:app --reload
