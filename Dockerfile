FROM python:3.9-slim
USER 1001
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl --fail http://localhost:5000 || exit 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py requirements.txt .

# Running as root - security issue
EXPOSE 5000
USER 1001
EXPOSE 5000
CMD ["python", "app.py"]
