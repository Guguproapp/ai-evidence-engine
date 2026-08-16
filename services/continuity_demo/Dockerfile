FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends openssl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY services/continuity_demo/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY services/continuity_demo/app.py ./app.py
COPY services/continuity_demo/static ./static
COPY apps/web/public/demo/version-3.png ./static/version-3.png

ENV PYTHONPATH=/app/src
ENV PORT=8080
ENV DEMO_EVIDENCE_PATH=/app/static/version-3.png

CMD exec gunicorn --bind :${PORT} --workers 1 --threads 8 --timeout 120 app:app
