"""
analysis/report_generator.py
----------------------------

Creates the final report returned to the frontend.
"""

from analysis.confidence_engine import confidence_report


# ==========================================================
# Main Report Generator
# ==========================================================

def generate_report(
    speech,
    voice,
    pauses,
    communication,
    scores
):

    confidence = confidence_report(
        communication=communication,
        scores=scores,
        pauses=pauses
    )

    return {

        "status": "success",

        # =====================================
        # Summary
        # =====================================

        "summary": {

            "overall_score": confidence["overall"],

            "confidence": confidence["confidence"],

            "label": confidence["label"],

            "interview_readiness": confidence["readiness"],

            "verdict": confidence["verdict"]

        },

        # =====================================
        # Analytics
        # Used directly by dashboard graphs
        # =====================================

        "analytics": {

            "voice_stability": scores["voice_stability"],

            "pause_quality": scores["pause_quality"],

            "energy": scores["energy"],

            "speech_rate": scores["speech_rate"],

            "communication": communication["communication"],

            "clarity": communication["clarity"],

            "fluency": communication["fluency"],

            "engagement": communication["engagement"],

            "pace": communication["pace"]

        },

        # =====================================
        # Speech
        # =====================================

        "speech": {

            "duration": speech["duration"],

            "speech_ratio": pauses["speech_ratio"],

            "pause_count": pauses["pause_count"],

            "average_pause": pauses["average_pause"],

            "longest_pause": pauses["longest_pause"]

        },

        # =====================================
        # Voice
        # =====================================

        "voice": {

            "stability": scores["voice_stability"],

            "energy": scores["energy"],

            "pitch_variation": voice["pitch_variation"],

            "loudness": voice["loudness"]

        },

        # =====================================
        # Communication
        # =====================================

        "communication": {

            "overall": communication["communication"],

            "clarity": communication["clarity"],

            "fluency": communication["fluency"],

            "engagement": communication["engagement"],

            "pace": communication["pace"]

        },

        # =====================================
        # Feedback
        # =====================================

        "feedback": {

            "strengths": confidence["strengths"],

            "improvements": confidence["improvements"]

        }

    }