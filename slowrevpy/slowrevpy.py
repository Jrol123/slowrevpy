import soundfile as sf
from ffmpeg import FFmpeg
import os
from pedalboard import Pedalboard, Reverb, Resample
from pedalboard.io import get_supported_read_formats, AudioFile

# https://github.com/asherchok/snr/blob/main/snr-generator.ipynb


def slowrevpy(audio, output_filename: str, speed: float):
    """

    :param audio:
    :param output_filename: Output filename + extension
    :param speed: Speed coefficient
    :return:

    """
    # Было важно в предыдущей версии, без авто-конвертора
    # if "." + audio.split(".")[-1] not in get_supported_read_formats():
    #     raise TypeError(
    #         f"Audio needs to be in one of the supported formats:\n{get_supported_read_formats()}"
    #     )

    # Import audio file
    print("Importing audio...")
    audio, sample_rate = sf.read(audio)

    # pedals for pedalboard
    pedals = []

    sample_rate_2 = int(sample_rate * speed)

    # Slow audio
    print("Slowing audio...")
    pedals.append(
        Resample(
            target_sample_rate=sample_rate_2, quality=Resample.Quality.WindowedSinc
        )
    )

    # speed = 0.85 & reverb = 0.10

    # Add reverb
    print("Adding reverb...")
    pedals.append(Reverb(room_size=0.75, damping=0.5, wet_level=0.08, dry_level=0.2))
    board = Pedalboard(pedals)

    # Add effects
    effected = board(audio, sample_rate)

    # Before exporting, convert to MP3 using ffmpeg
    tmp_dir = "tmp"
    os.makedirs(tmp_dir, exist_ok=True)
    temp_output = os.path.join(tmp_dir, "temp_output.wav")  # Temporary WAV file

    print("Exporting temp audio as WAV...")
    sf.write(temp_output, effected, sample_rate_2)

    # Convert to MP3 using ffmpeg
    print("Converting audio to MP3...")
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(temp_output)
        .output(output_filename, acodec="libmp3lame", ar="44100", ac=2, ab="192k")
    )

    ffmpeg.execute()
    # ffmpeg -i '.\07. Re Beautiful Morning _slowedreverb_0.65.wav' -vn -ar 44100 -ac 2 -b:a 192k output.mp3

    # Optionally, remove the temporary WAV file

    os.remove(temp_output)
    print("Done!")
    print(f"Output file: {output_filename}")
    print()

    # TODO: Это всё поломало
    # with AudioFile(output_filename, 'w', sample_rate_2, effected.shape[0]) as f:
    #     f.write(effected)
