import argparse as prs
from os.path import basename
from slowedreverb.slowedreverb import slowedreverb
parser = prs.ArgumentParser(prog="slowedreverb",
                            description="Python module that helps creating slowed and reverbed audio",
                            epilog='Text at the bottom of help')
parser.add_argument('audio', type=str, help='destination')
parser.add_argument(metavar="speed", nargs='?', dest='speed_coefficient', type=float, default=0.08, help='Speed coefficient')
parser.add_argument(metavar="name", nargs='?', dest='output_filename', type=str, default=None, help='Name of the output file')

# TODO: Добавить возможность кастомизировать замедление
if __name__ == '__main__':
    args = parser.parse_args()
    filename = basename(args.audio)
    ext = filename.split('.')[-1]
    ext = ext if ext != "mp3" else "wav"  # TODO: Is it correct? Or it is better to convert it at "slowedreverb.py" ...
    if args.output_filename is None:
        args.output_filename = ".".join(filename.split('.')[:-1]) + ' _slowedreverb.' + ext

    slowedreverb(args.audio, args.output_filename, args.speed_coefficient)