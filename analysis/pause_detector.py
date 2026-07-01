from silero_vad import (
    load_silero_vad,
    read_audio,
    get_speech_timestamps
)

model = load_silero_vad()


def detect_pauses(audio_path):

    wav = read_audio(audio_path)

    speech = get_speech_timestamps(
        wav,
        model,
        return_seconds=True
    )

    if len(speech) == 0:

        return {
            "pause_count": 0,
            "average_pause": 0,
            "longest_pause": 0,
            "speech_duration": 0,
            "silence_duration": 0,
            "speech_ratio": 0,
            "silence_ratio": 0,
            "segments": []
        }

    speech_duration = 0

    silence_duration = 0

    pauses = []

    for i, segment in enumerate(speech):

        speech_duration += (
            segment["end"] -
            segment["start"]
        )

        if i > 0:

            pause = (
                segment["start"] -
                speech[i - 1]["end"]
            )

            pauses.append(pause)

            silence_duration += pause

    total_duration = (
        speech_duration +
        silence_duration
    )

    average_pause = (
        sum(pauses) / len(pauses)
        if pauses else 0
    )

    longest_pause = (
        max(pauses)
        if pauses else 0
    )

    speech_ratio = (
        speech_duration / total_duration * 100
        if total_duration else 0
    )

    silence_ratio = (
        silence_duration / total_duration * 100
        if total_duration else 0
    )

    return {

        "pause_count": len(pauses),

        "average_pause": round(
            average_pause,
            2
        ),

        "longest_pause": round(
            longest_pause,
            2
        ),

        "speech_duration": round(
            speech_duration,
            2
        ),

        "silence_duration": round(
            silence_duration,
            2
        ),

        "speech_ratio": round(
            speech_ratio,
            2
        ),

        "silence_ratio": round(
            silence_ratio,
            2
        ),

        "segments": speech
    }