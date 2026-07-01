import os
import subprocess


def convert_to_wav(input_file):

    output_file = os.path.splitext(input_file)[0] + "_converted.wav"

    command = [
        "ffmpeg",
        "-y",
        "-i",
        input_file,
        "-ar",
        "16000",
        "-ac",
        "1",
        output_file
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    print(result.stdout)
    print(result.stderr)

    if result.returncode != 0:
        raise Exception(result.stderr)

    return output_file