FROM python:3.14-slim

WORKDIR /app

ENV FLASK_APP=app.py

COPY . .

RUN apt update && apt install -y cron && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
RUN echo "0 0 */7 * * /usr/local/bin/python /app/prune_archive.py" > /etc/cron.d/cleanup

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f http://localhost:5000 || exit 1

CMD ["/bin/bash", "/app/docker/entrypoint.sh"]