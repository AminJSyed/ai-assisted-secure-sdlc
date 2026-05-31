FROM python:3.11-slim

WORKDIR /app

RUN groupadd -r appuser \
    && useradd -r -g appuser -u 10001 appuser

COPY . .

RUN pip install --no-cache-dir flask \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/', timeout=2)" || exit 1

CMD ["python", "app.py"]
