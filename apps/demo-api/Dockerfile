FROM python:3.12-slim

WORKDIR /app

COPY . /app

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["python", "-m", "demo_api.main"]