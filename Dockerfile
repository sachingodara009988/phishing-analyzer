# Stage 1: Build the React frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the FastAPI backend
FROM python:3.10-slim AS backend-runner
WORKDIR /app/backend

# Install system dependencies (e.g., whois)
RUN apt-get update && apt-get install -y --no-install-recommends \
    whois \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY backend/ ./

# Copy built frontend assets from the frontend-builder stage
COPY --from=frontend-builder /app/backend/static ./static

EXPOSE 10000

ENV PORT=10000
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
