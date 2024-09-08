import soundfile as sf
from pedalboard import Pedalboard, Reverb
from pedalboard.io import get_supported_read_formats
from math import trunc

def slowedreverb(audio, output: str):
    """

    :param audio:
    :param output: Output filename + extension
    :return:

    """
    if "." + audio.split(".")[-1] not in get_supported_read_formats():
        print('Audio needs to be in one of the supported formats:')
        print(get_supported_read_formats())
        return



    # Import audio file
    print('Importing audio...')
    audio, sample_rate = sf.read(audio)

    # Slow audio
    print('Slowing audio...')
    sample_rate -= trunc(sample_rate*0.08)

    # Add reverb
    print('Adding reverb...')
    board = Pedalboard([Reverb(
        room_size=0.75,
        damping=0.5,
        wet_level=0.08,
        dry_level=0.2
        )])

    # Add effects
    effected = board(audio, sample_rate)

    # Export audio
    print('Exporting audio...')
    sf.write(output, effected, sample_rate)