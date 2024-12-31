import argparse as prs
import os.path
from slowrevpy import slowrevpy
parser = prs.ArgumentParser(prog="slowrevpy",
                            description="Python module that helps creating slowed and reverbed audio",
                            epilog='Text at the bottom of help')
parser.add_argument('audio', type=str, help='destination')
parser.add_argument('-s', '--speed', nargs='?', dest='speed_coefficient', type=float, default=0.65, help='Speed coefficient')
parser.add_argument('-o', '--output', nargs='?', dest='output_filename', type=str, default=None, help='Name of the output file(s)')
parser.add_argument('-f', '--format', nargs='?', dest='file_format', type=str, default='mp3', help='Format of the output file(s). Applies only when name is none')
# parser.add_argument('-s', dest='silent_mode', help='NoAdditionalInfo')


def file_processing(filename, speed_coefficient, output_filename: str | None):
    print(f"Now processing {filename}")
    
    # TODO: Сделать глобальную конвертацию в определённый формат при наличии флага. Сделать систему по типу -f mp3 или -f flac
    if output_filename is None:
        ext = "mp3"  # По-умолчанию сохраняет в mp3, если не задано своё название
        output_filename= ".".join(''.join(filename.split('\\')[1:]).split('.')[:-1]) + '_slowedreverb_' + str(speed_coefficient) + '.' + ext
    else:
        ext = output_filename.split('.')[-1]
    print(f"Track will be build with the {ext} extension in the {output_filename}")

    slowrevpy(filename, ext, output_filename, speed_coefficient)

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

