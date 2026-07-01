import os
import subprocess


def convert_to_wav(input_file):

    output_file = os.path.splitext(input_file)[0] + ".wav"

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

    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return output_file