"""
analysis/scoring.py
-------------------

Converts raw voice and pause metrics into normalized scores (0-100).
"""

from analysis.scoring_config import (
    JITTER,
    SHIMMER,
    HNR,
    LOUDNESS,
    ENERGY,
    PITCH_VARIATION,
    AVERAGE_PAUSE,
    LONGEST_PAUSE,
    SPEECH_RATIO,
    WPM,
    CONFIDENCE_LABELS,
)


# =====================================================
# Helpers
# =====================================================

def get_label(score):

    for threshold, label in CONFIDENCE_LABELS:

        if score >= threshold:
            return label

    return "Poor"


def clamp(score):

    return max(0, min(100, round(score)))


# =====================================================
# Voice Stability
# =====================================================

def voice_stability_score(voice):

    score = 100

    jitter = voice["jitter"]

    shimmer = voice["shimmer"]

    hnr = voice["hnr"]


    # ---------- Jitter ----------

    if jitter > JITTER["poor"]:
        score -= 40

    elif jitter > JITTER["average"]:
        score -= 25

    elif jitter > JITTER["good"]:
        score -= 10


    # ---------- Shimmer ----------

    if shimmer > SHIMMER["poor"]:
        score -= 30

    elif shimmer > SHIMMER["average"]:
        score -= 20

    elif shimmer > SHIMMER["good"]:
        score -= 8


    # ---------- HNR ----------

    if hnr < HNR["poor"]:
        score -= 30

    elif hnr < HNR["average"]:
        score -= 20

    elif hnr < HNR["good"]:
        score -= 10

    return clamp(score)


# =====================================================
# Energy
# =====================================================

def energy_score(speech):

    energy = speech["energy"]

    if energy >= ENERGY["excellent"]:
        return 100

    elif energy >= ENERGY["good"]:
        return 90

    elif energy >= ENERGY["average"]:
        return 80

    elif energy >= ENERGY["low"]:
        return 65

    return 45


# =====================================================
# Pitch
# =====================================================

def pitch_score(voice):

    pitch = voice["pitch_variation"]

    if pitch >= PITCH_VARIATION["excellent"]:
        return 95

    elif pitch >= PITCH_VARIATION["good"]:
        return 85

    elif pitch >= PITCH_VARIATION["low"]:
        return 70

    return 50


# =====================================================
# Pause Quality
# =====================================================

def pause_quality_score(pauses):

    score = 100


    # Average Pause

    avg = pauses["average_pause"]

    if avg > AVERAGE_PAUSE["poor"]:
        score -= 35

    elif avg > AVERAGE_PAUSE["average"]:
        score -= 20

    elif avg > AVERAGE_PAUSE["good"]:
        score -= 10


    # Longest Pause

    longest = pauses["longest_pause"]

    if longest > LONGEST_PAUSE["poor"]:
        score -= 30

    elif longest > LONGEST_PAUSE["average"]:
        score -= 20

    elif longest > LONGEST_PAUSE["good"]:
        score -= 10


    # Speech Ratio

    ratio = pauses["speech_ratio"]

    if ratio >= SPEECH_RATIO["excellent"]:
        score += 0

    elif ratio >= SPEECH_RATIO["good"]:
        score -= 5

    elif ratio >= SPEECH_RATIO["average"]:
        score -= 15

    else:
        score -= 25

    return clamp(score)


# =====================================================
# Speech Rate
# =====================================================

def speech_rate_score(wpm):

    if WPM["ideal_low"] <= wpm <= WPM["ideal_high"]:
        return 95

    elif WPM["slow"] <= wpm < WPM["ideal_low"]:
        return 85

    elif WPM["ideal_high"] < wpm <= WPM["fast"]:
        return 80

    elif WPM["too_slow"] <= wpm < WPM["slow"]:
        return 65

    elif WPM["fast"] < wpm <= WPM["too_fast"]:
        return 65

    return 45


# =====================================================
# Main Scoring
# =====================================================

def generate_scores(
    speech,
    voice,
    pauses,
    wpm=140
):

    return {

        "voice_stability": voice_stability_score(
            voice
        ),

        "pause_quality": pause_quality_score(
            pauses
        ),

        "energy": energy_score(
            speech
        ),

        "pitch": pitch_score(
            voice
        ),

        "speech_rate": speech_rate_score(
            wpm
        )

    }