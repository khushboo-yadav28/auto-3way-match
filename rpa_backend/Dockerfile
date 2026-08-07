# rpa_backend/Dockerfile
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Keep the container alive to run scripts manually
CMD ["tail", "-f", "/dev/null"]