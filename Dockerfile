FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Restrict threading globally to fit within container limits
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV OPENBLAS_NUM_THREADS=1
ENV VECLIB_MAXIMUM_THREADS=1
ENV NUMEXPR_NUM_THREADS=1

# ----------------------------------------------------
# Install Linux packages
# ----------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
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

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------
# Pre-download VAD Model during Build Stage (Cache it)
# ----------------------------------------------------
RUN python -c "from silero_vad import load_silero_vad; load_silero_vad(onnx=True)"

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
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]