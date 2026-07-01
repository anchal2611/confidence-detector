"""
analysis/communication_engine.py
"""

def calculate_clarity(voice):

    score = 85

    if voice["jitter"] < 0.03:
        score += 5

    if voice["hnr"] > 10:
        score += 5

    if voice["shimmer"] < 1.2:
        score += 5

    return min(score, 95)


def calculate_fluency(pauses):

    score = 100

    score -= pauses["pause_count"] * 0.5

    score -= pauses["average_pause"] * 8

    score -= max(
        0,
        pauses["longest_pause"] - 2
    ) * 3

    return max(60, round(score, 2))


def calculate_engagement(voice):

    score = 80

    if voice["pitch_variation"] >= 0.10:
        score += 5

    if voice["pitch_variation"] >= 0.15:
        score += 5

    if voice["loudness"] >= 0.30:
        score += 5

    return min(score, 95)


def calculate_pace(pauses):

    ratio = pauses["speech_ratio"]

    if ratio >= 85:
        return 95

    elif ratio >= 75:
        return 85

    elif ratio >= 65:
        return 75

    return 65


def communication_report(
    speech,
    voice,
    pauses
):

    clarity = calculate_clarity(voice)

    fluency = calculate_fluency(pauses)

    engagement = calculate_engagement(voice)

    pace = calculate_pace(pauses)

    communication = round(

        (
            clarity +
            fluency +
            engagement +
            pace
        ) / 4,

        2

    )

    return {

        "communication": communication,

        "clarity": clarity,

        "fluency": fluency,

        "engagement": engagement,

        "pace": pace

    }