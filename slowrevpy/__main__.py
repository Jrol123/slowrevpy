import argparse as prs
import os.path
from slowrevpy import slowrevpy
parser = prs.ArgumentParser(prog="slowedreverb",
                            description="Python module that helps creating slowed and reverbed audio",
                            epilog='Text at the bottom of help')
parser.add_argument('audio', type=str, help='destination')
parser.add_argument(metavar="speed", nargs='?', dest='speed_coefficient', type=float, default=0.65, help='Speed coefficient')
parser.add_argument(metavar="name", nargs='?', dest='output_filename', type=str, default=None, help='Name of the output file')
# parser.add_argument('-s', dest='silent_mode', help='NoAdditionalInfo')


def file_processing(filename, speed_coefficient, output_filename: str | None):
    print(f"Now processing {filename}")
    ext = "mp3"  # По-умолчанию сохраняет в mp3, если не задано своё название
    if output_filename is None:
        output_filename = ".".join(filename.split('.')[:-1]) + ' _slowedreverb_' + str(speed_coefficient) + '.' + ext

    slowrevpy(filename, output_filename, speed_coefficient)

def dir_processing(dir):
    for item in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, item)):
            # При впихивании папки output_filename не работает.
            print("Processing: " + item)
            try:
                file_processing(os.path.join(dir, item), args.speed_coefficient, None)
            except Exception as e:
                print(f"Error happened while processing file {item}: \n" + str(e))
            finally:
                print("Done\n")
        else:
            dir_processing(os.path.join(dir, item))

# TODO: Добавить возможность кастомизировать реверберации
if __name__ == '__main__':
    args = parser.parse_args()
    if os.path.isdir(args.audio):
        dir_processing(args.audio)
    else:
        file_processing(args.audio, args.speed_coefficient, args.output_filename)

