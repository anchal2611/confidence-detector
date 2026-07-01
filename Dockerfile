FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# ----------------------------------------------------
# Install Linux packages
# ----------------------------------------------------

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    libgomp1 \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------
# Working Directory
# ----------------------------------------------------

WORKDIR /app

# ----------------------------------------------------
# Install Python dependencies
# ----------------------------------------------------

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------
# Copy Project
# ----------------------------------------------------

COPY . .

RUN mkdir -p uploads

# ----------------------------------------------------
# Expose Port
# ----------------------------------------------------

EXPOSE 10000

# ----------------------------------------------------
# Start FastAPI
# ----------------------------------------------------

CMD ["uvicorn","app:app","--host","0.0.0.0","--port","10000"]