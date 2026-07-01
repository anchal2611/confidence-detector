import os
import shutil
import traceback

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from analysis.audio_converter import convert_to_wav
from analysis.feature_extractor import extract_features
from analysis.pause_detector import detect_pauses
from analysis.scoring import generate_scores
from analysis.communication_engine import communication_report
from analysis.report_generator import generate_report


# ---------------------------------------------------
# FastAPI App
# ---------------------------------------------------

app = FastAPI(
    title="FinalRound Speech Analysis API",
    version="1.0.0"
)


# ---------------------------------------------------
# CORS
# ---------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        # Add your deployed frontend later
        "https://your-finalround.vercel.app",
        "https://confidence-detector.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------
# Upload Folder
# ---------------------------------------------------

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------------------------------------------------
# Home
# ---------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "FinalRound Speech Analysis API 🚀",
        "version": "1.0.0"
    }


# ---------------------------------------------------
# Health Check
# ---------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "Speech Analysis API",
        "version": "1.0.0"
    }


# ---------------------------------------------------
# Analyze Audio
# ---------------------------------------------------

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):

    input_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    wav_path = None

    try:

        # Save uploaded file

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # -----------------------------
        # Audio Conversion
        # -----------------------------

        wav_path = convert_to_wav(input_path)

        # -----------------------------
        # Feature Extraction
        # -----------------------------

        features = extract_features(wav_path)

        speech = features["speech"]
        voice = features["voice"]

        # -----------------------------
        # Pause Detection
        # -----------------------------

        pauses = detect_pauses(wav_path)

        # -----------------------------
        # Voice Scoring
        # -----------------------------

        scores = generate_scores(
            speech=speech,
            voice=voice,
            pauses=pauses
        )

        # -----------------------------
        # Communication Analysis
        # -----------------------------

        communication = communication_report(
            speech=speech,
            voice=voice,
            pauses=pauses
        )

        # -----------------------------
        # Final Report
        # -----------------------------

        report = generate_report(
            speech=speech,
            voice=voice,
            pauses=pauses,
            communication=communication,
            scores=scores
        )

        return report

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        # Remove original upload

        if os.path.exists(input_path):
            os.remove(input_path)

        # Remove generated wav

        if wav_path and os.path.exists(wav_path):
            os.remove(wav_path)