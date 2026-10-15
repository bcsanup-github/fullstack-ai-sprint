FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONBUFFERED=1

WORKDIR /app

COPY requiremets.txt .
RUN pip install --no-cache-dir -r requiremets.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--blind", "0.0.0.0:8000"]
