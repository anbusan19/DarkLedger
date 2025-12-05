# Stage 1: COBOL Compiler
FROM debian:bullseye-slim AS cobol-builder
RUN apt-get update && apt-get install -y gnucobol
WORKDIR /build
COPY cobol/ ./cobol/
RUN cobc -x -o cobol/bin/payroll cobol/payroll.cbl

# Stage 2: Frontend Build
FROM node:18-alpine AS frontend-builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Final Stage: Runtime
FROM python:3.11-slim
RUN apt-get update && apt-get install -y libcob4-runtime && rm -rf /var/lib/apt/lists/*
WORKDIR /app

# Copy COBOL binary
COPY --from=cobol-builder /build/cobol/bin/ ./cobol/bin/

# Copy frontend build
COPY --from=frontend-builder /app/dist ./frontend/dist

# Copy backend
COPY backend/ ./backend/
COPY data/ ./data/
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Use PORT environment variable if provided (for Render), otherwise default to 8000
# Render automatically sets the PORT environment variable
CMD sh -c "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"
