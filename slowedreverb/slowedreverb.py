import soundfile as sf
from pedalboard import Pedalboard, Reverb, Resample
from pedalboard.io import get_supported_read_formats, AudioFile

# https://github.com/asherchok/snr/blob/main/snr-generator.ipynb

def slowedreverb(audio, output_filename: str, speed: float):
    """

    :param audio:
    :param output_filename: Output filename + extension
    :param speed: Speed coefficient
    :return:

    """
    if "." + audio.split(".")[-1] not in get_supported_read_formats():
        raise TypeError(f'Audio needs to be in one of the supported formats:\n{get_supported_read_formats()}')

    # Import audio file
    print('Importing audio...')
    audio, sample_rate = sf.read(audio)

    # pedals for pedalboard
    pedals = []

    sample_rate_2 = int(sample_rate * speed)

    # Slow audio
    print('Slowing audio...')
    pedals.append(Resample(target_sample_rate=sample_rate_2, quality=Resample.Quality.WindowedSinc))

    # speed = 0.85 & reverb = 0.10

    # Add reverb
    print('Adding reverb...')
    pedals.append(Reverb(
        room_size=0.75,
        damping=0.5,
        wet_level=0.08,
        dry_level=0.2
    ))
    board = Pedalboard(pedals)

    # Add effects
    effected = board(audio, sample_rate)

    # Export audio
    print('Exporting audio...')
    # TODO: Это всё поломало
    # with AudioFile(output_filename, 'w', sample_rate_2, effected.shape[0]) as f:
    #     f.write(effected)
    sf.write(output_filename, effected, sample_rate_2)
