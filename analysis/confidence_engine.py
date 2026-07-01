"""
analysis/confidence_engine.py
-----------------------------

Final confidence engine for FinalRound.
Combines scoring and communication results into a final evaluation.
"""

from analysis.scoring import get_label


# ==========================================================
# Overall Score
# ==========================================================

def calculate_overall(scores, communication):

    weights = {
        "voice_stability": 0.20,
        "pause_quality": 0.15,
        "energy": 0.15,
        "speech_rate": 0.10,
        "clarity": 0.15,
        "fluency": 0.10,
        "engagement": 0.10,
        "pace": 0.05,
    }

    overall = (
        scores["voice_stability"] * weights["voice_stability"] +
        scores["pause_quality"] * weights["pause_quality"] +
        scores["energy"] * weights["energy"] +
        scores["speech_rate"] * weights["speech_rate"] +
        communication["clarity"] * weights["clarity"] +
        communication["fluency"] * weights["fluency"] +
        communication["engagement"] * weights["engagement"] +
        communication["pace"] * weights["pace"]
    )

    return round(overall, 2)


# ==========================================================
# Interview Readiness
# ==========================================================

def interview_readiness(score):

    if score >= 90:
        return "Excellent"

    elif score >= 80:
        return "Ready"

    elif score >= 70:
        return "Almost Ready"

    elif score >= 60:
        return "Needs Practice"

    return "Needs Significant Improvement"


# ==========================================================
# Strengths
# ==========================================================

def generate_strengths(scores, communication, pauses):

    strengths = []

    if scores["voice_stability"] >= 80:
        strengths.append(
            "Maintained stable voice quality throughout the response."
        )

    if communication["clarity"] >= 85:
        strengths.append(
            "Speech was clear and easy to understand."
        )

    if communication["fluency"] >= 80:
        strengths.append(
            "Maintained good fluency with minimal hesitation."
        )

    if communication["engagement"] >= 85:
        strengths.append(
            "Good vocal engagement throughout the answer."
        )

    if pauses["speech_ratio"] >= 80:
        strengths.append(
            "Maintained a healthy speaking rhythm."
        )

    if scores["energy"] >= 85:
        strengths.append(
            "Spoke with strong vocal energy."
        )

    if not strengths:
        strengths.append(
            "Maintained consistent communication."
        )

    return strengths


# ==========================================================
# Improvements
# ==========================================================

def generate_improvements(scores, communication, pauses):

    improvements = []

    if pauses["longest_pause"] > 3:
        improvements.append(
            "Reduce long pauses between ideas."
        )

    if pauses["average_pause"] > 1:
        improvements.append(
            "Reduce hesitation during your response."
        )

    if communication["pace"] < 80:
        improvements.append(
            "Maintain a more consistent speaking pace."
        )

    if scores["energy"] < 80:
        improvements.append(
            "Speak with slightly more vocal energy."
        )

    if communication["clarity"] < 80:
        improvements.append(
            "Improve pronunciation for better clarity."
        )

    if communication["fluency"] < 75:
        improvements.append(
            "Practice speaking continuously without unnecessary breaks."
        )

    if not improvements:
        improvements.append(
            "Keep practicing mock interviews to build confidence."
        )

    return improvements


# ==========================================================
# Verdict
# ==========================================================

def generate_verdict(overall, pauses):

    if overall >= 90:

        return (
            "Excellent interview performance with confident delivery and clear communication."
        )

    elif overall >= 80:

        if pauses["longest_pause"] > 5:

            return (
                "Good communication overall. Reducing long pauses will make your answers more impactful."
            )

        return (
            "Strong communication with good confidence and speaking flow."
        )

    elif overall >= 70:

        return (
            "A solid performance with room to improve speaking consistency and confidence."
        )

    return (
        "Continue practicing to improve speaking confidence and interview readiness."
    )


# ==========================================================
# Main Engine
# ==========================================================

def confidence_report(
    communication,
    scores,
    pauses
):

    overall = calculate_overall(
        scores,
        communication
    )

    confidence = round(
        (
            overall +
            communication["communication"]
        ) / 2,
        2
    )

    return {

        "overall": overall,

        "confidence": confidence,

        "label": get_label(confidence),

        "readiness": interview_readiness(confidence),

        "verdict": generate_verdict(
            overall,
            pauses
        ),

        "strengths": generate_strengths(
            scores,
            communication,
            pauses
        ),

        "improvements": generate_improvements(
            scores,
            communication,
            pauses
        )

    }