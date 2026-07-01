"""
FinalRound Filler Detector

Detects common filler words from a transcript.
"""

import re
from collections import Counter

def filler_severity(total_fillers):

    if total_fillers <= 2:
        return "Excellent"

    elif total_fillers <= 5:
        return "Good"

    elif total_fillers <= 8:
        return "Average"

    elif total_fillers <= 12:
        return "Needs Improvement"

    return "Poor"

FILLER_WORDS = [

    "um",
    "uh",
    "erm",
    "hmm",

    "like",
    "actually",
    "basically",
    "literally",

    "you know",
    "kind of",
    "sort of",

    "i mean",

    "okay",
    "ok",
    "right"

]


def detect_fillers(transcript: str):

    transcript = transcript.lower()

    total_words = len(
        re.findall(r"\b\w+\b", transcript)
    )

    filler_counter = Counter()

    total_fillers = 0

    for filler in FILLER_WORDS:

        matches = re.findall(
            r"\b" + re.escape(filler) + r"\b",
            transcript
        )

        count = len(matches)

        if count:

            filler_counter[filler] = count

            total_fillers += count

    filler_percentage = 0

    if total_words:

        filler_percentage = round(
            (total_fillers / total_words) * 100,
            2
        )

    severity = filler_severity(total_fillers)

    return {

        "total_words": total_words,

        "total_fillers": total_fillers,

        "filler_percentage": filler_percentage,

        "fillers": dict(filler_counter),

        "severity": severity

    }