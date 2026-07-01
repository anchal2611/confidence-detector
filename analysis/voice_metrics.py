def get_voice_metrics(smile):

    return {

        # Pitch

        "pitch_mean": round(
            smile["F0semitoneFrom27.5Hz_sma3nz_amean"],
            2
        ),

        "pitch_variation": round(
            smile["F0semitoneFrom27.5Hz_sma3nz_stddevNorm"],
            2
        ),

        # Loudness

        "loudness": round(
            smile["loudness_sma3_amean"],
            2
        ),

        # Voice Stability

        "jitter": round(
            smile["jitterLocal_sma3nz_amean"],
            4
        ),

        "shimmer": round(
            smile["shimmerLocaldB_sma3nz_amean"],
            4
        ),

        "hnr": round(
            smile["HNRdBACF_sma3nz_amean"],
            2
        ),

        # Speaking Behaviour

        "voice_segments_per_sec": round(
            smile["VoicedSegmentsPerSec"],
            2
        ),

        "average_voice_segment": round(
            smile["MeanVoicedSegmentLengthSec"],
            2
        ),

        "average_silence": round(
            smile["MeanUnvoicedSegmentLength"],
            2
        ),

        # Volume

        "sound_level": round(
            smile["equivalentSoundLevel_dBp"],
            2
        )

    }