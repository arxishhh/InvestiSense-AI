FROM python:3.10-slim

WORKDIR /app


COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY app/backend ./backend
COPY database ./database

# Expose FastAPI default port
EXPOSE 8000

# Run the FastAPI main with uvicorn
CMD ["uvicorn", "backend.main.server:app", "--host", "0.0.0.0", "--port", "8000"]
