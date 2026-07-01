import librosa
import numpy as np
import opensmile

from analysis.voice_metrics import get_voice_metrics

# ----------------------------------------------------
# OpenSMILE Model
# ----------------------------------------------------

smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.eGeMAPSv02,
    feature_level=opensmile.FeatureLevel.Functionals,
)


# ----------------------------------------------------
# Feature Extraction
# ----------------------------------------------------

def extract_features(audio_path):

    # -----------------------------
    # Load Audio
    # -----------------------------

    y, sr = librosa.load(
        audio_path,
        sr=16000
    )

    # -----------------------------
    # Basic Speech Metrics
    # -----------------------------

    duration = librosa.get_duration(
        y=y,
        sr=sr
    )

    rms = float(
        np.mean(
            librosa.feature.rms(y=y)
        )
    )

    zcr = float(
        np.mean(
            librosa.feature.zero_crossing_rate(y)
        )
    )

    spectral_centroid = float(
        np.mean(
            librosa.feature.spectral_centroid(
                y=y,
                sr=sr
            )
        )
    )

    # -----------------------------
    # OpenSMILE Features
    # -----------------------------

    smile_df = smile.process_file(audio_path)

    raw_features = smile_df.iloc[0].to_dict()

    raw_features = {
        key: float(value)
        for key, value in raw_features.items()
    }

    # -----------------------------
    # Voice Metrics
    # -----------------------------

    voice = get_voice_metrics(raw_features)

    # -----------------------------
    # Final Response
    # -----------------------------

    return {

        "speech": {

            "duration": round(duration, 2),

            "energy": round(rms, 4),

            "zero_crossing_rate": round(zcr, 4),

            "spectral_centroid": round(
                spectral_centroid,
                2
            )

        },

        "voice": voice,

        # Keep internally for future analysis.
        # Remove from API response if you don't need it.
        "raw_features": raw_features

    }