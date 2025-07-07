FROM python:3.11-slim


WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8002
ENV DATABASE_URL="postgresql://openpg:openpgpwd@db-client:5432/product_db"
ENV RABBITMQ_URL="amqp://guest:guest@rabbitmq:5672/"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]