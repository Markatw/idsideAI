FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY Sprint26 /app/Sprint26
RUN pip install --no-cache-dir fastapi==0.110.0 "uvicorn[standard]==0.29.0"
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
